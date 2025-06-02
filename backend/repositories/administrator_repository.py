# backend/repositories/administrator_repository.py
from sqlalchemy.orm import Session
from models.administrator import Administrator
from schemas.administrator import AdministratorCreate

class AdministratorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, admin_id: int) -> Administrator:
        return self.db.query(Administrator).filter(Administrator.id == admin_id).first()

    def get_by_login(self, login: str) -> Administrator:
        return self.db.query(Administrator).filter(Administrator.login == login).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Administrator).offset(skip).limit(limit).all()

    def create(self, admin: AdministratorCreate, password_hash: str) -> Administrator:
        db_admin = Administrator(
            name=admin.name,
            login=admin.login,
            rights=admin.rights,
            password_hash=password_hash
        )
        self.db.add(db_admin)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin

    def update(self, admin_id: int, updates: dict) -> Administrator:
        db_admin = self.get(admin_id)
        for key, value in updates.items():
            setattr(db_admin, key, value)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin

    def delete(self, admin_id: int) -> None:
        db_admin = self.get(admin_id)
        if db_admin:
            self.db.delete(db_admin)
            self.db.commit()