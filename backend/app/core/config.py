"""Application configuration."""

from pydantic import BaseModel

from app.core.constants import API_V1_PREFIX, APP_NAME, APP_VERSION


class Settings(BaseModel):
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    api_v1_prefix: str = API_V1_PREFIX


settings = Settings()

