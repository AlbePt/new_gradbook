# backend/models/parent.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    contact_info = Column(String(100), nullable=True)

    # Отношения - НЕ удаляем детей при удалении родителя
    children = relationship('Student', back_populates='parent')