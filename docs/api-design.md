# API Design

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/proposals/generate` | Upload document → start agent pipeline. Returns `job_id` |
| `GET` | `/api/proposals/{job_id}` | Poll for status + results. Returns current stage, agent outputs, final proposal |

---

## Request: Generate Proposal

**`POST /api/proposals/generate`**

- Content-Type: `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | File (PDF) | No* | Uploaded requirement document |
| `text` | string | No* | Pasted requirement text |

> *One of `file` or `text` must be provided.

**Response:**
```json
{
  "job_id": "abc123-uuid",
  "status": "processing",
  "message": "Pipeline started"
}
```

---

## Response: Poll Status

**`GET /api/proposals/{job_id}`**

```json
{
  "job_id": "abc123-uuid",
  "status": "researching",
  "current_stage": "researching",
  "stages_completed": ["analyzing"],
  "agent_outputs": {
    "analyzer": "## Requirement Analysis\n\n### Key Requirements...",
    "researcher": null,
    "estimator": null,
    "reviewer": null,
    "writer": null
  },
  "final_proposal": null,
  "metadata": {
    "started_at": "2026-04-17T10:30:00Z",
    "elapsed_seconds": 45
  },
  "created_at": "2026-04-17T10:30:00Z"
}
```

**When completed:**
```json
{
  "job_id": "abc123-uuid",
  "status": "completed",
  "current_stage": "completed",
  "stages_completed": ["analyzing", "researching", "estimating", "reviewing", "writing"],
  "agent_outputs": {
    "analyzer": "## Requirement Analysis\n...",
    "researcher": "## Technology Research\n...",
    "estimator": "## Project Estimation\n...",
    "reviewer": "## Review Summary\n...",
    "writer": null
  },
  "final_proposal": "# Project Proposal: E-Commerce Platform\n\n## Executive Summary\n...",
  "metadata": {
    "started_at": "2026-04-17T10:30:00Z",
    "completed_at": "2026-04-17T10:33:15Z",
    "elapsed_seconds": 195,
    "revision_triggered": true
  },
  "created_at": "2026-04-17T10:30:00Z"
}
```

---

## Request/Response Models

```python
# models.py
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

class GenerateRequest(BaseModel):
    text: Optional[str] = None  # Used when text is pasted (no file)

class GenerateResponse(BaseModel):
    job_id: str
    status: ProposalStatus
    message: str

class ProposalResponse(BaseModel):
    job_id: str
    status: ProposalStatus
    current_stage: str
    stages_completed: list[str]
    agent_outputs: dict[str, Optional[str]]  # {agent_name: output}
    final_proposal: Optional[str]            # Markdown
    metadata: dict                            # time, tokens, etc
    created_at: str
```

---

## Polling Flow (Frontend)

```
User clicks "Generate"
       │
       ▼
POST /api/proposals/generate
       │
       ▼ Returns job_id
       │
       ▼
Start polling: GET /api/proposals/{job_id} every 3 seconds
       │
       ├── status: "analyzing"    → Show step 1 active
       ├── status: "researching"  → Show step 2 active, step 1 output
       ├── status: "estimating"   → Show step 3 active, step 1-2 output
       ├── status: "reviewing"    → Show step 4 active, step 1-3 output
       ├── status: "writing"      → Show step 5 active, step 1-4 output
       └── status: "completed"    → Stop polling, show everything
```

---

## Error Handling

| Scenario | HTTP Code | Response |
|---|---|---|
| No file or text provided | 400 | `{"detail": "Provide either a PDF file or requirement text"}` |
| Invalid PDF (can't parse) | 422 | `{"detail": "Could not extract text from PDF"}` |
| Job not found | 404 | `{"detail": "Job not found"}` |
| Pipeline failure (LLM error) | 200* | Status set to `"failed"` with error in metadata |

> *Pipeline failures return 200 on the poll endpoint with `status: "failed"` — the job exists, it just failed mid-execution.
