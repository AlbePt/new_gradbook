# backend/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings


# Создаем движок SQLAlchemy
engine = create_engine(
    str(settings.DATABASE_URL),   # ✅ оборачиваем в str()
    echo=True,  # вывод SQL-запросов в логи, можно переключить на False
)

# Фабрика сессий, для зависимостей FastAPI
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для всех моделей
Base = declarative_base()

# Dependency для получения сессии БД

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
