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

from app.importer.mark_sheet_parser import MarkSheetParser
from models.grade import TermTypeEnum, GradeKindEnum


def make_file(path: Path) -> None:
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None, None, None],
            ["Класс: 1A", None, None, None, None],
            ["Ученик: Kid", None, None, None, None],
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
    assert first.student_name == "Kid"
    assert first.class_name == "1A"
    assert first.academic_year_name == "2024/2025"
    assert first.subject_name == "Математика"
    assert first.term_type == "quarter"
    assert first.term_index == 1
    assert first.grade_kind == "period_final"
    assert first.grade_value == 5
    assert isinstance(first.lesson_date, date)

def test_map_columns():
    df = pd.DataFrame([["Предмет", "1 четверть", "1 четверть ср", "2 четверть", "Год"]])
    parser = MarkSheetParser("dummy")
    headers = df.iloc[0]
    subj_col = parser._find_subject_column(headers)
    mapping = parser._map_columns(df, 0, subj_col)
    assert mapping == {
        1: (TermTypeEnum.quarter, 1, GradeKindEnum.period_final),
        2: (TermTypeEnum.quarter, 1, GradeKindEnum.avg),
        3: (TermTypeEnum.quarter, 2, GradeKindEnum.period_final),
        4: (TermTypeEnum.year, 1, GradeKindEnum.year_final),
    }


def test_map_columns_multiline():
    df = pd.DataFrame(
        [
            [None, "Предмет", "Учебные периоды", None, "Год. оценка"],
            ["№", None, None, None, None],
            ["п/п", "1 четверть", "2 четверть", None, None],
            [None, "итог", "итог", None, None],
        ]
    )
    parser = MarkSheetParser("dummy")
    headers = df.iloc[0]
    subj_col = parser._find_subject_column(headers)
    mapping = parser._map_columns(df, 0, subj_col)
    assert mapping == {
        2: (TermTypeEnum.quarter, 2, GradeKindEnum.period_final),
        4: (TermTypeEnum.year, 1, GradeKindEnum.year_final),
    }


def test_parser_with_row_numbers(tmp_path):
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None, None, None, None],
            ["Класс: 1A", None, None, None, None, None],
            ["Ученик: Kid", None, None, None, None, None],
            ["№ п/п", "Предмет", "1 четверть", "1 четверть ср", "2 четверть", "Год"],
            [1, "Математика", 5, 4.5, 5, 5],
            [2, "История", 4, 4.0, 5, 5],
        ]
    )
    file = tmp_path / "rows.xlsx"
    df.to_excel(file, header=False, index=False)
    parser = MarkSheetParser(str(file))
    items = list(parser.parse())
    assert len(items) == 8
    assert items[0].subject_name == "Математика"


def test_parser_multiple_students(tmp_path):
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None],
            ["Класс: 1A", None, None],
            ["Ученик: Kid1", None, None],
            ["Предмет", "1 четверть", "Год"],
            ["Math", 5, 5],
            ["History", 4, 4],
            [None, None, None],
            ["Учебный год: 2024/2025", None, None],
            ["Класс: 1A", None, None],
            ["Ученик: Kid2", None, None],
            ["Предмет", "1 четверть", "Год"],
            ["Math", 3, 4],
            ["History", 4, 5],
        ]
    )
    file = tmp_path / "multi.xlsx"
    df.to_excel(file, header=False, index=False)
    parser = MarkSheetParser(str(file))
    items = list(parser.parse())
    assert len(items) == 8
    assert items[0].student_name == "Kid1"
    assert items[-1].student_name == "Kid2"


def test_parser_multiline_header(tmp_path):
    df = pd.DataFrame(
        [
            ["Учебный год: 2024/2025", None, None, None, None],
            ["Класс: 1A", None, None, None, None],
            ["Ученик: Kid", None, None, None, None],
            [None, "Предмет", "Учебные периоды", None, "Год. оценка"],
            ["№", None, None, None, None],
            ["п/п", "1 четверть", "2 четверть", None, None],
            [None, "итог", "итог", None, None],
            [1, "Математика", 5, 5, 5],
            [2, "История", 4, 5, 5],
        ]
    )
    file = tmp_path / "multi.xlsx"
    df.to_excel(file, header=False, index=False)
    parser = MarkSheetParser(str(file))
    items = list(parser.parse())
    assert len(items) == 4  # 2 subjects * (quarter + year)


def test_map_columns_weighted_avg():
    df = pd.DataFrame([["Предмет", "1 четверть", "1 четверть ср взв"]])
    parser = MarkSheetParser("dummy")
    headers = df.iloc[0]
    subj_col = parser._find_subject_column(headers)
    mapping = parser._map_columns(df, 0, subj_col)
    assert mapping == {
        1: (TermTypeEnum.quarter, 1, GradeKindEnum.period_final),
        2: (TermTypeEnum.quarter, 1, GradeKindEnum.weighted_avg),
    }


def test_map_columns_missing_period_info():
    df = pd.DataFrame(
        [
            ["Предмет", "Учебные периоды", None, None],
            ["№", None, None, None],
            ["п/п", "1 четверть", None, None],
            [None, "Средний балл", "Ср. взв. балл", "Итог"],
        ]
    )
    parser = MarkSheetParser("dummy")
    headers = df.iloc[0]
    subj_col = parser._find_subject_column(headers)
    mapping = parser._map_columns(df, 0, subj_col)
    assert mapping == {
        1: (TermTypeEnum.quarter, 1, GradeKindEnum.avg),
        2: (TermTypeEnum.quarter, 1, GradeKindEnum.weighted_avg),
        3: (TermTypeEnum.quarter, 1, GradeKindEnum.period_final),
    }


def test_map_columns_year_avg():
    df = pd.DataFrame([["Предмет", "Год ср", "Год ср взв", "Год"]])
    parser = MarkSheetParser("dummy")
    headers = df.iloc[0]
    subj_col = parser._find_subject_column(headers)
    mapping = parser._map_columns(df, 0, subj_col)
    assert mapping == {
        1: (TermTypeEnum.year, 1, GradeKindEnum.avg),
        2: (TermTypeEnum.year, 1, GradeKindEnum.weighted_avg),
        3: (TermTypeEnum.year, 1, GradeKindEnum.year_final),
    }
