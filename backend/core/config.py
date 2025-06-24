# backend/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    """
    Основные настройки приложения из переменных окружения
    """
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Файл с переменными окружения
        env_file = './.env'
        env_file_encoding = 'utf-8'


settings = Settings()
