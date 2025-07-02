# backend/schemas/attendance.py
from pydantic import BaseModel
from datetime import date
from models.attendance import AttendanceStatusEnum

class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatusEnum
    minutes_late: int | None = None
    comment: str | None = None
    student_id: int
    lesson_event_id: int
    academic_year_id: int | None = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceRead(AttendanceBase):
    id: int

    class Config:
        from_attributes = True
