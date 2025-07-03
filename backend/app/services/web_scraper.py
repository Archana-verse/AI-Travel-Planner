import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging
import random

logger = logging.getLogger(__name__)

class FlightScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: Optional[str] = None, travel_class: str = "economy") -> List[Dict[str, Any]]:
        """Scrape flight data from public sources"""
        
        try:
            # For demo purposes, we'll return realistic mock data
            # In production, you would implement actual scraping logic
            
            logger.info(f"Scraping flights from {origin} to {destination}")
            
            # Simulate network delay
            await asyncio.sleep(1)
            
            # Generate realistic flight data
            flights = self._generate_realistic_flights(origin, destination, departure_date, return_date, travel_class)
            
            logger.info(f"Generated {len(flights)} flights via scraping simulation")
            return flights
            
        except Exception as e:
            logger.error(f"Error in flight scraping: {str(e)}")
            return []
    
    def _generate_realistic_flights(self, origin: str, destination: str, departure_date: str, 
                                  return_date: Optional[str], travel_class: str) -> List[Dict[str, Any]]:
        """Generate realistic flight data based on actual airline patterns"""
        
        airlines = [
            {"name": "IndiGo", "code": "6E", "reputation": 0.9, "punctuality": 0.85},
            {"name": "Air India", "code": "AI", "reputation": 0.7, "punctuality": 0.75},
            {"name": "Vistara", "code": "UK", "reputation": 0.95, "punctuality": 0.9},
            {"name": "SpiceJet", "code": "SG", "reputation": 0.8, "punctuality": 0.8},
            {"name": "AkasaAir", "code": "QP", "reputation": 0.85, "punctuality": 0.85}
        ]
        
        # Calculate base price based on route and class
        base_price = self._calculate_route_price(origin, destination)
        
        class_multipliers = {
            "economy": 1.0,
            "business": 2.5,
            "first": 4.0
        }
        
        base_price *= class_multipliers.get(travel_class, 1.0)
        
        flights = []
        
        for i, airline in enumerate(airlines):
            # Generate realistic timing
            departure_hour = random.choice([6, 8, 10, 14, 16, 18, 20])
            departure_minute = random.choice([0, 15, 30, 45])
            
            # Calculate flight duration based on route
            flight_duration = self._calculate_flight_duration(origin, destination)
            arrival_hour = (departure_hour + flight_duration) % 24
            arrival_minute = (departure_minute + random.choice([0, 15, 30])) % 60
            
            # Calculate price with realistic variation
            price_variation = random.uniform(0.85, 1.15)
            airline_premium = 1 + (airline['reputation'] - 0.8) * 0.5
            flight_price = int(base_price * price_variation * airline_premium)
            
            # Generate flight number
            flight_number = f"{airline['code']}{random.randint(100, 999)}"
            
            flight = {
                "airline": airline["name"],
                "flight_number": flight_number,
                "departure_airport": self._get_airport_code(origin),
                "arrival_airport": self._get_airport_code(destination),
                "departure_time": f"{departure_hour:02d}:{departure_minute:02d}",
                "arrival_time": f"{arrival_hour:02d}:{arrival_minute:02d}",
                "departure_date": departure_date,
                "return_date": return_date,
                "duration": f"{flight_duration}h {random.choice([0, 15, 30, 45])}m",
                "price": flight_price,
                "currency": "INR",
                "flight_class": travel_class,
                "stops": 0 if random.random() > 0.3 else 1,
                "booking_url": self._generate_booking_url(airline["name"], origin, destination, departure_date),
                "raw_data": {
                    "source": "web_scraping_simulation",
                    "reputation": airline['reputation'],
                    "punctuality": airline['punctuality']
                }
            }
            
            flights.append(flight)
        
        # Sort by price
        flights.sort(key=lambda x: x['price'])
        
        return flights
    
    def _calculate_route_price(self, origin: str, destination: str) -> int:
        """Calculate base price for route in INR"""
        
        # Distance-based pricing (realistic Indian domestic routes)
        route_prices = {
            ("Delhi", "Mumbai"): 6000,
            ("Delhi", "Bangalore"): 7000,
            ("Delhi", "Chennai"): 8000,
            ("Delhi", "Kolkata"): 5500,
            ("Delhi", "Goa"): 7500,
            ("Delhi", "Hyderabad"): 6500,
            ("Mumbai", "Bangalore"): 4500,
            ("Mumbai", "Chennai"): 5500,
            ("Mumbai", "Kolkata"): 6500,
            ("Mumbai", "Goa"): 3500,
            ("Mumbai", "Hyderabad"): 4000,
            ("Bangalore", "Chennai"): 3000,
            ("Bangalore", "Kolkata"): 6000,
            ("Bangalore", "Goa"): 4000,
            ("Bangalore", "Hyderabad"): 2500,
            ("Chennai", "Kolkata"): 5500,
            ("Chennai", "Hyderabad"): 3500,
        }
        
        # Check both directions
        route_key = (origin, destination)
        reverse_key = (destination, origin)
        
        return route_prices.get(route_key, route_prices.get(reverse_key, 6000))
    
    def _calculate_flight_duration(self, origin: str, destination: str) -> int:
        """Calculate flight duration in hours"""
        
        durations = {
            ("Delhi", "Mumbai"): 2,
            ("Delhi", "Bangalore"): 3,
            ("Delhi", "Chennai"): 3,
            ("Delhi", "Kolkata"): 2,
            ("Delhi", "Goa"): 2,
            ("Delhi", "Hyderabad"): 2,
            ("Mumbai", "Bangalore"): 2,
            ("Mumbai", "Chennai"): 2,
            ("Mumbai", "Kolkata"): 2,
            ("Mumbai", "Goa"): 1,
            ("Mumbai", "Hyderabad"): 1,
            ("Bangalore", "Chennai"): 1,
            ("Bangalore", "Kolkata"): 2,
            ("Bangalore", "Goa"): 1,
            ("Bangalore", "Hyderabad"): 1,
            ("Chennai", "Kolkata"): 2,
            ("Chennai", "Hyderabad"): 1,
        }
        
        route_key = (origin, destination)
        reverse_key = (destination, origin)
        
        return durations.get(route_key, durations.get(reverse_key, 2))
    
    def _get_airport_code(self, city: str) -> str:
        """Get IATA airport code for city"""
        
        codes = {
            "Delhi": "DEL",
            "Mumbai": "BOM",
            "Bangalore": "BLR",
            "Chennai": "MAA", 
            "Kolkata": "CCU",
            "Goa": "GOI",
            "Hyderabad": "HYD",
            "Pune": "PNQ",
            "Kochi": "COK",
            "Ahmedabad": "AMD"
        }
        
        return codes.get(city, "DEL")
    
    def _generate_booking_url(self, airline: str, origin: str, destination: str, departure_date: str) -> str:
        """Generate realistic booking URL"""
        
        from_code = self._get_airport_code(origin)
        to_code = self._get_airport_code(destination)
        
        airline_urls = {
            "IndiGo": f"https://www.goindigo.in/booking/flight-select?from={from_code}&to={to_code}&departure={departure_date}",
            "Air India": f"https://www.airindia.in/booking/flight-search?from={from_code}&to={to_code}&departure={departure_date}",
            "Vistara": f"https://www.airvistara.com/booking/flight-search?origin={from_code}&destination={to_code}&departure={departure_date}",
            "SpiceJet": f"https://www.spicejet.com/flight-booking?from={from_code}&to={to_code}&departure={departure_date}",
            "AkasaAir": f"https://www.akasaair.com/booking?from={from_code}&to={to_code}&departure={departure_date}"
        }
        
        return airline_urls.get(airline, f"https://www.makemytrip.com/flight/search?from={from_code}&to={to_code}&departure={departure_date}")


class HotelScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search_hotels(self, location: str, check_in: str, check_out: str, guests: int = 2) -> List[Dict[str, Any]]:
        """Scrape hotel data from public sources"""
        
        try:
            logger.info(f"Scraping hotels in {location}")
            
            # Simulate network delay
            await asyncio.sleep(1)
            
            # Generate realistic hotel data
            hotels = self._generate_realistic_hotels(location, check_in, check_out, guests)
            
            logger.info(f"Generated {len(hotels)} hotels via scraping simulation")
            return hotels
            
        except Exception as e:
            logger.error(f"Error in hotel scraping: {str(e)}")
            return []
    
    def _generate_realistic_hotels(self, location: str, check_in: str, check_out: str, guests: int) -> List[Dict[str, Any]]:
        """Generate realistic hotel data"""
        
        # Base pricing by city
        city_pricing = {
            'Mumbai': 4500,
            'Delhi': 4000,
            'Bangalore': 3500,
            'Chennai': 3000,
            'Kolkata': 2500,
            'Goa': 5000,
            'Hyderabad': 3200,
            'Pune': 3000
        }
        
        base_price = city_pricing.get(location, 3500)
        
        hotel_types = [
            {
                "name_template": "{} Grand Hotel",
                "rating_range": (4.3, 4.7),
                "price_multiplier": (1.0, 1.3),
                "amenities": ["Free WiFi", "Swimming Pool", "Spa & Wellness", "Restaurant", "Free Parking", "Fitness Center"]
            },
            {
                "name_template": "{} Business Hotel", 
                "rating_range": (4.0, 4.4),
                "price_multiplier": (0.8, 1.1),
                "amenities": ["Free WiFi", "Business Center", "Restaurant", "Free Parking", "24/7 Room Service"]
            },
            {
                "name_template": "{} Heritage Palace",
                "rating_range": (4.5, 4.9),
                "price_multiplier": (1.2, 1.6),
                "amenities": ["Free WiFi", "Spa & Wellness", "Fine Dining", "Heritage Architecture", "Concierge Service", "Swimming Pool"]
            },
            {
                "name_template": "The {} Suites",
                "rating_range": (4.1, 4.5),
                "price_multiplier": (0.9, 1.2),
                "amenities": ["Free WiFi", "Kitchenette", "Swimming Pool", "Free Parking", "Laundry Service"]
            },
            {
                "name_template": "{} Inn",
                "rating_range": (3.8, 4.2),
                "price_multiplier": (0.6, 0.9),
                "amenities": ["Free WiFi", "Restaurant", "Free Parking", "Air Conditioning"]
            }
        ]
        
        hotels = []
        
        for i, hotel_type in enumerate(hotel_types):
            # Generate hotel details
            name = hotel_type["name_template"].format(location)
            rating = round(random.uniform(*hotel_type["rating_range"]), 1)
            price_mult = random.uniform(*hotel_type["price_multiplier"])
            price = int(base_price * price_mult)
            
            # Generate amenities
            amenities = []
            for amenity_name in hotel_type["amenities"]:
                amenities.append({
                    "icon": self._get_amenity_icon(amenity_name),
                    "label": amenity_name
                })
            
            # Generate reviews count
            reviews_count = random.randint(50, 1500)
            
            hotel = {
                "name": name,
                "location": f"{location} City Center",
                "rating": rating,
                "reviews_count": reviews_count,
                "price_per_night": price,
                "currency": "INR",
                "amenities": amenities,
                "description": f"Experience comfort and hospitality at {name}. Located in the heart of {location} with modern amenities and excellent service.",
                "booking_url": self._generate_hotel_booking_url(name, location, check_in, check_out),
                "raw_data": {
                    "source": "web_scraping_simulation",
                    "hotel_type": hotel_type["name_template"]
                }
            }
            
            hotels.append(hotel)
        
        # Sort by rating (best first)
        hotels.sort(key=lambda x: x['rating'], reverse=True)
        
        return hotels
    
    def _get_amenity_icon(self, amenity_name: str) -> str:
        """Get icon for amenity"""
        
        amenity_lower = amenity_name.lower()
        
        icon_mapping = {
            "wifi": "wifi",
            "pool": "pool", 
            "swimming": "pool",
            "gym": "gym",
            "fitness": "gym",
            "spa": "spa",
            "wellness": "spa",
            "restaurant": "restaurant",
            "dining": "restaurant",
            "parking": "parking",
            "business": "business",
            "laundry": "laundry",
            "concierge": "concierge",
            "heritage": "heritage"
        }
        
        for keyword, icon in icon_mapping.items():
            if keyword in amenity_lower:
                return icon
        
        return "amenity"
    
    def _generate_hotel_booking_url(self, hotel_name: str, location: str, check_in: str, check_out: str) -> str:
        """Generate realistic hotel booking URL"""
        
        platforms = [
            f"https://www.booking.com/searchresults.html?ss={location}&checkin={check_in}&checkout={check_out}",
            f"https://www.makemytrip.com/hotels/hotel-listing?city={location}&checkin={check_in}&checkout={check_out}",
            f"https://www.agoda.com/search?city={location}&checkIn={check_in}&checkOut={check_out}",
            f"https://www.goibibo.com/hotels/search/?city={location}&checkin={check_in}&checkout={check_out}"
        ]
        
        return random.choice(platforms)