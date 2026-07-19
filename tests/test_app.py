"""
Integration tests for the Flask API routes.
Run with: pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Campus Assist" in resp.data


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_chat_returns_reply(client):
    resp = client.post("/api/chat", json={"message": "how do I pay my fees"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "reply" in data
    assert data["intent"] == "fees"


def test_chat_rejects_empty_message(client):
    resp = client.post("/api/chat", json={"message": "   "})
    assert resp.status_code == 400


def test_history_endpoint_returns_list(client):
    client.post("/api/chat", json={"message": "hi"})
    with client.session_transaction() as sess:
        session_id = sess.get("session_id")
    resp = client.get(f"/api/history/{session_id}")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_stats_endpoint(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)
