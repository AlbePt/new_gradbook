from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.db import get_db
from repositories.user_repository import UserRepository
from utils.utils import hash_password, verify_password, create_access_token
from schemas.user import UserCreate, UserRead, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user_in.password)
    user = repo.create(user_in, hashed)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}

