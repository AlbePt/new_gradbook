# backend/models/city.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    region = relationship('Region', back_populates='cities')
    schools = relationship('School', back_populates='city', cascade='all, delete-orphan')
