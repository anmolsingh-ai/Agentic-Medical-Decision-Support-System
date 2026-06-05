from crewai import Agent, LLM
from tools.serper_tool import SerperSearchTool
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

search_tool = SerperSearchTool()

def create_clinic_agent():
    return Agent(
        role="Clinic Finder Specialist",
        goal="Find nearby doctors and clinics based on disease and location",
        backstory="You help users locate relevant healthcare providers.",
        tools=[search_tool],
        llm=llm,
        verbose=True
    )