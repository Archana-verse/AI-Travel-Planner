from app.crew.crew_manager import run_itinerary_crew
from app.schemas.itinerary import ItineraryRequest

def generate_itinerary(request: ItineraryRequest):
    return run_itinerary_crew(request.destination, request.days, request.preferences)
