import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINIAPI_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

if not GEMINI_API_KEY:
    raise ValueError(" GEMINIAPI_KEY not found in .env file")


def generate_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to Gemini API and returns the generated text response.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        print(" Sending prompt to Gemini API...")
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            print("⚠️ No candidates returned from Gemini.")
            return "Gemini gave no response."

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            print("⚠️ No parts returned in Gemini content.")
            return "Gemini gave an empty response."

        return parts[0].get("text", "Gemini gave no response.")

    except requests.exceptions.RequestException as e:
        print("⚠️ Gemini API request failed:", e)
        return "Gemini failed to respond due to request error."

    except Exception as e:
        print("⚠️ Unexpected error from Gemini:", e)
        return "Gemini failed to respond."
