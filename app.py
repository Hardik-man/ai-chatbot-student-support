"""
app.py

Flask application entry point for the AI Chatbot for Student Support Services.

Routes
------
GET  /                 -> Chat UI
POST /api/chat         -> Send a message, get a bot reply (JSON)
GET  /api/history/<id> -> Retrieve chat history for a session
GET  /api/stats        -> Aggregate intent stats (simple admin view)
GET  /api/health       -> Health check
"""

import uuid

from flask import Flask, jsonify, render_template, request, session

from chatbot.database import get_history, get_intent_stats, init_db, log_message
from chatbot.engine import engine

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"  # override via env var in production

init_db()


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    session_id = session.get("session_id") or data.get("session_id") or "anonymous"

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    result = engine.get_response(user_message)

    log_message(session_id, "user", user_message)
    log_message(session_id, "bot", result["reply"], result["intent"], result["confidence"])

    return jsonify(
        {
            "reply": result["reply"],
            "intent": result["intent"],
            "confidence": result["confidence"],
            "session_id": session_id,
        }
    )


@app.route("/api/history/<session_id>")
def history(session_id):
    return jsonify(get_history(session_id))


@app.route("/api/stats")
def stats():
    return jsonify(get_intent_stats())


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
