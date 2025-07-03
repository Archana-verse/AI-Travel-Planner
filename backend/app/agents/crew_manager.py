from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.itinerary_agent import ItineraryAgent
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TravelPlannerCrew:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )
        
        self.flight_agent_instance = FlightAgent()
        self.hotel_agent_instance = HotelAgent()
        self.itinerary_agent_instance = ItineraryAgent()
        
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup CrewAI agents with specific roles and tools"""
        
        # Flight Search Agent
        self.flight_agent = Agent(
            role="Flight Search Specialist",
            goal="Find the best flight options based on user preferences and budget",
            backstory="""You are an expert flight search specialist with deep knowledge of 
            airline routes, pricing patterns, and travel optimization. You excel at finding 
            flights that balance cost, convenience, and user preferences.""",
            llm=self.llm,
            tools=[],
            verbose=True,
            allow_delegation=False
        )
        
        # Hotel Search Agent
        self.hotel_agent = Agent(
            role="Hotel Search Specialist", 
            goal="Find perfect accommodation options matching user preferences and location",
            backstory="""You are a hospitality expert with extensive knowledge of hotels, 
            guest houses, and accommodation options across India. You understand traveler 
            needs and can match them with the perfect stay.""",
            llm=self.llm,
            tools=[],
            verbose=True,
            allow_delegation=False
        )
        
        # Itinerary Planning Agent
        self.itinerary_agent = Agent(
            role="Travel Itinerary Planner",
            goal="Create detailed, personalized day-by-day travel itineraries",
            backstory="""You are a seasoned travel planner with deep cultural knowledge 
            of Indian destinations. You create immersive, authentic travel experiences 
            that respect local culture while maximizing traveler satisfaction.""",
            llm=self.llm,
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    async def plan_complete_trip(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the complete trip planning process"""
        
        try:
            logger.info(f"Starting trip planning for: {preferences.get('to_location')}")
            
            # Task 1: Search Flights
            flight_task = Task(
                description=f"""
                Search for flights from {preferences.get('from_location')} to {preferences.get('to_location')}
                - Departure: {preferences.get('departure_date')}
                - Return: {preferences.get('return_date', 'One way')}
                - Class: {preferences.get('travel_class')}
                - Budget: {preferences.get('budget')}
                - Travelers: {preferences.get('travelers')}
                
                Provide 3-5 best options with detailed reasoning for recommendations.
                """,
                agent=self.flight_agent,
                expected_output="List of flight options with prices, timings, and AI recommendations"
            )
            
            # Task 2: Search Hotels
            hotel_task = Task(
                description=f"""
                Find hotels in {preferences.get('to_location')}
                - Check-in: {preferences.get('departure_date')}
                - Check-out: {preferences.get('return_date', 'TBD')}
                - Budget: {preferences.get('budget')}
                - Travelers: {preferences.get('travelers')}
                - Interests: {preferences.get('interests', [])}
                
                Provide 3-5 best accommodation options with detailed analysis.
                """,
                agent=self.hotel_agent,
                expected_output="List of hotel options with amenities, pricing, and recommendations"
            )
            
            # Task 3: Create Itinerary
            itinerary_task = Task(
                description=f"""
                Create a detailed day-by-day itinerary for {preferences.get('to_location')}
                - Duration: {preferences.get('departure_date')} to {preferences.get('return_date', 'TBD')}
                - Interests: {preferences.get('interests', [])}
                - Diet: {preferences.get('diet', 'No restrictions')}
                - Budget: {preferences.get('budget')}
                - Travelers: {preferences.get('travelers')}
                
                Include specific timings, activities, costs, and cultural insights.
                Consider local festivals, weather, and authentic experiences.
                """,
                agent=self.itinerary_agent,
                expected_output="Complete day-wise itinerary with activities, timings, and costs",
                dependencies=[flight_task, hotel_task]
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[self.flight_agent, self.hotel_agent, self.itinerary_agent],
                tasks=[flight_task, hotel_task, itinerary_task],
                verbose=True
            )
            
            # Execute the crew and get results
            crew_result = crew.kickoff()
            
            # Process individual agent results
            flights = await self.flight_agent_instance.search_flights(preferences)
            hotels = await self.hotel_agent_instance.search_hotels(preferences)
            itinerary = await self.itinerary_agent_instance.create_itinerary(preferences, flights, hotels)
            
            return {
                "flights": flights,
                "hotels": hotels,
                "itinerary": itinerary,
                "crew_output": str(crew_result),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in trip planning: {str(e)}")
            raise Exception(f"Trip planning failed: {str(e)}")
    
    async def enhance_with_chat(self, message: str, context: Dict[str, Any]) -> str:
        """Use CrewAI for intelligent chat responses with travel context"""
        
        chat_agent = Agent(
            role="Travel Assistant",
            goal="Provide helpful, contextual travel advice and answer user questions",
            backstory="""You are Raahi, an expert AI travel assistant for India. You have 
            deep knowledge of Indian destinations, culture, food, transportation, and travel 
            logistics. You provide practical, culturally-aware advice.""",
            llm=self.llm,
            verbose=False
        )
        
        chat_task = Task(
            description=f"""
            User message: {message}
            
            Travel context: {context}
            
            Provide a helpful, informative response. Be conversational but informative.
            If the context includes trip details, reference them appropriately.
            """,
            agent=chat_agent,
            expected_output="Helpful travel advice response"
        )
        
        chat_crew = Crew(
            agents=[chat_agent],
            tasks=[chat_task],
            verbose=False
        )
        
        result = chat_crew.kickoff()
        return str(result)