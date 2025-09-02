from app.services.serpapi_service import search_hotels
from app.services.gemini_service import generate_gemini_response
import json
import re
import random
from datetime import datetime


def get_hotel_recommendations(city, checkin_date, checkout_date, preferences):
    """
    Uses SerpAPI to fetch hotel listings and Gemini to select the best one
    based on user preferences (interests, budget, travelers, diet).
    """
    hotels = search_hotels(city, checkin_date, checkout_date)

    if not hotels:
        print("⚠️ No hotels returned from SerpAPI. Using fallback hotels.")
        affordability = preferences.get("hotelAffordability", "medium")
        hotels = generate_fallback_hotels(city, checkin_date, checkout_date, affordability)
    else:
        # Fallback pricing for hotels with no price
        affordability = preferences.get("hotelAffordability", "medium")
        for hotel in hotels:
            if "price" not in hotel or hotel["price"] is None:
                hotel["price"] = estimate_price_from_name(hotel.get("name", ""), hotel.get("description", ""), affordability)
                hotel["priceFallback"] = True
            else:
                hotel["priceFallback"] = False

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


def estimate_price_from_name(name: str, desc: str, affordability: str) -> int:
    """
    Estimate price based on name/description and affordability.
    """
    text = (name + " " + desc).lower()
    is_oyo = "oyo" in text
    is_basic = any(word in text for word in ["budget", "lodge", "inn"])
    is_luxury = any(word in text for word in ["resort", "5-star", "luxury", "palace"])
    is_midrange = any(word in text for word in ["residency", "comfort", "classic"])

    if affordability == "low":
        if is_oyo or is_basic:
            return random.randint(800, 1200)
        elif is_midrange:
            return random.randint(1200, 1800)
        else:
            return random.randint(1500, 2200)

    elif affordability == "high":
        if is_luxury:
            return random.randint(6000, 9000)
        elif is_midrange:
            return random.randint(4500, 6000)
        else:
            return random.randint(3500, 5000)

    # default = medium
    if is_oyo or is_basic:
        return random.randint(1500, 2500)
    elif is_luxury:
        return random.randint(5000, 7000)
    elif is_midrange:
        return random.randint(2500, 4000)
    return random.randint(3000, 4500)


def generate_fallback_hotels(city, checkin_date, checkout_date, affordability="medium"):
    sample_hotels = [
        {
            "id": f"fallback-{i}",
            "name": f"{prefix} {city} Stay {i+1}",
            "rating": round(random.uniform(3.8, 4.9), 1),
            "reviews": random.randint(200, 800),
            "location": f"{city} Central",
            "description": f"A {prefix.lower()} accommodation in {city} with great access to city highlights.",
            "price": estimate_price_from_name(prefix, city, affordability),
            "priceFallback": True,
            "image": f"https://via.placeholder.com/300x200?text=Hotel+{i+1}",
            "amenities": ["Free WiFi", "Restaurant", "24h Desk", "Air Conditioning"]
        }
        for i, prefix in enumerate(["Budget", "Popular", "Top Rated"])
    ]
    return sample_hotels
