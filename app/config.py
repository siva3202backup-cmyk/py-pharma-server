from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Pharmacy API"
    app_version: str = "2.0.0"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 5000
    client_origin: str = "http://localhost:4200"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/pharmacy_db"
    jwt_secret: str = Field(default="change-this-local-secret", min_length=16)
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 1440
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
