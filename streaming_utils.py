"""Helpers for progressively streaming text in the Streamlit UI."""

import time
from typing import Iterator


def stream_text(text: str, chunk_size: int = 4, delay: float = 0.01) -> Iterator[str]:
    """Yield text in small chunks to create a streaming effect in the UI."""
    if not text:
        return

    for start in range(0, len(text), chunk_size):
        yield text[start : start + chunk_size]
        time.sleep(delay)
