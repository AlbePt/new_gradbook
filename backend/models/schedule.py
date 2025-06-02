# backend/models/schedule.py
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    class_name = Column(String(10), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='RESTRICT'), nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    teacher = relationship('Teacher', back_populates='schedules')
    subject = relationship('Subject', back_populates='schedules')
    school = relationship('School', back_populates='schedules')
    academic_year = relationship('AcademicYear', back_populates='schedules')