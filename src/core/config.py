from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BASE_URL: str = "http://localhost:8000"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    IS_PRODUCTION: bool = False

    ESI_URL: str
    ESI_CLIENT_ID: str
    ESI_CLIENT_SECRET: str
    ESI_REDIRECT_URI: str

    class Config:
        env_file = ".env"


settings = Settings()
