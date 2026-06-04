from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import os

app = FastAPI(title = "Resume Feedback API")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        reader = PdfReader(file.file)
        texts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text is not None:
                texts.append(page.extract_text())
            else:
                return {"error": "Unable to extract text from the page {page}."}
        combined_text = "".join(texts)
        return {"filename" : file.filename, "content": combined_text}
    else:
        return {"error": "Unsupported filetype. PLease upload a different file."}