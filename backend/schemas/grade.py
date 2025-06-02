# backend/schemas/grade.py
from pydantic import BaseModel
from datetime import date

class GradeBase(BaseModel):
    value: int
    date: date
    student_id: int
    teacher_id: int
    subject_id: int

class GradeCreate(GradeBase):
    pass

class GradeRead(GradeBase):
    id: int

    class Config:
        from_attributes = True