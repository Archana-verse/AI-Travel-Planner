from app.agents.flight_agent import get_flight_recommendations
from app.agents.hotel_agent import get_hotel_recommendations
from app.agents.itinerary_agent import generate_daywise_itinerary
from app.utils.iata_lookup import get_iata_code  

def generate_full_plan(plan):
    """
    Orchestrates the full travel planning process:
    - Fetches flight options (city name → IATA)
    - Recommends hotels (city name directly)
    - Generates daywise itinerary
    """
    preferences = plan.dict()

    # ✅ Convert city names to IATA codes for flights only
    from_iata = get_iata_code(preferences["from_"])
    to_iata = get_iata_code(preferences["to"])

    # ✈️ Flight Recommendations
    flights = get_flight_recommendations(
        from_city=from_iata,
        to_city=to_iata,
        departure_date=preferences["departureDate"],
        preferences=preferences
    )

    # 🏨 Hotel Recommendations (use city name as-is)
    hotels = get_hotel_recommendations(
        city=preferences["to"],
        checkin_date=preferences["departureDate"],
        checkout_date=preferences["returnDate"],
        preferences=preferences
    )

    # 📅 Itinerary Generation (use city name as-is)
    itinerary = generate_daywise_itinerary(
        city=preferences["to"],
        from_date=preferences["departureDate"],
        to_date=preferences["returnDate"],
        preferences=preferences
    )

    return {
        "flights": flights,
        "hotels": hotels,
        "itinerary": itinerary
    }
