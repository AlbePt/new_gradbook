# backend/schemas/administrator.py
from pydantic import BaseModel

class AdministratorBase(BaseModel):
    name: str
    login: str
    rights: str

class AdministratorCreate(AdministratorBase):
    password: str

class AdministratorRead(AdministratorBase):
    id: int

    class Config:
        from_attributes = True
