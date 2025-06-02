# backend/models/attendance.py
from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    student = relationship('Student', back_populates='attendance_records')
    academic_year = relationship('AcademicYear', back_populates='attendance_records')