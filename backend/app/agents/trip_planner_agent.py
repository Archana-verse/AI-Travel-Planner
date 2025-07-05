from app.services.serpapi_service import search_flights
from app.services.gemini_service import get_ai_flight_recommendation
from app.utils.iata_lookup import get_iata_code

def generate_full_plan(plan):
    # 🔁 Convert city names to IATA airport codes
    origin_code = get_iata_code(plan.from_)
    destination_code = get_iata_code(plan.to)

    # ✈️ Get real-time flights from SerpAPI
    flights = search_flights(origin_code, destination_code, plan.departure_date)

    # 🤖 Get AI recommendation using Gemini
    ai_response = get_ai_flight_recommendation(flights)

    recommended_id = ai_response.get("recommended_id")
    reasoning = ai_response.get("reason", {})

    # 🧠 Mark the recommended flight and add reasoning
    for flight in flights:
        if flight["id"] == recommended_id:
            flight["aiRecommended"] = True
            flight["ai_reasoning"] = reasoning
        else:
            flight["ai_reasoning"] = flight.get("ai_reasoning", {})

    return {
        "flights": flights,
        "hotels": [],      # Will be filled by hotel_agent later
        "itinerary": []    # Will be filled by itinerary_agent later
    }
