# backend/repositories/teacher_subject_repository.py
from sqlalchemy.orm import Session
from models.teacher_subject import TeacherSubject
from schemas.teacher_subject import TeacherSubjectCreate

class TeacherSubjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, teacher_id: int, subject_id: int) -> TeacherSubject:
        return self.db.query(TeacherSubject).filter(
            TeacherSubject.teacher_id == teacher_id,
            TeacherSubject.subject_id == subject_id
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(TeacherSubject).offset(skip).limit(limit).all()

    def create(self, ts: TeacherSubjectCreate) -> TeacherSubject:
        db_ts = TeacherSubject(**ts.dict())
        self.db.add(db_ts)
        self.db.commit()
        return db_ts

    def delete(self, teacher_id: int, subject_id: int) -> None:
        db_ts = self.get(teacher_id, subject_id)
        if db_ts:
            self.db.delete(db_ts)
            self.db.commit()

