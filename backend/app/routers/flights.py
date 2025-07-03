from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import FlightResponse
from app.models import Flight
from typing import List

router = APIRouter()

@router.get("/flights", response_model=List[FlightResponse])
async def get_flights(
    session_id: str = Query(..., description="Session ID"),
    db: Session = Depends(get_db)
):
    """Get all flights for a session"""
    
    flights = db.query(Flight).filter(Flight.session_id == session_id).all()
    
    if not flights:
        raise HTTPException(status_code=404, detail="No flights found for this session")
    
    return [
        FlightResponse(
            id=f.id,
            airline=f.airline,
            flight_number=f.flight_number,
            departure_airport=f.departure_airport,
            arrival_airport=f.arrival_airport,
            departure_time=f.departure_time,
            arrival_time=f.arrival_time,
            duration=f.duration,
            price=f.price,
            currency=f.currency,
            flight_class=f.flight_class,
            stops=f.stops,
            booking_url=f.booking_url,
            thumbnail=f.thumbnail,
            ai_recommended=f.ai_recommended,
            ai_reasoning=f.ai_reasoning
        ) for f in flights
    ]