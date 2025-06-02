# backend/schemas/attendance.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceBase(BaseModel):
    date: date
    is_present: bool
    reason: Optional[str] = None
    student_id: int

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceRead(AttendanceBase):
    id: int

    class Config:
        from_attributes = True