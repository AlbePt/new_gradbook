# backend/schemas/schedule.py
from pydantic import BaseModel
from datetime import date

class ScheduleBase(BaseModel):
    date: date
    class_name: str
    teacher_id: int
    subject_id: int
    school_id: int  # Новое поле
    academic_year_id: int  # Новое поле

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleRead(ScheduleBase):
    id: int

    class Config:
        from_attributes = True