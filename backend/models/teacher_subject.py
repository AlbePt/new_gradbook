# backend/models/teacher_subject.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base

class TeacherSubject(Base):
    __tablename__ = 'teacher_subjects'
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)

    teacher = relationship('Teacher', back_populates='teacher_subjects')
    subject = relationship('Subject', back_populates='teacher_subjects')
