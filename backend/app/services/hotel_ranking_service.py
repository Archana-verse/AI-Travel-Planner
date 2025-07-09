import json
from app.services.serpapi_service import search_hotels
from app.services.gemini_service import generate_gemini_response
from app.utils.location_utils import resolve_city_from_iata


def rank_hotels_with_gemini(hotels, user_prefs):
    """
    Ranks hotels using Gemini based on user preferences.
    Returns top 3 hotels with AI-generated reasoning.
    """
    hotels_json = json.dumps(hotels[:10], indent=2)

    prompt = f"""
You are a hotel analyst. Given these hotel listings:

{hotels_json}

And the user's preferences:
- Destination: {user_prefs['destination']}
- Check-in: {user_prefs['checkin_date']}
- Check-out: {user_prefs['checkout_date']}
- Budget: {user_prefs['budget_range']}
- Travelers: {user_prefs['travelers']}
- Interests: {user_prefs['interests']}
- Diet: {user_prefs.get('dietary_pref', 'No preference')}

Select the top 3 best-value hotels and explain why they are suitable.
Be concise, insightful, and helpful.

Format output as a JSON list of objects with:
name, location, price_per_night, rating, amenities, reason.
"""

    result = generate_gemini_response(prompt)

    try:
        recommendations = json.loads(result)
        return recommendations
    except json.JSONDecodeError:
        print("⚠️ Failed to parse Gemini response as JSON.")
        return []


def get_ranked_hotels_from_iata(iata_code, checkin_date, checkout_date, preferences):
    """
    Fetches hotels for a city (from IATA) and ranks them using Gemini.
    """
    city = resolve_city_from_iata(iata_code)
    hotels = search_hotels(city, checkin_date, checkout_date)

    if not hotels:
        return []

    user_prefs = {
        "destination": city,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "budget_range": preferences.get("budget_range"),
        "travelers": preferences.get("travelers"),
        "interests": preferences.get("interests"),
        "dietary_pref": preferences.get("dietary_pref", None),
    }

    return rank_hotels_with_gemini(hotels, user_prefs)
