from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./raahi.db"
    
    # External APIs
    SERPAPI_KEY: str
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # Gemini Configuration
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_LOCATION: str = "us-central1"
    
    class Config:
        env_file = ".env"

settings = Settings()