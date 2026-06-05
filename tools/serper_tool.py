import os
import requests
from crewai.tools import BaseTool


class SerperSearchTool(BaseTool):
    name: str = "serper_search"
    description: str = "Search for clinics and doctors using Google Serper API"

    def _run(self, query: str):
        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }

        payload = {"q": query}

        response = requests.post(url, json=payload, headers=headers)
        return response.json()