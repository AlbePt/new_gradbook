from __future__ import annotations

from datetime import date
import re
from sqlalchemy.orm import Session

from models import AcademicYear, Class, Student


def resolve_or_create_year(db: Session, name: str) -> int:
    """Return ID of academic year with given name, create if missing."""
    ay = db.query(AcademicYear).filter_by(name=name).first()
    if ay is None:
        m = re.search(r"(\d{4})/(\d{4})", name)
        if m:
            start_year, end_year = int(m.group(1)), int(m.group(2))
            ay = AcademicYear(
                name=name,
                year_start=date(start_year, 9, 1),
                year_end=date(end_year, 8, 31),
            )
        else:
            ay = AcademicYear(
                name=name,
                year_start=date.today(),
                year_end=date.today(),
            )
        db.add(ay)
        db.flush([ay])
    return ay.id


def resolve_or_create_class(
    db: Session, name: str, school_id: int, academic_year_id: int
) -> int:
    """Return ID of class by name and school, create if missing."""
    cls = (
        db.query(Class)
        .filter_by(name=name, school_id=school_id, academic_year_id=academic_year_id)
        .first()
    )
    if cls is None:
        cls = Class(
            name=name,
            school_id=school_id,
            academic_year_id=academic_year_id,
        )
        db.add(cls)
        db.flush([cls])
    return cls.id


def resolve_or_create_student(
    db: Session,
    full_name: str,
    school_id: int,
    class_id: int,
    class_name: str,
) -> int:
    """Return ID of student by name and school, create if missing."""
    student = (
        db.query(Student)
        .filter_by(full_name=full_name, school_id=school_id)
        .first()
    )
    if student is None:
        student = Student(
            full_name=full_name,
            class_name=class_name,
            class_id=class_id,
            school_id=school_id,
        )
        db.add(student)
        db.flush([student])
    else:
        # update class info if student moved to a different class
        if student.class_id != class_id:
            student.class_id = class_id
            student.class_name = class_name
            db.flush([student])
    return student.id
