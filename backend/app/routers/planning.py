from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TravelPreferences, PlanResponse
from app.models import TravelSession, Flight, Hotel, Itinerary
from app.services.free_data_service import FreeDataService
from app.services.free_ai_service import FreeAIService
from app.services.booking_service import BookingService
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate-plan", response_model=PlanResponse)
async def generate_travel_plan(
    preferences: TravelPreferences,
    db: Session = Depends(get_db)
):
    """Generate complete travel plan with flights, hotels, and itinerary using FREE services"""
    
    try:
        # Create new session
        session_id = str(uuid.uuid4())
        session = TravelSession(
            id=session_id,
            user_preferences=preferences.dict()
        )
        db.add(session)
        db.commit()
        
        # Initialize FREE services
        data_service = FreeDataService()
        ai_service = FreeAIService()
        booking_service = BookingService()
        
        # Search flights using FREE data
        logger.info(f"Searching flights for session {session_id} using FREE service")
        flight_results = await data_service.search_flights(
            origin=preferences.from_location,
            destination=preferences.to_location,
            departure_date=preferences.departure_date,
            return_date=preferences.return_date,
            travel_class=preferences.travel_class
        )
        
        # Analyze flights with FREE AI
        flight_results = await ai_service.analyze_flight_recommendations(
            flight_results, preferences.dict()
        )
        
        # Save flights to database
        flight_objects = []
        for flight_data in flight_results:
            booking_url = booking_service.generate_flight_booking_url(
                flight_data, preferences.departure_date
            )
            
            flight = Flight(
                session_id=session_id,
                airline=flight_data.get('airline', ''),
                flight_number=flight_data.get('flight_number', ''),
                departure_airport=flight_data.get('departure_airport', ''),
                arrival_airport=flight_data.get('arrival_airport', ''),
                departure_time=flight_data.get('departure_time', ''),
                arrival_time=flight_data.get('arrival_time', ''),
                duration=flight_data.get('duration', ''),
                price=flight_data.get('price', 0),
                flight_class=preferences.travel_class,
                stops=flight_data.get('stops', 0),
                booking_url=booking_url,
                thumbnail=flight_data.get('thumbnail', ''),
                ai_recommended=flight_data.get('ai_recommended', False),
                ai_reasoning=flight_data.get('ai_reasoning', {}),
                raw_data=flight_data
            )
            db.add(flight)
            flight_objects.append(flight)
        
        # Search hotels using FREE data
        logger.info(f"Searching hotels for session {session_id} using FREE service")
        hotel_results = await data_service.search_hotels(
            location=preferences.to_location,
            check_in=preferences.departure_date,
            check_out=preferences.return_date or preferences.departure_date,
            guests=2
        )
        
        # Analyze hotels with FREE AI
        hotel_results = await ai_service.analyze_hotel_recommendations(
            hotel_results, preferences.dict()
        )
        
        # Save hotels to database
        hotel_objects = []
        for hotel_data in hotel_results:
            booking_url = booking_service.generate_hotel_booking_url(
                hotel_data,
                preferences.departure_date,
                preferences.return_date or preferences.departure_date,
                preferences.to_location
            )
            
            hotel = Hotel(
                session_id=session_id,
                name=hotel_data.get('name', ''),
                location=hotel_data.get('location', ''),
                rating=hotel_data.get('rating', 0.0),
                reviews_count=hotel_data.get('reviews_count', 0),
                price_per_night=hotel_data.get('price_per_night', 0),
                amenities=hotel_data.get('amenities', []),
                description=hotel_data.get('description', ''),
                booking_url=booking_url,
                thumbnail=hotel_data.get('thumbnail', ''),
                ai_recommended=hotel_data.get('ai_recommended', False),
                ai_reasoning=hotel_data.get('ai_reasoning', {}),
                raw_data=hotel_data
            )
            db.add(hotel)
            hotel_objects.append(hotel)
        
        # Generate itinerary using FREE AI
        logger.info(f"Generating itinerary for session {session_id} using FREE AI")
        itinerary_data = await ai_service.generate_itinerary(
            preferences.dict(), flight_results, hotel_results
        )
        
        # Save itinerary to database
        itinerary = Itinerary(
            session_id=session_id,
            title=itinerary_data.get('title', ''),
            description=itinerary_data.get('description', ''),
            total_days=itinerary_data.get('total_days', 0),
            estimated_cost=itinerary_data.get('estimated_cost', 0),
            daily_plans=itinerary_data.get('daily_plans', [])
        )
        db.add(itinerary)
        
        db.commit()
        
        # Prepare response
        from app.schemas import FlightResponse, HotelResponse, ItineraryResponse, DayPlan
        
        flights_response = [
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
            ) for f in flight_objects
        ]
        
        hotels_response = [
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
            ) for h in hotel_objects
        ]
        
        itinerary_response = ItineraryResponse(
            id=itinerary.id,
            session_id=session_id,
            title=itinerary.title,
            description=itinerary.description,
            total_days=itinerary.total_days,
            estimated_cost=itinerary.estimated_cost,
            currency=itinerary.currency,
            daily_plans=[DayPlan(**day) for day in itinerary.daily_plans],
            selected_flight=None,
            selected_hotel=None
        )
        
        return PlanResponse(
            session_id=session_id,
            flights=flights_response,
            hotels=hotels_response,
            itinerary=itinerary_response
        )
        
    except Exception as e:
        logger.error(f"Error generating travel plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate travel plan: {str(e)}")