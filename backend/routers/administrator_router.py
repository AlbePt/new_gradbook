# backend/routers/administrator_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.administrator import AdministratorCreate, AdministratorRead
from repositories.administrator_repository import AdministratorRepository
from utils.utils import hash_password

router = APIRouter(prefix="/administrators", tags=["administrators"])

@router.post("/", response_model=AdministratorRead)
def create_administrator(admin: AdministratorCreate, db: Session = Depends(get_db)):
    repo = AdministratorRepository(db)
    hashed = hash_password(admin.password)
    return repo.create(admin, hashed)

@router.get("/{admin_id}", response_model=AdministratorRead)
def read_administrator(admin_id: int, db: Session = Depends(get_db)):
    repo = AdministratorRepository(db)
    db_admin = repo.get(admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrator not found")
    return db_admin

@router.get("/", response_model=list[AdministratorRead])
def read_administrators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AdministratorRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{admin_id}", response_model=AdministratorRead)
def update_administrator(admin_id: int, updates: AdministratorCreate, db: Session = Depends(get_db)):
    repo = AdministratorRepository(db)
    db_admin = repo.get(admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Administrator not found")
    # Если пароль обновляется, нужно хешировать
    hashed = hash_password(updates.password)
    return repo.update(admin_id, {**updates.dict(exclude={"password"}), "password_hash": hashed})

@router.delete("/{admin_id}")
def delete_administrator(admin_id: int, db: Session = Depends(get_db)):
    repo = AdministratorRepository(db)
    repo.delete(admin_id)
    return {"ok": True}
