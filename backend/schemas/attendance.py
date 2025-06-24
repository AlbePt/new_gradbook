# backend/schemas/attendance.py
from pydantic import BaseModel
from datetime import date

class AttendanceBase(BaseModel):
    date: date
    is_present: bool
    student_id: int

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceRead(AttendanceBase):
    id: int

    class Config:
        from_attributes = True