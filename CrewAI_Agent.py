import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai import LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate API Keys
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not ZHIPU_API_KEY or not SERPER_API_KEY:
    st.error("❌ Missing API Keys! Please set ZHIPU_API_KEY and SERPER_API_KEY in your .env file")
    st.stop()

os.environ["ZHIPU_API_KEY"] = ZHIPU_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

# Page config
st.set_page_config(layout="wide", page_title="CrewAI Streamlit Interface")
st.title("🤖 Symptoms Analyzer")

# Initialize LLM with Zhipu AI
try:
    llm = LLM(
        model="glm-4.5-flash",  # Using Zhipu AI model
        api_key=ZHIPU_API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.4
    )
    st.success("✅ Zhipu AI LLM initialized successfully!")
except Exception as e:
    st.error(f"❌ Failed to initialize Zhipu AI LLM: {str(e)}")
    st.info("Make sure your API key is valid and has access to GLM-4.5-Flash model")
    logger.error(f"Zhipu AI initialization error: {str(e)}")
    st.stop()

# Tool
try:
    Search = SerperDevTool()
except Exception as e:
    st.error(f"❌ Failed to initialize Search Tool: {str(e)}")
    st.stop()

# Add disclaimer
with st.expander("⚠️ Medical Disclaimer"):
    st.warning(
        "This tool is for educational purposes only and should NOT be used for actual medical diagnosis. "
        "Always consult with a qualified healthcare professional for medical advice. "
        "In case of emergency, call your local emergency services immediately."
    )

# Form
with st.form("Symptoms_Form"):
    col1, col2 = st.columns(2)
    
    with col1:
        Gender = st.text_input("Your Gender:", placeholder="e.g., Male, Female").strip()
        Age = st.text_input("Your Age:", placeholder="e.g., 25").strip()
    
    with col2:
        City = st.text_input("Your City:", placeholder="e.g., New York").strip()
        Symptoms = st.text_input(
            "Symptoms You Are Facing:", 
            placeholder="Write all your symptoms here, comma-separated\ne.g., fever, cough, headache"
        ).strip()
    
    submit_btn = st.form_submit_button("🔍 Analyze", use_container_width=True)

def validate_inputs(Gender, Age, Symptoms, City):
    """Validate user inputs"""
    errors = []
    
    if not Gender:
        errors.append("Gender is required")
    if not Age:
        errors.append("Age is required")
    if not Symptoms:
        errors.append("Symptoms are required")
    if not City:
        errors.append("City is required")
    
    # Validate age is numeric
    if Age:
        try:
            age_num = int(Age)
            if age_num < 0 or age_num > 150:
                errors.append("Age must be between 0 and 150")
        except ValueError:
            errors.append("Age must be a valid number")
    
    return errors

def create_crew_and_run(Gender, Age, Symptoms, City):
    """Create crew and run analysis"""
    try:
        diagnoser = Agent(
            name="Diagnoser",
            role="Disease Diagnoser",
            goal=f"Diagnose a disease or illness from {Gender}, {Age} years old, with symptoms: {Symptoms}. Check for emergency red flags.",
            backstory="You are a highly professional medical expert who can accurately diagnose diseases and provide effective treatments.",
            llm=llm,
            verbose=True
        )

        clinic_suggestor = Agent(
            name="Clinic_Suggestor",
            role="Clinic Suggestor",
            goal=f"Suggest clinics based on the treatment required by the patient along with contact and address details in {City}.",
            backstory="You are a healthcare assistant who suggests top-rated clinics and hospitals for the required treatment.",
            llm=llm,
            verbose=True
        )

        disease_task = Task(
            name="Disease_Diagnoser",
            description=f"Diagnose diseases or illnesses from Gender: {Gender}, Age: {Age}, Symptoms: {Symptoms}. After diagnosis, provide detailed and safe treatments. IMPORTANT: Always remind that this is for educational purposes only and they should consult a real doctor.",
            expected_output="List 2-3 possible diseases with detailed treatment recommendations in a clear and understandable format.",
            agent=diagnoser
        )

        clinic_task = Task(
            name="Clinic_Suggestion",
            context=[disease_task],
            description=f"Using web search, suggest 2-3 good clinics in {City} based on the required treatment with address and contact info. If exact clinics cannot be found, provide general guidance on types of healthcare facilities to visit.",
            expected_output="Provide clinic name, address, phone number, and website (if available) in an easy-to-read format.",
            agent=clinic_suggestor
        )

        crew = Crew(
            agents=[diagnoser, clinic_suggestor],
            tasks=[disease_task, clinic_task],
            verbose=True
        )

        result = crew.kickoff()
        
        disease = result.tasks_output[0].raw if result.tasks_output else "No diagnosis available"
        clinics = result.tasks_output[1].raw if len(result.tasks_output) > 1 else "No clinic suggestions available"
        
        return disease, clinics
    
    except Exception as e:
        logger.error(f"Error during crew execution: {str(e)}")
        raise

