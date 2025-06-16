# backend/schemas/subject.py
from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    school_id: int


class SubjectCreate(SubjectBase):
    pass


class SubjectRead(SubjectBase):
    id: int

    class Config:
        from_attributes = True
