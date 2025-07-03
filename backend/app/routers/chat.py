from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.models import ChatMessage, TravelSession
from app.services.gemini_service import GeminiService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI travel assistant"""
    
    try:
        gemini = GeminiService()
        
        # Build context from session if provided
        context = ""
        if request.session_id:
            session = db.query(TravelSession).filter(TravelSession.id == request.session_id).first()
            if session and session.user_preferences:
                prefs = session.user_preferences
                context = f"""
                User's current trip context:
                - Destination: {prefs.get('to_location', 'Not specified')}
                - Travel dates: {prefs.get('departure_date', 'Not specified')}
                - Budget: {prefs.get('budget', 'Not specified')}
                - Travelers: {prefs.get('travelers', 'Not specified')}
                - Interests: {', '.join(prefs.get('interests', []))}
                """
        
        # Generate AI response
        ai_response = await gemini.chat_response(request.message, context)
        
        # Save chat message
        chat_message = ChatMessage(
            session_id=request.session_id,
            message=request.message,
            response=ai_response
        )
        db.add(chat_message)
        db.commit()
        
        return ChatResponse(
            response=ai_response,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")