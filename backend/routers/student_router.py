# backend/routers/student_router.py
from fastapi import APIRouter, Depends, HTTPException
from utils.dependencies import administrator_required
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.student import StudentCreate, StudentRead
from repositories.student_repository import StudentRepository

router = APIRouter(prefix="/students", tags=["students"], dependencies=[Depends(administrator_required)])

@router.post("/", response_model=StudentRead)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    return repo.create(student)

@router.get("/{student_id}", response_model=StudentRead)
def read_student(student_id: int, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    db_student = repo.get(student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/", response_model=list[StudentRead])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: int, updates: StudentCreate, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    db_student = repo.get(student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return repo.update(student_id, updates.dict())

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    repo = StudentRepository(db)
    repo.delete(student_id)
    return {"ok": True}
