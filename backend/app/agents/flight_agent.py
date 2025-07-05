from app.services.serpapi_service import search_flights
from app.services.gemini_service import generate_gemini_response
import json

def get_flight_recommendations(from_city, to_city, departure_date, preferences):
    flights = search_flights(from_city, to_city, departure_date)

    if not flights:
        return []

    # Sort by price and mark the cheapest flight
    def clean_price(price_str):
        return int(str(price_str).replace("₹", "").replace(",", "").strip())

    flights.sort(key=lambda x: clean_price(x["price"]))
    flights[0]["cheapest"] = True

    # Prepare structured prompt for Gemini
    try:
        prompt = f"""
You are an AI travel assistant. A user is flying from {from_city} to {to_city} on {departure_date}.
Their preferences: interests = {preferences.get("interests")}, class = {preferences.get("travelClass")}, diet = {preferences.get("diet")}.

Here are available flight options (in JSON format):
{json.dumps(flights, indent=2)}

Pick the best flight and explain why.
Respond ONLY in this strict JSON format:
{{
  "recommended_id": "<flight_id>",
  "reason": {{
    "price": "...",
    "duration": "...",
    "airline": "...",
    "departure": "..."
  }}
}}
        """.strip()

        gemini_reply = generate_gemini_response(prompt)
        print("\n🧠 Gemini Raw Response:\n", gemini_reply)

        # Strip markdown and extract JSON only
        gemini_reply = gemini_reply.strip()

        # Remove backticks and ```json if present
        if gemini_reply.startswith("```json"):
            gemini_reply = gemini_reply[7:]
        if gemini_reply.endswith("```"):
            gemini_reply = gemini_reply[:-3]

        parsed = json.loads(gemini_reply)

        # Match and update the recommended flight
        for flight in flights:
            if flight["id"] == parsed.get("recommended_id"):
                flight["aiRecommended"] = True
                flight["aiReasoning"] = parsed.get("reason", {})
                flight["popular"] = True

    except json.JSONDecodeError as je:
        print("⚠️ JSON Decode Error from Gemini:", je)
        print("⚠️ Raw Gemini reply:", gemini_reply)
    except Exception as e:
        print("⚠️ Gemini AI Reasoning Error:", e)

    return flights
