# backend/repositories/parent_repository.py
from sqlalchemy.orm import Session
from models.parent import Parent
from schemas.parent import ParentCreate

class ParentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, parent_id: int) -> Parent:
        return self.db.query(Parent).filter(Parent.id == parent_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Parent).offset(skip).limit(limit).all()

    def create(self, parent: ParentCreate) -> Parent:
        db_parent = Parent(**parent.dict())
        self.db.add(db_parent)
        self.db.commit()
        self.db.refresh(db_parent)
        return db_parent

    def update(self, parent_id: int, updates: dict) -> Parent:
        db_parent = self.get(parent_id)
        for key, value in updates.items():
            setattr(db_parent, key, value)
        self.db.commit()
        self.db.refresh(db_parent)
        return db_parent

    def delete(self, parent_id: int) -> None:
        db_parent = self.get(parent_id)
        if db_parent:
            self.db.delete(db_parent)
            self.db.commit()

