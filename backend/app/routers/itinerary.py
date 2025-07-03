from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItineraryResponse, DayPlan, FlightResponse, HotelResponse, ActivityResponse
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
                departure_date=flight.departure_date,
                return_date=flight.return_date,
                duration=flight.duration,
                price=flight.price,
                currency=flight.currency,
                flight_class=flight.flight_class,
                stops=flight.stops,
                booking_url=selected_flight.booking_url,
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
                ai_recommended=hotel.ai_recommended,
                ai_reasoning=hotel.ai_reasoning
            )
    
    # Convert daily plans to response format
    daily_plans_response = []
    for day_plan in itinerary.daily_plans:
        activities = [
            ActivityResponse(
                time=activity.get('time', ''),
                icon=activity.get('icon', ''),
                activity=activity.get('activity', ''),
                duration=activity.get('duration', ''),
                cost=activity.get('cost', 0),
                description=activity.get('description', '')
            ) for activity in day_plan.get('activities', [])
        ]
        
        daily_plans_response.append(
            DayPlan(
                day=day_plan.get('day', 1),
                date=day_plan.get('date', ''),
                title=day_plan.get('title', ''),
                activities=activities,
                estimated_cost=day_plan.get('estimated_cost', 0)
            )
        )
    
    return ItineraryResponse(
        id=itinerary.id,
        session_id=session_id,
        title=itinerary.title,
        description=itinerary.description,
        total_days=itinerary.total_days,
        estimated_cost=itinerary.estimated_cost,
        currency=itinerary.currency,
        daily_plans=daily_plans_response,
        ai_insights=itinerary.ai_insights,
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
    
    # Get selected flight data
    selected_flight_data = None
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
                'arrival_time': flight.arrival_time,
                'departure_date': flight.departure_date,
                'return_date': flight.return_date,
                'duration': flight.duration,
                'price': flight.price,
                'flight_class': flight.flight_class,
                'rating': None,
                'reviews_count': None,
                'amenities': None
            }
    
    # Get selected hotel data
    selected_hotel_data = None
    selected_hotel = db.query(SelectedHotel).filter(SelectedHotel.session_id == session_id).first()
    if selected_hotel:
        hotel = db.query(Hotel).filter(Hotel.id == selected_hotel.hotel_id).first()
        if hotel:
            selected_hotel_data = {
                'name': hotel.name,
                'location': hotel.location,
                'rating': hotel.rating,
                'reviews_count': hotel.reviews_count,
                'price_per_night': hotel.price_per_night,
                'amenities': hotel.amenities
            }
    
    # Prepare itinerary data for PDF
    itinerary_data = {
        'title': itinerary.title,
        'description': itinerary.description,
        'total_days': itinerary.total_days,
        'estimated_cost': itinerary.estimated_cost,
        'currency': itinerary.currency,
        'daily_plans': itinerary.daily_plans,
        'ai_insights': itinerary.ai_insights
    }
    
    # Generate PDF
    pdf_service = PDFService()
    pdf_bytes = pdf_service.generate_itinerary_pdf(
        itinerary_data=itinerary_data,
        selected_flight=selected_flight_data,
        selected_hotel=selected_hotel_data
    )
    
    # Return PDF response
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=raahi_itinerary_{session_id}.pdf",
            "Content-Length": str(len(pdf_bytes))
        }
    )