from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import FlightSelection, HotelSelection
from app.models import SelectedFlight, SelectedHotel, Flight, Hotel, TravelSession
from app.services.booking_service import BookingService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/select-flight")
async def select_flight(
    selection: FlightSelection,
    db: Session = Depends(get_db)
):
    """Select a flight and generate booking URL"""
    
    try:
        # Verify session exists
        session = db.query(TravelSession).filter(TravelSession.id == selection.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get flight details
        flight = db.query(Flight).filter(Flight.id == selection.flight_id).first()
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        # Get user preferences for dates
        preferences = session.user_preferences
        departure_date = preferences.get('departure_date')
        
        # Generate specific booking URL
        booking_service = BookingService()
        booking_url = booking_service.generate_flight_booking_url(
            {
                'airline': flight.airline,
                'departure_airport': flight.departure_airport,
                'arrival_airport': flight.arrival_airport,
                'booking_url': flight.booking_url
            },
            departure_date
        )
        
        # Remove any existing selection for this session
        db.query(SelectedFlight).filter(SelectedFlight.session_id == selection.session_id).delete()
        
        # Save new selection
        selected_flight = SelectedFlight(
            session_id=selection.session_id,
            flight_id=selection.flight_id,
            booking_url=booking_url
        )
        db.add(selected_flight)
        db.commit()
        
        return {
            "message": "Flight selected successfully",
            "booking_url": booking_url,
            "flight_details": {
                "airline": flight.airline,
                "flight_number": flight.flight_number,
                "route": f"{flight.departure_airport} → {flight.arrival_airport}",
                "price": flight.price
            }
        }
        
    except Exception as e:
        logger.error(f"Error selecting flight: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to select flight")

@router.post("/select-hotel")
async def select_hotel(
    selection: HotelSelection,
    db: Session = Depends(get_db)
):
    """Select a hotel and generate booking URL"""
    
    try:
        # Verify session exists
        session = db.query(TravelSession).filter(TravelSession.id == selection.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get hotel details
        hotel = db.query(Hotel).filter(Hotel.id == selection.hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        # Get user preferences for location
        preferences = session.user_preferences
        location = preferences.get('to_location', '')
        
        # Generate specific booking URL
        booking_service = BookingService()
        booking_url = booking_service.generate_hotel_booking_url(
            {
                'name': hotel.name,
                'booking_url': hotel.booking_url
            },
            selection.check_in_date,
            selection.check_out_date,
            location
        )
        
        # Remove any existing selection for this session
        db.query(SelectedHotel).filter(SelectedHotel.session_id == selection.session_id).delete()
        
        # Save new selection
        selected_hotel = SelectedHotel(
            session_id=selection.session_id,
            hotel_id=selection.hotel_id,
            check_in_date=selection.check_in_date,
            check_out_date=selection.check_out_date,
            booking_url=booking_url
        )
        db.add(selected_hotel)
        db.commit()
        
        return {
            "message": "Hotel selected successfully",
            "booking_url": booking_url,
            "hotel_details": {
                "name": hotel.name,
                "location": hotel.location,
                "rating": hotel.rating,
                "price_per_night": hotel.price_per_night,
                "check_in": selection.check_in_date,
                "check_out": selection.check_out_date
            }
        }
        
    except Exception as e:
        logger.error(f"Error selecting hotel: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to select hotel")