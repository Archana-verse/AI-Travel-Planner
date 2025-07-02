from fastapi import APIRouter
from app.services.itinerary_generator import generate_itinerary
from app.schemas.itinerary import ItineraryRequest

router = APIRouter()

@router.post("/")
def generate(request: ItineraryRequest):
    return generate_itinerary(request)
