# backend/schemas/city.py
from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

class CityBase(BaseModel):
    name: str
    region_id: int

class CityCreate(CityBase):
    pass

class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True

class CityWithSchools(CityRead):
    schools: List['SchoolRead'] = []

from .school import SchoolRead        