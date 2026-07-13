# 📚 LearnEase AI - Course Content Simplification Agent

## 📌 Overview

LearnEase AI is an AI-powered web application that simplifies complex educational content into easy-to-understand study material. It helps students learn faster by generating concise summaries, simplified notes, key concepts, definitions, MCQs, and revision notes from uploaded study documents.

This project was developed as part of the **AICTE Virtual Internship 2026** in collaboration with **Edunet Foundation** using **IBM watsonx.ai**.

---

## 🚀 Features

- 📄 Upload study materials
  - PDF
  - DOC
  - DOCX
  - PPT
  - PPTX
  - TXT

- 🤖 AI-powered content simplification
- 📘 Smart Summary Generation
- 📖 Simplified Notes
- ⭐ Key Concepts Extraction
- 📚 Important Definitions
- ❓ AI-generated MCQs
- 📝 Revision Notes
- 🌙 Dark Mode
- 👤 User Login & Registration

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

### AI
- IBM watsonx.ai Runtime
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
├── services/
│   ├── ai_service.py
│   └── pdf_service.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── result.html
│   ├── profile.html
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

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CourseSimplifierAI.git
```

Move into the project

```bash
cd CourseSimplifierAI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

## 📷 Application Workflow

1. User Login
2. Upload Study Material
3. Text Extraction
4. IBM watsonx.ai API
5. AI Simplification
6. Display Smart Notes
7. Revision & Practice

---

## 🎯 Future Enhancements

- AI Flashcards
- Voice-based Learning
- Multilingual Support
- OCR for Images
- Download Notes as PDF
- AI Chatbot
- Learning Progress Dashboard

---

## 👩‍💻 Developed By

**Ankam Supritha**

AICTE Virtual Internship 2026

Edunet Foundation

---

## 🙏 Acknowledgements

- IBM watsonx.ai
- IBM Cloud
- Edunet Foundation
- AICTE

---

## 📜 License

This project is developed for educational purposes under the AICTE Virtual Internship Program.