# backend/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.user import UserCreate, UserRead
from repositories.user_repository import UserRepository
from utils.utils import hash_password
from utils.dependencies import admin_or_superuser_required

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(admin_or_superuser_required)])

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user_in.password)
    return repo.create(user_in, hashed)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 100, school_id: int | None = None, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_all(skip, limit, school_id)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    repo.delete(user_id)
    return {"ok": True}
