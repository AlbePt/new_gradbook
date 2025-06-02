# backend/schemas/academic_year.py
from __future__ import annotations
from pydantic import BaseModel
from datetime import date

class AcademicYearBase(BaseModel):
    year_start: date
    year_end: date
    name: str

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearRead(AcademicYearBase):
    id: int

    class Config:
        from_attributes = True