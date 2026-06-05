from crewai import Crew
from agents.diagnoser_agent import create_diagnoser_agent
from agents.clinic_agent import create_clinic_agent
from tasks.symptom_tasks import create_symptom_task, create_clinic_task


class SympTrackCrew:

    def run(self, symptoms, age, gender, city):

        diagnoser = create_diagnoser_agent()
        clinic_finder = create_clinic_agent()

        # Step 1: symptom analysis
        task1 = create_symptom_task(diagnoser, symptoms, age, gender)

        # Step 2: clinic search (simplified chaining)
        task2 = create_clinic_task(clinic_finder, city, "derived from task1 output")

        crew = Crew(
            agents=[diagnoser, clinic_finder],
            tasks=[task1, task2],
            verbose=True
        )

        return crew.kickoff()