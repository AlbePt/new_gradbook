# backend/schemas/school.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class SchoolBase(BaseModel):
    name: str
    city_id: int
    full_name: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolRead(SchoolBase):
    id: int

    class Config:
        from_attributes = True

class SchoolNested(SchoolRead):
    city: 'CityRead'

from .city import CityRead        