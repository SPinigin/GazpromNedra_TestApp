from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Gazprom Nedra TestApp"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://user:password@db:5432/app.db"

    API_V1_STR: str = "/api/v1"

    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
