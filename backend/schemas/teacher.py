# backend/schemas/teacher.py
from pydantic import BaseModel
from typing import Optional

class TeacherBase(BaseModel):
    first_name: str
    last_name: str

class TeacherCreate(TeacherBase):
    pass

class TeacherRead(TeacherBase):
    id: int

    class Config:
        from_attributes = True