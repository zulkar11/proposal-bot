from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ProposalStatus(str, Enum):
    PROCESSING = "processing"
    ANALYZING = "analyzing"
    RESEARCHING = "researching"
    ESTIMATING = "estimating"
    REVIEWING = "reviewing"
    WRITING = "writing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerateResponse(BaseModel):
    job_id: str
    status: ProposalStatus
    message: str


class ProposalResponse(BaseModel):
    job_id: str
    status: ProposalStatus
    current_stage: str
    stages_completed: list[str]
    agent_outputs: dict[str, Optional[str]]
    final_proposal: Optional[str]
    metadata: dict
    created_at: str


class ReviewDecision(BaseModel):
    needs_revision: bool
    feedback: str
    confidence_score: float
