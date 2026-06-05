from crewai import Agent, LLM
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

def create_diagnoser_agent():
    return Agent(
        role="Medical Symptom Analyzer",
        goal="Analyze symptoms and suggest possible diseases (non-diagnostic)",
        backstory="Expert assistant trained to interpret symptoms safely.",
        llm=llm,
        verbose=True
    )