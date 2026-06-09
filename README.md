# CrewAI Symptoms Analyzer

Simple Streamlit app that uses CrewAI and Zhipu AI to analyze symptoms and suggest clinics (educational purposes only).

## Deploy to Render

- Ensure `runtime.txt` is `python-3.11.9` (already present).
- Add the following environment variables in the Render dashboard:
  - `ZHIPU_API_KEY`
  - `SERPER_API_KEY`

Create a `Procfile` (already included) with the start command:

```bash
web: streamlit run CrewAI_Agent.py --server.port $PORT --server.address 0.0.0.0
```

## Local setup

```powershell
# Create a Python 3.11 venv (Windows)
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
streamlit run CrewAI_Agent.py
```

## Notes
- Do not commit `.env` (it is in `.gitignore`).
- Ensure the rendered service uses Python 3.11 to avoid binary build issues (numpy wheels, etc.).