if submit_btn:
    # Validate inputs
    validation_errors = validate_inputs(Gender, Age, Symptoms, City)
    
    if validation_errors:
        st.error("❌ Please fix the following errors:")
        for error in validation_errors:
            st.error(f"  • {error}")
    else:
        try:
            with st.spinner("🤖 Crew is analyzing symptoms with Zhipu AI... This may take a minute..."):
                disease, clinics = create_crew_and_run(Gender, Age, Symptoms, City)
            
            st.success("✅ Analysis Complete!")
            
            st.markdown("## 🧠 Disease Diagnosis")
            st.write(disease)
            
            st.markdown("## 🏥 Clinic Suggestions")
            st.write(clinics)
            
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.info("Please check your Zhipu AI API key and try again. Make sure you have a valid ZHIPU_API_KEY in your .env file")
            logger.error(f"Error: {str(e)}")
import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai import LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate API Keys
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not ZHIPU_API_KEY or not SERPER_API_KEY:
    st.error("❌ Missing API Keys! Please set ZHIPU_API_KEY and SERPER_API_KEY in your .env file")
    st.stop()

os.environ["ZHIPU_API_KEY"] = ZHIPU_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

# Page config
st.set_page_config(layout="wide", page_title="CrewAI Streamlit Interface")
st.title("🤖 Symptoms Analyzer")

# Initialize LLM with Zhipu AI
try:
    llm = LLM(
        model="glm-4.5-flash",  # Using Zhipu AI model
        api_key=ZHIPU_API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        temperature=0.4
    )
    st.success("✅ Zhipu AI LLM initialized successfully!")
except Exception as e:
    st.error(f"❌ Failed to initialize Zhipu AI LLM: {str(e)}")
    st.info("Make sure your API key is valid and has access to GLM-4.5-Flash model")
    logger.error(f"Zhipu AI initialization error: {str(e)}")
    st.stop()

# Tool
try:
    Search = SerperDevTool()
except Exception as e:
    st.error(f"❌ Failed to initialize Search Tool: {str(e)}")
    st.stop()

# Add disclaimer
with st.expander("⚠️ Medical Disclaimer"):
    st.warning(
        "This tool is for educational purposes only and should NOT be used for actual medical diagnosis. "
        "Always consult with a qualified healthcare professional for medical advice. "
        "In case of emergency, call your local emergency services immediately."
    )

# Form
with st.form("Symptoms_Form"):
    col1, col2 = st.columns(2)
    
    with col1:
        Gender = st.text_input("Your Gender:", placeholder="e.g., Male, Female").strip()
        Age = st.text_input("Your Age:", placeholder="e.g., 25").strip()
    
    with col2:
        City = st.text_input("Your City:", placeholder="e.g., New York").strip()
        Symptoms = st.text_input(
            "Symptoms You Are Facing:", 
            placeholder="Write all your symptoms here, comma-separated\ne.g., fever, cough, headache"
        ).strip()
    
    submit_btn = st.form_submit_button("🔍 Analyze", use_container_width=True)

