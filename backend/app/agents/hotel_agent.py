from app.services.serpapi_service import search_hotels
from app.services.gemini_service import get_best_hotel_reason

class HotelAgent:
    def __init__(self, plan):
        self.plan = plan

    def get_hotels(self):
        hotels = search_hotels(
            destination=self.plan.destination,
            checkin_date=self.plan.departure_date,
            checkout_date=self.plan.return_date,
            budget=self.plan.budget,
            group_type=self.plan.group_type,
            travel_class=self.plan.travel_class,
            dietary_preferences=self.plan.dietary_preferences,
            interests=self.plan.interests
        )

        recommended, reason = get_best_hotel_reason(hotels, self.plan)
        for h in hotels:
            h["recommended"] = (h == recommended)
            if h["recommended"]:
                h["reason"] = reason
        return hotels
