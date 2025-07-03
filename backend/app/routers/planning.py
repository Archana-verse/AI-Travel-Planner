from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TravelPreferences, PlanResponse
from app.models import TravelSession, Flight, Hotel, Itinerary
from app.agents.crew_manager import TravelPlannerCrew
from app.services.booking_service import BookingService
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate-plan", response_model=PlanResponse)
async def generate_travel_plan(
    preferences: TravelPreferences,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate complete travel plan using CrewAI agents"""
    
    try:
        # Create new session
        session_id = str(uuid.uuid4())
        session = TravelSession(
            id=session_id,
            user_preferences=preferences.dict(),
            status="processing"
        )
        db.add(session)
        db.commit()
        
        logger.info(f"Started trip planning for session {session_id} to {preferences.to_location}")
        
        # Initialize CrewAI manager
        crew_manager = TravelPlannerCrew()
        booking_service = BookingService()
        
        # Execute CrewAI workflow
        crew_results = await crew_manager.plan_complete_trip(preferences.dict())
        
        if crew_results['status'] != 'success':
            raise HTTPException(status_code=500, detail="AI agents failed to generate plan")
        
        # Process and save flight results
        flight_objects = []
        for i, flight_data in enumerate(crew_results['flights'][:5]):
            # Generate booking URL
            booking_url = booking_service.generate_flight_booking_url(
                flight_data, 
                preferences.dict()
            )
            
            flight = Flight(
                session_id=session_id,
                airline=flight_data.get('airline', ''),
                flight_number=flight_data.get('flight_number', ''),
                departure_airport=flight_data.get('departure_airport', ''),
                arrival_airport=flight_data.get('arrival_airport', ''),
                departure_time=flight_data.get('departure_time', ''),
                arrival_time=flight_data.get('arrival_time', ''),
                departure_date=flight_data.get('departure_date', preferences.departure_date),
                return_date=flight_data.get('return_date', preferences.return_date),
                duration=flight_data.get('duration', ''),
                price=flight_data.get('price', 0),
                flight_class=flight_data.get('flight_class', preferences.travel_class),
                stops=flight_data.get('stops', 0),
                booking_url=booking_url,
                ai_recommended=flight_data.get('ai_recommended', False),
                ai_reasoning=flight_data.get('ai_reasoning', {}),
                raw_data=flight_data
            )
            db.add(flight)
            flight_objects.append(flight)
        
        # Process and save hotel results
        hotel_objects = []
        for i, hotel_data in enumerate(crew_results['hotels'][:5]):
            # Generate booking URL
            booking_url = booking_service.generate_hotel_booking_url(
                hotel_data,
                preferences.dict()
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
                ai_recommended=hotel_data.get('ai_recommended', False),
                ai_reasoning=hotel_data.get('ai_reasoning', {}),
                raw_data=hotel_data
            )
            db.add(hotel)
            hotel_objects.append(hotel)
        
        # Process and save itinerary
        itinerary_data = crew_results['itinerary']
        itinerary = Itinerary(
            session_id=session_id,
            title=itinerary_data.get('title', ''),
            description=itinerary_data.get('description', ''),
            total_days=itinerary_data.get('total_days', 0),
            estimated_cost=itinerary_data.get('estimated_cost', 0),
            daily_plans=itinerary_data.get('daily_plans', []),
            ai_insights=itinerary_data.get('ai_insights', {})
        )
        db.add(itinerary)
        
        # Update session status
        session.status = "completed"
        
        db.commit()
        
        logger.info(f"Successfully generated plan for session {session_id}")
        
        # Prepare response using schemas
        from app.schemas import FlightResponse, HotelResponse, ItineraryResponse, DayPlan, ActivityResponse
        
        flights_response = [
            FlightResponse(
                id=f.id,
                airline=f.airline,
                flight_number=f.flight_number,
                departure_airport=f.departure_airport,
                arrival_airport=f.arrival_airport,
                departure_time=f.departure_time,
                arrival_time=f.arrival_time,
                departure_date=f.departure_date,
                return_date=f.return_date,
                duration=f.duration,
                price=f.price,
                currency=f.currency,
                flight_class=f.flight_class,
                stops=f.stops,
                booking_url=f.booking_url,
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
                ai_recommended=h.ai_recommended,
                ai_reasoning=h.ai_reasoning
            ) for h in hotel_objects
        ]
        
        # Convert daily plans
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
        
        itinerary_response = ItineraryResponse(
            id=itinerary.id,
            session_id=session_id,
            title=itinerary.title,
            description=itinerary.description,
            total_days=itinerary.total_days,
            estimated_cost=itinerary.estimated_cost,
            currency=itinerary.currency,
            daily_plans=daily_plans_response,
            ai_insights=itinerary.ai_insights,
            selected_flight=None,
            selected_hotel=None
        )
        
        return PlanResponse(
            session_id=session_id,
            flights=flights_response,
            hotels=hotels_response,
            itinerary=itinerary_response,
            status="completed"
        )
        
    except Exception as e:
        logger.error(f"Error generating travel plan: {str(e)}")
        
        # Update session status to failed
        if 'session' in locals():
            session.status = "failed"
            db.commit()
        
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate travel plan: {str(e)}"
        )