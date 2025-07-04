from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.itinerary_agent import ItineraryAgent

class TripPlannerAgent:
    def __init__(self, plan):
        self.plan = plan

    def run(self):
        # Step 1: Get flight recommendations
        flight_agent = FlightAgent(self.plan)
        flights = flight_agent.get_flights()

        # Step 2: Get hotel recommendations
        hotel_agent = HotelAgent(self.plan)
        hotels = hotel_agent.get_hotels()

        # Step 3: Generate itinerary
        itinerary_agent = ItineraryAgent(self.plan)
        itinerary = itinerary_agent.generate_itinerary()

        return flights, hotels, itinerary
