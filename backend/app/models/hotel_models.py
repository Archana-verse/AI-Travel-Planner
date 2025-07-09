from typing import List, Optional
from pydantic import BaseModel


class HotelRequest(BaseModel):
    destination: str             
    checkin_date: str            
    checkout_date: str           
    budget_range: str            
    travelers: str              
    interests: List[str]         
    dietary_pref: Optional[str]  


class HotelRecommendation(BaseModel):
    name: str
    location: str
    price_per_night: int
    rating: float
    amenities: List[str]
    reason: str                   


class HotelResponse(BaseModel):
    recommendations: List[HotelRecommendation]
