AI Resume Analyzer — README
# 🧠 AI Resume Analyzer

An AI-powered web application that evaluates how well a resume matches a job description.  
It provides a fit score, insights, and actionable recommendations using modern LLMs.

---

## 🚀 Live Demo

👉 https://airesumeanalyzer-production-ba95.up.railway.app/

---

## 📌 Features

- 📄 Upload resume as PDF
- 📊 AI-generated fit score (0–10)
- 🧠 Detailed reasoning for score
- ✅ Strengths identification
- ❌ Missing skills detection
- 🔧 Improvement suggestions
- 🎨 Clean UI with color-coded scoring

---

## 🧠 How It Works

1. User uploads a resume (PDF)  
2. User provides a job description  
3. Backend extracts text from the resume  
4. AI analyzes the data and returns structured insights  

---

## 🛠️ Tech Stack

- Backend: Python, FastAPI  
- AI: OpenRouter API (LLMs)  
- PDF Processing: PyPDF2  
- Frontend: HTML, JavaScript  
- Deployment: Railway  

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/hotnerd000/AI_Resume_Analyzer.git
cd AI_Resume_Analyzer

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

4. Create .env file
OPENROUTER_API_KEY=your_api_key_here
5. Run the application
uvicorn main:app --reload
6. Open in browser
http://127.0.0.1:8000
🌐 Deployment

The app is deployed using Railway.

Steps:
Push code to GitHub
Connect repo to Railway
Add environment variable:
OPENROUTER_API_KEY
Generate domain in Railway Networking tab
📊 API Endpoints
Analyze Resume (PDF)
POST /analyze-file

Form Data:

file → PDF resume
job_description → text
Analyze Resume (Text)
POST /analyze

JSON Body:

{
  "resume": "text",
  "job_description": "text"
}
🧩 Example Output
{
  "fit_score": 7,
  "reason": "Strong frontend experience but missing system design exposure.",
  "missing_skills": ["System Design", "Database Management"],
  "strengths": ["HTML, CSS, JavaScript", "Performance optimization"],
  "improvements": ["Add backend experience", "Include scalable architecture projects"]
}
⚠️ Known Limitations
PDF text extraction may fail for scanned documents
AI output may require validation for strict JSON formatting
Free models may produce inconsistent results
🔮 Future Improvements
DOCX file support
ATS-style keyword scoring
Downloadable PDF report
Authentication system
History tracking
💼 Use Cases
Job seekers optimizing resumes
Recruiters evaluating candidates
Career platforms integrating AI insights

🧑‍💻 Author

Built by [Hotnerd000]

⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
