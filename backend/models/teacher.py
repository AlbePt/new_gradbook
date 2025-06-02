# backend/models/teacher.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    subjects = relationship('TeacherSubject', back_populates='teacher')
    grades = relationship('Grade', back_populates='teacher')
    schedules = relationship('Schedule', back_populates='teacher')
