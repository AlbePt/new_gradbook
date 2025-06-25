import os
import sys
from pathlib import Path

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

import pandas as pd
import testing.postgresql
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.import_teachers.service import import_teachers_from_file
from backend.core.db import Base
from models import (
    City,
    Class,
    ClassTeacher,
    ClassTeacherRole,
    Region,
    School,
    Subject,
    Teacher,
    TeacherSubject,
    AcademicYear,
)


def run_migrations(url: str) -> None:
    os.environ['DATABASE_URL'] = url
    cfg = Config('alembic.ini')
    command.upgrade(cfg, 'head')


def prepare_school(session):
    region = Region(name='R')
    city = City(name='C', region=region)
    school = School(name='S', full_name='Test School', city=city)
    session.add_all([region, city, school])
    session.commit()
    return school.id


def make_excel(path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                'ФИО педагога': 'Teacher One',
                'Классный руководитель': '',
                'Предмет': 'Literature',
                'Класс': '10A, 5A',
            },
            {
                'ФИО педагога': None,
                'Классный руководитель': '',
                'Предмет': 'Language',
                'Класс': '10A, 5A',
            },
            {
                'ФИО педагога': 'Teacher Two',
                'Классный руководитель': '1G',
                'Предмет': 'Math',
                'Класс': '1G, 4B',
            },
            {
                'ФИО педагога': None,
                'Классный руководитель': '',
                'Предмет': 'Talks',
                'Класс': '1G, 4B',
            },
        ]
    )
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name='Справочник педагоги', index=False, startrow=2)
        ws = writer.sheets['Справочник педагоги']
        ws.cell(row=1, column=1, value='Педагоги 2024/2025')
        ws.cell(row=2, column=1, value='Test School')


def test_import_happy_path(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        school_id = prepare_school(session)
        file = tmp_path / 'teachers.xlsx'
        make_excel(file)

        report = import_teachers_from_file(str(file), session)
        assert report.teachers_created == 2
        assert report.subjects_created == 4
        assert report.classes_created == 4
        assert report.teacher_subjects_created == 4
        assert report.class_teachers_created == 5

        teachers = session.query(Teacher).all()
        assert len(teachers) == 2
        assert session.query(ClassTeacher).filter_by(role=ClassTeacherRole.homeroom).count() == 1
        assert session.query(AcademicYear).filter_by(name='2024/2025').count() == 1
        session.close()


def test_reimport_no_duplicates(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        school_id = prepare_school(session)
        file = tmp_path / 'teachers.xlsx'
        make_excel(file)

        import_teachers_from_file(str(file), session)
        report = import_teachers_from_file(str(file), session)
        assert report.teachers_created == 0
        assert session.query(Teacher).count() == 2
        session.close()


def test_dry_run(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        school_id = prepare_school(session)
        file = tmp_path / 'teachers.xlsx'
        make_excel(file)

        report = import_teachers_from_file(str(file), session, dry_run=True)
        assert session.query(Teacher).count() == 0
        assert report.teachers_created == 2
        session.close()


def test_homeroom_conflict(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        school_id = prepare_school(session)
        file = tmp_path / 'teachers.xlsx'
        make_excel(file)
        import_teachers_from_file(str(file), session)

        df = pd.DataFrame(
            [
                {
                    'ФИО педагога': 'Another',
                    'Классный руководитель': '1G',
                    'Предмет': 'Other',
                    'Класс': '1G',
                }
            ]
        )
        file2 = tmp_path / 'conflict.xlsx'
        with pd.ExcelWriter(file2, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name='Справочник педагоги', index=False, startrow=2)
            ws = writer.sheets['Справочник педагоги']
            ws.cell(row=1, column=1, value='Педагоги 2024/2025')
            ws.cell(row=2, column=1, value='Test School')
        try:
            import_teachers_from_file(str(file2), session)
        except ValueError:
            pass
        else:
            assert False, 'conflict not raised'
        session.close()

