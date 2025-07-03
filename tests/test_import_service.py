import os
import sys
from datetime import date
from pathlib import Path

import testing.postgresql
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/db")
os.environ.setdefault("SECRET_KEY", "x")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "db")
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "pass")

from app.importer.service import ImportService
from app.importer.base import ParsedRow
from models import (
    AcademicYear,
    City,
    Class,
    Grade,
    LessonEvent,
    Region,
    School,
    Student,
    Subject,
    Teacher,
)


def run_migrations(url: str) -> None:
    os.environ["DATABASE_URL"] = url
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


def prepare(session):
    region = Region(name="R")
    city = City(name="C", region=region)
    school = School(name="S", full_name="Test School", city=city)
    ay = AcademicYear(
        name="2024/2025",
        year_start=date(2024, 9, 1),
        year_end=date(2025, 8, 31),
    )
    cls = Class(name="1A", school=school, academic_year=ay)
    teacher = Teacher(full_name="T", school=school)
    subj = Subject(name="Math", school=school)
    student = Student(
        full_name="Kid",
        class_name="1A",
        school_class=cls,
        school=school,
    )
    event = LessonEvent(
        subject=subj,
        school_class=cls,
        lesson_date=date(2024, 9, 10),
    )
    session.add_all([region, city, school, ay, cls, teacher, subj, student, event])
    session.commit()
    return teacher.id, subj.id, student.id, event.lesson_date, event.id, ay.id


def test_import_service_sets_year(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        _, _, _, d, _, ay_id = prepare(session)

        row = ParsedRow(
            student_name="Kid",
            class_name="1A",
            academic_year_name="2024/2025",
            subject_name="Math",
            teacher_name="T",
            lesson_date=d,
            grade_value=5,
            grade_kind="regular",
            term_type="year",
            term_index=1,
        )
        svc = ImportService(session)
        svc.import_items([row])
        db_grade = session.query(Grade).one()
        assert db_grade.academic_year_id == ay_id
        session.close()
