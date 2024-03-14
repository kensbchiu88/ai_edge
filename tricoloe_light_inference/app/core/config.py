from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LABELING_SYSTEM_URI: str
    GET_STREAMING_API: str
    GET_LABEL_API: str
    LABEL_TYPE: str
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()    