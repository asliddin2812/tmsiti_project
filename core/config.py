from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    UPLOAD_DIR: str
    MAX_FILE_SIZE: int
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
