# backend/repositories/class_teacher_repository.py
from sqlalchemy.orm import Session
from models.class_ import ClassTeacher
from schemas.class_teacher import ClassTeacherCreate


class ClassTeacherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(
        self, class_id: int, teacher_id: int, academic_year_id: int
    ) -> ClassTeacher:
        """Retrieve a class-teacher relation for a specific academic year."""

        return (
            self.db.query(ClassTeacher)
            .filter(
                ClassTeacher.class_id == class_id,
                ClassTeacher.teacher_id == teacher_id,
                ClassTeacher.academic_year_id == academic_year_id,
            )
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(ClassTeacher).offset(skip).limit(limit).all()

    def create(self, ct: ClassTeacherCreate) -> ClassTeacher:
        """Create a relation if it doesn't exist."""

        db_ct = self.get(ct.class_id, ct.teacher_id, ct.academic_year_id)
        if db_ct:
            return db_ct

        db_ct = ClassTeacher(**ct.dict())
        self.db.add(db_ct)
        self.db.commit()
        self.db.refresh(db_ct)
        return db_ct

    def delete(self, class_id: int, teacher_id: int, academic_year_id: int) -> None:
        db_ct = self.get(class_id, teacher_id, academic_year_id)
        if db_ct:
            self.db.delete(db_ct)
            self.db.commit()
