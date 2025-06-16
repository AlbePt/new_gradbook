# backend/routers/teacher_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.teacher import TeacherCreate, TeacherRead
from repositories.teacher_repository import TeacherRepository

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/", response_model=TeacherRead)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    repo = TeacherRepository(db)
    return repo.create(teacher)

@router.get("/{teacher_id}", response_model=TeacherRead)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    repo = TeacherRepository(db)
    db_teacher = repo.get(teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@router.get("/", response_model=list[TeacherRead])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = TeacherRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{teacher_id}", response_model=TeacherRead)
def update_teacher(teacher_id: int, updates: TeacherCreate, db: Session = Depends(get_db)):
    repo = TeacherRepository(db)
    db_teacher = repo.get(teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return repo.update(teacher_id, updates.dict())

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    repo = TeacherRepository(db)
    repo.delete(teacher_id)
    return {"ok": True}
