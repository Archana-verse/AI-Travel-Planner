from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import HotelResponse
from app.models import Hotel
from typing import List

router = APIRouter()

@router.get("/hotels", response_model=List[HotelResponse])
async def get_hotels(
    session_id: str = Query(..., description="Session ID"),
    db: Session = Depends(get_db)
):
    """Get all hotels for a session"""
    
    hotels = db.query(Hotel).filter(Hotel.session_id == session_id).all()
    
    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found for this session")
    
    return [
        HotelResponse(
            id=h.id,
            name=h.name,
            location=h.location,
            rating=h.rating,
            reviews_count=h.reviews_count,
            price_per_night=h.price_per_night,
            currency=h.currency,
            amenities=h.amenities,
            description=h.description,
            booking_url=h.booking_url,
            thumbnail=h.thumbnail,
            ai_recommended=h.ai_recommended,
            ai_reasoning=h.ai_reasoning
        ) for h in hotels
    ]