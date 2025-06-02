# backend/routers/grade_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.grade import GradeCreate, GradeRead
from repositories.grade_repository import GradeRepository

router = APIRouter(prefix="/grades", tags=["grades"])

@router.post("/", response_model=GradeRead)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    repo = GradeRepository(db)
    return repo.create(grade)

@router.get("/{grade_id}", response_model=GradeRead)
def read_grade(grade_id: int, db: Session = Depends(get_db)):
    repo = GradeRepository(db)
    db_grade = repo.get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade

@router.get("/", response_model=list[GradeRead])
def read_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = GradeRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{grade_id}", response_model=GradeRead)
def update_grade(grade_id: int, updates: GradeCreate, db: Session = Depends(get_db)):
    repo = GradeRepository(db)
    db_grade = repo.get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return repo.update(grade_id, updates.dict())

@router.delete("/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    repo = GradeRepository(db)
    repo.delete(grade_id)
    return {"ok": True}
