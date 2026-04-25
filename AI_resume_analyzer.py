from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

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
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return {
        "result": response.choices[0].message.content
    }