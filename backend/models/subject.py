# backend/models/subject.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    teachers = relationship('TeacherSubject', back_populates='subject')
    grades = relationship('Grade', back_populates='subject')
    schedules = relationship('Schedule', back_populates='subject')