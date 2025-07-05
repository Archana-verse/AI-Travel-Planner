import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch API key securely
GEMINI_API_KEY = os.getenv("GEMINIAPI_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Ensure API key is present
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINIAPI_KEY not found in .env file")

def generate_gemini_response(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Safely extract and return generated text
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Gemini gave no response.")

    except requests.exceptions.RequestException as e:
        print("⚠️ Gemini API request failed:", e)
        return "Gemini failed to respond due to request error."

    except Exception as e:
        print("⚠️ Unexpected error from Gemini:", e)
        return "Gemini failed to respond."
