from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.types import JSON
from datetime import datetime
from app.core.database import Base

class TravelSession(Base):
    __tablename__ = "travel_sessions"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_date = Column(String)
    return_date = Column(String)
    budget = Column(String)
    travel_class = Column(String)
    group_type = Column(String)
    interests = Column(String)  # We'll store as comma-separated string
    dietary_preferences = Column(String)

    flights = Column(JSON)
    hotels = Column(JSON)
    itinerary = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
