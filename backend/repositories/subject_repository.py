# backend/repositories/subject_repository.py
from sqlalchemy.orm import Session
from models.subject import Subject
from schemas.subject import SubjectCreate

class SubjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, subject_id: int) -> Subject:
        return self.db.query(Subject).filter(Subject.id == subject_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Subject).offset(skip).limit(limit).all()

    def create(self, subject: SubjectCreate) -> Subject:
        db_subject = Subject(**subject.dict())
        self.db.add(db_subject)
        self.db.commit()
        self.db.refresh(db_subject)
        return db_subject

    def update(self, subject_id: int, updates: dict) -> Subject:
        db_subject = self.get(subject_id)
        for key, value in updates.items():
            setattr(db_subject, key, value)
        self.db.commit()
        self.db.refresh(db_subject)
        return db_subject

    def delete(self, subject_id: int) -> None:
        db_subject = self.get(subject_id)
        if db_subject:
            self.db.delete(db_subject)
            self.db.commit()

