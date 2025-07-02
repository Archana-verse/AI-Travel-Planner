# app/crew/agents/planner_agent.py

from crewai import Agent

def get_planner_agent():
    return Agent(
        name="Planner Agent",
        role="Travel Planner",
        goal="Collect and understand the user's travel preferences to initiate trip planning.",
        backstory="An expert travel consultant that understands user goals and sets up planning context for the crew.",
        verbose=True,
        allow_delegation=True
    )
