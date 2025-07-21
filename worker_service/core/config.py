from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    LOG_LEVEL: str

    class Config:
        env_file = ".env"
        env_prefix = ""

settings = Settings()
