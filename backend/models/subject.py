# backend/models/subject.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id'), nullable=False, index=True)

    
    school = relationship('School', back_populates='subjects')

    # связи с TeacherSubject, Grade, Schedule остаются прежними
    teachers = relationship('Teacher', secondary='teacher_subjects', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')
    schedules = relationship('Schedule', back_populates='subject')
    teacher_subjects = relationship(
        'TeacherSubject',
        back_populates='subject',
        cascade='all, delete-orphan'
    )
