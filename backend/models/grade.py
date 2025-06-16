# backend/models/grade.py
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='RESTRICT'), nullable=False)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    student = relationship('Student', back_populates='grades')
    teacher = relationship('Teacher', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')
    academic_year = relationship('AcademicYear', back_populates='grades')
