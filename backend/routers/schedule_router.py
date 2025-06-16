# backend/routers/schedule_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.schedule import ScheduleCreate, ScheduleRead
from repositories.schedule_repository import ScheduleRepository

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/", response_model=ScheduleRead)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    return repo.create(schedule)

@router.get("/{schedule_id}", response_model=ScheduleRead)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    db_schedule = repo.get(schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return db_schedule

@router.get("/", response_model=list[ScheduleRead])
def read_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(schedule_id: int, updates: ScheduleCreate, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    db_schedule = repo.get(schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return repo.update(schedule_id, updates.dict())

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    repo.delete(schedule_id)
    return {"ok": True}
