from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_gemini_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_gemini(request: ChatRequest):
    response = generate_gemini_response(request.query)
    return {"response": response}