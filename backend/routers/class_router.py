# backend/routers/class_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.dependencies import administrator_required
from core.db import get_db
from schemas.class_ import ClassCreate, ClassRead
from repositories.class_repository import ClassRepository

router = APIRouter(prefix="/classes", tags=["classes"], dependencies=[Depends(administrator_required)])


@router.post("/", response_model=ClassRead)
def create_class(school_class: ClassCreate, db: Session = Depends(get_db)):
    repo = ClassRepository(db)
    return repo.create(school_class)


@router.get("/{class_id}", response_model=ClassRead)
def read_class(class_id: int, db: Session = Depends(get_db)):
    repo = ClassRepository(db)
    db_class = repo.get(class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class


@router.get("/", response_model=list[ClassRead])
def read_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ClassRepository(db)
    return repo.get_all(skip, limit)


@router.put("/{class_id}", response_model=ClassRead)
def update_class(class_id: int, updates: ClassCreate, db: Session = Depends(get_db)):
    repo = ClassRepository(db)
    if not repo.get(class_id):
        raise HTTPException(status_code=404, detail="Class not found")
    return repo.update(class_id, updates.dict())


@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    repo = ClassRepository(db)
    repo.delete(class_id)
    return {"ok": True}
