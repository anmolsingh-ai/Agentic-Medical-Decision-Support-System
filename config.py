"""
config.py — Centralized configuration for LLM and environment variables.

All environment loading and validation happens here so the rest of the
codebase never calls os.getenv() directly.
"""

import os
import logging
from functools import lru_cache

from crewai import LLM
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def get_required_env(key: str) -> str:
    """Fetch a required environment variable or raise a clear error."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: '{key}'. "
            f"Please add it to your .env file."
        )
    return value


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    """
    Build and cache the LLM instance.

    Uses lru_cache so Streamlit re-renders never reconstruct the object —
    the same instance is returned on every call.
    """
    api_key = get_required_env("ZHIPU_API_KEY")

    logger.info("Initializing Zhipu AI LLM (glm-4.5-flash)...")
    return LLM(
        model="glm-4.5-flash",
        api_key=api_key,
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.4,
    )


def validate_api_keys() -> None:
    """
    Validate all required API keys upfront.
    Raises EnvironmentError listing every missing key at once.
    """
    required = ["ZHIPU_API_KEY", "SERPER_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(
            f"Missing API keys: {', '.join(missing)}. "
            f"Please set them in your .env file."
        )

    # Make keys available to sub-libraries that read from os.environ directly
    for key in required:
        os.environ[key] = os.getenv(key)  # type: ignore[arg-type]