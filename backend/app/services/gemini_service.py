import json
from app.services.gemini_service import call_gemini

def get_best_flight_reason(flights: list, plan) -> tuple:
    if not flights:
        return None, "No flights available."

    flight_json = json.dumps(flights, indent=2)
    prompt = f"""
You are an AI travel planner. A user is flying from {plan.source} to {plan.destination}
on {plan.departure_date} and returning on {plan.return_date}.
Their preferences are:
- Budget: {plan.budget}
- Travel Class: {plan.travel_class}
- Group Type: {plan.group_type}

Here is a list of available flights:
{flight_json}

Pick the best flight from the list and explain why it's the best match.
Respond ONLY in this JSON format:

{{
  "index": <index_of_best_flight>,
  "reason": "<reason_for_selection>"
}}
"""

    try:
        result = call_gemini(prompt)
        print("🧠 Gemini Flight Output:", result)
        parsed = json.loads(result)
        best_index = parsed.get("index", -1)
        reason = parsed.get("reason", "No reason provided.")
        if best_index == -1 or best_index >= len(flights):
            return flights[0], "Default flight"
        return flights[best_index], reason
    except Exception as e:
        print("❌ Gemini flight reasoning error:", e)
        return flights[0], "Default flight"


def get_best_hotel_reason(hotels: list, plan) -> tuple:
    if not hotels:
        return None, "No hotels available."

    hotel_json = json.dumps(hotels, indent=2)
    prompt = f"""
You are an AI travel planner helping a user plan a trip to {plan.destination}.
The user's preferences:
- Travel Dates: {plan.departure_date} to {plan.return_date}
- Budget: {plan.budget}
- Group Type: {plan.group_type}
- Interests: {', '.join(plan.interests)}
- Dietary: {plan.dietary_preferences}

Here are the available hotels:
{hotel_json}

Select the best hotel and explain why. Respond ONLY in this JSON format:

{{
  "index": <index_of_best_hotel>,
  "reason": "<reason_for_selection>"
}}
"""

    try:
        result = call_gemini(prompt)
        print("🧠 Gemini Hotel Output:", result)
        parsed = json.loads(result)
        best_index = parsed.get("index", -1)
        reason = parsed.get("reason", "No reason provided.")
        if best_index == -1 or best_index >= len(hotels):
            return hotels[0], "Default hotel"
        return hotels[best_index], reason
    except Exception as e:
        print("❌ Gemini hotel reasoning error:", e)
        return hotels[0], "Default hotel"


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

    try:
        result = call_gemini(prompt)
        print("🧠 Gemini Itinerary Output:", result)
        parsed = json.loads(result)
        return parsed
    except Exception as e:
        print("❌ Gemini itinerary error:", e)
        return [{"day": 1, "plan": "Arrival and relax"}]
