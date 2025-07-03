from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from contextlib import asynccontextmanager

# Import database and models
from app.database import engine
from app.models import Base
from app.config import settings

# Import routers
from app.routers import planning, flights, hotels, itinerary, chat, booking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Raahi.ai Backend")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
    
    # Verify environment
    if not settings.GOOGLE_API_KEY:
        logger.warning("GOOGLE_API_KEY not set - AI features may not work properly")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Raahi.ai Backend")

# Create FastAPI app
app = FastAPI(
    title="Raahi.ai API",
    description="AI-Powered Travel Planning Backend with CrewAI and Gemini Pro",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://vercel.app",
        "https://netlify.app",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error responses"""
    
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    elif isinstance(exc, SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error occurred"}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Include routers
app.include_router(planning.router, prefix="/api", tags=["Trip Planning"])
app.include_router(flights.router, prefix="/api", tags=["Flights"])
app.include_router(hotels.router, prefix="/api", tags=["Hotels"])
app.include_router(itinerary.router, prefix="/api", tags=["Itinerary"])
app.include_router(chat.router, prefix="/api", tags=["AI Chat"])
app.include_router(booking.router, prefix="/api", tags=["Booking"])

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Raahi.ai Backend API",
        "version": "2.0.0",
        "description": "AI-Powered Travel Planning with CrewAI and Gemini Pro",
        "docs": "/docs",
        "features": [
            "Multi-agent trip planning with CrewAI",
            "Gemini Pro powered AI assistance",
            "Real-time flight and hotel search",
            "Intelligent itinerary generation",
            "PDF export capabilities",
            "Skyscanner and Booking.com integration"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Check database connection
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Check AI service
    ai_status = "healthy" if settings.GOOGLE_API_KEY else "missing_api_key"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": "raahi-backend",
        "version": "2.0.0",
        "database": db_status,
        "ai_service": ai_status,
        "features": {
            "crewai": True,
            "gemini_pro": bool(settings.GOOGLE_API_KEY),
            "serpapi": bool(settings.SERPAPI_KEY),
            "pdf_generation": True
        }
    }

@app.get("/api/status")
async def api_status():
    """Detailed API status for monitoring"""
    
    return {
        "api_version": "2.0.0",
        "environment": "development" if settings.DEBUG else "production",
        "database_url": settings.DATABASE_URL.split("://")[0] + "://***",  # Hide credentials
        "endpoints": {
            "planning": "/api/generate-plan",
            "flights": "/api/flights",
            "hotels": "/api/hotels", 
            "itinerary": "/api/itinerary/{session_id}",
            "pdf_download": "/api/itinerary/{session_id}/pdf",
            "chat": "/api/chat",
            "booking": "/api/select-flight, /api/select-hotel"
        },
        "external_integrations": {
            "skyscanner": True,
            "booking_com": True,
            "serpapi": bool(settings.SERPAPI_KEY),
            "gemini_pro": bool(settings.GOOGLE_API_KEY)
        }
    }

# Development server runner
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )