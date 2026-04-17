import uuid
import threading
import logging

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import ProposalStatus, GenerateResponse, ProposalResponse
from app.config import CORS_ORIGINS
from app.services.pdf_parser import extract_text_from_pdf
from app.services.job_store import get_job_store
from app.crew.pipeline import run_pipeline
from app.utils.helpers import sanitize_job_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ProposalBot API",
    description="Multi-agent AI system that transforms requirement documents into professional project proposals",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/proposals/generate", response_model=GenerateResponse)
async def generate_proposal(
    file: UploadFile = File(None),
    text: str = Form(None),
):
    # Validate input
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="Provide either a PDF file or requirement text",
        )

    requirement_text = ""

    if file:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported",
            )
        try:
            file_bytes = await file.read()
            requirement_text = extract_text_from_pdf(file_bytes)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from PDF",
            )
    else:
        requirement_text = text.strip()

    if not requirement_text:
        raise HTTPException(
            status_code=400,
            detail="Requirement text is empty",
        )

    # Create job
    job_id = str(uuid.uuid4())
    store = get_job_store()
    store.create(job_id)

    # Start pipeline in background thread
    thread = threading.Thread(
        target=run_pipeline,
        args=(job_id, requirement_text),
        daemon=True,
    )
    thread.start()

    return GenerateResponse(
        job_id=job_id,
        status=ProposalStatus.PROCESSING,
        message="Pipeline started",
    )


@app.get("/api/proposals/{job_id}", response_model=ProposalResponse)
def get_proposal(job_id: str):
    if not sanitize_job_id(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID")

    store = get_job_store()
    job = store.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return ProposalResponse(**job)
