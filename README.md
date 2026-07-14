# 📚 LearnEase AI - Course Content Simplification Agent

## 📌 Overview

LearnEase AI is an AI-powered web application that simplifies complex educational content into easy-to-understand study material. It helps students learn faster by generating concise summaries, simplified notes, key concepts, definitions, MCQs, and revision notes from uploaded study documents.

This project also features a **conversational AI Agent** built on **IBM watsonx Orchestrate**, allowing students to interactively ask questions, get explanations, and practise with MCQs in a multi-turn chat interface.

Developed as part of the **AICTE Virtual Internship 2026** in collaboration with **Edunet Foundation** using **IBM watsonx.ai**.

---

## 🚀 Features

- 📄 Upload study materials — PDF, DOC, DOCX, PPT, PPTX, TXT
- 🤖 AI-powered content simplification
- 📘 Smart Summary Generation
- 📖 Simplified Notes
- ⭐ Key Concepts Extraction
- 📚 Important Definitions
- ❓ AI-generated MCQs
- 📝 Revision Notes
- 💬 **IBM watsonx Orchestrate Agent** (multi-turn conversational chat)
- 🌙 Dark Mode
- 👤 User Login & Registration

---

## 🤖 IBM watsonx Orchestrate Agent

LearnEase AI exposes a fully conversational educational agent via a REST API that is compatible with IBM watsonx Orchestrate.

### Agent Capabilities
- Multi-turn conversation with memory of prior turns
- Explain any course topic in plain language
- Generate practice MCQ questions on demand
- Define technical terms
- Summarise document content

### REST API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/agent/chat` | Send a message and receive a reply; maintains conversation history |
| `POST` | `/api/agent/simplify` | Submit raw text and receive structured study notes |

#### `/api/agent/chat` — Request
```json
{
  "message": "Explain machine learning in simple terms",
  "history": []
}
```

#### `/api/agent/chat` — Response
```json
{
  "reply": "Machine learning is a branch of AI where computers learn patterns from data...",
  "history": [
    { "role": "user",      "text": "Explain machine learning in simple terms" },
    { "role": "assistant", "text": "Machine learning is a branch of AI..." }
  ]
}
```

### Importing into IBM watsonx Orchestrate
1. Open **IBM watsonx Orchestrate**.
2. Go to **Skills & Apps → Import → OpenAPI**.
3. Upload `agent/openapi_skill.yaml`.
4. Set the server URL to your deployed application endpoint.
5. Create a new **Agent** and attach the imported skills.
6. Copy the personality / instructions from `agent/agent_config.yaml`.

---

## 🛠 Tech Stack

### Frontend
- HTML5, CSS3, JavaScript

### Backend
- Python, Flask

### Database
- SQLite

### AI
- IBM watsonx.ai Runtime
- IBM watsonx Orchestrate
- Mistral Small 3.1 24B Instruct

---

## 📂 Project Structure

```
CourseSimplifierAI/
│
├── app.py
├── learnease.db
├── .env
├── requirements.txt
│
├── agent/
│   ├── openapi_skill.yaml   ← OpenAPI spec for watsonx Orchestrate import
│   └── agent_config.yaml    ← Agent personality & skill configuration
│
├── services/
│   ├── ai_service.py        ← Structured simplification (Summary, MCQs, etc.)
│   ├── agent_service.py     ← Multi-turn conversational agent
│   └── pdf_service.py       ← File text extraction
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── agent.html           ← Conversational agent chat UI
│   ├── result.html
│   ├── history.html
│   └── about.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
└── README.md
```

---

## ⚙ Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/CourseSimplifierAI.git
cd CourseSimplifierAI

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
IBM_API_KEY=your_ibm_api_key
IBM_PROJECT_ID=your_project_id
IBM_URL=https://us-south.ml.cloud.ibm.com
```

### Run the Application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## 📷 Application Workflow

1. User Login / Register
2. Upload Study Material
3. Text Extraction
4. IBM watsonx.ai API → Structured Simplification
5. Display Smart Notes (Summary, MCQs, Definitions …)
6. Chat with the Agent for follow-up questions
7. Revision & Practice

---

## 🎯 Future Enhancements

- AI Flashcards
- Voice-based Learning
- Multilingual Support
- OCR for Images
- Download Notes as PDF
- Learning Progress Dashboard
- Document History Storage

---

## 👩‍💻 Developed By

**Ankam Supritha**

AICTE Virtual Internship 2026 · Edunet Foundation

---

## 🙏 Acknowledgements

- IBM watsonx.ai
- IBM watsonx Orchestrate
- IBM Cloud
- Edunet Foundation
- AICTE

---

## 📜 License

This project is developed for educational purposes under the AICTE Virtual Internship Program.
