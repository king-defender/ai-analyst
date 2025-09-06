from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Analyst API"
    DEBUG: bool = True  # Default to True for development
    ENVIRONMENT: str = "development"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"]

    # API Host and Port (for Docker Compose compatibility)
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    GCS_BUCKET_NAME: str = ""
    VERTEX_AI_LOCATION: str = "us-central1"
    BIGQUERY_DATASET: str = "ai_analyst_benchmarks"
    
    # Database
    FIRESTORE_DATABASE: str = "(default)"
    
    # Authentication
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()