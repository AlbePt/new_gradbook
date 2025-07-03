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
        term_type = None
        term_index = None
        grade_kind: GradeKindEnum | None = None

        if "четвер" in s:
            term_type = TermTypeEnum.quarter
        elif "трим" in s:
            term_type = TermTypeEnum.trimester
        elif "семестр" in s or "полугод" in s:
            term_type = TermTypeEnum.semester
        elif "год" in s:
            term_type = TermTypeEnum.year
            term_index = 1
            grade_kind = GradeKindEnum.year_final
            return term_type, term_index, grade_kind
        if "экз" in s:
            term_type = term_type or TermTypeEnum.year
            term_index = term_index or 1
            grade_kind = GradeKindEnum.exam
            return term_type, term_index, grade_kind
        if term_type is None:
            return None, None, None
        m = re.search(r"(\d+)", s)
        if m:
            term_index = int(m.group(1))
        else:
            term_index = 1
        if "ср" in s or "avg" in s or "бал" in s:
            grade_kind = GradeKindEnum.avg
        else:
            grade_kind = GradeKindEnum.period_final
        return term_type, term_index, grade_kind

    def _map_columns(
        self, headers: pd.Series
    ) -> Dict[int, Tuple[TermTypeEnum, int, GradeKindEnum]]:
        """Map header columns to grade parameters."""
        mapping: Dict[int, Tuple[TermTypeEnum, int, GradeKindEnum]] = {}
        for col in range(1, len(headers)):
            term_type, term_index, grade_kind = self._parse_header(str(headers[col]))
            if term_type is not None and grade_kind is not None:
                mapping[col] = (term_type, term_index, grade_kind)
        return mapping

    def parse(self) -> Iterator[ParsedRow]:
        df = pd.read_excel(self.path, header=None)
        header_idx = self._find_header_row(df)
        if header_idx is None:
            return

        academic_year, class_name, student_name = self._extract_info(df, header_idx)

        headers = df.iloc[header_idx]
        mapping = self._map_columns(headers)
        for row_idx in range(header_idx + 1, len(df)):
            row = df.iloc[row_idx]
            subject = row[0]
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
