# backend/models/region.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Отношения
    cities = relationship('City', back_populates='region', cascade='all, delete-orphan')