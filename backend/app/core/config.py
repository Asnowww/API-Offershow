from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OfferShow Backend"
    env: str = "development"
    secret_key: str = "dev-secret"
    access_token_expire_minutes: int = 120
    database_url: str
    postgres_admin_database: str = "postgres"
    postgres_schema: str = "offershow"
    redis_url: str = ""
    backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> List[str]:
        return [item.strip() for item in self.backend_cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
