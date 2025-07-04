import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# ✈️ Flight Search
def search_flights(origin, destination, departure_date, return_date, travel_class):
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "return_date": return_date,
        "adults": 1,
        "travel_class": travel_class.lower(),
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    flights = results.get("best_flights", []) + results.get("other_flights", [])
    
    return [
        {
            "airline": f["airline"],
            "price": f["price"],
            "duration": f.get("duration"),
            "link": f.get("booking_link")
        }
        for f in flights[:5]
    ]

# 🏨 Hotel Search
def search_hotels(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    budget: str = "",
    travel_class: str = "",
    group_type: str = ""
):
    # You can optionally use budget/travel_class/group_type to modify query
    # Example:
    location = f"{destination} hotels {budget} budget for {group_type}"

    params = {
        "engine": "google_hotels",
        "q": location,
        "check_in_date": checkin_date,
        "check_out_date": checkout_date,
        "hl": "en",
        "gl": "in",
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Realistic filtering — assuming results['hotels_results'] contains hotel list
    hotels = []
    for hotel in results.get("hotels_results", []):
        hotels.append({
            "name": hotel.get("name", "Unknown"),
            "price": hotel.get("price", {}).get("aggregated_price", "N/A"),
            "rating": hotel.get("rating", "N/A"),
            "reviews": hotel.get("reviews", "N/A"),
            "address": hotel.get("address", "N/A"),
            "link": hotel.get("link", "")
        })

    return hotels
