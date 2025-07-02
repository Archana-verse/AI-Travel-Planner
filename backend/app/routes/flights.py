from fastapi import APIRouter, Query
from app.services.serpapi_service import search_flights
from typing import Optional

router = APIRouter()

@router.get("/")
def get_flights(from_location: str, to_location: str, date: str):
    return search_flights(from_location, to_location, date)
