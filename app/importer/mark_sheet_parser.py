from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterator, Tuple

import pandas as pd

from backend.schemas.grade import GradeCreate
from models.grade import GradeKindEnum, TermTypeEnum

from .base import BaseParser


class MarkSheetParser(BaseParser):
    """Parse "Табель" mark sheets exported to XLSX."""

    def __init__(self, path: str) -> None:
        self.path = path

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

    def parse(self) -> Iterator[GradeCreate]:
        df = pd.read_excel(self.path, header=None)
        header_idx = self._find_header_row(df)
        if header_idx is None:
            return
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
                yield GradeCreate.model_construct(
                    value=num,
                    date=date.today(),
                    student_id=0,
                    teacher_id=0,
                    subject_id=0,
                    term_type=tt,
                    term_index=ti,
                    grade_kind=gk,
                    lesson_event_id=None,
                )
