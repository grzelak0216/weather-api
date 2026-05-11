from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    APP_TITLE: str = "Weather Scoring API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()