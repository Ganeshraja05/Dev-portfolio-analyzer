# routes/resume.py
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import PyPDF2
import docx
from auth.auth_bearer import JWTBearer
from services.ai_evaluator import evaluate_text
from services.dynamic_scoring import compute_dynamic_scores
from services.auto_enhancements import generate_enhancement_suggestions

router = APIRouter()

@router.post("/analyze", dependencies=[Depends(JWTBearer())])
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze an uploaded resume file (PDF or DOCX) and return an aggregated report.
    The report includes metadata, extracted content (first 1000 characters),
    evaluation (sentiment and readability), dynamic scoring, and enhancement suggestions.
    """
    try:
        filename = file.filename.lower()
        contents = await file.read()
        text = ""

        if filename.endswith(".pdf"):
            # Use PyPDF2 to extract text from PDF files.
            pdf_reader = PyPDF2.PdfReader(BytesIO(contents))
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif filename.endswith(".docx"):
            # Use python-docx to extract text from DOCX files.
            doc = docx.Document(BytesIO(contents))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            # Fallback for plain text files.
            text = contents.decode("utf-8", errors="ignore")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Unable to extract text from the file.")

        metadata = {"filename": file.filename}
        evaluation = evaluate_text(text)
        scoring = compute_dynamic_scores(text, evaluation)
        enhancements = generate_enhancement_suggestions(text)
        
        report = {
            "metadata": metadata,
            "content_analysis": text[:1000] + "..." if len(text) > 1000 else text,
            "evaluation": evaluation,
            "scoring": scoring,
            "enhancements": enhancements,
        }
        return JSONResponse(content=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
