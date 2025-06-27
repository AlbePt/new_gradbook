# backend/models/grade.py
import enum

from core.db import Base
from sqlalchemy import (Column, Date, Enum, ForeignKey, Index, Integer,
                        Numeric, SmallInteger)
from sqlalchemy.orm import relationship


class TermTypeEnum(str, enum.Enum):
    trimester = "trimester"
    quarter = "quarter"
    semester = "semester"
    year = "year"


class GradeKindEnum(str, enum.Enum):
    regular = "regular"
    avg = "avg"
    weighted_avg = "weighted_avg"
    period_final = "period_final"
    year_final = "year_final"
    exam = "exam"
    state_exam = "state_exam"


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Numeric(4, 2), nullable=False)
    date = Column(Date, nullable=False)
    term_type = Column(Enum(TermTypeEnum), nullable=False)
    term_index = Column(SmallInteger, nullable=False)
    grade_kind = Column(Enum(GradeKindEnum), nullable=False)
    lesson_event_id = Column(
        Integer,
        ForeignKey("lesson_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        nullable=False,
    )
    academic_year_id = Column(
        Integer,
        ForeignKey("academic_years.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Отношения
    student = relationship("Student", back_populates="grades")
    teacher = relationship("Teacher", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
    academic_year = relationship("AcademicYear", back_populates="grades")
    lesson_event = relationship("LessonEvent", back_populates="grades")


Index(
    "uq_grade_unique",
    Grade.student_id,
    Grade.subject_id,
    Grade.term_type,
    Grade.term_index,
    Grade.grade_kind,
    Grade.lesson_event_id,
    unique=True,
)
