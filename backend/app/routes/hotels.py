from fastapi import APIRouter
from app.services.serpapi_service import search_hotels

router = APIRouter()

@router.get("/")
def get_hotels(location: str):
    return search_hotels(location)
