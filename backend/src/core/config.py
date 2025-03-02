from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Globetrotter"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A geography quiz game API"

    # Database Settings
    SQLITE_DB_FILE: str = "globetrotter.db"
    DATABASE_URL: Optional[str] = None

    # Application Settings
    DEBUG: bool = False
    RELOAD: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Data Settings
    DATA_FILE_PATH: str = "data/data.json"

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite+aiosqlite:///{self.SQLITE_DB_FILE}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
