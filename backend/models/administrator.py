# backend/models/administrator.py
from sqlalchemy import Column, Integer, String
from core.db import Base

class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rights = Column(String(100), nullable=False)
