from app.services.serpapi_service import search_hotels
from app.services.gemini_service import generate_gemini_response
import json
import re

def get_hotel_recommendations(city, checkin_date, checkout_date, preferences):
    """
    Uses SerpAPI to fetch hotel listings and Gemini to select the best one
    based on user preferences (interests, budget, travelers, diet).
    """
    hotels = search_hotels(city, checkin_date, checkout_date)
    if not hotels:
        print("⚠️ No hotels returned from SerpAPI.")
        return []

    # 🧠 Prepare prompt for Gemini
    prompt = f"""
You are an AI travel expert helping users choose the best hotel in {city} from {checkin_date} to {checkout_date}.
User preferences:
- Interests: {preferences.get("interests")}
- Budget: {preferences.get("budget")}
- Travelers: {preferences.get("travelers")}
- Diet: {preferences.get("diet")}

Hotels available (in JSON):
{json.dumps(hotels[:5], indent=2)}

Pick one hotel and explain why.
Reply ONLY in JSON like this:
{{
  "recommended_id": "<hotel_id>",
  "reason": {{
    "rating": "...",
    "location": "...",
    "amenities": "...",
    "value": "..."
  }}
}}
"""

    try:
        gemini_reply = generate_gemini_response(prompt)
        print("\n🏨 Gemini Hotel Raw Response:\n", gemini_reply)

        # Extract valid JSON from Gemini reply
        match = re.search(r'\{.*\}', gemini_reply, re.DOTALL)
        if match:
            parsed = json.loads(match.group())

            for hotel in hotels:
                if hotel["id"] == parsed.get("recommended_id"):
                    hotel["aiRecommended"] = True
                    hotel["ai_reasoning"] = parsed.get("reason", {})
                else:
                    hotel["ai_reasoning"] = hotel.get("ai_reasoning", {})
        else:
            print("⚠️ No valid JSON found in Gemini hotel reply.")

    except Exception as e:
        print("⚠️ Error in hotel recommendation:", e)

    return hotels
