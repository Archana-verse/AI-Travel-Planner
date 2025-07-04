from app.services.serpapi_service import search_flights
from app.services.gemini_service import get_best_flight_reason

class FlightAgent:
    def __init__(self, plan):
        self.plan = plan

    def get_flights(self):
        flights = search_flights(
            origin=self.plan.source,
            destination=self.plan.destination,
            departure_date=self.plan.departure_date,
            return_date=self.plan.return_date,
            travel_class=self.plan.travel_class
        )

        # Fallback if no flights found
        if not flights:
            return [{
                "airline": "IndiGo",
                "price": "₹5000",
                "recommended": True,
                "reason": "Default flight"
            }]

        # Get best recommendation using Gemini
        recommended, reason = get_best_flight_reason(flights, self.plan)
        for f in flights:
            f["recommended"] = (f == recommended)
            if f["recommended"]:
                f["reason"] = reason
        return flights
