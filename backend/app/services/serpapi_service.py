import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SerpAPIService:
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
        self.base_url = "https://serpapi.com/search"
    
    async def search_flights(self, origin: str, destination: str, departure_date: str, 
                           return_date: Optional[str] = None, travel_class: str = "economy") -> List[Dict[str, Any]]:
        """Search for flights using SerpAPI Google Flights"""
        
        if not self.api_key:
            logger.warning("SerpAPI key not available")
            return []
        
        params = {
            "engine": "google_flights",
            "departure_id": self._get_airport_code(origin),
            "arrival_id": self._get_airport_code(destination),
            "outbound_date": departure_date,
            "currency": "INR",
            "hl": "en",
            "gl": "in",
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
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                flights = []
                
                # Parse best flights
                if "best_flights" in data:
                    for flight in data["best_flights"][:5]:
                        parsed_flight = self._parse_flight_data(flight, departure_date, return_date)
                        if parsed_flight:
                            flights.append(parsed_flight)
                
                # Parse other flights
                if "other_flights" in data and len(flights) < 5:
                    for flight in data["other_flights"][:5-len(flights)]:
                        parsed_flight = self._parse_flight_data(flight, departure_date, return_date)
                        if parsed_flight:
                            flights.append(parsed_flight)
                
                logger.info(f"Found {len(flights)} flights via SerpAPI")
                return flights
                
        except Exception as e:
            logger.error(f"Error searching flights via SerpAPI: {str(e)}")
            return []
    
    async def search_hotels(self, location: str, check_in: str, check_out: str, 
                          guests: int = 2) -> List[Dict[str, Any]]:
        """Search for hotels using SerpAPI Google Hotels"""
        
        if not self.api_key:
            logger.warning("SerpAPI key not available")
            return []
        
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
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                hotels = []
                if "properties" in data:
                    for hotel in data["properties"][:8]:
                        parsed_hotel = self._parse_hotel_data(hotel, check_in, check_out)
                        if parsed_hotel:
                            hotels.append(parsed_hotel)
                
                logger.info(f"Found {len(hotels)} hotels via SerpAPI")
                return hotels
                
        except Exception as e:
            logger.error(f"Error searching hotels via SerpAPI: {str(e)}")
            return []
    
    def _parse_flight_data(self, flight_data: Dict[str, Any], departure_date: str, return_date: Optional[str]) -> Optional[Dict[str, Any]]:
        """Parse SerpAPI flight data into our format"""
        
        try:
            flights = flight_data.get("flights", [])
            if not flights:
                return None
                
            main_flight = flights[0]
            
            # Extract airline info
            airline = main_flight.get("airline", "Unknown")
            flight_number = main_flight.get("flight_number", "")
            
            # Extract airports
            departure_airport = main_flight.get("departure_airport", {})
            arrival_airport = main_flight.get("arrival_airport", {})
            
            # Extract times
            departure_time = departure_airport.get("time", "")
            arrival_time = arrival_airport.get("time", "")
            
            # Extract price
            price = flight_data.get("price", 0)
            if isinstance(price, dict):
                price = price.get("value", 0)
            
            return {
                "airline": airline,
                "flight_number": flight_number,
                "departure_airport": departure_airport.get("id", ""),
                "arrival_airport": arrival_airport.get("id", ""),
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "departure_date": departure_date,
                "return_date": return_date,
                "duration": flight_data.get("total_duration", ""),
                "price": float(price) if price else 0,
                "currency": "INR",
                "flight_class": "economy",
                "stops": len(flights) - 1,
                "booking_url": self._extract_booking_url(flight_data),
                "raw_data": flight_data
            }
            
        except Exception as e:
            logger.error(f"Error parsing flight data: {str(e)}")
            return None
    
    def _parse_hotel_data(self, hotel_data: Dict[str, Any], check_in: str, check_out: str) -> Optional[Dict[str, Any]]:
        """Parse SerpAPI hotel data into our format"""
        
        try:
            # Extract basic info
            name = hotel_data.get("name", "Unknown Hotel")
            
            # Extract rating
            rating = hotel_data.get("overall_rating", 0)
            if isinstance(rating, str):
                try:
                    rating = float(rating)
                except:
                    rating = 0
            
            # Extract reviews count
            reviews = hotel_data.get("reviews", 0)
            if isinstance(reviews, str):
                try:
                    reviews = int(reviews.replace(",", ""))
                except:
                    reviews = 0
            
            # Extract price
            rate_info = hotel_data.get("rate_per_night", {})
            price = 0
            if isinstance(rate_info, dict):
                price = rate_info.get("extracted_lowest", 0)
            elif isinstance(rate_info, (int, float)):
                price = rate_info
            
            # Extract amenities
            amenities = []
            if "amenities" in hotel_data:
                for amenity in hotel_data["amenities"][:6]:  # Limit to 6 amenities
                    if isinstance(amenity, str):
                        amenities.append({
                            "icon": self._get_amenity_icon(amenity),
                            "label": amenity
                        })
            
            # Generate booking URL
            booking_url = hotel_data.get("link", "")
            if not booking_url:
                booking_url = f"https://www.booking.com/searchresults.html?ss={name}&checkin={check_in}&checkout={check_out}"
            
            return {
                "name": name,
                "location": hotel_data.get("description", ""),
                "rating": float(rating),
                "reviews_count": int(reviews),
                "price_per_night": float(price) if price else 0,
                "currency": "INR",
                "amenities": amenities,
                "description": hotel_data.get("description", f"Quality accommodation in {name}"),
                "booking_url": booking_url,
                "raw_data": hotel_data
            }
            
        except Exception as e:
            logger.error(f"Error parsing hotel data: {str(e)}")
            return None
    
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
            "Ahmedabad": "AMD",
            "Jaipur": "JAI",
            "Lucknow": "LKO",
            "Bhubaneswar": "BBI",
            "Thiruvananthapuram": "TRV"
        }
        
        return codes.get(city, "DEL")
    
    def _get_amenity_icon(self, amenity: str) -> str:
        """Get icon for amenity"""
        
        amenity_lower = amenity.lower()
        
        if "wifi" in amenity_lower:
            return "wifi"
        elif "pool" in amenity_lower or "swimming" in amenity_lower:
            return "pool"
        elif "gym" in amenity_lower or "fitness" in amenity_lower:
            return "gym"
        elif "spa" in amenity_lower:
            return "spa"
        elif "restaurant" in amenity_lower or "dining" in amenity_lower:
            return "restaurant"
        elif "parking" in amenity_lower:
            return "parking"
        elif "business" in amenity_lower:
            return "business"
        elif "laundry" in amenity_lower:
            return "laundry"
        else:
            return "amenity"
    
    def _extract_booking_url(self, flight_data: Dict) -> str:
        """Extract booking URL from flight data"""
        
        booking_options = flight_data.get("booking_options", [])
        if booking_options and len(booking_options) > 0:
            return booking_options[0].get("link", "")
        
        return ""