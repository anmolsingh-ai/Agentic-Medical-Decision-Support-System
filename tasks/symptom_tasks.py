from crewai import Task

def create_symptom_task(agent, symptoms, age, gender):
    return Task(
        description=f"""
Patient Information:
Age: {age}
Gender: {gender}
Symptoms: {symptoms}

Step 1: Analyze symptoms carefully
Step 2: Suggest possible diseases (DO NOT give final diagnosis)
Step 3: Keep response medically safe and uncertain
""",

        expected_output="""
A structured list of possible conditions with:
- Disease name
- Reasoning based on symptoms
- Confidence level (low/medium/high)
- Safety disclaimer
""",

        agent=agent
    )


def create_clinic_task(agent, city, diseases):
    return Task(
        description=f"""
Based on possible conditions: {diseases}

Find relevant clinics and doctors in {city}.
Return hospital name, specialization, and location.
""",

        expected_output="""
A list of clinics with:
- Name
- Specialty
- Address
- Contact (if available)
""",

        agent=agent
    )