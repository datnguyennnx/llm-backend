from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Content Store API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str
    
    # Vector settings
    OPENAI_API_KEY: str
    DIFY_API_KEY: str
    VECTOR_DIMENSION: int = 1536
    BATCH_SIZE: int = 100

    # CORS settings
    ALLOWED_ORIGINS: List = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()