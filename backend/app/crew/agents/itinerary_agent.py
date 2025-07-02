# app/crew/agents/itinerary_agent.py

from crewai import Agent

def get_itinerary_agent():
    return Agent(
        name="Itinerary Creator Agent",
        role="Trip planner",
        goal="Create a detailed, enjoyable, and balanced day-by-day itinerary for the user.",
        backstory="You specialize in creating dynamic and AI-personalized travel itineraries using Gemini LLM.",
        verbose=True,
        allow_delegation=False
    )
