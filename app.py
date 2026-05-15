from fastapi import FastAPI
from pydantic import BaseModel
from CrewAI_Agent import create_crew_and_run,llm
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Symptoms Analyzer")

class Inputs(BaseModel):
    Gender: str
    Age: str
    Symptoms: str
    City: str

@app.post("/analyze/")
def disease_analyze(data: Inputs):
    result = create_crew_and_run(data.Gender, data.Age, data.Symptoms, data.City)
    if isinstance(result, tuple):
        disease, clinics = result
        response_content = {
            "diagnosis": str(disease),
            "clinics": str(clinics)
        }
    else:
        response_content = {"result": str(result)}

    return jsonable_encoder(response_content)
