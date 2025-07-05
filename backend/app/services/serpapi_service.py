import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ✅ Add this

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_flights(from_city, to_city, departure_date):
    try:
        print("🔍 Fetching flights from SerpAPI...")
        print("🔑 API Key being used:", SERPAPI_API_KEY[:6] + "..." if SERPAPI_API_KEY else "❌ Not loaded")

        params = {
            "engine": "google_flights",
            "departure_id": from_city,
            "arrival_id": to_city,
            "outbound_date": departure_date,
            "type": "2",  # One-way
            "hl": "en",
            "gl": "us",
            "currency": "INR",
            "api_key": SERPAPI_API_KEY,
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        print("📦 Raw SerpAPI Response:", data)

        best_flights = data.get("best_flights", []) + data.get("other_flights", [])
        parsed_flights = []

        for i, flight_option in enumerate(best_flights):
            f = flight_option["flights"][0]

            flight = {
                "id": f"flight{i}",
                "airline": f.get("airline", "Unknown"),
                "code": f.get("flight_number", "NA"),
                "departure": f.get("departure_airport", {}).get("time", "")[-5:],
                "arrival": f.get("arrival_airport", {}).get("time", "")[-5:],
                "departureAirport": f.get("departure_airport", {}).get("id", from_city),
                "arrivalAirport": f.get("arrival_airport", {}).get("id", to_city),
                "duration": f"{int(f.get('duration', 0) // 60)}h {int(f.get('duration', 0) % 60)}m",
                "type": f.get("type", "Non-stop"),
                "price": f"₹{flight_option.get('price', 0)}",
                "class": f.get("travel_class", "Economy"),
            }

            parsed_flights.append(flight)

        return parsed_flights

    except Exception as e:
        print("❌ Error fetching flights from SerpAPI:", e)
        return []
