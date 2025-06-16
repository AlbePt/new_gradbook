from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.school import SchoolCreate, SchoolRead
from repositories.school_repository import SchoolRepository

router = APIRouter(prefix="/schools", tags=["schools"])

@router.post("/", response_model=SchoolRead)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    repo = SchoolRepository(db)
    return repo.create(school)

@router.get("/{school_id}", response_model=SchoolRead)
def read_school(school_id: int, db: Session = Depends(get_db)):
    repo = SchoolRepository(db)
    db_school = repo.get(school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@router.get("/", response_model=list[SchoolRead])
def read_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SchoolRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{school_id}", response_model=SchoolRead)
def update_school(school_id: int, updates: SchoolCreate, db: Session = Depends(get_db)):
    repo = SchoolRepository(db)
    db_school = repo.get(school_id)
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    return repo.update(school_id, updates.dict())

@router.delete("/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_db)):
    repo = SchoolRepository(db)
    repo.delete(school_id)
    return {"ok": True}
