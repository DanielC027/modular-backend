from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI WS App"

    # JWT
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # DB
    DATABASE_URL: str = "sqlite:///./app.db"

    class Config:
        env_file = ".env"


settings = Settings()
