from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TravelPreferences(BaseModel):
    from_location: str = Field(..., description="Origin city/airport")
    to_location: str = Field(..., description="Destination city/airport")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date (YYYY-MM-DD)")
    travel_class: str = Field("economy", description="Flight class")
    budget: str = Field(..., description="Budget range")
    travelers: str = Field(..., description="Number of travelers")
    interests: List[str] = Field(default=[], description="Travel interests")
    diet: Optional[str] = Field(None, description="Dietary preferences")

class FlightResponse(BaseModel):
    id: str
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    currency: str
    flight_class: str
    stops: int
    booking_url: str
    thumbnail: Optional[str]
    ai_recommended: bool
    ai_reasoning: Optional[Dict[str, Any]]

class HotelResponse(BaseModel):
    id: str
    name: str
    location: str
    rating: float
    reviews_count: int
    price_per_night: float
    currency: str
    amenities: List[Dict[str, Any]]
    description: str
    booking_url: str
    thumbnail: Optional[str]
    ai_recommended: bool
    ai_reasoning: Optional[Dict[str, Any]]

class DayPlan(BaseModel):
    day: int
    date: str
    title: str
    activities: List[Dict[str, Any]]

class ItineraryResponse(BaseModel):
    id: str
    session_id: str
    title: str
    description: str
    total_days: int
    estimated_cost: float
    currency: str
    daily_plans: List[DayPlan]
    selected_flight: Optional[FlightResponse]
    selected_hotel: Optional[HotelResponse]

class PlanResponse(BaseModel):
    session_id: str
    flights: List[FlightResponse]
    hotels: List[HotelResponse]
    itinerary: ItineraryResponse

class FlightSelection(BaseModel):
    session_id: str
    flight_id: str

class HotelSelection(BaseModel):
    session_id: str
    hotel_id: str
    check_in_date: str
    check_out_date: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None