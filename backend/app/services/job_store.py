import threading
from datetime import datetime, timezone
from typing import Optional

from app.models import ProposalStatus


class JobStore:
    """In-memory job status store (thread-safe)."""

    def __init__(self):
        self._jobs: dict = {}
        self._lock = threading.Lock()

    def create(self, job_id: str) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        job = {
            "job_id": job_id,
            "status": ProposalStatus.PROCESSING,
            "current_stage": "processing",
            "stages_completed": [],
            "agent_outputs": {
                "analyzer": None,
                "researcher": None,
                "estimator": None,
                "reviewer": None,
                "writer": None,
            },
            "final_proposal": None,
            "metadata": {
                "started_at": now,
                "elapsed_seconds": 0,
                "revision_triggered": False,
            },
            "created_at": now,
        }
        with self._lock:
            self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> Optional[dict]:
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, job_id: str, **kwargs) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return

            if "status" in kwargs:
                job["status"] = kwargs["status"]
                job["current_stage"] = kwargs["status"].value if hasattr(kwargs["status"], "value") else kwargs["status"]

                if kwargs["status"] != ProposalStatus.PROCESSING and kwargs["status"] != ProposalStatus.FAILED:
                    stage_name = kwargs["status"].value if hasattr(kwargs["status"], "value") else kwargs["status"]
                    if stage_name not in job["stages_completed"]:
                        job["stages_completed"].append(stage_name)

            if "stage_output" in kwargs:
                job["agent_outputs"].update(kwargs["stage_output"])

            if "final_proposal" in kwargs:
                job["final_proposal"] = kwargs["final_proposal"]

            if "error" in kwargs:
                job["metadata"]["error"] = kwargs["error"]

            if "revision_triggered" in kwargs:
                job["metadata"]["revision_triggered"] = kwargs["revision_triggered"]

            now = datetime.now(timezone.utc)
            started = datetime.fromisoformat(job["metadata"]["started_at"])
            job["metadata"]["elapsed_seconds"] = int((now - started).total_seconds())

            if kwargs.get("status") == ProposalStatus.COMPLETED:
                job["metadata"]["completed_at"] = now.isoformat()


# Singleton instance
_store: Optional[JobStore] = None


def get_job_store() -> JobStore:
    global _store
    if _store is None:
        _store = JobStore()
    return _store
