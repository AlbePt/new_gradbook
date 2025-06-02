# backend/models/schedule.py
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    class_name = Column(String(10), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id'), nullable=False)  # Новое поле
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False)  # Новое поле

    # Отношения
    teacher = relationship('Teacher', back_populates='schedules')
    subject = relationship('Subject', back_populates='schedules')
    school = relationship('School', back_populates='schedules')  # Новое отношение
    academic_year = relationship('AcademicYear', back_populates='schedules')  # Новое отношение