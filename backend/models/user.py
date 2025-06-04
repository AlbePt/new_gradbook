import enum
from sqlalchemy import Column, Integer, String, Enum
from core.db import Base

class RoleEnum(str, enum.Enum):
    superuser = "superuser"
    administrator = "administrator"
    teacher = "teacher"
    student = "student"
    parent = "parent"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

