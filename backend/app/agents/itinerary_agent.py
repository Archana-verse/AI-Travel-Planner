from app.services.gemini_service import generate_itinerary

class ItineraryAgent:
    def __init__(self, plan):
        self.plan = plan

    def generate_itinerary(self):
        return generate_itinerary(self.plan)
