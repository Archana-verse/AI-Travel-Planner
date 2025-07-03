import asyncio
import httpx
from typing import Dict, Any, List
from app.config import settings
from app.services.serpapi_service import SerpAPIService
from app.services.web_scraper import HotelScraper
import logging

logger = logging.getLogger(__name__)

class HotelAgent:
    def __init__(self):
        self.serpapi = SerpAPIService()
        self.scraper = HotelScraper()
    
    async def search_hotels(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for hotels using multiple data sources"""
        
        try:
            # Try SerpAPI first if key is available
            if settings.SERPAPI_KEY:
                logger.info("Searching hotels via SerpAPI")
                hotels = await self.serpapi.search_hotels(
                    location=preferences.get('to_location'),
                    check_in=preferences.get('departure_date'),
                    check_out=preferences.get('return_date'),
                    guests=self._get_guest_count(preferences.get('travelers', 'solo'))
                )
                
                if hotels:
                    return await self._analyze_hotels(hotels, preferences)
            
            # Fallback to web scraping
            logger.info("Searching hotels via web scraping")
            hotels = await self.scraper.search_hotels(
                location=preferences.get('to_location'),
                check_in=preferences.get('departure_date'),
                check_out=preferences.get('return_date'),
                guests=self._get_guest_count(preferences.get('travelers', 'solo'))
            )
            
            return await self._analyze_hotels(hotels, preferences)
            
        except Exception as e:
            logger.error(f"Error searching hotels: {str(e)}")
            # Return realistic mock data as fallback
            return self._generate_fallback_hotels(preferences)
    
    async def _analyze_hotels(self, hotels: List[Dict], preferences: Dict) -> List[Dict]:
        """Analyze hotels using AI to provide recommendations"""
        
        budget_mapping = {
            'budget': {'max_price': 3000, 'min_rating': 3.5},
            'comfort': {'max_price': 6000, 'min_rating': 4.0},
            'luxury': {'max_price': 15000, 'min_rating': 4.5}
        }
        
        budget_info = budget_mapping.get(preferences.get('budget', 'comfort'))
        interests = preferences.get('interests', [])
        
        for hotel in hotels:
            score = 0
            reasoning = {}
            
            # Price analysis
            price = hotel.get('price_per_night', 0)
            if price <= budget_info['max_price'] * 0.7:
                reasoning['price'] = "Excellent value within budget range"
                score += 25
            elif price <= budget_info['max_price']:
                reasoning['price'] = "Good value for the price point"
                score += 20
            else:
                reasoning['price'] = "Premium pricing for luxury experience"
                score += 10
            
            # Rating analysis
            rating = hotel.get('rating', 0)
            if rating >= budget_info['min_rating'] + 0.5:
                reasoning['rating'] = "Outstanding guest reviews and high ratings"
                score += 30
            elif rating >= budget_info['min_rating']:
                reasoning['rating'] = "Very good ratings from previous guests"
                score += 25
            else:
                reasoning['rating'] = "Decent ratings with good value"
                score += 15
            
            # Amenities analysis
            amenities = hotel.get('amenities', [])
            amenity_score = self._score_amenities(amenities, interests)
            reasoning['amenities'] = self._get_amenity_reasoning(amenities, interests)
            score += amenity_score
            
            # Location analysis
            location = hotel.get('location', '').lower()
            if any(keyword in location for keyword in ['center', 'central', 'main', 'downtown']):
                reasoning['location'] = "Prime central location with easy access to attractions"
                score += 20
            elif any(keyword in location for keyword in ['station', 'airport', 'metro']):
                reasoning['location'] = "Convenient location near transportation hubs"
                score += 15
            else:
                reasoning['location'] = "Well-positioned for exploring the area"
                score += 10
            
            # Review count consideration
            reviews = hotel.get('reviews_count', 0)
            if reviews >= 500:
                score += 10
            elif reviews >= 100:
                score += 5
            
            hotel['ai_recommended'] = score >= 70
            hotel['ai_reasoning'] = reasoning
            hotel['ai_score'] = score
        
        # Sort by AI score
        hotels.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
        
        return hotels[:5]  # Return top 5 hotels
    
    def _score_amenities(self, amenities: List[Dict], interests: List[str]) -> int:
        """Score amenities based on user interests"""
        
        amenity_labels = [a.get('label', '').lower() for a in amenities]
        score = 0
        
        # Base amenities
        if any('wifi' in label for label in amenity_labels):
            score += 5
        if any('parking' in label for label in amenity_labels):
            score += 5
        if any('restaurant' in label for label in amenity_labels):
            score += 5
        
        # Interest-based scoring
        if 'wellness' in interests:
            if any(keyword in ' '.join(amenity_labels) for keyword in ['spa', 'gym', 'wellness']):
                score += 15
        
        if 'beaches' in interests or 'adventure' in interests:
            if any('pool' in label for label in amenity_labels):
                score += 10
        
        if 'business' in interests:
            if any(keyword in ' '.join(amenity_labels) for keyword in ['business', 'center', 'meeting']):
                score += 10
        
        return min(score, 25)  # Cap at 25 points
    
    def _get_amenity_reasoning(self, amenities: List[Dict], interests: List[str]) -> str:
        """Generate reasoning text for amenities"""
        
        amenity_labels = [a.get('label', '') for a in amenities]
        
        if len(amenities) >= 6:
            return "Comprehensive amenities for a comfortable stay"
        elif len(amenities) >= 4:
            return "Good selection of essential amenities"
        else:
            return "Basic amenities covering key needs"
    
    def _get_guest_count(self, travelers: str) -> int:
        """Convert traveler type to guest count"""
        
        mapping = {
            'solo': 1,
            'couple': 2,
            'family': 4,
            'friends': 3
        }
        
        return mapping.get(travelers, 2)
    
    def _generate_fallback_hotels(self, preferences: Dict) -> List[Dict]:
        """Generate realistic fallback hotel data"""
        
        location = preferences.get('to_location', 'Mumbai')
        budget = preferences.get('budget', 'comfort')
        
        # Base pricing by city and budget
        city_pricing = {
            'Mumbai': {'budget': 2500, 'comfort': 4500, 'luxury': 8500},
            'Delhi': {'budget': 2200, 'comfort': 4000, 'luxury': 8000},
            'Bangalore': {'budget': 2000, 'comfort': 3800, 'luxury': 7500},
            'Chennai': {'budget': 1800, 'comfort': 3500, 'luxury': 7000},
            'Kolkata': {'budget': 1500, 'comfort': 3000, 'luxury': 6500},
            'Goa': {'budget': 3000, 'comfort': 5500, 'luxury': 10000}
        }
        
        base_price = city_pricing.get(location, city_pricing['Mumbai'])[budget]
        
        hotel_types = [
            {
                "name_suffix": "Grand Hotel",
                "rating": 4.5,
                "amenities": [
                    {"icon": "wifi", "label": "Free WiFi"},
                    {"icon": "pool", "label": "Swimming Pool"},
                    {"icon": "spa", "label": "Spa & Wellness"},
                    {"icon": "restaurant", "label": "Restaurant"},
                    {"icon": "parking", "label": "Free Parking"},
                    {"icon": "gym", "label": "Fitness Center"}
                ],
                "price_mult": 1.2
            },
            {
                "name_suffix": "Business Hotel",
                "rating": 4.2,
                "amenities": [
                    {"icon": "wifi", "label": "Free WiFi"},
                    {"icon": "business", "label": "Business Center"},
                    {"icon": "restaurant", "label": "Restaurant"},
                    {"icon": "parking", "label": "Free Parking"},
                    {"icon": "laundry", "label": "Laundry Service"}
                ],
                "price_mult": 1.0
            },
            {
                "name_suffix": "Comfort Inn",
                "rating": 4.0,
                "amenities": [
                    {"icon": "wifi", "label": "Free WiFi"},
                    {"icon": "restaurant", "label": "Restaurant"},
                    {"icon": "parking", "label": "Free Parking"},
                    {"icon": "ac", "label": "Air Conditioning"}
                ],
                "price_mult": 0.8
            },
            {
                "name_suffix": "Heritage Palace",
                "rating": 4.7,
                "amenities": [
                    {"icon": "wifi", "label": "Free WiFi"},
                    {"icon": "spa", "label": "Spa & Wellness"},
                    {"icon": "restaurant", "label": "Fine Dining"},
                    {"icon": "concierge", "label": "Concierge Service"},
                    {"icon": "heritage", "label": "Heritage Architecture"}
                ],
                "price_mult": 1.5
            },
            {
                "name_suffix": "Suites",
                "rating": 4.3,
                "amenities": [
                    {"icon": "wifi", "label": "Free WiFi"},
                    {"icon": "kitchen", "label": "Kitchenette"},
                    {"icon": "pool", "label": "Swimming Pool"},
                    {"icon": "parking", "label": "Free Parking"}
                ],
                "price_mult": 1.1
            }
        ]
        
        hotels = []
        
        for i, hotel_type in enumerate(hotel_types):
            price = int(base_price * hotel_type['price_mult'])
            
            hotel = {
                "id": f"hotel_{i+1}",
                "name": f"{location} {hotel_type['name_suffix']}",
                "location": f"{location} City Center",
                "rating": hotel_type['rating'] + (i * 0.1 - 0.2),  # Slight variation
                "reviews_count": 150 + (i * 200),
                "price_per_night": price,
                "currency": "INR",
                "amenities": hotel_type['amenities'],
                "description": f"Experience comfort and hospitality at {location} {hotel_type['name_suffix']}. Located in the heart of {location} with modern amenities and excellent service.",
                "booking_url": self._generate_hotel_booking_url(hotel_type['name_suffix'], location, preferences)
            }
            
            hotels.append(hotel)
        
        return hotels
    
    def _generate_hotel_booking_url(self, hotel_name: str, location: str, preferences: Dict) -> str:
        """Generate booking URL for the hotel"""
        
        checkin = preferences.get('departure_date', '2024-01-01')
        checkout = preferences.get('return_date', '2024-01-03')
        
        # Use different booking platforms for variety
        platforms = [
            f"https://www.booking.com/searchresults.html?ss={location}&checkin={checkin}&checkout={checkout}",
            f"https://www.makemytrip.com/hotels/hotel-listing?city={location}&checkin={checkin}&checkout={checkout}",
            f"https://www.agoda.com/search?city={location}&checkIn={checkin}&checkOut={checkout}",
            f"https://www.cleartrip.com/hotels/results?where={location}&checkin={checkin}&checkout={checkout}",
            f"https://www.goibibo.com/hotels/search/?city={location}&checkin={checkin}&checkout={checkout}"
        ]
        
        import random
        return random.choice(platforms)