import os
import requests

class LLMService:
    def __init__(self):
        self.endpoint = os.getenv("MODAL_LLM_URL")

    def get_reasoning(self, query: str, context: str):
        prompt = f"System: Use context to answer. Context: {context}\nUser: {query}"
        response = requests.post(self.endpoint, json={"prompt": prompt})
        return response.json().get("answer", "Error connecting to LLM")
