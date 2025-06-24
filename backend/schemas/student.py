# backend/schemas/student.py
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    full_name: str
    class_name: str
    parent_id: Optional[int] = None
    contact_info: Optional[str] = None
    school_id: int 

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True