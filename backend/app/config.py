import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
