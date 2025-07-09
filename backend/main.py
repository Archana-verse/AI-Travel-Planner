from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.plan import router as plan_router
from app.routes.redirect import router as redirect_router
from app.routes.itinerary import router as itinerary_router
from app.routes import chat
from dotenv import load_dotenv
import os

load_dotenv()
serp_key = os.getenv("SERPAPI_API_KEY", "")
gemini_key = os.getenv("GEMINIAPI_KEY", "")

print("SERPAPI_API_KEY loaded:", serp_key[:8] + "********" if serp_key else "❌ Not Found")
print("GEMINIAPI_KEY loaded:", gemini_key[:8] + "********" if gemini_key else "❌ Not Found")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_router, prefix="/api")
app.include_router(redirect_router, prefix="/api")
app.include_router(itinerary_router)
app.include_router(chat.router, prefix="/api")