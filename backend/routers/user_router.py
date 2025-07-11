# backend/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.user import UserCreate, UserRead, AdminCreate, TeacherUserCreate
from schemas.teacher import TeacherCreate
from repositories.user_repository import UserRepository
from repositories.teacher_repository import TeacherRepository
from utils.utils import hash_password
from utils.dependencies import admin_or_superuser_required
from models.user import RoleEnum

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(admin_or_superuser_required)])

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user_in.password)
    return repo.create(user_in, hashed)


@router.post("/administrators", response_model=UserRead)
def create_administrator(admin: AdminCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(admin.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(admin.password)
    user_in = UserCreate(
        username=admin.username,
        password=admin.password,
        role=RoleEnum.administrator,
        school_id=admin.school_id,
        full_name=admin.full_name,
    )
    return repo.create(user_in, hashed)


@router.post("/teachers", response_model=UserRead)
def create_teacher_user(data: TeacherUserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    teacher_repo = TeacherRepository(db)
    if user_repo.get_by_username(data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(data.password)
    user_in = UserCreate(
        username=data.username,
        password=data.password,
        role=RoleEnum.teacher,
        school_id=data.school_id,
        full_name=data.teacher_full_name if data.mode == "new" else None,
    )
    user = user_repo.create(user_in, hashed)
    if data.mode == "existing":
        teacher = teacher_repo.get(data.teacher_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        teacher.user_id = user.id
        db.commit()
    else:
        teacher = TeacherCreate(
            full_name=data.teacher_full_name or data.username,
            contact_info=data.contact_info,
            school_id=data.school_id,
            user_id=user.id,
        )
        teacher_repo.create(teacher)
    return user

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
