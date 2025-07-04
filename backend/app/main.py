from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables

# Future route imports (to be added step-by-step)
from app.routes.plan import router as plan_router  # <-- Add this import

app = FastAPI(title="Raahi.ai - AI Travel Planner")

# CORS (allow frontend on localhost or your deployed domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(plan_router)  

@app.get("/api/health")
def health_check():
    return {"status": "Raahi.ai backend is running 🚀"}
