from app.services.serpapi_service import search_hotels
from app.services.gemini_service import get_ai_hotel_recommendation

class HotelAgent:
    def __init__(self, plan_data):
        self.plan = plan_data

    def run(self):
        destination = self.plan["to"]
        check_in = self.plan["departure_date"]
        check_out = self.plan["return_date"]

        hotels = search_hotels(destination, check_in, check_out)

        if not hotels:
            return []

        ai_response = get_ai_hotel_recommendation(hotels)
        recommended_id = ai_response.get("recommended_id")
        reasoning = ai_response.get("reason", {})

        for hotel in hotels:
            if hotel["id"] == recommended_id:
                hotel["aiRecommended"] = True
                hotel["ai_reasoning"] = reasoning
            else:
                hotel["ai_reasoning"] = hotel.get("ai_reasoning", {})

        return hotels
