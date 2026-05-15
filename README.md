# 🧠 SympTrack — Multi-Agent Symptom Analyzer & Clinic Suggestion System

> **An AI-powered healthcare assistant** that diagnoses the most probable diseases from symptoms and suggests the best nearby clinics using **CrewAI**, **Gemini LLM**, and **Streamlit**.

---

## 🚀 Overview

**SympTrack** is a **multi-agent system** built using [CrewAI](https://github.com/joaomdmoura/crewAI) that:
1. Analyzes user-provided symptoms (age, gender, city, symptoms).
2. Diagnoses the **most probable diseases** using an AI medical expert.
3. Suggests **reputed clinics nearby** for consultation and treatment.

This app provides a simple **Streamlit UI** for interaction and can easily integrate with a **FastAPI backend** for production use.

---

## 🧩 Features

✅ Multi-agent architecture using **CrewAI**  
✅ AI-powered disease diagnosis using **Google Gemini**  
✅ Clinic search using **Serper API**  
✅ User-friendly **Streamlit interface**  
✅ Expandable to include appointment booking & patient record storage  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend / UI** | Streamlit |
| **Backend (LLM Agents)** | CrewAI |
| **LLM Provider** | Google Gemini (`crewai[google-genai]`) |
| **Search Tool** | Serper.dev API |
| **Optional Backend API** | FastAPI |
| **Language** | Python 3.10+ |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/medicrew-ai.git
cd medicrew-ai

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -U crewai streamlit python-dotenv
pip install "crewai[google-genai]"
or
pip install -r requirements.txt

4. Set Environment Variables
Create a .env file in the project root and add:
SERPER_API_KEY=your_serper_api_key
GOOGLE_API_KEY=your_google_api_key

🧠 How It Works

The system uses two agents:

Disease Diagnoser Agent – analyzes symptoms and returns probable diseases + treatments.

Clinic Suggestor Agent – searches clinics in your city using Serper.dev.

Both are coordinated via CrewAI’s Crew() class.
Example flow:
User Input ➜ Diagnoser Agent ➜ Predicted Disease ➜ Clinic Agent ➜ Output Clinics

🖥️ Run the Streamlit App
streamlit run app.py or python -m streamlit run app.py

🧩 Example Output:

👨‍⚕️ Most Probable Diseases:
- Influenza (Flu)
- Common Cold
- Acute Bronchitis

💊 Suggested Clinics (Lucknow):
- Mayo Clinic — 200 First St SW, Rochester, MN — (507) 284-2511
- Medanta Hospital — Lucknow — (0522) 4505050
