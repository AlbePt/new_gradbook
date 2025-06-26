import os
import sys
import time
from pathlib import Path

import pandas as pd
import pytest
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

from app.import_teachers.service import import_teachers_from_file
from backend.core.db import Base
from models import Region, City, School


def run_migrations(url: str) -> None:
    os.environ["DATABASE_URL"] = url
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


@pytest.mark.skipif(os.environ.get("CI") and not os.environ.get("PERF"), reason="no perf")
def test_large_import_perf(tmp_path):
    with testing.postgresql.Postgresql() as pg:
        run_migrations(pg.url())
        engine = create_engine(pg.url())
        Session = sessionmaker(bind=engine)
        session = Session()
        region = Region(name="R")
        city = City(name="C", region=region)
        school = School(name="S", full_name="Test School", city=city)
        session.add_all([region, city, school])
        session.commit()

        teachers = [f"T{i}" for i in range(100)]
        subjects = [f"S{i}" for i in range(20)]
        classes = [f"{i}A" for i in range(5)]
        rows = [
            {
                "ФИО педагога": teachers[i % len(teachers)],
                "Классный руководитель": "",
                "Предмет": subjects[i % len(subjects)],
                "Класс": classes[i % len(classes)],
            }
            for i in range(10000)
        ]
        file = tmp_path / "large.xlsx"
        df = pd.DataFrame(rows)
        with pd.ExcelWriter(file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Справочник педагоги", index=False, startrow=2)
            ws = writer.sheets["Справочник педагоги"]
            ws.cell(row=1, column=1, value="Педагоги 2024/2025")
            ws.cell(row=2, column=1, value="Test School")
        start = time.perf_counter()
        import_teachers_from_file(str(file), session)
        duration = time.perf_counter() - start
        assert duration < 8
        session.close()
