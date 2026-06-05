from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import google.generativeai as genai

app = FastAPI(title = "Resume Feedback API")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(resume_text):
    prompt = f"""
    Analyze this resume and provide :
    
    1. Candidate summary
    2. Technical Skills
    3. projects & Technologies
    4. Suitable Job Roles
    5. Skill Gaps (if any)
    6. Recommended Projects
    7. Resume Score (0-100)
    
    Resume:
    
    {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return {"error": str(e)}

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
        return {"error": "Unsupported filetype. PLease upload a different file."}