# backend/schemas/academic_period.py
from __future__ import annotations

from datetime import date
from pydantic import BaseModel

from models.grade import TermTypeEnum


class AcademicPeriodBase(BaseModel):
    academic_year_id: int
    term_type: TermTypeEnum
    term_index: int
    start_date: date
    end_date: date


class AcademicPeriodCreate(AcademicPeriodBase):
    pass


class AcademicPeriodRead(AcademicPeriodBase):
    id: int

    class Config:
        from_attributes = True
