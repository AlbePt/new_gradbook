# backend/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    class_name = Column(String(10), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=True)
    contact_info = Column(String(100), nullable=True)

    parent = relationship('Parent', back_populates='children')
    grades = relationship('Grade', back_populates='student')
    attendance_records = relationship('Attendance', back_populates='student')