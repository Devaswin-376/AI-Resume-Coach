from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

app = FastAPI(title = "Resume Feedback API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(resume_text):
    prompt = f"""
    Determine whether the uploaded document is a resume/CV. 
    If it is not, return:
    {{
    "is_resume": false,
    "message": "Uploaded document is not a resume."
    }}
    
    If it is,
    Analyze this resume and provide :
    
    1. Candidate summary
    2. Technical Skills
    3. projects & Technologies
    4. Suitable Job Roles
    5. Skill Gaps (if any)
    6. Recommended Projects
    7. Resume Score (0-100)
    
    Return ONLY valid JSON that can be parseable by the Python json.loads() in the following format without categorising the skills:

    {{
    "candidate_summary": "",
    "technical_skills": [],
    "projects": [],
    "job_roles": [],
    "skill_gaps": [],
    "recommended_projects": [],
    "resume_score": 0
    }}
    
    Resume:
    
    {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip()
        
        if cleaned_response.startswith("```json") and cleaned_response.endswith("```"):
            cleaned_response = cleaned_response.replace("```json", "")[:-3].strip()
        parsed_response = json.loads(cleaned_response)
        return parsed_response
    
    except Exception as e:
        return {
            "error": "AI service temporarily unavailable. Please try again later.",
            "details": str(e)
            }

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        reader = PdfReader(file.file)
        texts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text is not None:
                texts.append(page_text)
            else:
                return {"error": "Unable to extract text from the page."}
        combined_text = "".join(texts)
        analysis = analyze_resume(combined_text)
        return {"analysis": analysis}
    else:
        return {"error": "Unsupported filetype. Please upload a different file."}