"""
main.py — Programmatic entry point for the SympTrack crew.

Use this to run the crew from the terminal or from tests
without needing a Streamlit session.

    python main.py

Or import run() directly in scripts / notebooks:

    from main import run
    disease, clinics = run("Female", "34", "fatigue, joint pain", "Delhi")
"""

import logging
from typing import Tuple

from config import validate_api_keys
from crew import SympTrackCrew
from validators import parse_patient_input, validate_patient_inputs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(
    gender: str,
    age: str,
    symptoms: str,
    city: str,
) -> Tuple[str, str]:
    """
    Validate inputs, kick off the crew, and return results.

    Returns:
        (diagnosis_text, clinic_text)

    Raises:
        ValueError: if inputs fail validation
        EnvironmentError: if required API keys are missing
        Exception: on crew execution failure
    """
    # 1 — Validate API keys before doing anything
    validate_api_keys()

    # 2 — Validate inputs
    errors = validate_patient_inputs(gender, age, symptoms, city)
    if errors:
        raise ValueError("Invalid inputs:\n" + "\n".join(f"  • {e}" for e in errors))

    patient = parse_patient_input(gender, age, symptoms, city)

    # 3 — Build inputs dict for placeholder resolution in YAML
    inputs = {
        "gender": patient.gender,
        "age": str(patient.age),
        "symptoms": patient.symptoms,
        "city": patient.city,
    }

    logger.info("Starting SympTrack crew for patient: %s, %s, %s", patient.gender, patient.age, patient.city)

    # 4 — Kick off the crew
    result = SympTrackCrew().crew().kickoff(inputs=inputs)

    diagnosis = (
        result.tasks_output[0].raw
        if result.tasks_output
        else "No diagnosis available."
    )
    clinics = (
        result.tasks_output[1].raw
        if len(result.tasks_output) > 1
        else "No clinic suggestions available."
    )

    return diagnosis, clinics


if __name__ == "__main__":
    # Quick smoke-test with sample data
    diagnosis, clinics = run(
        gender="Male",
        age="30",
        symptoms="fever, cough, sore throat",
        city="Lucknow",
    )
    print("\n===== DIAGNOSIS =====")
    print(diagnosis)
    print("\n===== CLINICS =====")
    print(clinics)