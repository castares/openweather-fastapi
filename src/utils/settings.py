from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    OPENWEATHERMAP_API_KEY: Optional[str]

    class Config:
        env_file: str = ".env"
