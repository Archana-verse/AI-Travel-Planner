from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.plan import router as plan_router
from dotenv import load_dotenv
import os

# ✅ Load .env variables
load_dotenv()  # Looks for .env in current directory

# ✅ Print keys to confirm
print("🔑 SERPAPI_API_KEY loaded:", os.getenv("SERPAPI_API_KEY")[:8], "********")
print("🔑 GEMINIAPI_KEY loaded:", os.getenv("GEMINIAPI_KEY")[:8], "********")

app = FastAPI()

# ✅ CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all backend routes under /api
app.include_router(plan_router, prefix="/api")
