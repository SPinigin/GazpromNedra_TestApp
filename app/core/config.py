from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/license_db"
    app_name: str = "Gazprom-Nedra TestApp"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
