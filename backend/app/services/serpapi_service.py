import httpx
from typing import List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SerpAPIService:
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
        self.base_url = "https://serpapi.com/search"
    
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: str = None, travel_class: str = "economy") -> List[Dict[str, Any]]:
        """Search for flights using SerpAPI Google Flights"""
        
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "currency": "INR",
            "hl": "en",
            "api_key": self.api_key
        }
        
        if return_date:
            params["return_date"] = return_date
            params["type"] = "2"  # Round trip
        else:
            params["type"] = "1"  # One way
            
        if travel_class != "economy":
            params["travel_class"] = travel_class
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                flights = []
                if "best_flights" in data:
                    for flight in data["best_flights"][:10]:  # Limit to top 10
                        flights.append(self._parse_flight_data(flight))
                
                if "other_flights" in data:
                    for flight in data["other_flights"][:5]:  # Add 5 more options
                        flights.append(self._parse_flight_data(flight))
                
                return flights
                
        except Exception as e:
            logger.error(f"Error searching flights: {str(e)}")
            return []
    
    async def search_hotels(self, location: str, check_in: str, check_out: str, 
                          guests: int = 2) -> List[Dict[str, Any]]:
        """Search for hotels using SerpAPI Google Hotels"""
        
        params = {
            "engine": "google_hotels",
            "q": location,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": guests,
            "currency": "INR",
            "gl": "in",
            "hl": "en",
            "api_key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                hotels = []
                if "properties" in data:
                    for hotel in data["properties"][:15]:  # Limit to top 15
                        hotels.append(self._parse_hotel_data(hotel))
                
                return hotels
                
        except Exception as e:
            logger.error(f"Error searching hotels: {str(e)}")
            return []
    
    def _parse_flight_data(self, flight_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SerpAPI flight data into our format"""
        
        # Extract flight details
        flights = flight_data.get("flights", [])
        if not flights:
            return {}
            
        main_flight = flights[0]
        
        return {
            "airline": main_flight.get("airline", "Unknown"),
            "flight_number": main_flight.get("flight_number", ""),
            "departure_airport": main_flight.get("departure_airport", {}).get("id", ""),
            "arrival_airport": main_flight.get("arrival_airport", {}).get("id", ""),
            "departure_time": main_flight.get("departure_airport", {}).get("time", ""),
            "arrival_time": main_flight.get("arrival_airport", {}).get("time", ""),
            "duration": flight_data.get("total_duration", ""),
            "price": flight_data.get("price", 0),
            "stops": len(flights) - 1,
            "booking_url": flight_data.get("booking_options", [{}])[0].get("link", ""),
            "thumbnail": main_flight.get("airline_logo", ""),
            "raw_data": flight_data
        }
    
    def _parse_hotel_data(self, hotel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SerpAPI hotel data into our format"""
        
        return {
            "name": hotel_data.get("name", "Unknown Hotel"),
            "location": hotel_data.get("description", ""),
            "rating": hotel_data.get("overall_rating", 0.0),
            "reviews_count": hotel_data.get("reviews", 0),
            "price_per_night": hotel_data.get("rate_per_night", {}).get("extracted_lowest", 0),
            "amenities": hotel_data.get("amenities", []),
            "description": hotel_data.get("description", ""),
            "booking_url": hotel_data.get("link", ""),
            "thumbnail": hotel_data.get("images", [{}])[0].get("thumbnail", "") if hotel_data.get("images") else "",
            "raw_data": hotel_data
        }