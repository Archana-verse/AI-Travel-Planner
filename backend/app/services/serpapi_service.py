import os
from serpapi import GoogleSearch
from app.config import settings

def search_flights(from_location, to_location, date):
    params = {
        "engine": "google_flights",
        "departure_id": from_location,
        "arrival_id": to_location,
        "departure_date": date,
        "api_key": settings.SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    return search.get_dict()

def search_hotels(location):
    params = {
        "engine": "google_hotels",
        "q": f"hotels in {location}",
        "api_key": settings.SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    return search.get_dict()
