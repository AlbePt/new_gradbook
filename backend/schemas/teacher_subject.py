# backend/schemas/teacher_subject.py
from pydantic import BaseModel

class TeacherSubjectBase(BaseModel):
    teacher_id: int
    subject_id: int

class TeacherSubjectCreate(TeacherSubjectBase):
    pass

class TeacherSubjectRead(TeacherSubjectBase):
    class Config:
        from_attributes = True
