# admin_dashboard.py
import streamlit as st
import pandas as pd
from database import get_all_bookings


def render_admin_dashboard():
    st.title("📋 Admin Dashboard")
    st.markdown("View and manage all confirmed bookings")

    bookings = get_all_bookings()

    df = pd.DataFrame(
        bookings,
        columns=[
            "booking_id",
            "name",
            "email",
            "phone",
            "service",
            "date",
            "time",
            "created_at"
        ]
    )

    if df.empty:
        st.info("No bookings available.")
        return

    df["name"] = df["name"].astype(str)
    df["email"] = df["email"].astype(str)

    st.subheader("🔍 Search Filters")

    name_filter = st.text_input("Search by Name")
    email_filter = st.text_input("Search by Email")

    filtered_df = df.copy()

    if name_filter:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(name_filter, case=False, na=False)
        ]

    if email_filter:
        filtered_df = filtered_df[
            filtered_df["email"].str.contains(email_filter, case=False, na=False)
        ]

    st.subheader("📊 Booking Records")

    if filtered_df.empty:
        st.warning("No matching bookings found.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    st.caption(f"Showing {len(filtered_df)} of {len(df)} total bookings")
