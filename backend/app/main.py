from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.database import engine, get_db
from app.models import Base
from app.routers import planning, flights, hotels, itinerary, chat, booking
from app.config import settings

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Raahi.ai API",
    description="AI-powered travel planning backend with real-time data",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(planning.router, prefix="/api", tags=["Planning"])
app.include_router(flights.router, prefix="/api", tags=["Flights"])
app.include_router(hotels.router, prefix="/api", tags=["Hotels"])
app.include_router(itinerary.router, prefix="/api", tags=["Itinerary"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(booking.router, prefix="/api", tags=["Booking"])

@app.get("/")
async def root():
    return {"message": "Raahi.ai Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "raahi-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )