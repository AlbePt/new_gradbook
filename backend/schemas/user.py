from pydantic import BaseModel
from models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

