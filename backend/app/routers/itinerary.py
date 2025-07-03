from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItineraryResponse, DayPlan, FlightResponse, HotelResponse
from app.models import Itinerary, SelectedFlight, SelectedHotel, Flight, Hotel
from app.services.pdf_service import PDFService

router = APIRouter()

@router.get("/itinerary/{session_id}", response_model=ItineraryResponse)
async def get_itinerary(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get complete itinerary with selected flight and hotel"""
    
    # Get itinerary
    itinerary = db.query(Itinerary).filter(Itinerary.session_id == session_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    # Get selected flight
    selected_flight_data = None
    selected_flight = db.query(SelectedFlight).filter(SelectedFlight.session_id == session_id).first()
    if selected_flight:
        flight = db.query(Flight).filter(Flight.id == selected_flight.flight_id).first()
        if flight:
            selected_flight_data = FlightResponse(
                id=flight.id,
                airline=flight.airline,
                flight_number=flight.flight_number,
                departure_airport=flight.departure_airport,
                arrival_airport=flight.arrival_airport,
                departure_time=flight.departure_time,
                arrival_time=flight.arrival_time,
                duration=flight.duration,
                price=flight.price,
                currency=flight.currency,
                flight_class=flight.flight_class,
                stops=flight.stops,
                booking_url=selected_flight.booking_url,
                thumbnail=flight.thumbnail,
                ai_recommended=flight.ai_recommended,
                ai_reasoning=flight.ai_reasoning
            )
    
    # Get selected hotel
    selected_hotel_data = None
    selected_hotel = db.query(SelectedHotel).filter(SelectedHotel.session_id == session_id).first()
    if selected_hotel:
        hotel = db.query(Hotel).filter(Hotel.id == selected_hotel.hotel_id).first()
        if hotel:
            selected_hotel_data = HotelResponse(
                id=hotel.id,
                name=hotel.name,
                location=hotel.location,
                rating=hotel.rating,
                reviews_count=hotel.reviews_count,
                price_per_night=hotel.price_per_night,
                currency=hotel.currency,
                amenities=hotel.amenities,
                description=hotel.description,
                booking_url=selected_hotel.booking_url,
                thumbnail=hotel.thumbnail,
                ai_recommended=hotel.ai_recommended,
                ai_reasoning=hotel.ai_reasoning
            )
    
    return ItineraryResponse(
        id=itinerary.id,
        session_id=session_id,
        title=itinerary.title,
        description=itinerary.description,
        total_days=itinerary.total_days,
        estimated_cost=itinerary.estimated_cost,
        currency=itinerary.currency,
        daily_plans=[DayPlan(**day) for day in itinerary.daily_plans],
        selected_flight=selected_flight_data,
        selected_hotel=selected_hotel_data
    )

@router.get("/itinerary/{session_id}/pdf")
async def download_itinerary_pdf(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Download itinerary as PDF"""
    
    # Get itinerary data
    itinerary = db.query(Itinerary).filter(Itinerary.session_id == session_id).first()
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    # Get selected flight and hotel data
    selected_flight_data = {}
    selected_flight = db.query(SelectedFlight).filter(SelectedFlight.session_id == session_id).first()
    if selected_flight:
        flight = db.query(Flight).filter(Flight.id == selected_flight.flight_id).first()
        if flight:
            selected_flight_data = {
                'airline': flight.airline,
                'flight_number': flight.flight_number,
                'departure_airport': flight.departure_airport,
                'arrival_airport': flight.arrival_airport,
                'departure_time': flight.departure_time,
                'arrival_time': flight.arrival_time
            }
    
    selected_hotel_data = {}
    selected_hotel = db.query(SelectedHotel).filter(SelectedHotel.session_id == session_id).first()
    if selected_hotel:
        hotel = db.query(Hotel).filter(Hotel.id == selected_hotel.hotel_id).first()
        if hotel:
            selected_hotel_data = {
                'name': hotel.name,
                'location': hotel.location,
                'rating': hotel.rating
            }
    
    # Generate PDF
    pdf_service = PDFService()
    itinerary_data = {
        'title': itinerary.title,
        'description': itinerary.description,
        'total_days': itinerary.total_days,
        'estimated_cost': itinerary.estimated_cost,
        'daily_plans': itinerary.daily_plans
    }
    
    pdf_bytes = pdf_service.generate_itinerary_pdf(
        itinerary_data, 
        selected_flight_data, 
        selected_hotel_data
    )
    
    # Return PDF response
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=itinerary_{session_id}.pdf"}
    )