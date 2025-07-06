# from app.services.serpapi_service import search_flights
# from app.services.gemini_service import get_ai_flight_recommendation
# from app.utils.iata_lookup import get_iata_code

# def generate_full_plan(plan):
#     # 🔁 Convert city names to IATA airport codes
#     origin_code = get_iata_code(plan.from_)
#     destination_code = get_iata_code(plan.to)

#     # ✈️ Get real-time flights from SerpAPI
#     flights = search_flights(origin_code, destination_code, plan.departure_date)

#     # 🤖 Get AI recommendation using Gemini
#     ai_response = get_ai_flight_recommendation(flights)

#     recommended_id = ai_response.get("recommended_id")
#     reasoning = ai_response.get("reason", {})

#     # 🧠 Mark the recommended flight and add reasoning
#     for flight in flights:
#         if flight["id"] == recommended_id:
#             flight["aiRecommended"] = True
#             flight["ai_reasoning"] = reasoning
#         else:
#             flight["ai_reasoning"] = flight.get("ai_reasoning", {})

#     return {
#         "flights": flights,
#         "hotels": [],      # Will be filled by hotel_agent later
#         "itinerary": []    # Will be filled by itinerary_agent later
#     }


from app.services.serpapi_service import search_flights, search_hotels
from app.services.gemini_service import get_ai_flight_recommendation, get_ai_hotel_recommendation
from app.utils.iata_lookup import get_iata_code

def generate_full_plan(plan):
    # 🔁 Convert city names to IATA airport codes
    origin_code = get_iata_code(plan.from_)
    destination_code = get_iata_code(plan.to)

    # ✈️ Get real-time flights from SerpAPI
    flights = search_flights(origin_code, destination_code, plan.departure_date)

    # 🤖 Get AI recommendation using Gemini for flights
    ai_response = get_ai_flight_recommendation(flights)
    recommended_id = ai_response.get("recommended_id")
    reasoning = ai_response.get("reason", {})

    for flight in flights:
        if flight["id"] == recommended_id:
            flight["aiRecommended"] = True
            flight["ai_reasoning"] = reasoning
        else:
            flight["ai_reasoning"] = flight.get("ai_reasoning", {})

    # 🏨 Get real-time hotels in destination city
    hotels_raw = search_hotels(plan.to, plan.departure_date, plan.return_date or plan.departure_date)

    # 🧠 Use Gemini to recommend a hotel
    hotel_ai = get_ai_hotel_recommendation(hotels_raw)
    hotel_recommended_id = hotel_ai.get("recommended_id")
    hotel_reasoning = hotel_ai.get("reason", {})

    for hotel in hotels_raw:
        if hotel["id"] == hotel_recommended_id:
            hotel["aiRecommended"] = True
            hotel["ai_reasoning"] = hotel_reasoning
        else:
            hotel["ai_reasoning"] = hotel.get("ai_reasoning", {})

    return {
        "flights": flights,
        "hotels": hotels_raw,
        "itinerary": []  # Will be filled by itinerary_agent later
    }


