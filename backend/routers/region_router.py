from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.region import RegionCreate, RegionRead
from repositories.region_repository import RegionRepository

router = APIRouter(prefix="/regions", tags=["regions"])

@router.post("/", response_model=RegionRead)
def create_region(region: RegionCreate, db: Session = Depends(get_db)):
    repo = RegionRepository(db)
    return repo.create(region)

@router.get("/{region_id}", response_model=RegionRead)
def read_region(region_id: int, db: Session = Depends(get_db)):
    repo = RegionRepository(db)
    db_region = repo.get(region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region

@router.get("/", response_model=list[RegionRead])
def read_regions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = RegionRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{region_id}", response_model=RegionRead)
def update_region(region_id: int, updates: RegionCreate, db: Session = Depends(get_db)):
    repo = RegionRepository(db)
    db_region = repo.get(region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return repo.update(region_id, updates.dict())

@router.delete("/{region_id}")
def delete_region(region_id: int, db: Session = Depends(get_db)):
    repo = RegionRepository(db)
    repo.delete(region_id)
    return {"ok": True}
