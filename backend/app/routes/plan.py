from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.flight_agent import get_flight_recommendations

router = APIRouter()

class PlanInput(BaseModel):
    from_: str
    to: str
    departureDate: str
    returnDate: str
    travelClass: str
    budget: str
    travelers: str
    interests: list[str]
    diet: str

@router.post("/generate-plan")  # ✅ FIXED: Removed extra /api
def generate_plan(plan: PlanInput):
    preferences = plan.dict()

    flights = get_flight_recommendations(
        from_city=preferences["from_"],
        to_city=preferences["to"],
        departure_date=preferences["departureDate"],
        preferences=preferences
    )

    return {
        "flights": flights,
        "hotels": [],      # To be filled next
        "itinerary": []    # To be filled next
    }
