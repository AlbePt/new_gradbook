# backend/repositories/class_teacher_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.class_ import ClassTeacher, ClassTeacherRole, ClassTeacherRoleAssociation
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
        """Create a relation if it doesn't exist.

        Additionally ensures only one homeroom teacher exists per class and
        academic year. If another homeroom teacher is already assigned, a
        ``ValueError`` is raised.
        """

        # Check for existing record with the same primary key
        db_ct = self.get(ct.class_id, ct.teacher_id, ct.academic_year_id)
        if db_ct is None:
            db_ct = ClassTeacher(
                class_id=ct.class_id,
                teacher_id=ct.teacher_id,
                academic_year_id=ct.academic_year_id,
            )
            self.db.add(db_ct)

        if ct.role == ClassTeacherRole.homeroom:
            conflict = (
                self.db.query(ClassTeacherRoleAssociation)
                .filter(
                    ClassTeacherRoleAssociation.class_id == ct.class_id,
                    ClassTeacherRoleAssociation.academic_year_id == ct.academic_year_id,
                    ClassTeacherRoleAssociation.role == ClassTeacherRole.homeroom,
                )
                .first()
            )
            if conflict and conflict.teacher_id != ct.teacher_id:
                raise ValueError("homeroom already assigned")

        exists_role = (
            self.db.query(ClassTeacherRoleAssociation)
            .filter(
                ClassTeacherRoleAssociation.class_id == ct.class_id,
                ClassTeacherRoleAssociation.teacher_id == ct.teacher_id,
                ClassTeacherRoleAssociation.academic_year_id == ct.academic_year_id,
                ClassTeacherRoleAssociation.role == ct.role,
            )
            .first()
        )
        if exists_role:
            return db_ct

        self.db.add(
            ClassTeacherRoleAssociation(
                class_id=ct.class_id,
                teacher_id=ct.teacher_id,
                academic_year_id=ct.academic_year_id,
                role=ct.role,
            )
        )
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(db_ct)
        return db_ct

    def delete(
        self, class_id: int, teacher_id: int, academic_year_id: int
    ) -> None:
        db_ct = self.get(class_id, teacher_id, academic_year_id)
        if db_ct:
            (
                self.db.query(ClassTeacherRoleAssociation)
                .filter(
                    ClassTeacherRoleAssociation.class_id == class_id,
                    ClassTeacherRoleAssociation.teacher_id == teacher_id,
                    ClassTeacherRoleAssociation.academic_year_id == academic_year_id,
                )
                .delete()
            )
            self.db.delete(db_ct)
            self.db.commit()
