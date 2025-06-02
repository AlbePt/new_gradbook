# backend/schemas/schedule.py
from pydantic import BaseModel
from datetime import date

class ScheduleBase(BaseModel):
    date: date
    class_name: str
    teacher_id: int
    subject_id: int

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleRead(ScheduleBase):
    id: int

    class Config:
        from_attributes = True