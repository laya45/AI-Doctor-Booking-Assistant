import streamlit as st
from transformers import pipeline
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline

from rag_pipeline import build_vectorstore
from booking_flow import is_booking_intent, get_next_question
from database import init_db, save_booking
from email_service import send_email

# -------------------------------------------------
# Initialize database (IMPORTANT)
# -------------------------------------------------
init_db()
# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Booking Assistant",
    layout="wide"
)

# -------------------------------------------------
# Sidebar navigation
# -------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Chat Assistant", "Admin Dashboard"]
)

if page == "Admin Dashboard":
    from admin_dashboard import render_admin_dashboard
    render_admin_dashboard()
    st.stop()

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🩺 AI Doctor Booking Assistant")

# -------------------------------------------------
# Session state initialization
# -------------------------------------------------
st.session_state.setdefault("messages", [])
st.session_state.setdefault("booking_data", {})
st.session_state.setdefault("awaiting_confirmation", False)
st.session_state.setdefault("current_field", None)

# -------------------------------------------------
# PDF upload (RAG)
# -------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload clinic or service related PDFs",
    type="pdf",
    accept_multiple_files=True
)

qa_chain = None

if uploaded_files:
    with st.spinner("Processing documents..."):
        vectorstore = build_vectorstore(uploaded_files)

        hf_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=256
        )

        llm = HuggingFacePipeline(pipeline=hf_pipeline)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
        )

# -------------------------------------------------
# Display chat history (last 25 messages)
# -------------------------------------------------
for msg in st.session_state.messages[-25:]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------------------------------
# Chat input
# -------------------------------------------------
user_input = st.chat_input("Ask a question or book an appointment")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    response = ""

    # -------------------------------------------------
    # Booking confirmation step
    # -------------------------------------------------
    if st.session_state.awaiting_confirmation:
        if user_input.lower() in ["yes", "confirm", "okay", "go ahead", "y"]:
            booking_id = save_booking(st.session_state.booking_data)

            email_status = send_email(
                st.session_state.booking_data["email"],
                booking_id,
                st.session_state.booking_data
            )

            response = (
                "✅ **Booking Confirmed!**\n\n"
                f"📌 Booking ID: {booking_id}\n"
                f"👤 Name: {st.session_state.booking_data['name']}\n"
                f"🩺 Service: {st.session_state.booking_data['booking_type']}\n"
                f"📅 Date: {st.session_state.booking_data['date']}\n"
                f"⏰ Time: {st.session_state.booking_data['time']}"
            )

            if not email_status:
                response += (
                    "\n\n⚠️ Email could not be sent, "
                    "but the booking was saved successfully."
                )

            st.session_state.booking_data.clear()
            st.session_state.awaiting_confirmation = False
            st.session_state.current_field = None

        else:
            response = "❌ Booking cancelled. You can start again anytime."
            st.session_state.booking_data.clear()
            st.session_state.awaiting_confirmation = False
            st.session_state.current_field = None

    # -------------------------------------------------
    # Booking intent & slot filling
    # -------------------------------------------------
    elif is_booking_intent(user_input) or st.session_state.current_field:
        next_question = get_next_question(
            st.session_state.booking_data,
            user_input,
            st.session_state
        )

        if next_question:
            response = next_question
        else:
            response = (
                "Please confirm your booking details:\n\n"
                f"{st.session_state.booking_data}\n\n"
                "Type **yes** to confirm or **cancel** to stop."
            )
            st.session_state.awaiting_confirmation = True

    # -------------------------------------------------
    # RAG-based document Q&A
    # -------------------------------------------------
    elif qa_chain:
        with st.spinner("Assistant is thinking..."):
            response = qa_chain.run(user_input)

    else:
        response = "Please upload PDFs or start a booking."

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.chat_message("assistant").write(response)
