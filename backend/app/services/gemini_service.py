from app.config import settings
import google.generativeai as genai
from app.schemas.plan import PlanRequest

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_plan(request: PlanRequest):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Generate a travel plan for: {request.destination} for {request.days} days. Interests: {', '.join(request.interests)}"
    response = model.generate_content(prompt)
    return {"plan": response.text}
