🤖 AI Doctor Booking Assistant
📌 Overview

The AI Doctor Booking Assistant is a chat-based application designed to help users interact with clinic information and book doctor appointments in a natural, conversational way.

The system combines Retrieval-Augmented Generation (RAG) for answering questions from uploaded PDFs with a multi-turn booking flow that collects user details, confirms them, and stores bookings securely.
An Admin Dashboard is included to manage and view all bookings.

This project was developed as part of an AI Engineer assessment.

🎯 Objectives

Provide a conversational interface for booking doctor appointments

Enable question answering from clinic documents using RAG

Detect booking intent and collect required details step-by-step

Confirm booking details before saving

Send email confirmation after booking

Provide an admin dashboard to view stored bookings

Deploy the solution with a public Streamlit Cloud URL

✨ Key Features

💬 Chat-based UI using Streamlit

📄 Multi-PDF upload support

🔍 RAG pipeline for document-based Q&A

🧠 Booking intent detection

📝 Slot-filling booking flow

✅ Explicit user confirmation before saving

🗄️ SQLite database for persistence

📧 Email confirmation after successful booking

🧑‍💼 Admin Dashboard with filtering options

☁️ Deployed on Streamlit Cloud

🛠️ Technology Stack

Python

Streamlit

LangChain

FAISS Vector Store

OpenAI Embeddings / LLM

SQLite

SMTP (Email Notifications)

📂 Project Structure
AI-Doctor-Booking-Assistant/
│
├── main.py               # Streamlit entry point (Chat + Navigation)
├── booking_flow.py       # Booking intent & slot-filling logic
├── rag_pipeline.py       # PDF ingestion & RAG implementation
├── admin_dashboard.py    # Admin UI for viewing bookings
├── database.py           # SQLite database operations
├── email_service.py      # Email confirmation logic
├── requirements.txt      # Project dependencies
├── .gitignore
└── README.md

🔄 Booking Flow

User starts chatting with the assistant

System detects booking intent

Assistant collects:

Name

Email

Phone number

Booking type

Preferred date & time

Assistant summarizes collected details

User confirms or cancels

On confirmation:

Booking is stored in database

Confirmation email is sent

Booking ID is returned to the user

📄 RAG Design

Users upload one or more clinic-related PDFs

Documents are:

Extracted

Chunked

Embedded

Stored in FAISS vector store

User questions are answered by combining:

Retrieved document chunks

LLM-generated responses

🧑‍💼 Admin Dashboard

The Admin Dashboard allows:

Viewing all bookings

Filtering bookings by:

Customer name

Email

Booking date

Simple and clean UI for administration
