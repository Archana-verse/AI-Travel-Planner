from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import flights, hotels, plan, itinerary

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(flights.router, prefix="/flights", tags=["Flights"])
app.include_router(hotels.router, prefix="/hotels", tags=["Hotels"])
app.include_router(plan.router, prefix="/plan", tags=["Plan"])
app.include_router(itinerary.router, prefix="/itinerary", tags=["Itinerary"])
