from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI项目"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080"]
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        case_sensitive = True

settings = Settings() 