# SympTrack — Agentic Medical Decision Support System

SympTrack is a Streamlit-based application that uses CrewAI and Zhipu AI to analyze a patient’s symptoms and provide:

- a structured diagnosis report,
- treatment suggestions,
- emergency red-flag guidance, and
- clinic or hospital recommendations for the selected city.

The app is intended for educational purposes only and should not replace professional medical advice.

## Features

- Clean Streamlit frontend for symptom input
- Multi-agent workflow with:
  - a medical diagnoser agent
  - a clinic recommendation agent
- Progressive text streaming in the UI so responses appear step by step
- Input validation for patient details
- Environment-based API key handling

## Project structure

- [app.py](app.py) — Streamlit user interface
- [main.py](main.py) — Programmatic entry point for running the workflow
- [crew.py](crew.py) — CrewAI agent and task orchestration
- [config.py](config.py) — LLM and environment configuration
- [validators.py](validators.py) — Patient input validation
- [config/agents.yaml](config/agents.yaml) — Agent instructions
- [config/tasks.yaml](config/tasks.yaml) — Task prompts and expected outputs
- [tools/__init__.py](tools/__init__.py) — Search tooling for clinic lookup

## Requirements

Python 3.11 is recommended.

Install dependencies:

```powershell
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in the project root with:

```env
ZHIPU_API_KEY=your_zhipu_api_key
SERPER_API_KEY=your_serper_api_key
```

## Run locally

```powershell
streamlit run app.py
```

## Run as a Python script

```powershell
venv\Scripts\python.exe main.py
```

## Deployment notes

If you deploy to Render or another cloud platform:

- use Python 3.11,
- set the same environment variables in the hosting dashboard,
- ensure the app starts with Streamlit on the assigned port.

Example Render start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Notes

- Do not commit your `.env` file. It is already ignored in [.gitignore](.gitignore).
- The system is meant for educational use and should not be treated as medical diagnosis or treatment advice.
