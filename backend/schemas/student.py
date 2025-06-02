# backend/schemas/student.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    class_name: str
    parent_id: Optional[int] = None
    contact_info: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True