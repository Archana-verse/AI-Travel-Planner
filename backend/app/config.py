from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./raahi.db"
    
    # AI Configuration
    GOOGLE_API_KEY: Optional[str] = None
    SERPAPI_KEY: Optional[str] = None
    
    # Agent Configuration
    MAX_RETRIES: int = 3
    AGENT_TIMEOUT: int = 60
    
    # External URLs
    SKYSCANNER_BASE_URL: str = "https://www.skyscanner.com"
    BOOKING_COM_BASE_URL: str = "https://www.booking.com"
    
    class Config:
        env_file = ".env"

settings = Settings()