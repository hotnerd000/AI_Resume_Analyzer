from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File, Form
import PyPDF2
import io
import traceback

# Load environment variables
load_dotenv()

app = FastAPI()

# Get API key from .env
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

class RequestData(BaseModel):
    resume: str
    job_description: str

@app.post("/analyze")

def analyze(data: RequestData):
    try:
        prompt = f"""
You are an expert HR recruiter.

Task:
Analyze the resume against the job description.

Return output in JSON format:

{{
  "match_score": (0-100),
  "missing_skills": [],
  "strengths": [],
  "improvements": [],
  "final_feedback": ""
}}

Instructions:
- Be honest and critical
- Focus on skills, experience, and keywords
- Keep feedback concise
- Respond ONLY with valid JSON

Resume:
{data.resume}

Job Description:
{data.job_description}
"""
        response = client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>AI Resume Analyzer</title>
    </head>

    <body style="font-family: Arial; max-width: 800px; margin: auto;">
        <h2>AI Resume Analyzer</h2>

        <p><strong>Upload Resume (PDF):</strong></p>
        <input type="file" id="file"><br><br>

        <p><strong>Paste Job Description:</strong></p>
        <textarea id="job" rows="10" style="width:100%"></textarea><br><br>

        <button onclick="upload()">Analyze</button>

        <div id="result" style="background:#f5f5f5; padding:15px; margin-top:20px;"></div>

        <script>
        async function upload() {
            const file = document.getElementById("file").files[0];
            const job = document.getElementById("job").value;

            if (!file) {
                alert("Please upload a PDF resume");
                return;
            }

            let formData = new FormData();
            formData.append("file", file);
            formData.append("job_description", job);

            const res = await fetch("/analyze-file", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            try {
                const result = JSON.parse(data.result);

                const color =
                    result.fit_score >= 7 ? "green" :
                    result.fit_score >= 4 ? "orange" : "red";

                document.getElementById("result").innerHTML = `
                    <h3 style="color:${color}">Fit Score: ${result.fit_score} / 10</h3>
                    <p><strong>Reason:</strong> ${result.reason}</p>

                    <h4>Strengths:</h4>
                    <ul>${result.strengths.map(s => `<li>${s}</li>`).join("")}</ul>

                    <h4>Missing Skills:</h4>
                    <ul>${result.missing_skills.map(s => `<li>${s}</li>`).join("")}</ul>

                    <h4>Improvements:</h4>
                    <ul>${result.improvements.map(s => `<li>${s}</li>`).join("")}</ul>
                `;
            } catch (e) {
                document.getElementById("result").innerText = data.result;
            }
        }
        </script>

    </body>
    </html>
    """

@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        contents = await file.read()

        if not contents:
            return {"error": "Empty file"}

        pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))

        resume_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        if not resume_text.strip():
            return {"error": "Could not extract text from PDF"}

        prompt = f"""
You are an expert recruiter.

Evaluate how well the resume matches the job description.

Return ONLY valid JSON in this format:

{{
  "fit_score": number (0-10),
  "reason": "",
  "missing_skills": [],
  "strengths": [],
  "improvements": []
}}

Scoring rules:
- 0-3 = poor match
- 4-6 = moderate match
- 7-8 = good match
- 9-10 = excellent match

Be strict and realistic.

Resume:
{resume_text}

Job Description:
{job_description}
"""

        response = client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[{"role": "user", "content": prompt}],
        )

        return {"result": response.choices[0].message.content}

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}