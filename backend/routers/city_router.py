# backend/routers/city_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.city import CityCreate, CityRead
from repositories.city_repository import CityRepository

router = APIRouter(prefix="/cities", tags=["cities"])

@router.post("/", response_model=CityRead)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    repo = CityRepository(db)
    return repo.create(city)

@router.get("/{city_id}", response_model=CityRead)
def read_city(city_id: int, db: Session = Depends(get_db)):
    repo = CityRepository(db)
    db_city = repo.get(city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.get("/", response_model=list[CityRead])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = CityRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{city_id}", response_model=CityRead)
def update_city(city_id: int, updates: CityCreate, db: Session = Depends(get_db)):
    repo = CityRepository(db)
    if not repo.get(city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return repo.update(city_id, updates.dict())

@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    repo = CityRepository(db)
    repo.delete(city_id)
    return {"ok": True}
