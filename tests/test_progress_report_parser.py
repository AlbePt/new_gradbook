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

from datetime import date

from app.importer.progress_report_parser import ProgressReportParser
from app.importer.base import ParsedRow
from models.grade import GradeKindEnum


def make_file(path: Path) -> None:
    """Create a small XLSX file emulating the real ``Отчёт`` format."""
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None],
            ["Класс: 1A", None, None],
            ["Период с 01.09.2024 по 02.09.2024", None, None],
            ["Ученик: Kid1", None, None],
            ["Предмет", "сентябрь", "сентябрь"],
            ["", 1, 2],
            ["Math", "5/Н", "4"],
            ["History", "Б", ""],
            ["Ученик: Kid2", None, None],
            ["Предмет", "сентябрь", "сентябрь"],
            ["", 1, 2],
            ["Math", "3", "4"],
            ["History", "О", ""],
        ]
    )
    df.to_excel(path, header=False, index=False)


def make_multi_file(path: Path) -> None:
    """File containing multiple grades in one cell."""
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None, None],
            ["Класс: 1A", None, None, None],
            ["Период с 01.09.2024 по 03.09.2024", None, None, None],
            ["Ученик: Kid", None, None, None],
            ["Предмет", "сентябрь", "сентябрь", "сентябрь"],
            ["", 1, 2, 3],
            ["Math", "4/3", "О 2", ""],
        ]
    )
    df.to_excel(path, header=False, index=False)


def make_single_period_file(path: Path) -> None:
    """Minimal file for single-table format."""
    df = pd.DataFrame(
        [
            ["Учебный год: 2025/2026", None, None],
            ["Класс: 2A", None, None],
            ["Период с 05.09.2025 по 07.09.2025", None, None],
        ]
    )
    df.to_excel(path, header=False, index=False)


def test_progress_report_parser(tmp_path):
    file = tmp_path / "report.xlsx"
    make_file(file)
    parser = ProgressReportParser(str(file))
    rows = list(parser.parse())
    assert len(rows) == 7

    first = rows[0]
    assert isinstance(first, ParsedRow)
    assert first.student_name == "Kid1"
    assert first.subject_name == "Math"
    assert first.lesson_date == date(2024, 9, 1)
    assert first.grade_kind == GradeKindEnum.regular.value
    assert first.grade_value == 5

    absent = rows[1]
    assert absent.attendance_status == "absent"
    assert absent.lesson_date == date(2024, 9, 1)

    kid2_day2 = rows[5]
    assert kid2_day2.student_name == "Kid2"
    assert kid2_day2.subject_name == "Math"
    assert kid2_day2.lesson_date == date(2024, 9, 2)
    assert kid2_day2.grade_value == 4

    history = rows[3]
    assert history.subject_name == "History"
    assert history.attendance_status == "sick"


def test_parser_multiple_grades(tmp_path):
    file = tmp_path / "multi.xlsx"
    make_multi_file(file)
    parser = ProgressReportParser(str(file))
    rows = list(parser.parse())
    # 4 rows: two grades for day1 and late+grade for day2
    assert len(rows) == 4
    grades = [r for r in rows if r.grade_value is not None]
    assert [g.grade_value for g in grades] == [4, 3, 2]
    statuses = [r.attendance_status for r in rows if r.attendance_status]
    assert statuses == ["late"]


def test_get_class_period_multi(tmp_path):
    file = tmp_path / "period.xlsx"
    make_file(file)
    parser = ProgressReportParser(str(file))
    cls, year, start, end = parser.get_class_period()
    assert cls == "1A"
    assert year == "2024/2025"
    assert start == date(2024, 9, 1)
    assert end == date(2024, 9, 2)


def test_get_class_period_single(tmp_path):
    file = tmp_path / "single.xlsx"
    make_single_period_file(file)
    parser = ProgressReportParser(str(file))
    cls, year, start, end = parser.get_class_period()
    assert cls == "2A"
    assert year == "2025/2026"
    assert start == date(2025, 9, 5)
    assert end == date(2025, 9, 7)
