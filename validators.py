"""
validators.py — Patient input validation.

Pure Python — zero Streamlit or CrewAI imports.
This means validation logic is fully testable with pytest
without spinning up a UI or calling any APIs.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PatientInput:
    """Typed container for validated patient data."""
    gender: str
    age: int
    symptoms: str
    city: str


def validate_patient_inputs(
    gender: str,
    age: str,
    symptoms: str,
    city: str,
) -> List[str]:
    """
    Validate raw string inputs from the UI form.

    Returns a list of human-readable error messages.
    An empty list means all inputs are valid.
    """
    errors: List[str] = []

    if not gender.strip():
        errors.append("Gender is required.")
    if not symptoms.strip():
        errors.append("Symptoms are required.")
    if not city.strip():
        errors.append("City is required.")

    if not age.strip():
        errors.append("Age is required.")
    else:
        try:
            age_num = int(age.strip())
            if not (0 <= age_num <= 150):
                errors.append("Age must be between 0 and 150.")
        except ValueError:
            errors.append("Age must be a valid whole number (e.g., 25).")

    return errors


def parse_patient_input(
    gender: str,
    age: str,
    symptoms: str,
    city: str,
) -> PatientInput:
    """
    Convert raw strings to a typed PatientInput.
    Call only after validate_patient_inputs() returns no errors.
    """
    return PatientInput(
        gender=gender.strip(),
        age=int(age.strip()),
        symptoms=symptoms.strip(),
        city=city.strip(),
    )