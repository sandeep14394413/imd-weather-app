from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "India Weather Forecast App"
    database_url: str = "sqlite:///./weather_app.db"
    jwt_secret: str = "change-this-secret-before-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    model_api_url: str = "http://localhost:8010"

    class Config:
        env_file = ".env"


settings = Settings()
