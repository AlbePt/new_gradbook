from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.db import get_db
from models.grade import Grade, TermTypeEnum
from models.student import Student

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/average-grade")
def average_grade(
    school_id: int,
    academic_year_id: int,
    class_id: int | None = None,
    quarter: int | None = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(func.avg(Grade.value))
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.school_id == school_id, Grade.academic_year_id == academic_year_id)
    )
    if class_id is not None:
        query = query.filter(Student.class_id == class_id)
    if quarter is not None:
        query = query.filter(Grade.term_type == TermTypeEnum.quarter, Grade.term_index == quarter)
    avg = query.scalar()
    return {"average": float(avg) if avg is not None else None}
