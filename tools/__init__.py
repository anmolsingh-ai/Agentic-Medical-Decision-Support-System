"""
tools/__init__.py — Tool registry for the SympTrack crew.

Add new tools here as the project grows (e.g., PubMed search,
drug-interaction checker, clinic rating API).
"""

from functools import lru_cache

from crewai_tools import SerperDevTool


@lru_cache(maxsize=1)
def get_search_tool() -> SerperDevTool:
    """
    Return a cached SerperDevTool instance.

    Cached with lru_cache so multiple agents sharing the tool
    get the same object — avoids re-initializing on each Streamlit run.
    """
    return SerperDevTool()