from pydantic import BaseModel
from typing import List


class PlanRequest(BaseModel):
    from_: str            
    to: str               
    departureDate: str    
    returnDate: str       
    travelClass: str      
    budget: str           
    travelers: str        
    interests: List[str]  
    diet: str          
