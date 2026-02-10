import os
import requests


class LLMService:
    def __init__(self):
        # The URL of your Modal deployment
        self.endpoint = os.getenv(
            "MODAL_LLM_URL",
            "https://vidhiai-in--arthasetu-brain-fastapi-app.modal.run/v1/generate",
        )
        # The API Key you set in Modal's environment variables
        self.api_key = os.getenv("API_KEY")

    def get_reasoning(self, query: str, context: str):
        if not self.endpoint:
            return "Error: Modal LLM Endpoint not configured."

        # payload must match your Modal GenerateRequest schema
        payload = {
            "prompt": query,
            "context": context,
            "temperature": 0.1,
            "top_p": 0.9,
            "max_tokens": 1024,
        }

        # Your Modal function specifically checks for 'X-API-Key' header
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

        try:
            print(f"🧠 Calling Modal with X-API-Key...")
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=90,  # Increased for cold starts
            )
            response.raise_for_status()

            data = response.json()
            return data.get("answer", "No answer field found.")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "❌ Auth Error: Invalid X-API-Key on Modal side."
            return f"❌ HTTP Error: {str(e)}"
        except Exception as e:
            return f"❌ LLM Call Failed: {str(e)}"
