"""
Unit tests for the chatbot NLP engine.
Run with: pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chatbot.engine import ChatbotEngine, preprocess


def test_preprocess_lowercases_and_strips_punctuation():
    assert preprocess("Hello, WORLD!!") == "hello world"


def test_preprocess_removes_stopwords():
    result = preprocess("What is the exam schedule for this week")
    assert "the" not in result.split()
    assert "exam" in result
    assert "schedule" in result


def test_greeting_intent_detected():
    engine = ChatbotEngine()
    result = engine.get_response("hello")
    assert result["intent"] == "greeting"


def test_admissions_intent_detected():
    engine = ChatbotEngine()
    result = engine.get_response("how do I apply for admission")
    assert result["intent"] == "admissions"


def test_exam_intent_detected():
    engine = ChatbotEngine()
    result = engine.get_response("when does my exam timetable come out")
    assert result["intent"] == "exams"


def test_gibberish_falls_back():
    engine = ChatbotEngine()
    result = engine.get_response("zxqv plorm fizzbuzz nadalax")
    assert result["intent"] == "fallback"


def test_empty_message_falls_back():
    engine = ChatbotEngine()
    result = engine.get_response("")
    assert result["intent"] == "fallback"


def test_response_payload_shape():
    engine = ChatbotEngine()
    result = engine.get_response("hi")
    assert set(result.keys()) == {"reply", "intent", "confidence"}
    assert isinstance(result["reply"], str) and result["reply"]
    assert 0.0 <= result["confidence"] <= 1.0
