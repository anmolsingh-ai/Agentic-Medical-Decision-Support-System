import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai import LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
os.environ["SERPER_API_KEY"] = "YOUR_SERPER_API_KEY"

st.set_page_config(layout="wide", page_title="CrewAI Streamlit Interface")
st.title("🤖 Symptoms Analyzer")

# Initialize LLM
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.4
)

# Tool
Search = SerperDevTool()

with st.form("Symptoms"):
    Gender = st.text_input("Your Gender:").strip()
    Age = st.text_input("Your Age:").strip()
    Symptoms = st.text_input("Symptoms You Are Facing:", placeholder="Write all your symptoms here, comma-separated").strip()
    City = st.text_input("Your City:").strip()

    submit_btn = st.form_submit_button("🔍 Analyze")

def create_crew_and_run(Gender, Age, Symptoms, City):
    diagnoser = Agent(
        name="Diagnoser",
        role="Disease Diagnoser",
        goal=f"Diagnose a disease or illness from {Gender}, {Age}, {Symptoms}. Check for emergency red flags.",
        backstory="You are a highly professional medical expert who can accurately diagnose diseases and provide effective treatments.",
        llm=llm
    )

    clinic_suggestor = Agent(
        name="Clinic_Suggestor",
        role="Clinic Suggestor",
        goal=f"Suggest clinics based on the treatment required by the patient along with contact and address details in {City}.",
        backstory="You are a healthcare assistant who suggests top-rated clinics and hospitals for the required treatment.",
        llm=llm
    )

    disease_task = Task(
        name="Disease_Diagnoser",
        description=f"Diagnose diseases or illnesses from {Gender}, {Age}, {Symptoms}. After diagnosis, provide detailed and safe treatments.",
        expected_output="List 2-3 possible diseases with detailed treatment recommendations in a clear and understandable format.",
        agent=diagnoser
    )

    clinic_task = Task(
        name="Clinic_Suggestion",
        context=[disease_task],
        description=f"Using the {Search}, suggest 2-3 good clinics in {City} based on the required treatment with address and contact info.",
        expected_output="Provide clinic name, address, and contact in an easy-to-read format.",
        agent=clinic_suggestor
    )

    crew = Crew(
        agents=[diagnoser, clinic_suggestor],
        tasks=[disease_task, clinic_task]
    )

    with st.spinner("🤖 Crew is analyzing symptoms..."):
        result = crew.kickoff()
        disease=result.tasks_output[0].raw
        clinics=result.tasks_output[1].raw

    return disease, clinics

if submit_btn:
        disease, clinics = create_crew_and_run(Gender, Age, Symptoms, City)
        st.markdown("## 🧠 Disease Diagnosis")
        st.write(disease)
        st.markdown("## 🏥 Clinic Suggestions")
        st.write(clinics)