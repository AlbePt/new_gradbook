# backend/routers/academic_year_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.academic_year import AcademicYearCreate, AcademicYearRead
from repositories.academic_year_repository import AcademicYearRepository

router = APIRouter(prefix="/academic-years", tags=["academic_years"])

@router.post("/", response_model=AcademicYearRead)
def create_academic_year(year: AcademicYearCreate, db: Session = Depends(get_db)):
    repo = AcademicYearRepository(db)
    return repo.create(year)

@router.get("/{year_id}", response_model=AcademicYearRead)
def read_academic_year(year_id: int, db: Session = Depends(get_db)):
    repo = AcademicYearRepository(db)
    db_year = repo.get(year_id)
    if not db_year:
        raise HTTPException(status_code=404, detail="Academic year not found")
    return db_year

@router.get("/", response_model=list[AcademicYearRead])
def read_academic_years(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AcademicYearRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{year_id}", response_model=AcademicYearRead)
def update_academic_year(year_id: int, updates: AcademicYearCreate, db: Session = Depends(get_db)):
    repo = AcademicYearRepository(db)
    if not repo.get(year_id):
        raise HTTPException(status_code=404, detail="Academic year not found")
    return repo.update(year_id, updates.dict())

@router.delete("/{year_id}")
def delete_academic_year(year_id: int, db: Session = Depends(get_db)):
    repo = AcademicYearRepository(db)
    repo.delete(year_id)
    return {"ok": True}
