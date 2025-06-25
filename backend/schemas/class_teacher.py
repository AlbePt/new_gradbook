# backend/schemas/class_teacher.py
from pydantic import BaseModel
from models.class_ import ClassTeacherRole


class ClassTeacherBase(BaseModel):
    class_id: int
    teacher_id: int
    academic_year_id: int
    role: ClassTeacherRole


class ClassTeacherCreate(ClassTeacherBase):
    pass


class ClassTeacherRead(ClassTeacherBase):
    class Config:
        from_attributes = True
