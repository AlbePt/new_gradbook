# backend/routers/teacher_subject_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.teacher_subject import TeacherSubjectCreate, TeacherSubjectRead
from repositories.teacher_subject_repository import TeacherSubjectRepository

router = APIRouter(prefix="/teacher-subjects", tags=["teacher_subjects"])

@router.post("/", response_model=TeacherSubjectRead)
def assign_subject(ts: TeacherSubjectCreate, db: Session = Depends(get_db)):
    repo = TeacherSubjectRepository(db)
    return repo.create(ts)

@router.delete("/{teacher_id}/{subject_id}")
def unassign_subject(teacher_id: int, subject_id: int, db: Session = Depends(get_db)):
    repo = TeacherSubjectRepository(db)
    repo.delete(teacher_id, subject_id)
    return {"ok": True}
