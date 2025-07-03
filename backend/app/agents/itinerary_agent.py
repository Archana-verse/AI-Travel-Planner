import asyncio
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class ItineraryAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )
    
    async def create_itinerary(self, preferences: Dict[str, Any], flights: List[Dict], hotels: List[Dict]) -> Dict[str, Any]:
        """Create detailed itinerary using Gemini Pro"""
        
        try:
            # Calculate trip duration
            departure_date = preferences.get('departure_date')
            return_date = preferences.get('return_date')
            
            if departure_date and return_date:
                start = datetime.strptime(departure_date, '%Y-%m-%d')
                end = datetime.strptime(return_date, '%Y-%m-%d')
                total_days = (end - start).days
            else:
                total_days = 3  # Default for one-way trips
            
            destination = preferences.get('to_location')
            interests = preferences.get('interests', [])
            budget = preferences.get('budget', 'comfort')
            diet = preferences.get('diet', 'No restrictions')
            travelers = preferences.get('travelers', 'solo')
            
            # Create detailed prompt for Gemini
            prompt = f"""
            Create a detailed, day-by-day travel itinerary for {destination} in India.
            
            Trip Details:
            - Destination: {destination}
            - Duration: {total_days} days
            - Departure: {departure_date}
            - Return: {return_date}
            - Budget: {budget}
            - Travelers: {travelers}
            - Interests: {', '.join(interests)}
            - Dietary preferences: {diet}
            
            Available Context:
            - Top flights: {len(flights)} options available
            - Top hotels: {len(hotels)} options available
            
            Requirements:
            1. Create exactly {total_days} days of activities
            2. Include specific timings for each activity
            3. Consider local culture, festivals, and authentic experiences
            4. Include realistic costs in INR
            5. Factor in travel time between locations
            6. Suggest appropriate restaurants based on dietary preferences
            7. Include both popular attractions and hidden gems
            8. Consider the season and weather
            
            Return ONLY a valid JSON object with this exact structure:
            {{
                "title": "Trip title",
                "description": "Brief engaging description",
                "total_days": {total_days},
                "estimated_cost": 0,
                "daily_plans": [
                    {{
                        "day": 1,
                        "date": "{departure_date}",
                        "title": "Day title",
                        "activities": [
                            {{
                                "time": "09:00 AM",
                                "icon": "🏛️",
                                "activity": "Activity description",
                                "duration": "2 hours",
                                "cost": 500,
                                "description": "Detailed description with cultural context"
                            }}
                        ],
                        "estimated_cost": 2500
                    }}
                ],
                "ai_insights": {{
                    "best_time_to_visit": "Weather and season advice",
                    "cultural_tips": "Local customs and etiquette",
                    "local_cuisine": "Must-try dishes and restaurants",
                    "transportation": "Getting around recommendations",
                    "shopping": "Best places for shopping and souvenirs",
                    "safety_tips": "Important safety considerations"
                }}
            }}
            
            Make the itinerary authentic, culturally rich, and practically useful for travelers.
            """
            
            # Get response from Gemini
            response = await self.llm.ainvoke(prompt)
            response_text = response.content
            
            # Parse JSON response
            try:
                # Extract JSON from response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    itinerary_data = json.loads(json_str)
                    
                    # Validate and enhance the itinerary
                    return self._enhance_itinerary(itinerary_data, preferences)
                else:
                    raise ValueError("No valid JSON found in response")
                    
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                logger.error(f"Response text: {response_text}")
                return self._generate_fallback_itinerary(preferences, total_days)
            
        except Exception as e:
            logger.error(f"Error creating itinerary: {str(e)}")
            return self._generate_fallback_itinerary(preferences, total_days)
    
    def _enhance_itinerary(self, itinerary: Dict, preferences: Dict) -> Dict:
        """Enhance and validate the AI-generated itinerary"""
        
        # Ensure all required fields exist
        if not itinerary.get('daily_plans'):
            return self._generate_fallback_itinerary(preferences, itinerary.get('total_days', 3))
        
        # Add missing fields and validate structure
        enhanced_itinerary = {
            "title": itinerary.get('title', f"Amazing {preferences.get('to_location')} Journey"),
            "description": itinerary.get('description', f"Explore the best of {preferences.get('to_location')}"),
            "total_days": itinerary.get('total_days', len(itinerary.get('daily_plans', []))),
            "estimated_cost": 0,
            "daily_plans": [],
            "ai_insights": itinerary.get('ai_insights', {})
        }
        
        total_cost = 0
        departure_date = preferences.get('departure_date', '2024-01-01')
        
        for i, day_plan in enumerate(itinerary.get('daily_plans', [])):
            # Calculate date for this day
            current_date = datetime.strptime(departure_date, '%Y-%m-%d') + timedelta(days=i)
            
            # Ensure day activities have proper structure
            activities = []
            day_cost = 0
            
            for activity in day_plan.get('activities', []):
                enhanced_activity = {
                    "time": activity.get('time', '09:00 AM'),
                    "icon": activity.get('icon', '📍'),
                    "activity": activity.get('activity', 'Local exploration'),
                    "duration": activity.get('duration', '1 hour'),
                    "cost": activity.get('cost', 0),
                    "description": activity.get('description', '')
                }
                activities.append(enhanced_activity)
                day_cost += enhanced_activity['cost']
            
            enhanced_day = {
                "day": i + 1,
                "date": current_date.strftime('%Y-%m-%d'),
                "title": day_plan.get('title', f"Day {i + 1} Exploration"),
                "activities": activities,
                "estimated_cost": day_cost
            }
            
            enhanced_itinerary['daily_plans'].append(enhanced_day)
            total_cost += day_cost
        
        enhanced_itinerary['estimated_cost'] = total_cost
        
        return enhanced_itinerary
    
    def _generate_fallback_itinerary(self, preferences: Dict, total_days: int) -> Dict:
        """Generate fallback itinerary when AI fails"""
        
        destination = preferences.get('to_location', 'Mumbai')
        departure_date = preferences.get('departure_date', '2024-01-01')
        interests = preferences.get('interests', [])
        
        # Destination-specific activities
        city_activities = self._get_city_activities(destination, interests)
        
        daily_plans = []
        total_cost = 0
        
        for day in range(total_days):
            current_date = datetime.strptime(departure_date, '%Y-%m-%d') + timedelta(days=day)
            
            if day == 0:
                # Arrival day
                activities = [
                    {
                        "time": "10:00 AM",
                        "icon": "✈️",
                        "activity": "Arrive at destination",
                        "duration": "1 hour",
                        "cost": 0,
                        "description": "Airport arrival and transfer"
                    },
                    {
                        "time": "12:00 PM",
                        "icon": "🏨",
                        "activity": "Check-in to hotel",
                        "duration": "1 hour",
                        "cost": 0,
                        "description": "Hotel check-in and rest"
                    },
                    {
                        "time": "2:00 PM",
                        "icon": "🍽️",
                        "activity": "Local lunch",
                        "duration": "1 hour",
                        "cost": 500,
                        "description": "Experience local cuisine"
                    },
                    {
                        "time": "4:00 PM",
                        "icon": "🏛️",
                        "activity": city_activities[0],
                        "duration": "2 hours",
                        "cost": 300,
                        "description": "Begin exploration of the city"
                    },
                    {
                        "time": "7:00 PM",
                        "icon": "🍛",
                        "activity": "Dinner at local restaurant",
                        "duration": "1 hour",
                        "cost": 800,
                        "description": "Traditional dinner experience"
                    }
                ]
                title = "Arrival & First Impressions"
                
            elif day == total_days - 1:
                # Departure day
                activities = [
                    {
                        "time": "9:00 AM",
                        "icon": "🛍️",
                        "activity": "Shopping for souvenirs",
                        "duration": "2 hours",
                        "cost": 1000,
                        "description": "Last-minute shopping"
                    },
                    {
                        "time": "12:00 PM",
                        "icon": "🍽️",
                        "activity": "Farewell lunch",
                        "duration": "1 hour",
                        "cost": 600,
                        "description": "Final meal in the city"
                    },
                    {
                        "time": "2:00 PM",
                        "icon": "🏨",
                        "activity": "Check-out from hotel",
                        "duration": "30 minutes",
                        "cost": 0,
                        "description": "Hotel check-out"
                    },
                    {
                        "time": "4:00 PM",
                        "icon": "✈️",
                        "activity": "Departure",
                        "duration": "1 hour",
                        "cost": 0,
                        "description": "Journey back home"
                    }
                ]
                title = "Final Exploration & Departure"
                
            else:
                # Regular exploration days
                activity_idx = (day - 1) % len(city_activities)
                activities = [
                    {
                        "time": "9:00 AM",
                        "icon": "🌅",
                        "activity": city_activities[activity_idx],
                        "duration": "3 hours",
                        "cost": 500,
                        "description": "Morning exploration"
                    },
                    {
                        "time": "12:30 PM",
                        "icon": "🍽️",
                        "activity": "Lunch break",
                        "duration": "1 hour",
                        "cost": 500,
                        "description": "Midday meal"
                    },
                    {
                        "time": "2:00 PM",
                        "icon": "🏛️",
                        "activity": city_activities[(activity_idx + 1) % len(city_activities)],
                        "duration": "3 hours",
                        "cost": 600,
                        "description": "Afternoon sightseeing"
                    },
                    {
                        "time": "6:00 PM",
                        "icon": "☕",
                        "activity": "Evening tea/coffee",
                        "duration": "30 minutes",
                        "cost": 200,
                        "description": "Relaxing break"
                    },
                    {
                        "time": "8:00 PM",
                        "icon": "🍛",
                        "activity": "Dinner",
                        "duration": "1 hour",
                        "cost": 800,
                        "description": "Evening dining experience"
                    }
                ]
                title = f"Explore {destination}"
            
            day_cost = sum(activity['cost'] for activity in activities)
            
            daily_plans.append({
                "day": day + 1,
                "date": current_date.strftime('%Y-%m-%d'),
                "title": title,
                "activities": activities,
                "estimated_cost": day_cost
            })
            
            total_cost += day_cost
        
        return {
            "title": f"Amazing {total_days}-Day {destination} Adventure",
            "description": f"Discover the best of {destination} with this carefully crafted itinerary",
            "total_days": total_days,
            "estimated_cost": total_cost,
            "daily_plans": daily_plans,
            "ai_insights": {
                "best_time_to_visit": "October to March for pleasant weather",
                "cultural_tips": "Respect local customs and dress modestly at religious sites",
                "local_cuisine": "Try authentic local dishes and street food",
                "transportation": "Use local transport like auto-rickshaws and buses",
                "shopping": "Visit local markets for handicrafts and souvenirs",
                "safety_tips": "Keep valuables secure and stay hydrated"
            }
        }
    
    def _get_city_activities(self, city: str, interests: List[str]) -> List[str]:
        """Get city-specific activities based on interests"""
        
        city_activities = {
            'Mumbai': [
                'Visit Gateway of India',
                'Explore Elephanta Caves',
                'Walk along Marine Drive',
                'Experience Bollywood studio tour',
                'Visit Crawford Market',
                'Explore Dharavi slum tour',
                'Enjoy street food at Mohammed Ali Road'
            ],
            'Delhi': [
                'Visit Red Fort',
                'Explore India Gate',
                'Tour Qutub Minar',
                'Visit Lotus Temple',
                'Explore Chandni Chowk',
                'Visit Humayun\'s Tomb',
                'Experience Old Delhi heritage walk'
            ],
            'Kolkata': [
                'Visit Victoria Memorial',
                'Explore Howrah Bridge',
                'Tour Indian Museum',
                'Visit Kalighat Temple',
                'Explore College Street',
                'Experience Kumartuli pottery quarter',
                'Visit Dakshineswar Temple'
            ],
            'Goa': [
                'Relax at Baga Beach',
                'Visit Basilica of Bom Jesus',
                'Explore Anjuna Flea Market',
                'Tour spice plantations',
                'Experience water sports',
                'Visit Dudhsagar Falls',
                'Explore Fontainhas heritage area'
            ],
            'Chennai': [
                'Visit Marina Beach',
                'Explore Kapaleeshwarar Temple',
                'Tour Fort St. George',
                'Visit Government Museum',
                'Explore Mylapore neighborhood',
                'Experience classical music and dance',
                'Visit DakshinaChitra cultural center'
            ]
        }
        
        default_activities = [
            'Visit local monuments',
            'Explore city center',
            'Experience local markets',
            'Try regional cuisine',
            'Visit museums',
            'Enjoy cultural performances',
            'Shop for local crafts'
        ]
        
        return city_activities.get(city, default_activities)