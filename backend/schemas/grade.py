# backend/schemas/grade.py
from datetime import date

from models.grade import GradeKindEnum, TermTypeEnum
from pydantic import BaseModel


class GradeBase(BaseModel):
    value: float
    date: date
    student_id: int
    teacher_id: int
    subject_id: int
    term_type: TermTypeEnum
    term_index: int
    grade_kind: GradeKindEnum
    lesson_event_id: int
    academic_year_id: int | None = None


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int

    class Config:
        from_attributes = True
