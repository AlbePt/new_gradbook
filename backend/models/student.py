# backend/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    class_name = Column(String(10), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id', ondelete='SET NULL'), nullable=True)
    contact_info = Column(String(100), nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)

    # Отношения
    parent = relationship('Parent', back_populates='children')
    grades = relationship('Grade', back_populates='student', cascade='all, delete-orphan')
    attendance_records = relationship('Attendance', back_populates='student', cascade='all, delete-orphan')
    school = relationship('School', back_populates='students')
