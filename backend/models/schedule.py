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

    teacher = relationship('Teacher', back_populates='schedules')
    subject = relationship('Subject', back_populates='schedules')