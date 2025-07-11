from pydantic import BaseModel
from models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    role: RoleEnum
    school_id: int | None = None
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminCreate(BaseModel):
    username: str
    password: str
    full_name: str
    school_id: int


class TeacherUserCreate(BaseModel):
    username: str
    password: str
    school_id: int
    mode: str  # "existing" or "new"
    teacher_id: int | None = None
    teacher_full_name: str | None = None
    contact_info: str | None = None

