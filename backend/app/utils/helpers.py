import re


def estimate_tokens(text: str) -> int:
    """Rough token estimate (1 token ≈ 4 chars for English text)."""
    return len(text) // 4


def truncate_text(text: str, max_chars: int = 50000) -> str:
    """Truncate text to max_chars with a note about truncation."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[... Text truncated for processing ...]"


def sanitize_job_id(job_id: str) -> bool:
    """Validate that a job_id is a safe string."""
    return bool(re.match(r'^[a-zA-Z0-9\-]+$', job_id))
