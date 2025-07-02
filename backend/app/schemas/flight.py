from pydantic import BaseModel

class FlightSearch(BaseModel):
    from_location: str
    to_location: str
    date: str
