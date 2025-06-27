# backend/models/lesson_event.py
from sqlalchemy import Column, BigInteger, Integer, Date, SmallInteger, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from core.db import Base


class LessonEvent(Base):
    __tablename__ = "lesson_events"

    id = Column(BigInteger, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    lesson_date = Column(Date, nullable=False)
    lesson_index = Column(SmallInteger)
    created_at = Column(TIMESTAMP, server_default=text("now()"))

    subject = relationship("Subject")
    school_class = relationship("Class")
    grades = relationship("Grade", back_populates="lesson_event", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="lesson_event", cascade="all, delete-orphan")
