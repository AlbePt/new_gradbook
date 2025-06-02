# backend/schemas/region.py
from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

class RegionBase(BaseModel):
    name: str

class RegionCreate(RegionBase):
    pass

class RegionRead(RegionBase):
    id: int

    class Config:
        from_attributes = True

class RegionWithCities(RegionRead):
    cities: List['CityRead'] = []

from .city import CityRead    