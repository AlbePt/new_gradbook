from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_in: UserCreate, password_hash: str) -> User:
        user = User(username=user_in.username, role=user_in.role, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

