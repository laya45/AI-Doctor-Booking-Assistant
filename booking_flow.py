# booking_flow.py
import re
from datetime import datetime

BOOKING_FIELDS = [
    "name",
    "email",
    "phone",
    "booking_type",
    "date",
    "time"
]

QUESTIONS = {
    "name": "Please tell me your full name.",
    "email": "What is your email address?",
    "phone": "Please provide your phone number.",
    "booking_type": "What type of service would you like to book?",
    "date": "Which date do you prefer? (YYYY-MM-DD)",
    "time": "What time would you prefer?"
}

CONFIRM_WORDS = ["yes", "confirm", "okay", "go ahead", "y"]
CANCEL_WORDS = ["cancel", "stop", "no", "exit"]


def is_booking_intent(text: str) -> bool:
    keywords = ["book", "appointment", "schedule", "consultation"]
    return any(word in text.lower() for word in keywords)


# ---------------- VALIDATION ---------------- #

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)


def is_valid_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ---------------- CORE BOOKING FLOW ---------------- #

def get_next_question(booking_data: dict, user_input: str, session_state: dict):
    user_input = user_input.strip()

    # Cancel anytime
    if user_input.lower() in CANCEL_WORDS:
        session_state["current_field"] = None
        booking_data.clear()
        return "❌ Booking cancelled. You can start again anytime."

    # Start booking
    if session_state.get("current_field") is None:
        session_state["current_field"] = BOOKING_FIELDS[0]
        return QUESTIONS[session_state["current_field"]]

    current = session_state["current_field"]

    # Validation per field
    if current == "email" and not is_valid_email(user_input):
        return "❗ Please enter a valid email address."

    if current == "phone" and not is_valid_phone(user_input):
        return "❗ Please enter a valid 10-digit phone number."

    if current == "date" and not is_valid_date(user_input):
        return "❗ Please enter date in YYYY-MM-DD format."

    # Save valid input
    booking_data[current] = user_input

    # Move to next field
    current_index = BOOKING_FIELDS.index(current)

    if current_index + 1 < len(BOOKING_FIELDS):
        next_field = BOOKING_FIELDS[current_index + 1]
        session_state["current_field"] = next_field
        return QUESTIONS[next_field]

    # Completed all fields
    session_state["current_field"] = None
    return None
