# backend/models/grade.py
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)

    student = relationship('Student', back_populates='grades')
    teacher = relationship('Teacher', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')