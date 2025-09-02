import os
import random
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_API_KEY:
    raise ValueError("❌ SERPAPI_API_KEY not found in .env file.")


def search_flights(from_city, to_city, departure_date):
    try:
        print("✈️ Searching flights using SerpAPI...")
        print("🔑 API Key Loaded:", SERPAPI_API_KEY[:6] + "...")

        params = {
            "engine": "google_flights",
            "departure_id": from_city,
            "arrival_id": to_city,
            "outbound_date": departure_date,
            "type": "2",
            "hl": "en",
            "gl": "us",
            "currency": "INR",
            "api_key": SERPAPI_API_KEY,
        }

        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = response.json()

        print("📦 SerpAPI Raw Flight Response Received.")
        print("🔄 Quota Remaining:", response.headers.get("x-search-quota-remaining", "Unknown"))

        best_flights = data.get("best_flights", []) + data.get("other_flights", [])
        parsed_flights = []

        for i, flight_option in enumerate(best_flights):
            f = flight_option.get("flights", [{}])[0]

            airline = f.get("airline", "Unknown Airline")
            code = f.get("flight_number", "NA")
            departure = f.get("departure_airport", {}).get("time", "00:00")[-5:]
            arrival = f.get("arrival_airport", {}).get("time", "00:00")[-5:]
            departure_airport = f.get("departure_airport", {}).get("id", from_city)
            arrival_airport = f.get("arrival_airport", {}).get("id", to_city)
            duration_mins = f.get("duration", 90)
            duration = f"{int(duration_mins // 60)}h {int(duration_mins % 60)}m"
            flight_type = f.get("type", "Non-stop")
            price = f"₹{flight_option.get('price', 4999)}"
            travel_class = f.get("travel_class", "Economy")

            flight = {
                "id": f"flight{i}",
                "airline": airline,
                "code": code,
                "departure": departure,
                "arrival": arrival,
                "departureAirport": departure_airport,
                "arrivalAirport": arrival_airport,
                "duration": duration,
                "type": flight_type,
                "price": price,
                "class": travel_class,
            }

            parsed_flights.append(flight)

        if not parsed_flights:
            print("⚠️ No flights found from SerpAPI.")
        return parsed_flights

    except requests.exceptions.RequestException as e:
        print("❌ SerpAPI Flight Request Failed:", e)
        return []
    except Exception as e:
        print("❌ Unexpected Error While Fetching Flights:", e)
        return []


def get_fallback_price(total_budget, num_days, tier="mid"):
    hotel_budget = total_budget * 0.45
    base_per_night = hotel_budget / max(num_days, 1)

    if tier == "budget":
        min_price = max(700, base_per_night * 0.6)
        max_price = min(2000, base_per_night * 0.8)
    elif tier == "luxury":
        min_price = base_per_night * 1.3
        max_price = base_per_night * 1.8
    else:  # mid
        min_price = base_per_night * 0.9
        max_price = base_per_night * 1.2

    return f"₹{int(random.uniform(min_price, max_price))}"


def search_hotels(city, checkin_date, checkout_date, budget=None, travelers=None, hotel_affordability="medium"):
    try:
        print("🏨 Searching hotels using SerpAPI...")

        date1 = datetime.strptime(checkin_date, "%Y-%m-%d")
        date2 = datetime.strptime(checkout_date, "%Y-%m-%d")
        num_days = (date2 - date1).days or 1
        total_budget = int(budget or 30000)

        tier = "budget" if total_budget < 25000 else "luxury" if total_budget > 60000 else "mid"
        affordability = hotel_affordability or "medium"

        params = {
            "engine": "google_hotels",
            "q": f"hotels in {city}",
            "check_in_date": checkin_date,
            "check_out_date": checkout_date,
            "currency": "INR",
            "gl": "in",
            "hl": "en",
            "api_key": SERPAPI_API_KEY,
        }

        if budget:
            params["max_price"] = budget
        if travelers:
            params["adults"] = travelers

        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = response.json()

        print("📦 SerpAPI Raw Hotel Response Received.")
        print("🔄 Quota Remaining:", response.headers.get("x-search-quota-remaining", "Unknown"))

        hotels = (
            data.get("properties")
            or data.get("hotel_results")
            or data.get("organic_results")
            or []
        )

        parsed_hotels = []
        for i, h in enumerate(hotels):
            name = h.get("name", f"Hotel {i+1}")
            serp_price = h.get("price", {}).get("lead", {}).get("formatted") or h.get("price")
            rating = h.get("rating", round(random.uniform(3.2, 4.8), 1))
            reviews = h.get("reviews", f"{random.randint(80, 400)}+ reviews")
            location = h.get("address") or h.get("location") or f"{city}, India"
            thumbnail = h.get("thumbnail") or h.get("image") or f"https://via.placeholder.com/300x200?text=Hotel+{i+1}"
            link = h.get("link") or h.get("booking_link") or "https://www.google.com/travel/hotels"
            amenities = h.get("amenities", ["Free WiFi", "Breakfast Included"])

            if serp_price:
                price = serp_price
                price_fallback = False
            else:
                name_lower = name.lower()
                if any(word in name_lower for word in ["oyo", "lodge", "hostel", "dorm"]):
                    min_p, max_p = 500, 1400
                elif any(word in name_lower for word in ["resort", "marriott", "hilton", "luxury", "premium"]):
                    min_p, max_p = 4000, 8000
                elif rating >= 4.3:
                    min_p, max_p = 3500, 6000
                elif rating >= 3.8:
                    min_p, max_p = 2200, 4000
                else:
                    min_p, max_p = 1500, 2500

                if affordability == "low":
                    max_p = int(max_p * 0.7)
                    min_p = int(min_p * 0.7)
                elif affordability == "high":
                    max_p = int(max_p * 1.3)
                    min_p = int(min_p * 1.1)

                price = f"₹{random.randint(min_p, max_p)}"
                price_fallback = True

            hotel = {
                "id": f"hotel{i}",
                "name": name,
                "price": price,
                "priceFallback": price_fallback,
                "rating": rating,
                "reviews": reviews,
                "location": location,
                "amenities": amenities,
                "thumbnail": thumbnail,
                "link": link,
            }

            parsed_hotels.append(hotel)

        if not parsed_hotels:
            print("⚠️ No hotels found from SerpAPI. Generating fallback list...")
            for i in range(5):
                parsed_hotels.append({
                    "id": f"fallback_hotel{i}",
                    "name": f"Fallback Hotel {i+1}",
                    "price": get_fallback_price(total_budget, num_days, tier),
                    "priceFallback": True,
                    "rating": round(random.uniform(3.3, 4.6), 1),
                    "reviews": f"{random.randint(100, 500)}+ reviews",
                    "location": f"{city}, India",
                    "amenities": ["Free WiFi", "AC Room", "Breakfast Included"],
                    "thumbnail": f"https://via.placeholder.com/300x200?text=Hotel+{i+1}",
                    "link": "https://www.google.com/travel/hotels",
                })

        print(f" Total parsed hotels returned: {len(parsed_hotels)}")
        return parsed_hotels

    except requests.exceptions.RequestException as e:
        print(" SerpAPI Hotel Request Failed:", e)
        return []
    except Exception as e:
        print(" Unexpected Error While Fetching Hotels:", e)
        return []
