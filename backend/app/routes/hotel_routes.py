from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from app.services.hotel_ranking_service import get_ranked_hotels_from_iata

router = APIRouter()


class HotelRecommendationRequest(BaseModel):
    to: str
    departureDate: str
    returnDate: str
    budget: str
    travelers: str
    interests: List[str]
    diet: str


def extract_budget_value(budget_str: str) -> int:
    if "₹0" in budget_str:
        return 25000
    elif "₹25,000" in budget_str:
        return 60000
    else:
        return 100000


def extract_travelers_value(travelers_str: str) -> int:
    mapping = {
        "Solo": 1,
        "Couple": 2,
        "Family": 3,
        "Friends": 4
    }
    return mapping.get(travelers_str, 1)


@router.post("/recommend/hotels")
def recommend_hotels(preferences: HotelRecommendationRequest) -> Dict[str, Any]:
    budget_limit = extract_budget_value(preferences.budget)
    num_travelers = extract_travelers_value(preferences.travelers)

    print(f"🔍 Getting hotels for: {preferences.to}, ₹{budget_limit}, {num_travelers} travelers")
    prefs_dict = preferences.dict()
    prefs_dict["budget_range"] = f"₹{budget_limit}"
    prefs_dict["travelers"] = num_travelers
    prefs_dict["dietary_pref"] = prefs_dict.pop("diet")

    hotels = get_ranked_hotels_from_iata(
        iata_code=preferences.to,
        checkin_date=preferences.departureDate,
        checkout_date=preferences.returnDate,
        preferences=prefs_dict
    )

    return {"recommendations": hotels}
