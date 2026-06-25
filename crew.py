"""
crew.py — SympTrack multi-agent crew definition.

Uses the official CrewAI @CrewBase decorator pattern:
  - Agent definitions → loaded from config/agents.yaml
  - Task definitions  → loaded from config/tasks.yaml
  - Each @agent / @task method maps YAML config onto a live object
  - @crew assembles everything and exposes .kickoff(inputs={...})

Usage:
    from crew import SympTrackCrew

    result = SympTrackCrew().crew().kickoff(inputs={
        "gender": "Male",
        "age": "28",
        "symptoms": "fever, cough, headache",
        "city": "Mumbai",
    })
"""

import logging

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from config import get_llm
from tools import get_search_tool

logger = logging.getLogger(__name__)


@CrewBase
class SympTrackCrew:
    """
    SympTrack: Agentic Medical Decision Support System.

    Two-agent sequential crew:
      1. Diagnoser     — identifies possible conditions from symptoms
      2. ClinicSuggestor — finds real clinics via web search
    """

    # Paths are relative to this file; CrewBase resolves them automatically
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ------------------------------------------------------------------ #
    # Agents                                                               #
    # ------------------------------------------------------------------ #

    @agent
    def diagnoser(self) -> Agent:
        """
        Medical expert agent.
        Receives patient profile via task description placeholders
        ({gender}, {age}, {symptoms}) — no f-strings needed here.
        """
        return Agent(
            config=self.agents_config["diagnoser"],  # type: ignore[index]
            llm=get_llm(),
            verbose=True,
            # No tools: deliberate reasoning from medical knowledge
        )

    @agent
    def clinic_suggestor(self) -> Agent:
        """
        Healthcare navigator agent.
        Uses web search to find real, currently operating clinics.
        """
        return Agent(
            config=self.agents_config["clinic_suggestor"],  # type: ignore[index]
            llm=get_llm(),
            tools=[get_search_tool()],
            verbose=True,
        )

    # ------------------------------------------------------------------ #
    # Tasks                                                                #
    # ------------------------------------------------------------------ #

    @task
    def diagnosis_task(self) -> Task:
        """
        Primary task: diagnose from symptoms.
        Placeholders in tasks.yaml are resolved at kickoff() time via `inputs`.
        """
        return Task(
            config=self.tasks_config["diagnosis_task"],  # type: ignore[index]
        )

    @task
    def clinic_task(self) -> Task:
        """
        Secondary task: recommend clinics based on the diagnosis.
        `context` chains it after diagnosis_task so the agent sees
        the previous output automatically.
        """
        return Task(
            config=self.tasks_config["clinic_task"],  # type: ignore[index]
            context=[self.diagnosis_task()],
        )

    # ------------------------------------------------------------------ #
    # Crew                                                                 #
    # ------------------------------------------------------------------ #

    @crew
    def crew(self) -> Crew:
        """
        Assemble the crew.

        self.agents and self.tasks are auto-populated by @CrewBase
        from the decorated methods above — no manual list needed.
        """
        return Crew(
            agents=self.agents,   # type: ignore[attr-defined]
            tasks=self.tasks,     # type: ignore[attr-defined]
            process=Process.sequential,
            verbose=True,
        )