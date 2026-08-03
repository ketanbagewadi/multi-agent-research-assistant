# backend/db.py

import sqlite3
from datetime import datetime

# ---------------------------------------------------------
# SQLite storage for completed research reports.
# Simple, file-based DB — no server needed, good for a portfolio project.
# ---------------------------------------------------------

DB_PATH = "research_reports.db"


def init_db():
    """
    Creates the reports table if it doesn't already exist.
    Called once when the FastAPI server starts.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            report TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("[db] ✅ Table ready.")


def save_report(query: str, report: str):
    """
    Saves a completed research report to the database.
    Called by main.py after the Writer agent finishes.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reports (query, report, created_at) VALUES (?, ?, ?)",
        (query, report, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
    print(f"[db] 💾 Saved report for query: '{query}'")


def get_all_reports():
    """
    Returns all saved reports, most recent first.
    Useful later for a 'past research' page in the frontend.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, query, report, created_at FROM reports ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": r[0], "query": r[1], "report": r[2], "created_at": r[3]}
        for r in rows
    ]