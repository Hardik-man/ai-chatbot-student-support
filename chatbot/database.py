"""
chatbot/database.py

Very small SQLite wrapper used to persist chat history.
This lets the project demonstrate a full loop: user message -> NLP
engine -> stored conversation -> retrievable chat history via API.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chat_history.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL CHECK(sender IN ('user', 'bot')),
            message TEXT NOT NULL,
            intent TEXT,
            confidence REAL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def log_message(session_id: str, sender: str, message: str, intent: str = None, confidence: float = None):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO messages (session_id, sender, message, intent, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (session_id, sender, message, intent, confidence, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_history(session_id: str):
    conn = get_connection()
    rows = conn.execute(
        "SELECT sender, message, intent, confidence, created_at FROM messages "
        "WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_intent_stats():
    """Aggregate count of each intent triggered — useful for an admin dashboard."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT intent, COUNT(*) as count FROM messages "
        "WHERE sender = 'bot' AND intent IS NOT NULL "
        "GROUP BY intent ORDER BY count DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
