from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.database import SessionLocal
from app.models.travel_session import TravelSession
from app.agents.trip_planner_agent import TripPlannerAgent

router = APIRouter()

# 📥 Pydantic model for incoming data
class PlanRequest(BaseModel):
    source: str
    destination: str
    departure_date: str
    return_date: str
    budget: str
    travel_class: str
    group_type: str
    interests: List[str]
    dietary_preferences: str

# 📤 Response format
class PlanResponse(BaseModel):
    session_id: int
    flights: list
    hotels: list
    itinerary: list

@router.post("/api/generate-plan", response_model=PlanResponse)
def generate_plan(plan: PlanRequest):
    db = SessionLocal()

    try:
        # 🎯 Trigger the TripPlannerAgent (which uses CrewAI + Gemini + SerpAPI)
        planner = TripPlannerAgent(plan)
        flights, hotels, itinerary = planner.run()

        # 🧠 Save to SQLite
        session = TravelSession(
            source=plan.source,
            destination=plan.destination,
            departure_date=plan.departure_date,
            return_date=plan.return_date,
            budget=plan.budget,
            travel_class=plan.travel_class,
            group_type=plan.group_type,
            interests=",".join(plan.interests),
            dietary_preferences=plan.dietary_preferences,
            flights=flights,
            hotels=hotels,
            itinerary=itinerary,
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        return {
            "session_id": session.id,
            "flights": flights,
            "hotels": hotels,
            "itinerary": itinerary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
