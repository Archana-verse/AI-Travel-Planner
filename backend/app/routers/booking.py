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
    """Select a flight and generate Skyscanner booking URL"""
    
    try:
        # Verify session exists
        session = db.query(TravelSession).filter(TravelSession.id == selection.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get flight details
        flight = db.query(Flight).filter(Flight.id == selection.flight_id).first()
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        
        # Generate Skyscanner booking URL
        booking_service = BookingService()
        booking_url = booking_service.generate_flight_booking_url(
            {
                'departure_airport': flight.departure_airport,
                'arrival_airport': flight.arrival_airport,
                'departure_date': flight.departure_date,
                'return_date': flight.return_date,
                'flight_class': flight.flight_class,
                'price': flight.price
            },
            session.user_preferences
        )
        
        # Remove any existing flight selection for this session
        db.query(SelectedFlight).filter(SelectedFlight.session_id == selection.session_id).delete()
        
        # Save new selection
        selected_flight = SelectedFlight(
            session_id=selection.session_id,
            flight_id=selection.flight_id,
            booking_url=booking_url
        )
        db.add(selected_flight)
        db.commit()
        
        logger.info(f"Flight selected for session {selection.session_id}: {flight.airline} {flight.flight_number}")
        
        return {
            "message": "Flight selected successfully",
            "booking_url": booking_url,
            "flight_details": {
                "airline": flight.airline,
                "flight_number": flight.flight_number,
                "route": f"{flight.departure_airport} → {flight.arrival_airport}",
                "price": f"₹{flight.price:,.0f}",
                "departure_date": flight.departure_date,
                "departure_time": flight.departure_time
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
    """Select a hotel and generate Booking.com booking URL"""
    
    try:
        # Verify session exists
        session = db.query(TravelSession).filter(TravelSession.id == selection.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get hotel details
        hotel = db.query(Hotel).filter(Hotel.id == selection.hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        # Generate Booking.com booking URL
        booking_service = BookingService()
        booking_url = booking_service.generate_hotel_booking_url(
            {
                'name': hotel.name,
                'location': hotel.location,
                'price_per_night': hotel.price_per_night
            },
            {
                'departure_date': selection.check_in_date,
                'return_date': selection.check_out_date
            }
        )
        
        # Remove any existing hotel selection for this session
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
        
        logger.info(f"Hotel selected for session {selection.session_id}: {hotel.name}")
        
        return {
            "message": "Hotel selected successfully",
            "booking_url": booking_url,
            "hotel_details": {
                "name": hotel.name,
                "location": hotel.location,
                "rating": hotel.rating,
                "price_per_night": f"₹{hotel.price_per_night:,.0f}",
                "check_in": selection.check_in_date,
                "check_out": selection.check_out_date
            }
        }
        
    except Exception as e:
        logger.error(f"Error selecting hotel: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to select hotel")