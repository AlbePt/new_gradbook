# backend/repositories/class_repository.py
from sqlalchemy.orm import Session
from models.class_ import Class
from schemas.class_ import ClassCreate


class ClassRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, class_id: int) -> Class:
        return self.db.query(Class).filter(Class.id == class_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        school_id: int | None = None,
        academic_year_id: int | None = None,
    ):
        query = self.db.query(Class)
        if school_id is not None:
            query = query.filter(Class.school_id == school_id)
        if academic_year_id is not None:
            query = query.filter(Class.academic_year_id == academic_year_id)
        return query.offset(skip).limit(limit).all()

    def create(self, school_class: ClassCreate) -> Class:
        db_class = Class(**school_class.dict())
        self.db.add(db_class)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def update(self, class_id: int, updates: dict) -> Class:
        db_class = self.get(class_id)
        for key, value in updates.items():
            setattr(db_class, key, value)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def delete(self, class_id: int) -> None:
        db_class = self.get(class_id)
        if db_class:
            self.db.delete(db_class)
            self.db.commit()
