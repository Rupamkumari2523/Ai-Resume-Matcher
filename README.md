# 🚀 CareerAI - AI Resume Matcher & Career Assistant

CareerAI is an AI-powered career guidance platform that helps users analyze their resumes, identify missing skills, and discover suitable job roles using Artificial Intelligence.

The application provides personalized career insights through three intelligent modules:

- 📄 Resume Matcher
- 🎯 Skill Gap Analyzer
- 💼 Eligible Roles Predictor

---

## ✨ Features

### 📄 Resume Matcher
- Upload your resume (PDF)
- Paste target job description
- AI compares resume with job description
- Generates resume match score
- Highlights missing keywords and skills

---

### 🎯 Skill Gap Analyzer
- Upload resume
- Enter target job role
- Identifies missing technical skills
- Recommends YouTube learning resources
- Suggests technologies to learn

---

### 💼 Eligible Roles Predictor
- Upload resume
- AI analyzes experience and skills
- Predicts suitable job roles
- Displays multiple career opportunities based on profile

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Database & Authentication
- Supabase Authentication

### AI / APIs
- Groq API (Resume Analysis)
- YouTube Data API (Learning Recommendations)

---

## 📂 Project Structure

```text
AI-Resume-Matcher/
│
├── Frontend/
│   ├── auth.js
│   ├── index.html
│   ├── landing.html
│   ├── landing.css
│   ├── landing.js
│   ├── login.html
│   ├── login.js
│   ├── script.js
│   └── style.css
│
├── backend/
│   ├── venv/                 
│   ├── .env                 
│   ├── app.py
│   ├── requirements.txt
│   └── skills.json
│
├── .vscode/
│   └── settings.json
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI-Resume-Matcher.git
```

---

### 2. Navigate to Project

```bash
cd AI-Resume-Matcher
```

---

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file inside the backend folder.

Example:

```env
GROQ_API_KEY=YOUR_API_KEY
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_ANON_KEY=YOUR_SUPABASE_KEY
YOUTUBE_API_KEY=YOUR_API_KEY
```

---

### 5. Run Flask Server

```bash
python app.py
```

---

### 6. Run Frontend

Open

```
landing.html
```

using Live Server (VS Code).

---

# 🔥 Workflow

```text
User Login
      │
      ▼
Upload Resume
      │
      ▼
Choose Module
      │
 ┌───────────────┬────────────────┬────────────────┐
 │               │                │
 ▼               ▼                ▼
Resume       Skill Gap      Eligible Roles
Matcher      Analyzer         Predictor
 │               │                │
 ▼               ▼                ▼
AI Analysis   Missing Skills   Job Prediction
 │               │                │
 ▼               ▼                ▼
Results       YouTube Videos    Career Roles
```

---

# 🎯 Future Enhancements

- Resume Builder
- ATS Resume Score
- Company-wise Resume Optimization
- Interview Question Generator
- Cover Letter Generator
- AI Chat Career Assistant
- Resume Improvement Suggestions
- Job Recommendation Portal

---

# 📖 Learning Outcomes

This project helped in learning:

- Flask Backend Development
- REST APIs
- Supabase Authentication
- Resume Parsing
- Prompt Engineering
- AI API Integration
- Responsive UI Design
- Frontend-Backend Integration

---


# ⭐ Support

If you like this project,

⭐ Star this repository

---
