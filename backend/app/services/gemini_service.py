import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use model safely
def call_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # ✅ This is the correct path
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return ""

# 🔎 Safe JSON parser
def safe_parse_json(text: str):
    try:
        start = text.find('{') if '{' in text else text.find('[')
        if start == -1:
            raise ValueError("No JSON start character found.")
        json_data = text[start:]
        return json.loads(json_data)
    except Exception as e:
        print("❌ JSON parse error:", e)
        return None

# ✈️ Best Flight Selection
def get_best_flight_reason(flights: list, plan) -> tuple:
    if not flights:
        return None, "No flights available."

    prompt = f"""
You are an AI travel planner. A user is flying from {plan.source} to {plan.destination}
on {plan.departure_date} and returning on {plan.return_date}.
Their preferences are:
- Budget: {plan.budget}
- Travel Class: {plan.travel_class}
- Group Type: {plan.group_type}

Here is a list of available flights:
{json.dumps(flights, indent=2)}

Pick the best flight and explain why.
Respond ONLY in this JSON format:
{{
  "index": <index_of_best_flight>,
  "reason": "<reason_for_selection>"
}}
"""
    result = call_gemini(prompt)
    print("🧠 Gemini Flight Output:", result)
    parsed = safe_parse_json(result)
    if not parsed:
        return flights[0], "Default flight"

    best_index = parsed.get("index", 0)
    reason = parsed.get("reason", "No reason provided.")
    if best_index < 0 or best_index >= len(flights):
        best_index = 0
    return flights[best_index], reason

# 🏨 Best Hotel Selection
def get_best_hotel_reason(hotels: list, plan) -> tuple:
    if not hotels:
        return None, "No hotels available."

    prompt = f"""
You are an AI travel planner helping a user plan a trip to {plan.destination}.
The user's preferences:
- Travel Dates: {plan.departure_date} to {plan.return_date}
- Budget: {plan.budget}
- Group Type: {plan.group_type}
- Interests: {', '.join(plan.interests)}
- Dietary: {plan.dietary_preferences}

Here are the available hotels:
{json.dumps(hotels, indent=2)}

Select the best hotel and explain why.
Respond ONLY in this JSON format:
{{
  "index": <index_of_best_hotel>,
  "reason": "<reason_for_selection>"
}}
"""
    result = call_gemini(prompt)
    print("🧠 Gemini Hotel Output:", result)
    parsed = safe_parse_json(result)
    if not parsed:
        return hotels[0], "Default hotel"

    best_index = parsed.get("index", 0)
    reason = parsed.get("reason", "No reason provided.")
    if best_index < 0 or best_index >= len(hotels):
        best_index = 0
    return hotels[best_index], reason

# 📅 Itinerary Generator
def generate_itinerary(plan) -> list:
    prompt = f"""
You are an AI travel expert.

Generate a day-wise itinerary for a user visiting {plan.destination} from {plan.departure_date} to {plan.return_date}.
Preferences:
- Group: {plan.group_type}
- Interests: {', '.join(plan.interests)}
- Dietary: {plan.dietary_preferences}

Respond ONLY in this JSON format:
[
  {{
    "day": 1,
    "plan": "<activities for day 1>"
  }},
  ...
]
"""
    result = call_gemini(prompt)
    print("🧠 Gemini Itinerary Output:", result)
    parsed = safe_parse_json(result)
    if not parsed or not isinstance(parsed, list):
        return [{"day": 1, "plan": "Arrival and relax"}]
    return parsed
