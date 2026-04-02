from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name = "Dark Web Threat Intel API"
    app_version = "0.1.0"
    debug = False
    data_raw_path = "data/raw"
    data_processed_path = "data/processed"
    model_artifacts_path = "data/models"
    cors_origins = ["http://localhost:5173", "https://your-vercel-app.vercel.app"]

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()