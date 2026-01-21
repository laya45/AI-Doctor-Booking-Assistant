# database.py
import sqlite3
from datetime import datetime

DB_NAME = "bookings.db"


# ---------------- DATABASE CONNECTION ---------------- #

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ---------------- INITIALIZE DATABASE ---------------- #

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            booking_type TEXT,
            date TEXT,
            time TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- SAVE BOOKING ---------------- #

def save_booking(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert customer
    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        (data["name"], data["email"], data["phone"])
    )
    customer_id = cursor.lastrowid

    # Insert booking
    cursor.execute(
        """
        INSERT INTO bookings 
        (customer_id, booking_type, date, time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            data["booking_type"],
            data["date"],
            data["time"],
            "CONFIRMED",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return booking_id


# ---------------- FETCH ALL BOOKINGS (ADMIN) ---------------- #

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            b.id,
            c.name,
            c.email,
            c.phone,
            b.booking_type,
            b.date,
            b.time,
            b.created_at
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        ORDER BY b.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows
