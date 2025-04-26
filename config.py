import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import HttpUrl

load_dotenv()  # Load variables from .env into environment

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    RAPIDAPI_KEY: str = os.getenv("RAPIDAPI_KEY")
    LATEST_MUTUALFUND_URL: str = os.getenv("LATEST_MUTUALFUND_URL")
    LATEST_MUTUALFUND_HOST: str = os.getenv("LATEST_MUTUALFUND_HOST")

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