def validate_inputs(Gender, Age, Symptoms, City):
    """Validate user inputs"""
    errors = []
    
    if not Gender:
        errors.append("Gender is required")
    if not Age:
        errors.append("Age is required")
    if not Symptoms:
        errors.append("Symptoms are required")
    if not City:
        errors.append("City is required")
    
    # Validate age is numeric
    if Age:
        try:
            age_num = int(Age)
            if age_num < 0 or age_num > 150:
                errors.append("Age must be between 0 and 150")
        except ValueError:
            errors.append("Age must be a valid number")
    
    return errors

def create_crew_and_run(Gender, Age, Symptoms, City):
    """Create crew and run analysis"""
    try:
        diagnoser = Agent(
            name="Diagnoser",
            role="Disease Diagnoser",
            goal=f"Diagnose a disease or illness from {Gender}, {Age} years old, with symptoms: {Symptoms}. Check for emergency red flags.",
            backstory="You are a highly professional medical expert who can accurately diagnose diseases and provide effective treatments.",
            llm=llm,
            verbose=True
        )

        clinic_suggestor = Agent(
            name="Clinic_Suggestor",
            role="Clinic Suggestor",
            goal=f"Suggest clinics based on the treatment required by the patient along with contact and address details in {City}.",
            backstory="You are a healthcare assistant who suggests top-rated clinics and hospitals for the required treatment.",
            llm=llm,
            verbose=True
        )

        disease_task = Task(
            name="Disease_Diagnoser",
            description=f"Diagnose diseases or illnesses from Gender: {Gender}, Age: {Age}, Symptoms: {Symptoms}. After diagnosis, provide detailed and safe treatments. IMPORTANT: Always remind that this is for educational purposes only and they should consult a real doctor.",
            expected_output="List 2-3 possible diseases with detailed treatment recommendations in a clear and understandable format.",
            agent=diagnoser
        )

        clinic_task = Task(
            name="Clinic_Suggestion",
            context=[disease_task],
            description=f"Using web search, suggest 2-3 good clinics in {City} based on the required treatment with address and contact info. If exact clinics cannot be found, provide general guidance on types of healthcare facilities to visit.",
            expected_output="Provide clinic name, address, phone number, and website (if available) in an easy-to-read format.",
            agent=clinic_suggestor
        )

        crew = Crew(
            agents=[diagnoser, clinic_suggestor],
            tasks=[disease_task, clinic_task],
            verbose=True
        )

        result = crew.kickoff()
        
        disease = result.tasks_output[0].raw if result.tasks_output else "No diagnosis available"
        clinics = result.tasks_output[1].raw if len(result.tasks_output) > 1 else "No clinic suggestions available"
        
        return disease, clinics
    
    except Exception as e:
        logger.error(f"Error during crew execution: {str(e)}")
        raise

if submit_btn:
    # Validate inputs
    validation_errors = validate_inputs(Gender, Age, Symptoms, City)
    
    if validation_errors:
        st.error("❌ Please fix the following errors:")
        for error in validation_errors:
            st.error(f"  • {error}")
    else:
        try:
            with st.spinner("🤖 Crew is analyzing symptoms with Zhipu AI... This may take a minute..."):
                disease, clinics = create_crew_and_run(Gender, Age, Symptoms, City)
            
            st.success("✅ Analysis Complete!")
            
            st.markdown("## 🧠 Disease Diagnosis")
            st.write(disease)
            
            st.markdown("## 🏥 Clinic Suggestions")
            st.write(clinics)
            
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.info("Please check your Zhipu AI API key and try again. Make sure you have a valid ZHIPU_API_KEY in your .env file")
            logger.error(f"Error: {str(e)}")