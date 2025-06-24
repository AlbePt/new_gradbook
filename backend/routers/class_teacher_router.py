# backend/routers/class_teacher_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.class_teacher import ClassTeacherCreate, ClassTeacherRead
from repositories.class_teacher_repository import ClassTeacherRepository

router = APIRouter(prefix="/class-teachers", tags=["class_teachers"])


@router.post("/", response_model=ClassTeacherRead)
def assign_class_teacher(ct: ClassTeacherCreate, db: Session = Depends(get_db)):
    repo = ClassTeacherRepository(db)
    return repo.create(ct)


@router.delete("/{class_id}/{teacher_id}")
def remove_class_teacher(class_id: int, teacher_id: int, db: Session = Depends(get_db)):
    repo = ClassTeacherRepository(db)
    repo.delete(class_id, teacher_id)
    return {"ok": True}
