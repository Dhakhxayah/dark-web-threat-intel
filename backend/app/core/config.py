import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Dark Web Threat Intel API"
    app_version: str = "0.1.0"
    debug: bool = False
    data_raw_path: str = "data/raw"
    data_processed_path: str = "data/processed"
    artifacts_path: str = "data/models"
    cors_origins: str = "http://localhost:5173,https://your-vercel-app.vercel.app"

    model_config = {"protected_namespaces": ("settings_",)}

    def get_origins(self):
        return self.cors_origins.split(",")


@lru_cache()
def get_settings():
    return Settings()