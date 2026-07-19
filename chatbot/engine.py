"""
chatbot/engine.py

Core NLP engine for the Student Support Chatbot.

Approach
--------
This uses a lightweight, fully offline TF-IDF + cosine similarity
retrieval model to match a user's message against a bank of known
question patterns (intents.json). This avoids any dependency on
paid/external LLM APIs, making the project easy to run and grade
without API keys, while still demonstrating real NLP/ML concepts:

    1. Text preprocessing (lowercasing, punctuation & stopword removal)
    2. TF-IDF vectorization of training patterns
    3. Cosine similarity for intent classification
    4. Confidence thresholding with a graceful fallback intent

The design is intentionally modular so the retrieval model can later
be swapped for a transformer-based classifier or an LLM API call
without changing the Flask routes.
"""

import json
import random
import re
import string
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
INTENTS_PATH = BASE_DIR / "intents.json"

# Minimal English stopword list (kept local to avoid an nltk download step)
STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their", "this", "that", "these", "those",
    "do", "does", "did", "doing", "to", "of", "in", "on", "for", "with", "at",
    "by", "about", "as", "into", "like", "through", "after", "before", "between",
    "and", "or", "but", "if", "so", "than", "then", "there", "here", "up", "down",
    "can", "could", "will", "would", "should", "please", "just", "also"
}


def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, and remove stopwords from input text."""
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = [t for t in re.split(r"\s+", text) if t and t not in STOPWORDS]
    return " ".join(tokens) if tokens else text


class ChatbotEngine:
    """TF-IDF based intent classifier + response generator."""

    def __init__(self, intents_path: Path = INTENTS_PATH, confidence_threshold: float = 0.20):
        self.confidence_threshold = confidence_threshold
        self.intents = self._load_intents(intents_path)

        self.pattern_texts = []
        self.pattern_tags = []
        for intent in self.intents:
            for pattern in intent.get("patterns", []):
                self.pattern_texts.append(preprocess(pattern))
                self.pattern_tags.append(intent["tag"])

        self.tag_to_responses = {
            intent["tag"]: intent["responses"] for intent in self.intents
        }

        # Fit TF-IDF vectorizer on all known patterns
        self.vectorizer = TfidfVectorizer()
        self.pattern_matrix = self.vectorizer.fit_transform(self.pattern_texts)

    @staticmethod
    def _load_intents(path: Path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["intents"]

    def classify(self, message: str):
        """Return (tag, confidence) for the best-matching intent."""
        cleaned = preprocess(message)
        if not cleaned:
            return "fallback", 0.0

        query_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(query_vec, self.pattern_matrix).flatten()

        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])
        best_tag = self.pattern_tags[best_idx]

        if best_score < self.confidence_threshold:
            return "fallback", best_score
        return best_tag, best_score

    def get_response(self, message: str) -> dict:
        """Main entry point: classify a message and return a response payload."""
        tag, confidence = self.classify(message)
        responses = self.tag_to_responses.get(tag, self.tag_to_responses["fallback"])
        reply = random.choice(responses)
        return {
            "reply": reply,
            "intent": tag,
            "confidence": round(confidence, 3),
        }


# Singleton instance used by the Flask app
engine = ChatbotEngine()


if __name__ == "__main__":
    # Quick manual test from the command line
    print("Student Support Chatbot Engine — type 'quit' to exit")
    while True:
        msg = input("You: ")
        if msg.lower() in {"quit", "exit"}:
            break
        result = engine.get_response(msg)
        print(f"Bot [{result['intent']} | {result['confidence']}]: {result['reply']}")
