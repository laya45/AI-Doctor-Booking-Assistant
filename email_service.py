import smtplib
from email.message import EmailMessage

def send_email(to_email, booking_id, data):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Booking Confirmation"
        msg["From"] = "bogelayavardhan@gmail.com"
        msg["To"] = to_email

        msg.set_content(f"""
Hello {data['name']},

Your booking has been confirmed.

Booking ID: {booking_id}
Service: {data['booking_type']}
Date: {data['date']}
Time: {data['time']}

Thank you!
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                "bogelayavardhan@gmail.com",
                "bdjobzaaqlczopai"   # ← PASTE YOUR REAL APP PASSWORD HERE
            )
            server.send_message(msg)

        return True

    except Exception as e:
        print("Email error:", e)
        return False
