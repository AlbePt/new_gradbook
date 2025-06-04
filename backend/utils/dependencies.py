from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.db import get_db
from repositories.user_repository import UserRepository
from utils.utils import decode_access_token
from models.user import User, RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    repo = UserRepository(db)
    user = repo.get(int(user_id))
    if user is None:
        raise credentials_exception
    return user


def require_role(role: RoleEnum):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user
    return role_checker

superuser_required = require_role(RoleEnum.superuser)
administrator_required = require_role(RoleEnum.administrator)

