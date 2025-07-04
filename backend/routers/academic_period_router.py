# backend/routers/academic_period_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from schemas.academic_period import AcademicPeriodCreate, AcademicPeriodRead
from repositories.academic_period_repository import AcademicPeriodRepository

router = APIRouter(prefix="/academic-periods", tags=["academic_periods"])


@router.post("/", response_model=AcademicPeriodRead)
def create_academic_period(period: AcademicPeriodCreate, db: Session = Depends(get_db)):
    repo = AcademicPeriodRepository(db)
    return repo.create(period)


@router.get("/{period_id}", response_model=AcademicPeriodRead)
def read_academic_period(period_id: int, db: Session = Depends(get_db)):
    repo = AcademicPeriodRepository(db)
    db_period = repo.get(period_id)
    if not db_period:
        raise HTTPException(status_code=404, detail="Academic period not found")
    return db_period


@router.get("/", response_model=list[AcademicPeriodRead])
def read_academic_periods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AcademicPeriodRepository(db)
    return repo.get_all(skip, limit)


@router.put("/{period_id}", response_model=AcademicPeriodRead)
def update_academic_period(period_id: int, updates: AcademicPeriodCreate, db: Session = Depends(get_db)):
    repo = AcademicPeriodRepository(db)
    if not repo.get(period_id):
        raise HTTPException(status_code=404, detail="Academic period not found")
    return repo.update(period_id, updates.dict())


@router.delete("/{period_id}")
def delete_academic_period(period_id: int, db: Session = Depends(get_db)):
    repo = AcademicPeriodRepository(db)
    repo.delete(period_id)
    return {"ok": True}
