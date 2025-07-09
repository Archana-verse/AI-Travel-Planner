from app.services.gemini_service import generate_gemini_response
import re
import json

def generate_daywise_itinerary(city, from_date, to_date, preferences):
    """
    Generates a day-wise itinerary using Gemini based on city, dates, and user preferences.
    """

    # 🧠 Build prompt
    prompt = f"""
You are an AI travel planner. Generate a 3-day itinerary for a trip to {city} from {from_date} to {to_date}.
Preferences:
- Interests: {preferences.get("interests")}
- Group: {preferences.get("travelers")}
- Diet: {preferences.get("diet")}

Respond ONLY in JSON format:
[
  {{
    "day": 1,
    "date": "{from_date}",
    "title": "Arrival & Exploration",
    "activities": [
      {{ "time": "10:00 AM", "title": "Visit XYZ", "details": "..." }},
      ...
    ]
  }},
  ...
]
"""

    try:
        reply = generate_gemini_response(prompt)
        print("\n🗓️ Gemini Itinerary Raw Response:\n", reply)

        # 🔍 Extract JSON list from Gemini output
        match = re.search(r'\[.*\]', reply, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            print("⚠️ No valid JSON array found in Gemini response.")

    except Exception as e:
        print("⚠️ Error generating itinerary:", e)

    return []
