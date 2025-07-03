import httpx
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FreeDataService:
    """Free alternative to SerpAPI using web scraping and mock data"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: str = None, travel_class: str = "economy") -> List[Dict[str, Any]]:
        """Get flight data using free methods"""
        
        # Generate realistic mock flight data
        airlines = [
            {"name": "IndiGo", "code": "6E", "logo": "https://logos-world.net/wp-content/uploads/2023/01/IndiGo-Logo.png"},
            {"name": "Air India", "code": "AI", "logo": "https://logos-world.net/wp-content/uploads/2021/02/Air-India-Logo.png"},
            {"name": "SpiceJet", "code": "SG", "logo": "https://logos-world.net/wp-content/uploads/2023/01/SpiceJet-Logo.png"},
            {"name": "Vistara", "code": "UK", "logo": "https://logos-world.net/wp-content/uploads/2023/01/Vistara-Logo.png"},
            {"name": "AkasaAir", "code": "QP", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0a/Akasa_Air_logo.svg/1200px-Akasa_Air_logo.svg.png"}
        ]
        
        flights = []
        base_price = self._get_base_price(origin, destination)
        
        for i, airline in enumerate(airlines):
            # Generate realistic flight times
            dep_hour = random.randint(6, 22)
            dep_minute = random.choice([0, 15, 30, 45])
            duration_hours = random.randint(1, 4)
            duration_minutes = random.choice([0, 15, 30, 45])
            
            arr_hour = (dep_hour + duration_hours) % 24
            arr_minute = (dep_minute + duration_minutes) % 60
            
            # Price variation
            price_multiplier = random.uniform(0.8, 1.4)
            if airline["name"] == "IndiGo":
                price_multiplier *= 0.9  # IndiGo typically cheaper
            elif airline["name"] == "Vistara":
                price_multiplier *= 1.2  # Vistara premium
            
            flight_price = int(base_price * price_multiplier)
            
            flight = {
                "airline": airline["name"],
                "flight_number": f"{airline['code']}{random.randint(100, 999)}",
                "departure_airport": origin,
                "arrival_airport": destination,
                "departure_time": f"{dep_hour:02d}:{dep_minute:02d}",
                "arrival_time": f"{arr_hour:02d}:{arr_minute:02d}",
                "duration": f"{duration_hours}h {duration_minutes}m",
                "price": flight_price,
                "stops": 0 if random.random() > 0.3 else 1,
                "booking_url": f"https://www.makemytrip.com/flight/search?from={origin}&to={destination}&departure={departure_date}",
                "thumbnail": airline["logo"],
                "raw_data": {"source": "mock_data", "generated_at": datetime.now().isoformat()}
            }
            flights.append(flight)
        
        return flights
    
    async def search_hotels(self, location: str, check_in: str, check_out: str, 
                          guests: int = 2) -> List[Dict[str, Any]]:
        """Get hotel data using free methods"""
        
        # Generate realistic mock hotel data
        hotel_types = [
            {"suffix": "Grand Hotel", "rating": 4.5, "price_multiplier": 1.5},
            {"suffix": "Palace", "rating": 4.8, "price_multiplier": 2.0},
            {"suffix": "Inn", "rating": 4.0, "price_multiplier": 0.8},
            {"suffix": "Resort", "rating": 4.3, "price_multiplier": 1.3},
            {"suffix": "Suites", "rating": 4.2, "price_multiplier": 1.1},
            {"suffix": "Lodge", "rating": 3.8, "price_multiplier": 0.7},
            {"suffix": "Heritage Hotel", "rating": 4.6, "price_multiplier": 1.7},
            {"suffix": "Business Hotel", "rating": 4.1, "price_multiplier": 1.0}
        ]
        
        hotels = []
        base_price = self._get_base_hotel_price(location)
        
        for i, hotel_type in enumerate(hotel_types):
            hotel_name = f"{location} {hotel_type['suffix']}"
            price = int(base_price * hotel_type['price_multiplier'] * random.uniform(0.9, 1.1))
            
            amenities = self._generate_amenities()
            
            hotel = {
                "name": hotel_name,
                "location": f"{location} City Center",
                "rating": round(hotel_type['rating'] + random.uniform(-0.2, 0.2), 1),
                "reviews_count": random.randint(50, 2000),
                "price_per_night": price,
                "amenities": amenities,
                "description": f"Experience comfort and luxury at {hotel_name}. Located in the heart of {location} with modern amenities and excellent service.",
                "booking_url": f"https://www.booking.com/searchresults.html?ss={location}&checkin={check_in}&checkout={check_out}",
                "thumbnail": f"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=300&h=200&fit=crop",
                "raw_data": {"source": "mock_data", "generated_at": datetime.now().isoformat()}
            }
            hotels.append(hotel)
        
        return hotels
    
    def _get_base_price(self, origin: str, destination: str) -> int:
        """Calculate base flight price based on route"""
        
        # Distance-based pricing (simplified)
        route_prices = {
            ("Delhi", "Mumbai"): 8000,
            ("Delhi", "Bangalore"): 9000,
            ("Delhi", "Chennai"): 10000,
            ("Delhi", "Kolkata"): 7500,
            ("Delhi", "Goa"): 8500,
            ("Mumbai", "Bangalore"): 6000,
            ("Mumbai", "Chennai"): 7000,
            ("Mumbai", "Kolkata"): 8000,
            ("Mumbai", "Goa"): 4500,
            ("Bangalore", "Chennai"): 4000,
            ("Bangalore", "Kolkata"): 8500,
            ("Bangalore", "Goa"): 5000,
        }
        
        # Check both directions
        route_key = (origin, destination)
        reverse_key = (destination, origin)
        
        if route_key in route_prices:
            return route_prices[route_key]
        elif reverse_key in route_prices:
            return route_prices[reverse_key]
        else:
            # Default price for unknown routes
            return 8000
    
    def _get_base_hotel_price(self, location: str) -> int:
        """Calculate base hotel price based on location"""
        
        location_prices = {
            "Mumbai": 5000,
            "Delhi": 4500,
            "Bangalore": 4000,
            "Chennai": 3500,
            "Kolkata": 3000,
            "Goa": 6000,
            "Jaipur": 3500,
            "Udaipur": 4500,
            "Kerala": 4000,
            "Manali": 3000,
        }
        
        return location_prices.get(location, 3500)
    
    def _generate_amenities(self) -> List[Dict[str, Any]]:
        """Generate realistic hotel amenities"""
        
        all_amenities = [
            {"icon": "wifi", "label": "Free WiFi"},
            {"icon": "pool", "label": "Swimming Pool"},
            {"icon": "gym", "label": "Fitness Center"},
            {"icon": "spa", "label": "Spa & Wellness"},
            {"icon": "restaurant", "label": "Restaurant"},
            {"icon": "parking", "label": "Free Parking"},
            {"icon": "ac", "label": "Air Conditioning"},
            {"icon": "room_service", "label": "24/7 Room Service"},
            {"icon": "laundry", "label": "Laundry Service"},
            {"icon": "concierge", "label": "Concierge"},
            {"icon": "business", "label": "Business Center"},
            {"icon": "airport", "label": "Airport Shuttle"}
        ]
        
        # Randomly select 4-8 amenities
        num_amenities = random.randint(4, 8)
        return random.sample(all_amenities, num_amenities)