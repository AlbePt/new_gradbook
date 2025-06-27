from datetime import date
from pydantic import BaseModel
from models.exam import ExamKindEnum


class ExamIn(BaseModel):
    student_id: int
    subject_id: int
    exam_kind: ExamKindEnum
    exam_date: date
    value: int | None = None
    comment: str | None = None
