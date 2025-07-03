import json
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FreeAIService:
    """Free AI service using rule-based logic and templates"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    async def generate_itinerary(self, preferences: Dict[str, Any], 
                               flights: List[Dict[str, Any]], 
                               hotels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate itinerary using templates and rules"""
        
        destination = preferences.get('to_location', 'India')
        departure_date = preferences.get('departure_date')
        return_date = preferences.get('return_date')
        interests = preferences.get('interests', [])
        budget = preferences.get('budget', 'comfort')
        
        # Calculate trip duration
        if departure_date and return_date:
            try:
                start = datetime.strptime(departure_date, '%Y-%m-%d')
                end = datetime.strptime(return_date, '%Y-%m-%d')
                total_days = (end - start).days
            except:
                total_days = 3
        else:
            total_days = 3
        
        # Get destination-specific activities
        activities = self._get_destination_activities(destination, interests)
        
        # Generate daily plans
        daily_plans = []
        for day in range(1, total_days + 1):
            current_date = datetime.strptime(departure_date, '%Y-%m-%d') + timedelta(days=day-1)
            
            day_activities = self._generate_day_activities(
                day, destination, activities, budget, day == 1, day == total_days
            )
            
            daily_plans.append({
                "day": day,
                "date": current_date.strftime('%Y-%m-%d'),
                "title": f"Day {day} - {day_activities['title']}",
                "activities": day_activities['activities']
            })
        
        # Calculate estimated cost
        estimated_cost = self._calculate_estimated_cost(daily_plans, budget, total_days)
        
        return {
            "title": f"Amazing {total_days}-Day {destination} Adventure",
            "description": f"Discover the best of {destination} with this carefully crafted itinerary featuring {', '.join(interests[:3]) if interests else 'amazing experiences'}.",
            "total_days": total_days,
            "estimated_cost": estimated_cost,
            "daily_plans": daily_plans
        }
    
    async def chat_response(self, message: str, context: str = "") -> str:
        """Generate chat response using rule-based logic"""
        
        message_lower = message.lower()
        
        # Travel planning questions
        if any(word in message_lower for word in ['plan', 'itinerary', 'trip', 'travel']):
            return self._get_planning_response(message_lower, context)
        
        # Destination questions
        elif any(word in message_lower for word in ['where', 'destination', 'place', 'visit']):
            return self._get_destination_response(message_lower)
        
        # Budget questions
        elif any(word in message_lower for word in ['budget', 'cost', 'price', 'money', 'expensive']):
            return self._get_budget_response(message_lower)
        
        # Food questions
        elif any(word in message_lower for word in ['food', 'eat', 'restaurant', 'cuisine']):
            return self._get_food_response(message_lower)
        
        # Transportation questions
        elif any(word in message_lower for word in ['flight', 'train', 'bus', 'transport']):
            return self._get_transport_response(message_lower)
        
        # Weather questions
        elif any(word in message_lower for word in ['weather', 'climate', 'season', 'temperature']):
            return self._get_weather_response(message_lower)
        
        # Default response
        else:
            return self._get_default_response()
    
    async def analyze_flight_recommendations(self, flights: List[Dict[str, Any]], 
                                           preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze flights using rule-based logic"""
        
        budget = preferences.get('budget', 'comfort')
        
        for i, flight in enumerate(flights):
            price = flight.get('price', 0)
            airline = flight.get('airline', '')
            duration = flight.get('duration', '')
            departure_time = flight.get('departure_time', '')
            
            # Determine if AI recommended
            ai_recommended = False
            reasoning = {}
            
            # Price analysis
            if budget == 'budget' and price < 8000:
                reasoning['price'] = "Great value for budget travelers"
                ai_recommended = True
            elif budget == 'comfort' and 7000 <= price <= 12000:
                reasoning['price'] = "Perfect balance of price and comfort"
                ai_recommended = True
            elif budget == 'luxury' and price > 10000:
                reasoning['price'] = "Premium service worth the investment"
                ai_recommended = True
            else:
                reasoning['price'] = "Competitive pricing for the route"
            
            # Duration analysis
            duration_hours = self._extract_duration_hours(duration)
            if duration_hours <= 2:
                reasoning['duration'] = "Quick and convenient flight time"
            elif duration_hours <= 4:
                reasoning['duration'] = "Reasonable flight duration"
            else:
                reasoning['duration'] = "Longer flight but may offer better value"
            
            # Airline analysis
            if airline == "IndiGo":
                reasoning['airline'] = "Known for punctuality and value"
            elif airline == "Vistara":
                reasoning['airline'] = "Premium service and comfort"
            elif airline == "Air India":
                reasoning['airline'] = "National carrier with extensive network"
            else:
                reasoning['airline'] = "Reliable airline with good service"
            
            # Departure time analysis
            dep_hour = int(departure_time.split(':')[0]) if ':' in departure_time else 12
            if 6 <= dep_hour <= 9:
                reasoning['departure'] = "Morning flight - full day at destination"
            elif 10 <= dep_hour <= 16:
                reasoning['departure'] = "Convenient daytime departure"
            else:
                reasoning['departure'] = "Evening flight - may offer better prices"
            
            flight['ai_recommended'] = ai_recommended
            flight['ai_reasoning'] = reasoning
        
        return flights
    
    async def analyze_hotel_recommendations(self, hotels: List[Dict[str, Any]], 
                                          preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze hotels using rule-based logic"""
        
        budget = preferences.get('budget', 'comfort')
        interests = preferences.get('interests', [])
        
        for i, hotel in enumerate(hotels):
            price = hotel.get('price_per_night', 0)
            rating = hotel.get('rating', 0)
            amenities = hotel.get('amenities', [])
            
            ai_recommended = False
            reasoning = {}
            
            # Rating analysis
            if rating >= 4.5:
                reasoning['rating'] = "Excellent guest reviews and high ratings"
                ai_recommended = True
            elif rating >= 4.0:
                reasoning['rating'] = "Very good ratings from previous guests"
            else:
                reasoning['rating'] = "Good value option with decent ratings"
            
            # Location analysis
            reasoning['location'] = "Centrally located with easy access to attractions"
            
            # Amenities analysis
            amenity_labels = [a.get('label', '') for a in amenities]
            if 'Swimming Pool' in amenity_labels and 'Spa & Wellness' in amenity_labels:
                reasoning['amenities'] = "Excellent facilities for relaxation"
            elif 'Free WiFi' in amenity_labels and 'Restaurant' in amenity_labels:
                reasoning['amenities'] = "Essential amenities for comfortable stay"
            else:
                reasoning['amenities'] = "Good basic amenities provided"
            
            # Value analysis
            if budget == 'budget' and price < 3000:
                reasoning['value'] = "Excellent value for budget-conscious travelers"
                ai_recommended = True
            elif budget == 'comfort' and 3000 <= price <= 6000:
                reasoning['value'] = "Great balance of comfort and price"
                ai_recommended = True
            elif budget == 'luxury' and price > 5000:
                reasoning['value'] = "Premium experience with luxury amenities"
                ai_recommended = True
            else:
                reasoning['value'] = "Fair pricing for the facilities offered"
            
            hotel['ai_recommended'] = ai_recommended
            hotel['ai_reasoning'] = reasoning
        
        return hotels
    
    def _get_destination_activities(self, destination: str, interests: List[str]) -> Dict[str, List[str]]:
        """Get activities based on destination and interests"""
        
        activities_db = {
            "Mumbai": {
                "sightseeing": ["Gateway of India", "Marine Drive", "Elephanta Caves", "Chhatrapati Shivaji Terminus"],
                "food": ["Street food at Mohammed Ali Road", "Seafood at Koliwada", "Vada Pav tasting tour"],
                "culture": ["Bollywood studio tour", "Crawford Market", "Dhobi Ghat"],
                "beaches": ["Juhu Beach", "Versova Beach", "Aksa Beach"],
                "nightlife": ["Colaba Causeway", "Bandra bars", "Marine Drive evening walk"]
            },
            "Delhi": {
                "sightseeing": ["Red Fort", "India Gate", "Qutub Minar", "Lotus Temple"],
                "food": ["Chandni Chowk food walk", "Karim's for Mughlai", "Paranthe Wali Gali"],
                "culture": ["National Museum", "Humayun's Tomb", "Akshardham Temple"],
                "shopping": ["Connaught Place", "Khan Market", "Dilli Haat"],
                "heritage": ["Old Delhi heritage walk", "Raj Ghat", "Jama Masjid"]
            },
            "Goa": {
                "beaches": ["Baga Beach", "Calangute Beach", "Anjuna Beach", "Palolem Beach"],
                "nightlife": ["Tito's Club", "Club Cubana", "Beach shacks"],
                "culture": ["Basilica of Bom Jesus", "Se Cathedral", "Fontainhas heritage walk"],
                "adventure": ["Water sports", "Dudhsagar Falls", "Spice plantation tour"],
                "food": ["Goan fish curry", "Bebinca dessert", "Feni tasting"]
            },
            "Kolkata": {
                "culture": ["Victoria Memorial", "Howrah Bridge", "Kalighat Temple"],
                "food": ["Bengali sweets", "Fish market", "Street food tour"],
                "sightseeing": ["Indian Museum", "Dakshineswar Temple", "Park Street"],
                "heritage": ["College Street book market", "Kumartuli pottery", "Marble Palace"]
            }
        }
        
        # Default activities if destination not found
        default_activities = {
            "sightseeing": ["Local monuments", "City center", "Historical sites"],
            "culture": ["Local museums", "Traditional markets", "Religious sites"],
            "food": ["Local cuisine tasting", "Street food tour", "Traditional restaurants"],
            "adventure": ["Local adventures", "Nature walks", "Outdoor activities"]
        }
        
        return activities_db.get(destination, default_activities)
    
    def _generate_day_activities(self, day: int, destination: str, activities: Dict[str, List[str]], 
                               budget: str, is_first_day: bool, is_last_day: bool) -> Dict[str, Any]:
        """Generate activities for a specific day"""
        
        if is_first_day:
            title = "Arrival & Local Exploration"
            day_activities = [
                {"time": "10:00 AM", "icon": "✈️", "activity": "Arrive at destination", "duration": "1 hour", "cost": 0},
                {"time": "12:00 PM", "icon": "🏨", "activity": "Check-in to hotel", "duration": "1 hour", "cost": 0},
                {"time": "2:00 PM", "icon": "🍽️", "activity": "Local lunch", "duration": "1 hour", "cost": 500},
                {"time": "4:00 PM", "icon": "🏛️", "activity": f"Visit {random.choice(activities.get('sightseeing', ['local attractions']))}", "duration": "2 hours", "cost": 300},
                {"time": "7:00 PM", "icon": "🍛", "activity": "Dinner at local restaurant", "duration": "1.5 hours", "cost": 800}
            ]
        elif is_last_day:
            title = "Final Exploration & Departure"
            day_activities = [
                {"time": "9:00 AM", "icon": "🛍️", "activity": "Shopping for souvenirs", "duration": "2 hours", "cost": 1000},
                {"time": "12:00 PM", "icon": "🍽️", "activity": "Farewell lunch", "duration": "1 hour", "cost": 600},
                {"time": "2:00 PM", "icon": "🏨", "activity": "Check-out from hotel", "duration": "30 minutes", "cost": 0},
                {"time": "4:00 PM", "icon": "✈️", "activity": "Departure", "duration": "1 hour", "cost": 0}
            ]
        else:
            title = f"Explore {destination}"
            available_activities = []
            for category, acts in activities.items():
                available_activities.extend(acts)
            
            day_activities = [
                {"time": "9:00 AM", "icon": "🌅", "activity": f"Visit {random.choice(available_activities)}", "duration": "2 hours", "cost": 400},
                {"time": "12:00 PM", "icon": "🍽️", "activity": "Lunch break", "duration": "1 hour", "cost": 500},
                {"time": "2:00 PM", "icon": "🏛️", "activity": f"Explore {random.choice(available_activities)}", "duration": "3 hours", "cost": 600},
                {"time": "6:00 PM", "icon": "☕", "activity": "Evening tea/coffee", "duration": "30 minutes", "cost": 200},
                {"time": "8:00 PM", "icon": "🍛", "activity": "Dinner", "duration": "1.5 hours", "cost": 800}
            ]
        
        return {"title": title, "activities": day_activities}
    
    def _calculate_estimated_cost(self, daily_plans: List[Dict], budget: str, total_days: int) -> int:
        """Calculate estimated trip cost"""
        
        daily_cost = 0
        for day in daily_plans:
            for activity in day.get('activities', []):
                daily_cost += activity.get('cost', 0)
        
        # Add accommodation cost
        accommodation_cost = {
            'budget': 2000,
            'comfort': 4000,
            'luxury': 8000
        }.get(budget, 4000) * total_days
        
        return daily_cost + accommodation_cost
    
    def _extract_duration_hours(self, duration: str) -> float:
        """Extract hours from duration string"""
        try:
            if 'h' in duration:
                hours = float(duration.split('h')[0])
                if 'm' in duration:
                    minutes = float(duration.split('h')[1].replace('m', '').strip())
                    hours += minutes / 60
                return hours
        except:
            pass
        return 2.0  # Default
    
    def _get_planning_response(self, message: str, context: str) -> str:
        responses = [
            "I'd be happy to help you plan your trip! Tell me your destination, travel dates, and what interests you most.",
            "Planning a trip is exciting! Share your preferences and I'll create a personalized itinerary for you.",
            "Let's create an amazing travel experience! What destination are you considering?",
            "I can help you plan the perfect Indian adventure! Which cities or regions interest you?"
        ]
        return random.choice(responses)
    
    def _get_destination_response(self, message: str) -> str:
        responses = [
            "India offers incredible diversity! For beaches, try Goa or Kerala. For culture, Delhi and Rajasthan are amazing. For mountains, consider Himachal or Uttarakhand.",
            "Some must-visit destinations include: Mumbai for Bollywood, Agra for the Taj Mahal, Jaipur for palaces, and Kerala for backwaters.",
            "Popular destinations depend on your interests: Adventure seekers love Ladakh, food lovers enjoy Delhi, and beach lovers prefer Goa.",
            "Consider the Golden Triangle (Delhi-Agra-Jaipur) for first-time visitors, or explore South India for temples and cuisine."
        ]
        return random.choice(responses)
    
    def _get_budget_response(self, message: str) -> str:
        responses = [
            "Budget travel in India is very affordable! You can explore comfortably with ₹2000-3000 per day including accommodation, food, and local transport.",
            "For a comfortable trip, budget ₹4000-6000 per day. Luxury experiences start from ₹8000+ per day.",
            "India offers great value! Budget hotels cost ₹1000-2000, mid-range ₹3000-5000, and luxury ₹6000+ per night.",
            "Transportation is economical - trains and buses are budget-friendly, while flights offer convenience at higher costs."
        ]
        return random.choice(responses)
    
    def _get_food_response(self, message: str) -> str:
        responses = [
            "Indian cuisine is incredibly diverse! Try regional specialties like Rajasthani dal baati, Bengali fish curry, or South Indian dosas.",
            "Street food is a must-try! Visit local markets for chaat, vada pav, momos, and regional snacks. Always choose busy stalls for freshness.",
            "Each region has unique flavors: North India for rich curries, South for rice dishes, East for sweets, and West for seafood.",
            "Don't miss local specialties! Ask locals for recommendations and try traditional thalis for a complete meal experience."
        ]
        return random.choice(responses)
    
    def _get_transport_response(self, message: str) -> str:
        responses = [
            "Indian Railways is extensive and affordable! Book in advance for popular routes. Flights save time for long distances.",
            "For local transport, use app-based cabs, auto-rickshaws, or local buses. Metro systems in major cities are efficient.",
            "Domestic flights connect major cities quickly. Budget airlines offer competitive prices if booked in advance.",
            "Consider train journeys for the experience! AC classes offer comfort, while general coaches are budget-friendly."
        ]
        return random.choice(responses)
    
    def _get_weather_response(self, message: str) -> str:
        responses = [
            "India has diverse climates! October-March is ideal for most regions. Avoid monsoons (June-September) unless you enjoy rain.",
            "Winter (Dec-Feb) is perfect for North India and beaches. Summer (Mar-May) is hot but good for hill stations.",
            "Monsoon season brings lush greenery but can disrupt travel plans. Check regional weather patterns before planning.",
            "Best time varies by region: Rajasthan in winter, Kerala year-round, Himachal in summer, and Goa in winter."
        ]
        return random.choice(responses)
    
    def _get_default_response(self) -> str:
        responses = [
            "I'm here to help with your travel planning! Ask me about destinations, budgets, food, or anything travel-related.",
            "Feel free to ask about Indian destinations, travel tips, local culture, or planning advice!",
            "I can assist with itinerary planning, budget estimation, destination recommendations, and travel tips for India.",
            "What would you like to know about traveling in India? I'm here to help make your trip amazing!"
        ]
        return random.choice(responses)
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load response templates"""
        return {
            "greetings": ["Hello! Welcome to Raahi.ai", "Namaste! How can I help you today?"],
            "destinations": ["India has amazing destinations!", "Let me suggest some places..."],
            "planning": ["I'll help you plan the perfect trip!", "Let's create an amazing itinerary!"]
        }