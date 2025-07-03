from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./raahi.db"
    
    # Free alternatives
    OPENAI_API_KEY: Optional[str] = None
    USE_MOCK_DATA: bool = True
    ENABLE_WEB_SCRAPING: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()