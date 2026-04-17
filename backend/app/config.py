import os
from dotenv import load_dotenv

load_dotenv()

# LLM configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "glm-5.1")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.z.ai/api/paas/v4/")
MAX_REVISION_ROUNDS = int(os.getenv("MAX_REVISION_ROUNDS", "1"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Validation
if not OPENAI_API_KEY:
    import logging
    logging.getLogger(__name__).warning(
        "OPENAI_API_KEY is not set — LLM calls will fail"
    )


def get_llm_config():
    """Return kwargs for CrewAI's LLM class based on current config.

    Supports any OpenAI-compatible provider (z.ai, OpenRouter, etc.)
    by setting LLM_API_BASE. Without it, falls back to the default
    provider (OpenAI) based on LLM_MODEL.

    Example .env for z.ai:
        OPENAI_API_KEY=your-z-ai-key
        LLM_MODEL=glm-5.1
        LLM_API_BASE=https://api.z.ai/api/paas/v4/
    """
    from crewai import LLM

    kwargs = {
        "model": f"openai/{LLM_MODEL}" if LLM_API_BASE else LLM_MODEL,
        "api_key": OPENAI_API_KEY,
    }
    if LLM_API_BASE:
        kwargs["api_base"] = LLM_API_BASE
    return LLM(**kwargs)
