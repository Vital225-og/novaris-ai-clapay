"""Application configuration."""

import os

from pydantic import BaseModel, Field

from app.core.constants import API_V1_PREFIX, APP_NAME, APP_VERSION


class Settings(BaseModel):
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    api_v1_prefix: str = API_V1_PREFIX
    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./novaris_ai.db")
    )


settings = Settings()
