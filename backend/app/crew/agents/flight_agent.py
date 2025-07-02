# app/crew/agents/flight_agent.py

from crewai import Agent

def get_flight_agent():
    return Agent(
        name="Flight Search Agent",
        role="Flight researcher",
        goal="Find and suggest the best flights based on user's origin, destination, and travel dates.",
        backstory="Expert in using flight search engines and APIs like SerpAPI to get flight options.",
        verbose=True,
        allow_delegation=False
    )
