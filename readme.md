# AI-Based Interview Coach 🎤💼

## 📌 Project Overview

**AI-Based Interview Coach** is a web application designed to help users prepare for interviews. It uses Google's Gemini AI to generate realistic interview questions, provide intelligent responses, offer answer help, and track user progress.

---

## 🚀 Features

- ✅ User Registration & Login  
- 🎯 AI-generated interview questions by category (Technical, HR, Behavioral, etc.)  
- 🤖 Smart AI answers using Gemini API  
- 💬 Answer help for better responses  
- 🔁 Practice mode with random questions  
- 🕓 View session history  
- 🛠️ API endpoint for quick interactions

---

## 🛠️ Tech Stack

- **Frontend:** HTML (via Flask templates)  
- **Backend:** Python (Flask)  
- **Database:** SQLite using SQLAlchemy  
- **AI Integration:** Google Gemini API  
- **Other Libraries:** flask_sqlalchemy, datetime, json

---

## 📁 Folder Structure

```

ai\_interview\_coach/
│
├── app.py                   # Main Flask application
├── interview\_app.db         # SQLite DB
├── templates/               # HTML templates (UI)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── ask.html
│   ├── result.html
│   ├── practice.html
│   ├── answer\_help.html
│   └── history.html
├── static/                  # CSS, JS, etc.
├── requirements.txt         # Dependencies

````

---

## ⚙️ Setup Instructions

1. **Install dependencies**
   ```bash
   pip install flask flask_sqlalchemy google-generativeai
````

2. **Set your Gemini API key**
   Replace in `app.py`:

   ```python
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
   ```

3. **Initialize the database**

   ```bash
   python app.py
   ```

4. **Start the app**

   ```bash
   python app.py
   ```

5. **Open in browser**

   ```
   http://localhost:5000
   ```

---

## 🔗 Key URLs

* `/register` – User Registration
* `/login` – User Login
* `/dashboard` – Main Dashboard
* `/ask` – Ask Interview Question
* `/practice` – Practice Mode
* `/get_answer_help` – Help with Answering
* `/history` – View Previous Sessions
* `/api/quick_question` – API (POST request with JSON)

---

## 🧠 About AI Integration

The AI functionality uses Gemini's `GenerativeModel` to:

* Generate interview questions (`generate_practice_question`)
* Provide AI responses to user questions (`get_interview_response`)
* Help improve answers with structure/tips (`get_answer_help`)

---

## 🧪 Example API Request

```http
POST /api/quick_question
Content-Type: application/json

{
  "question": "What is your greatest strength?",
  "category": "HR"
}
```

---

## 📌 Note

* Ensure you have internet access for Gemini API to work.
* For demonstration, test with sample categories like *Technical*, *HR*, *Behavioral*, etc.