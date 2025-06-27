import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
sys.path.append(str(ROOT / "backend"))

import pandas as pd

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/db")
os.environ.setdefault("SECRET_KEY", "x")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "db")
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "pass")

from app.importer.mark_sheet_parser import MarkSheetParser
from models.grade import TermTypeEnum, GradeKindEnum


def make_file(path: Path) -> None:
    df = pd.DataFrame(
        [
            ["Предмет", "1 четверть", "1 четверть ср", "2 четверть", "Год"],
            ["Математика", 5, 4.5, 5, 5],
            ["История", 4, 4.0, 5, 5],
        ]
    )
    df.to_excel(path, header=False, index=False)


def test_mark_sheet_parser(tmp_path):
    file = tmp_path / "marks.xlsx"
    make_file(file)
    parser = MarkSheetParser(str(file))
    items = list(parser.parse())
    assert len(items) == 8  # 2 subjects * 4 periods
    first = items[0]
    assert first.term_type == TermTypeEnum.quarter
    assert first.term_index == 1
    assert first.grade_kind == GradeKindEnum.period_final
    assert first.value == 5
    assert first.lesson_event_id is None
