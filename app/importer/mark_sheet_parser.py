from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterator, Tuple

import pandas as pd

from models.grade import GradeKindEnum, TermTypeEnum

from .base import BaseParser, ParsedRow


class MarkSheetParser(BaseParser):
    """Parse "Табель" mark sheets exported to XLSX."""

    def __init__(self, path: str) -> None:
        self.path = path

    def _extract_info(self, df: pd.DataFrame, header_idx: int) -> tuple[str, str, str]:
        """Return academic year, class name and student name from rows above header."""
        academic_year = ""
        class_name = ""
        student_name = ""
        year_re = re.compile(r"учебный\s*год[:\s]*([\d/\\-]+)", re.I)
        class_re = re.compile(r"класс[:\s]*([^\s]+)", re.I)
        student_re = re.compile(r"ученик[:\s]*(.+)", re.I)
        for idx in range(header_idx - 1, -1, -1):
            row = df.iloc[idx]
            text = " ".join(str(c) for c in row if isinstance(c, str))
            if not academic_year:
                m = year_re.search(text)
                if m:
                    academic_year = m.group(1).strip()
            if not class_name:
                m = class_re.search(text)
                if m:
                    class_name = m.group(1).strip()
            if not student_name:
                m = student_re.search(text)
                if m:
                    student_name = m.group(1).strip()
            if academic_year and class_name and student_name:
                break
        return academic_year, class_name, student_name

    def _find_header_row(self, df: pd.DataFrame) -> int | None:
        for idx in range(len(df)):
            row = df.iloc[idx]
            if any(isinstance(cell, str) and "предмет" in cell.lower() for cell in row):
                return idx
        return None

    def _parse_header(self, header: str) -> Tuple[TermTypeEnum | None, int | None, GradeKindEnum | None]:
        if not isinstance(header, str):
            return None, None, None

        s = header.lower()

        term_type: TermTypeEnum | None = None
        term_index: int | None = None

        if "четвер" in s:
            term_type = TermTypeEnum.quarter
        elif "трим" in s:
            term_type = TermTypeEnum.trimester
        elif "семестр" in s or "полугод" in s:
            term_type = TermTypeEnum.semester
        elif "год" in s:
            term_type = TermTypeEnum.year
            term_index = 1

        if "экз" in s:
            term_type = term_type or TermTypeEnum.year
            term_index = term_index or 1
            grade_kind = GradeKindEnum.exam
            return term_type, term_index, grade_kind

        if term_index is None:
            m = re.search(r"(\d+)", s)
            if m:
                term_index = int(m.group(1))

        if "взв" in s or "взвеш" in s:
            grade_kind = GradeKindEnum.weighted_avg
        elif "ср" in s or "avg" in s or "бал" in s:
            grade_kind = GradeKindEnum.avg
        elif term_type == TermTypeEnum.year:
            grade_kind = GradeKindEnum.year_final
        elif "итог" in s:
            grade_kind = GradeKindEnum.period_final
        elif term_type is not None:
            grade_kind = GradeKindEnum.period_final
        else:
            grade_kind = None

        return term_type, term_index, grade_kind

    def _find_subject_column(self, headers: pd.Series) -> int:
        """Return the index of the column that contains the subject name."""
        for idx, cell in enumerate(headers):
            if isinstance(cell, str) and "предмет" in cell.lower():
                return idx
        return 0

    def _map_columns(
        self, df: pd.DataFrame, header_idx: int, subject_col: int
    ) -> Dict[int, Tuple[TermTypeEnum, int, GradeKindEnum]]:
        """Map header columns to grade parameters.

        This method supports multi-line headers by joining up to three
        subsequent rows after the header row and parsing the combined text.
        """

        rows = [df.iloc[header_idx]]
        for i in range(1, 4):
            if header_idx + i < len(df):
                rows.append(df.iloc[header_idx + i])

        mapping: Dict[int, Tuple[TermTypeEnum, int, GradeKindEnum]] = {}
        last_tt: TermTypeEnum | None = None
        last_ti: int | None = None
        for col in range(subject_col + 1, len(df.columns)):
            parts = []
            for row in rows:
                val = row[col]
                if isinstance(val, str):
                    val = val.strip()
                    if val:
                        parts.append(val)
            header_text = " ".join(parts)
            term_type, term_index, grade_kind = self._parse_header(header_text)
            if term_type is None:
                term_type = last_tt
            if term_index is None:
                term_index = last_ti
            if term_type is not None and grade_kind is not None:
                mapping[col] = (term_type, term_index or 1, grade_kind)
                last_tt = term_type
                last_ti = term_index
        return mapping

    def parse(self) -> Iterator[ParsedRow]:
        df = pd.read_excel(self.path, header=None)
        header_idx = self._find_header_row(df)
        if header_idx is None:
            return

        academic_year, class_name, student_name = self._extract_info(df, header_idx)

        headers = df.iloc[header_idx]
        subject_col = self._find_subject_column(headers)
        mapping = self._map_columns(df, header_idx, subject_col)
        for row_idx in range(header_idx + 1, len(df)):
            row = df.iloc[row_idx]
            subject = row[subject_col]
            if not isinstance(subject, str) or not subject.strip():
                continue
            for col, (tt, ti, gk) in mapping.items():
                val = row[col]
                if pd.isna(val):
                    continue
                try:
                    num = float(str(val).replace(",", "."))
                except ValueError:
                    continue
                yield ParsedRow(
                    student_name=student_name,
                    class_name=class_name,
                    academic_year_name=academic_year,
                    subject_name=str(subject).strip(),
                    teacher_name="",
                    lesson_date=date.today(),
                    grade_value=num,
                    grade_kind=gk.value,
                    term_type=tt.value,
                    term_index=ti,
                    lesson_index=None,
                    attendance_status=None,
                    minutes_late=None,
                    comment=None,
                )
