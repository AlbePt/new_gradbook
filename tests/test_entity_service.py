import os
import sys
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

from backend.services import (
    resolve_or_create_student,
    resolve_or_create_class,
    resolve_or_create_year,
)
from models import Region, City, School, Class, Student, AcademicYear


def run_migrations(url: str) -> None:
    os.environ["DATABASE_URL"] = url
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


def prepare_school(session):
    region = Region(name="R")
    city = City(name="C", region=region)
    school = School(name="S", full_name="Test School", city=city)
    session.add_all([region, city, school])
    session.commit()
    return school.id


def test_resolve_helpers_create_and_reuse(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        school_id = prepare_school(session)

        year_id = resolve_or_create_year(session, "2024/2025")
        session.commit()
        assert session.query(AcademicYear).count() == 1
        year_id2 = resolve_or_create_year(session, "2024/2025")
        session.commit()
        assert year_id2 == year_id
        assert session.query(AcademicYear).count() == 1

        class_id = resolve_or_create_class(session, "1A", school_id, year_id)
        session.commit()
        assert session.query(Class).count() == 1
        class_id2 = resolve_or_create_class(session, "1A", school_id, year_id)
        session.commit()
        assert class_id2 == class_id
        assert session.query(Class).count() == 1

        student_id = resolve_or_create_student(
            session,
            "Kid",
            school_id,
            class_id,
            "1A",
        )
        session.commit()
        assert session.query(Student).count() == 1
        student_id2 = resolve_or_create_student(
            session,
            "Kid",
            school_id,
            class_id,
            "1A",
        )
        session.commit()
        assert student_id2 == student_id
        assert session.query(Student).count() == 1
        session.close()
