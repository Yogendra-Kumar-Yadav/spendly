import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'spendly.db'))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123"))
    )
    demo_id = cursor.lastrowid

    expenses = [
        (demo_id, 12.50,  "Food",          "2026-07-01", "Breakfast at cafe"),
        (demo_id, 35.00,  "Transport",     "2026-07-03", "Monthly bus pass"),
        (demo_id, 120.00, "Bills",         "2026-07-05", "Electricity bill"),
        (demo_id, 45.00,  "Health",        "2026-07-07", "Pharmacy supplies"),
        (demo_id, 18.00,  "Entertainment", "2026-07-09", "Cinema ticket"),
        (demo_id, 60.00,  "Shopping",      "2026-07-11", "Clothing purchase"),
        (demo_id, 8.75,   "Other",         "2026-07-13", "Miscellaneous"),
        (demo_id, 22.00,  "Food",          "2026-07-15", "Grocery run"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()
