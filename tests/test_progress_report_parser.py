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

from app.importer.progress_report_parser import ProgressReportParser
from app.importer.base import ParsedRow
from models.grade import GradeKindEnum

def make_file(path: Path) -> None:
    df = pd.DataFrame(
        [
            ["Период с 01.09.2024 по 02.09.2024", None, None],
            ["", "01.09.2024", "02.09.2024"],
            ["ФИО", "Math", "Math"],
            ["Student", "Н/5", "4"],
        ]
    )
    df.to_excel(path, header=False, index=False)


def test_progress_report_parser(tmp_path):
    file = tmp_path / "report.xlsx"
    make_file(file)
    parser = ProgressReportParser(str(file))
    batches = list(parser.iter_batches(10))
    items = [item for batch in batches for item in batch]
    assert len(items) == 3
    assert isinstance(items[0], ParsedRow)
    assert items[0].academic_year_name == "2024/2025"
    assert items[0].attendance_status == "absent"
    assert isinstance(items[1], ParsedRow)
    assert items[1].grade_kind == GradeKindEnum.regular.value
    assert items[1].term_type == "quarter"
    assert items[1].term_index == 1
    assert items[1].grade_value == 5
    assert isinstance(items[2], ParsedRow)
    assert items[2].term_type == "quarter"
    assert items[2].term_index == 1
    assert items[2].grade_value == 4
