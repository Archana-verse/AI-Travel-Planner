from crewai import Crew, Task
from app.crew.agents.planner_agent import get_planner_agent
from app.crew.agents.flight_agent import get_flight_agent
from app.crew.agents.hotel_agent import get_hotel_agent
from app.crew.agents.itinerary_agent import get_itinerary_agent

class CrewManager:
    def __init__(self):
        self.planner_agent = get_planner_agent()
        self.flight_agent = get_flight_agent()
        self.hotel_agent = get_hotel_agent()
        self.itinerary_agent = get_itinerary_agent()

    def run_crew(self, user_input: str):
        crew = Crew(
            agents=[
                self.planner_agent,
                self.flight_agent,
                self.hotel_agent,
                self.itinerary_agent
            ],
            tasks=[
                Task(
                    description="Understand the user's travel preferences: destinations, budget, dates, interests.",
                    expected_output="A summary of user's travel goals.",
                    agent=self.planner_agent
                ),
                Task(
                    description="Search for flights based on user's origin, destination, and travel dates.",
                    expected_output="List of 3–5 good flight options.",
                    agent=self.flight_agent
                ),
                Task(
                    description="Find hotels matching user's preferences and budget at destination.",
                    expected_output="Top 3 hotel options with price and rating.",
                    agent=self.hotel_agent
                ),
                Task(
                    description="Generate a complete itinerary for the trip, with activities and timing.",
                    expected_output="A structured day-wise itinerary (Morning, Afternoon, Evening).",
                    agent=self.itinerary_agent
                )
            ],
            verbose=True
        )
        return crew.run()
def run_itinerary_crew(user_input: str):
    manager = CrewManager()
    return manager.run_crew(user_input)
