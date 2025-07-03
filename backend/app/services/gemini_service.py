import vertexai
from vertexai.generative_models import GenerativeModel, Part
from typing import Dict, Any, List
from app.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GEMINI_LOCATION)
        self.model = GenerativeModel(settings.GEMINI_MODEL)
    
    async def generate_itinerary(self, preferences: Dict[str, Any], 
                               flights: List[Dict[str, Any]], 
                               hotels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed itinerary using Gemini"""
        
        prompt = f"""
        You are an expert travel planner for India. Create a detailed, day-wise itinerary based on:
        
        TRAVEL PREFERENCES:
        - Destination: {preferences.get('to_location')}
        - Duration: {preferences.get('departure_date')} to {preferences.get('return_date', 'TBD')}
        - Budget: {preferences.get('budget')}
        - Travelers: {preferences.get('travelers')}
        - Interests: {', '.join(preferences.get('interests', []))}
        - Diet: {preferences.get('diet', 'No restrictions')}
        
        AVAILABLE OPTIONS:
        - Flights: {len(flights)} options available
        - Hotels: {len(hotels)} options available
        
        Create a JSON response with this exact structure:
        {{
            "title": "Trip title",
            "description": "Brief trip overview",
            "total_days": number,
            "estimated_cost": number,
            "daily_plans": [
                {{
                    "day": 1,
                    "date": "YYYY-MM-DD",
                    "title": "Day title",
                    "activities": [
                        {{
                            "time": "HH:MM AM/PM",
                            "icon": "emoji",
                            "activity": "Activity description",
                            "duration": "X hours",
                            "cost": number
                        }}
                    ]
                }}
            ]
        }}
        
        Requirements:
        - Include authentic local experiences and cultural activities
        - Consider dietary preferences for restaurant recommendations
        - Include realistic timing and costs in INR
        - Add travel time between activities
        - Include both popular attractions and hidden gems
        - Ensure activities match the stated interests
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                itinerary_data = json.loads(json_str)
                return itinerary_data
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            # Return fallback itinerary
            return self._get_fallback_itinerary(preferences)
    
    async def chat_response(self, message: str, context: str = "") -> str:
        """Generate chat response using Gemini"""
        
        prompt = f"""
        You are Raahi, an expert AI travel assistant for India. You help travelers plan amazing trips across India.
        
        Context: {context}
        
        User Message: {message}
        
        Respond as a helpful, knowledgeable travel expert. Provide specific, actionable advice about:
        - Destinations and attractions
        - Local culture and customs
        - Food recommendations
        - Transportation options
        - Budget planning
        - Best times to visit
        - Safety tips
        
        Keep responses conversational, informative, and focused on Indian travel.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
    
    async def analyze_flight_recommendations(self, flights: List[Dict[str, Any]], 
                                           preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use Gemini to analyze and recommend flights"""
        
        prompt = f"""
        Analyze these flight options for a trip from {preferences.get('from_location')} to {preferences.get('to_location')}:
        
        Budget: {preferences.get('budget')}
        Travel Class: {preferences.get('travel_class')}
        
        Flight Options:
        {json.dumps(flights[:5], indent=2)}
        
        For each flight, provide AI reasoning in this format:
        {{
            "flight_index": 0,
            "ai_recommended": true/false,
            "reasoning": {{
                "price": "Price analysis",
                "duration": "Duration analysis", 
                "airline": "Airline quality analysis",
                "departure": "Departure time analysis"
            }}
        }}
        
        Return a JSON array with analysis for each flight.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
                
                # Apply analysis to flights
                for i, flight_analysis in enumerate(analysis):
                    if i < len(flights):
                        flights[i]['ai_recommended'] = flight_analysis.get('ai_recommended', False)
                        flights[i]['ai_reasoning'] = flight_analysis.get('reasoning', {})
                
                return flights
            
        except Exception as e:
            logger.error(f"Error analyzing flights: {str(e)}")
        
        return flights
    
    async def analyze_hotel_recommendations(self, hotels: List[Dict[str, Any]], 
                                          preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use Gemini to analyze and recommend hotels"""
        
        prompt = f"""
        Analyze these hotel options for {preferences.get('to_location')}:
        
        Budget: {preferences.get('budget')}
        Travelers: {preferences.get('travelers')}
        Interests: {', '.join(preferences.get('interests', []))}
        
        Hotel Options:
        {json.dumps(hotels[:5], indent=2)}
        
        For each hotel, provide AI reasoning in this format:
        {{
            "hotel_index": 0,
            "ai_recommended": true/false,
            "reasoning": {{
                "rating": "Rating analysis",
                "location": "Location analysis",
                "amenities": "Amenities analysis",
                "value": "Value for money analysis"
            }}
        }}
        
        Return a JSON array with analysis for each hotel.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
                
                # Apply analysis to hotels
                for i, hotel_analysis in enumerate(analysis):
                    if i < len(hotels):
                        hotels[i]['ai_recommended'] = hotel_analysis.get('ai_recommended', False)
                        hotels[i]['ai_reasoning'] = hotel_analysis.get('reasoning', {})
                
                return hotels
            
        except Exception as e:
            logger.error(f"Error analyzing hotels: {str(e)}")
        
        return hotels
    
    def _get_fallback_itinerary(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback itinerary if Gemini fails"""
        return {
            "title": f"Explore {preferences.get('to_location')}",
            "description": f"A wonderful journey to {preferences.get('to_location')}",
            "total_days": 3,
            "estimated_cost": 15000,
            "daily_plans": [
                {
                    "day": 1,
                    "date": preferences.get('departure_date'),
                    "title": "Arrival and Local Exploration",
                    "activities": [
                        {
                            "time": "10:00 AM",
                            "icon": "✈️",
                            "activity": "Arrive at destination",
                            "duration": "1 hour",
                            "cost": 0
                        },
                        {
                            "time": "2:00 PM",
                            "icon": "🏛️",
                            "activity": "Visit local attractions",
                            "duration": "3 hours",
                            "cost": 500
                        }
                    ]
                }
            ]
        }