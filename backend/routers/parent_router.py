# backend/routers/parent_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.parent import ParentCreate, ParentRead
from repositories.parent_repository import ParentRepository

router = APIRouter(prefix="/parents", tags=["parents"])

@router.post("/", response_model=ParentRead)
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    repo = ParentRepository(db)
    return repo.create(parent)

@router.get("/{parent_id}", response_model=ParentRead)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    repo = ParentRepository(db)
    db_parent = repo.get(parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@router.get("/", response_model=list[ParentRead])
def read_parents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ParentRepository(db)
    return repo.get_all(skip, limit)

@router.put("/{parent_id}", response_model=ParentRead)
def update_parent(parent_id: int, updates: ParentCreate, db: Session = Depends(get_db)):
    repo = ParentRepository(db)
    db_parent = repo.get(parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return repo.update(parent_id, updates.dict())

@router.delete("/{parent_id}")
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    repo = ParentRepository(db)
    repo.delete(parent_id)
    return {"ok": True}