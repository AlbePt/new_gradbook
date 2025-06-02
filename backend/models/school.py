# backend/models/school.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)

    # Отношения
    city = relationship('City', back_populates='schools')
    students = relationship('Student', back_populates='school')
    teachers = relationship('Teacher', back_populates='school')
    schedules = relationship('Schedule', back_populates='school')
    subjects = relationship('Subject', back_populates='school', cascade='all, delete-orphan')