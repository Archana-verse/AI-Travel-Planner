from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
from app.services.gemini_service import generate_gemini_response
import json, re

router = APIRouter()

class ItineraryRequest(BaseModel):
    to: str
    departureDate: str
    returnDate: str
    interests: List[str]
    travelers: str
    diet: str

@router.post("/api/itinerary")
async def generate_itinerary(request: Request):
    try:
        body = await request.json()
        print("🟡 Received from frontend:", body)

        parsed = ItineraryRequest(**body)

        prompt = f"""
You are an AI travel planner. Generate a 3-day itinerary for a trip to {parsed.to} from {parsed.departureDate} to {parsed.returnDate}.
Preferences:
- Interests: {', '.join(parsed.interests)}
- Group: {parsed.travelers}
- Diet: {parsed.diet}

Respond ONLY in JSON format:
[
  {{
    "day": 1,
    "date": "{parsed.departureDate}",
    "title": "Arrival & Exploration",
    "activities": [
      {{ "time": "10:00 AM", "icon": "🛬", "activity": "Land at airport" }}
    ]
  }}
]
"""

        reply = generate_gemini_response(prompt)
        print("🟢 Gemini raw reply:\n", reply)

        match = re.search(r'\[.*\]', reply, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return {"error": "Invalid JSON response from Gemini."}

    except Exception as e:
        print("❌ Itinerary Error:", e)
        return {"error": str(e)}
