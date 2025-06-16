# backend/routers/attendance_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.attendance import AttendanceCreate, AttendanceRead
from repositories.attendance_repository import AttendanceRepository

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/", response_model=AttendanceRead)
def create_attendance(att: AttendanceCreate, db: Session = Depends(get_db)):
    repo = AttendanceRepository(db)
    existing = repo.get_by_student_date(att.student_id, att.date)
    if existing:
        raise HTTPException(status_code=400, detail="Attendance record already exists for this student and date")
    return repo.create(att)

@router.get("/{attendance_id}", response_model=AttendanceRead)
def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    repo = AttendanceRepository(db)
    db_att = repo.get(attendance_id)
    if not db_att:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return db_att

@router.get("/", response_model=list[AttendanceRead])
def read_attendance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AttendanceRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{attendance_id}", response_model=AttendanceRead)
def update_attendance(attendance_id: int, updates: AttendanceCreate, db: Session = Depends(get_db)):
    repo = AttendanceRepository(db)
    db_att = repo.get(attendance_id)
    if not db_att:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return repo.update(attendance_id, updates.dict())

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    repo = AttendanceRepository(db)
    repo.delete(attendance_id)
    return {"ok": True}
