# backend/models/academic_year.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from core.db import Base

class AcademicYear(Base):
    __tablename__ = 'academic_years'

    id = Column(Integer, primary_key=True, index=True)
    year_start = Column(Date, nullable=False)
    year_end = Column(Date, nullable=False)
    name = Column(String(20), nullable=False)

    # Отношения
    schedules = relationship('Schedule', back_populates='academic_year', cascade='all, delete-orphan')
    grades = relationship('Grade', back_populates='academic_year', cascade='all, delete-orphan')
    attendance_records = relationship('Attendance', back_populates='academic_year', cascade='all, delete-orphan')
