# backend/models/teacher.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='RESTRICT'), nullable=False)
    contact_info = Column(String(100), nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    subject = relationship('Subject', back_populates='teachers')
    grades = relationship('Grade', back_populates='teacher', cascade='all, delete-orphan')
    schedules = relationship('Schedule', back_populates='teacher', cascade='all, delete-orphan')
    school = relationship('School', back_populates='teachers')
