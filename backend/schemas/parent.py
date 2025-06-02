# backend/schemas/parent.py
from pydantic import BaseModel
from typing import List, Optional

class ParentBase(BaseModel):
    name: str
    phone: str
    messenger_id: Optional[str] = None

class ParentCreate(ParentBase):
    pass

class ParentRead(ParentBase):
    id: int

    class Config:
        from_attributes = True