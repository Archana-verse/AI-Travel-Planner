from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.models import ChatMessage, TravelSession
from app.agents.crew_manager import TravelPlannerCrew
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI travel assistant using Gemini Pro"""
    
    try:
        # Build context from session if provided
        context = {}
        session = None
        
        if request.session_id:
            session = db.query(TravelSession).filter(TravelSession.id == request.session_id).first()
            if session and session.user_preferences:
                context = {
                    "destination": session.user_preferences.get('to_location'),
                    "departure_date": session.user_preferences.get('departure_date'),
                    "return_date": session.user_preferences.get('return_date'),
                    "budget": session.user_preferences.get('budget'),
                    "travelers": session.user_preferences.get('travelers'),
                    "interests": session.user_preferences.get('interests', []),
                    "diet": session.user_preferences.get('diet')
                }
        
        # Use CrewAI for enhanced chat response
        crew_manager = TravelPlannerCrew()
        ai_response = await crew_manager.enhance_with_chat(request.message, context)
        
        # Generate suggestions based on message type and context
        suggestions = _generate_suggestions(request.message, context)
        
        # Save chat message
        chat_message = ChatMessage(
            session_id=request.session_id,
            message=request.message,
            response=ai_response,
            message_type=request.message_type
        )
        db.add(chat_message)
        db.commit()
        
        return ChatResponse(
            response=ai_response,
            session_id=request.session_id,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        
        # Fallback response using direct Gemini
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7
            )
            
            fallback_prompt = f"""
            You are Raahi, an expert AI travel assistant for India. 
            
            User question: {request.message}
            
            Context: {context if context else 'No specific trip context'}
            
            Provide a helpful, informative response about travel in India. 
            Be conversational but knowledgeable about Indian destinations, culture, food, and travel logistics.
            """
            
            response = await llm.ainvoke(fallback_prompt)
            ai_response = response.content
            
            # Save fallback response
            chat_message = ChatMessage(
                session_id=request.session_id,
                message=request.message,
                response=ai_response,
                message_type=request.message_type
            )
            db.add(chat_message)
            db.commit()
            
            return ChatResponse(
                response=ai_response,
                session_id=request.session_id,
                suggestions=_generate_suggestions(request.message, context)
            )
            
        except Exception as fallback_error:
            logger.error(f"Fallback chat also failed: {str(fallback_error)}")
            
            # Final fallback with rule-based response
            fallback_response = _get_rule_based_response(request.message, context)
            
            return ChatResponse(
                response=fallback_response,
                session_id=request.session_id,
                suggestions=[]
            )

def _generate_suggestions(message: str, context: dict) -> list:
    """Generate contextual suggestions for follow-up questions"""
    
    message_lower = message.lower()
    suggestions = []
    
    # General travel suggestions
    if any(word in message_lower for word in ['destination', 'place', 'visit', 'go']):
        suggestions.extend([
            "What's the best time to visit this destination?",
            "What are the must-try local dishes?",
            "How many days should I plan for this trip?"
        ])
    
    # Budget-related suggestions
    elif any(word in message_lower for word in ['budget', 'cost', 'price', 'money']):
        suggestions.extend([
            "What are some budget-friendly accommodation options?",
            "How can I save money on local transportation?",
            "What are the typical costs for meals?"
        ])
    
    # Food-related suggestions
    elif any(word in message_lower for word in ['food', 'eat', 'restaurant', 'cuisine']):
        suggestions.extend([
            "What are some must-try street foods?",
            "Which restaurants do locals recommend?",
            "Are there good vegetarian options?"
        ])
    
    # Transportation suggestions
    elif any(word in message_lower for word in ['transport', 'travel', 'flight', 'train']):
        suggestions.extend([
            "What's the best way to get around locally?",
            "Are there any travel passes available?",
            "How far in advance should I book?"
        ])
    
    # Context-based suggestions
    if context.get('destination'):
        destination = context['destination']
        suggestions.extend([
            f"What are the top attractions in {destination}?",
            f"What's the weather like in {destination}?",
            f"Are there any festivals happening in {destination}?"
        ])
    
    # Remove duplicates and limit to 3
    unique_suggestions = list(dict.fromkeys(suggestions))
    return unique_suggestions[:3]

def _get_rule_based_response(message: str, context: dict) -> str:
    """Generate rule-based response as final fallback"""
    
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'namaste', 'hey']):
        return "Namaste! I'm Raahi, your AI travel assistant. I'm here to help you plan an amazing journey through India. What would you like to know about your trip?"
    
    # Destination questions
    elif any(word in message_lower for word in ['where', 'destination', 'place']):
        if context.get('destination'):
            return f"You're planning to visit {context['destination']}! It's a wonderful destination with rich culture and amazing experiences. Would you like specific recommendations for attractions, food, or activities?"
        else:
            return "India offers incredible diversity! Popular destinations include Mumbai for Bollywood, Delhi for history, Goa for beaches, Kerala for backwaters, and Rajasthan for palaces. What type of experience are you looking for?"
    
    # Budget questions
    elif any(word in message_lower for word in ['budget', 'cost', 'price']):
        return "India offers great value for travelers! Budget-friendly trips can be done for ₹2,000-3,000 per day, while comfortable travel costs ₹4,000-6,000 per day. Luxury experiences start from ₹8,000+ per day. What's your budget range?"
    
    # Food questions
    elif any(word in message_lower for word in ['food', 'eat', 'cuisine']):
        return "Indian cuisine is incredibly diverse! Each region has unique flavors. Don't miss trying local street food, traditional thalis, and regional specialties. Always choose busy food stalls for the freshest options. Any specific dietary preferences?"
    
    # Transportation questions
    elif any(word in message_lower for word in ['transport', 'travel', 'how to reach']):
        return "India has excellent connectivity! Trains are affordable and extensive, flights save time for long distances, and local transport includes auto-rickshaws, buses, and metro systems in major cities. What route are you planning?"
    
    # Weather questions
    elif any(word in message_lower for word in ['weather', 'climate', 'season']):
        return "India has diverse climates! Generally, October to March is ideal for most regions. Avoid monsoons (June-September) unless you enjoy rain. Hill stations are great in summer, while winter is perfect for beaches and northern India."
    
    # Default response
    else:
        return "I'm here to help with your India travel plans! I can assist with destinations, budgets, food recommendations, transportation, weather advice, and cultural tips. What specific aspect of your trip would you like to discuss?"