# backend/schemas/class_.py
from pydantic import BaseModel

class ClassBase(BaseModel):
    name: str
    school_id: int

class ClassCreate(ClassBase):
    pass

class ClassRead(ClassBase):
    id: int

    class Config:
        from_attributes = True
