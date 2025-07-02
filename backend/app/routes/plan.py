from fastapi import APIRouter
from app.services.gemini_service import generate_plan
from app.schemas.plan import PlanRequest

router = APIRouter()

@router.post("/")
def create_plan(request: PlanRequest):
    return generate_plan(request)
