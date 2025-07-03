from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

class TravelSession(Base):
    __tablename__ = "travel_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_preferences = Column(JSON)
    status = Column(String, default="active")  # active, completed, expired
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    flights = relationship("Flight", back_populates="session", cascade="all, delete-orphan")
    hotels = relationship("Hotel", back_populates="session", cascade="all, delete-orphan")
    itinerary = relationship("Itinerary", back_populates="session", uselist=False, cascade="all, delete-orphan")
    selected_flight = relationship("SelectedFlight", back_populates="session", uselist=False, cascade="all, delete-orphan")
    selected_hotel = relationship("SelectedHotel", back_populates="session", uselist=False, cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    airline = Column(String)
    flight_number = Column(String)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_time = Column(String)
    arrival_time = Column(String)
    departure_date = Column(String)
    return_date = Column(String)
    duration = Column(String)
    price = Column(Float)
    currency = Column(String, default="INR")
    flight_class = Column(String)
    stops = Column(Integer, default=0)
    booking_url = Column(String)
    ai_recommended = Column(Boolean, default=False)
    ai_reasoning = Column(JSON)
    raw_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="flights")

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    name = Column(String)
    location = Column(String)
    rating = Column(Float)
    reviews_count = Column(Integer)
    price_per_night = Column(Float)
    currency = Column(String, default="INR")
    amenities = Column(JSON)
    description = Column(Text)
    booking_url = Column(String)
    ai_recommended = Column(Boolean, default=False)
    ai_reasoning = Column(JSON)
    raw_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="hotels")

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    title = Column(String)
    description = Column(Text)
    total_days = Column(Integer)
    estimated_cost = Column(Float)
    currency = Column(String, default="INR")
    daily_plans = Column(JSON)
    ai_insights = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="itinerary")

class SelectedFlight(Base):
    __tablename__ = "selected_flights"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    flight_id = Column(String, ForeignKey("flights.id"))
    booking_url = Column(String)
    selected_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="selected_flight")
    flight = relationship("Flight")

class SelectedHotel(Base):
    __tablename__ = "selected_hotels"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    hotel_id = Column(String, ForeignKey("hotels.id"))
    check_in_date = Column(String)
    check_out_date = Column(String)
    booking_url = Column(String)
    selected_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="selected_hotel")
    hotel = relationship("Hotel")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("travel_sessions.id"))
    message = Column(Text)
    response = Column(Text)
    message_type = Column(String, default="general")  # general, flight, hotel, itinerary
    created_at = Column(DateTime, server_default=func.now())
    
    session = relationship("TravelSession", back_populates="chat_messages")