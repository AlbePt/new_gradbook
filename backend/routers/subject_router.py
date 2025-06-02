# backend/routers/subject_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.subject import SubjectCreate, SubjectRead
from repositories.subject_repository import SubjectRepository

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=SubjectRead)
def create_subject(subj: SubjectCreate, db: Session = Depends(get_db)):
    repo = SubjectRepository(db)
    return repo.create(subj)

@router.get("/{subject_id}", response_model=SubjectRead)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    repo = SubjectRepository(db)
    db_subj = repo.get(subject_id)
    if not db_subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subj

@router.get("/", response_model=list[SubjectRead])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SubjectRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{subject_id}", response_model=SubjectRead)
def update_subject(subject_id: int, updates: SubjectCreate, db: Session = Depends(get_db)):
    repo = SubjectRepository(db)
    db_subj = repo.get(subject_id)
    if not db_subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return repo.update(subject_id, updates.dict())

@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    repo = SubjectRepository(db)
    repo.delete(subject_id)
    return {"ok": True}
