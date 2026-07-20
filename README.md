# 🎓 Campus Assist — AI Chatbot for Student Support Services
🔗 **[Try it live](https://ai-chatbot-student-support.onrender.com)**

*Note: hosted on a free tier — the app may take up to a minute to wake up if it's been inactive.*

An intelligent, rule-based/NLP chatbot that answers common student queries about **admissions, exams, fees, hostel, library, courses, timetables, IT support, grievances, and wellness/counseling** — built as a full-stack internship project with a Flask backend, a TF-IDF/cosine-similarity NLP engine, and a custom chat UI.

> Built to run **fully offline** — no paid API keys, no external LLM calls required. All intent classification happens locally using scikit-learn.

---

## 📌 Problem Statement

College help desks are flooded with repetitive queries — admission deadlines, exam dates, fee payment steps, hostel rules — that eat up staff time and leave students waiting. **Campus Assist** is a 24/7 virtual support desk that instantly answers these frequently asked questions and routes students to the right resource, while logging every conversation for analytics.

---

## ✨ Features

- 💬 **Real-time chat interface** styled as a campus help-desk directory
- 🧠 **NLP intent classification** using TF-IDF vectorization + cosine similarity (scikit-learn)
- 📚 **13 support categories**: admissions, exams, fees, library, hostel, courses, faculty contact, timetable, counseling/wellness, IT support, grievance redressal, greetings, and fallback handling
- 🎯 **Confidence-based fallback** — gracefully asks for clarification when it doesn't understand
- 🗂️ **Quick-access directory** sidebar for one-click common questions
- 🗄️ **Conversation logging** to SQLite for every session (auditable, extensible for analytics)
- 📊 **Stats API** for the most-asked topics — useful for a future admin dashboard
- ✅ **Unit + integration test suite** (pytest)
- 🔌 **Modular NLP engine** — swap in a transformer model or LLM API later without touching the Flask routes

---

## 🏗️ Architecture

```
User types message
        │
        ▼
 Flask route /api/chat
        │
        ▼
 chatbot/engine.py
   1. Preprocess text (lowercase, strip punctuation, remove stopwords)
   2. Vectorize with TF-IDF
   3. Cosine similarity vs. known intent patterns
   4. Pick best-matching intent (or fallback if confidence too low)
        │
        ▼
 chatbot/database.py  →  SQLite (data/chat_history.db)
        │
        ▼
 JSON response  →  rendered in chat UI
```

---

## 🛠️ Tech Stack

| Layer          | Technology                              |
|----------------|------------------------------------------|
| Backend        | Python, Flask                            |
| NLP / ML       | scikit-learn (TF-IDF + cosine similarity)|
| Database       | SQLite                                   |
| Frontend       | HTML, CSS, vanilla JavaScript            |
| Testing        | pytest                                   |

---

## 📂 Project Structure

```
ai-chatbot-student-support/
├── app.py                     # Flask application & API routes
├── chatbot/
│   ├── engine.py               # NLP intent classification engine
│   ├── database.py             # SQLite logging layer
│   └── intents.json            # Training data: patterns + responses per intent
├── templates/
│   └── index.html              # Chat UI markup
├── static/
│   ├── css/style.css           # Chat UI styling
│   └── js/script.js            # Chat UI interactivity
├── tests/
│   ├── test_engine.py          # NLP engine unit tests
│   └── test_app.py             # Flask API integration tests
├── data/                       # SQLite DB is created here at runtime
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ai-chatbot-student-support.git
cd ai-chatbot-student-support
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

### 5. Run the tests
```bash
pytest tests/ -v
```

---

## 🔌 API Reference

| Method | Endpoint               | Description                                  |
|--------|-------------------------|-----------------------------------------------|
| GET    | `/`                     | Chat UI                                       |
| POST   | `/api/chat`              | Send `{ "message": "..." }`, get bot reply    |
| GET    | `/api/history/<session_id>` | Get full conversation history for a session |
| GET    | `/api/stats`             | Aggregate count of triggered intents          |
| GET    | `/api/health`            | Health check                                  |

**Example request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "how do I apply for admission"}'
```

**Example response:**
```json
{
  "reply": "To apply for admission, visit the college admissions portal, fill in the application form, upload required documents, and pay the application fee before the deadline.",
  "intent": "admissions",
  "confidence": 1.0,
  "session_id": "58dd00ba-e715-4edf-8cc3-55b54fa12193"
}
```

---

## 🧠 How the NLP Engine Works

Rather than hardcoding `if/else` keyword rules, this project trains a small retrieval model:

1. **Training data** (`chatbot/intents.json`) defines ~13 intents, each with several example phrasings a student might type.
2. At startup, every example phrase is cleaned (lowercased, punctuation stripped, stopwords removed) and converted into a **TF-IDF vector**.
3. When a user sends a message, it's cleaned and vectorized the same way, then compared against all training phrases using **cosine similarity**.
4. The highest-scoring intent is chosen — if the best score is below a confidence threshold (default `0.20`), the bot returns a **fallback** response asking the user to rephrase.

This approach is transparent, fast, requires no GPU or internet access, and is easy for a reviewer to inspect and extend — a good demonstration of core NLP/ML concepts for an internship-level project.

---

## 🗺️ Roadmap / Future Improvements

- [ ] Swap the TF-IDF engine for a fine-tuned transformer (e.g. `sentence-transformers`) for better semantic matching
- [ ] Add multi-turn context (remembering what was asked previously in a session)
- [ ] Admin dashboard visualizing `/api/stats` with charts
- [ ] Multilingual support for regional languages
- [ ] Deploy to Render/Railway/Heroku with a production WSGI server (gunicorn)
- [ ] Connect to a real student information system (SIS) API for live, personalized answers (e.g. actual exam dates per student)
- [ ] Add authentication so chat history is tied to a real student account

---

## ⚠️ Disclaimer

This chatbot provides general, template-based guidance only. It is **not a substitute for professional counseling or official college communication**. For urgent mental health concerns, always direct students to your institution's official wellness center or a crisis helpline.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgements

Built as an internship project to demonstrate full-stack development, applied NLP, and API design skills.
