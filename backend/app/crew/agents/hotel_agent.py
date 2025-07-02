# app/crew/agents/hotel_agent.py

from crewai import Agent

def get_hotel_agent():
    return Agent(
        name="Hotel Recommender Agent",
        role="Hotel researcher",
        goal="Find hotels that match user preferences, budget, and location.",
        backstory="A specialist at finding the best stays using online sources via SerpAPI.",
        verbose=True,
        allow_delegation=False
    )
