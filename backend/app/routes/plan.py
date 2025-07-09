from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.agents.trip_planner_agent import generate_full_plan
from app.utils.iata_lookup import get_iata_code  

router = APIRouter()

class PlanInput(BaseModel):
    from_: str
    to: str
    departureDate: str
    returnDate: str
    travelClass: str
    budget: str
    travelers: str
    interests: List[str]
    diet: str


@router.post("/generate-plan")
def generate_plan(plan: PlanInput):
    """
    Main endpoint for generating a full travel plan.
    - Converts from/to cities to IATA for flight search
    - Passes raw city name for hotel and itinerary
    - Returns structured response: flights, hotels, and itinerary
    """
    plan.from_ = get_iata_code(plan.from_)
    plan.to = get_iata_code(plan.to)

    # 🌍 Proceed with the full plan generation
    plan_response = generate_full_plan(plan)
    return plan_response
