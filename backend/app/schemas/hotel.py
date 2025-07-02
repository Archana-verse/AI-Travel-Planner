from pydantic import BaseModel

class HotelSearch(BaseModel):
    location: str
