from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterator, List, Tuple

import pandas as pd

from models.grade import GradeKindEnum, TermTypeEnum
from models.attendance import AttendanceStatusEnum

from .base import BaseParser, ParsedRow
from .constants import STATUS_CHAR_MAP, split_cell


class ProgressReportParser(BaseParser):
    """Parse progress report tables exported to XLSX."""

    def __init__(self, path: str, class_id: int = 0, subject_map: Dict[str, int] | None = None) -> None:
        self.path = path
        self.class_id = class_id
        self.subject_map = subject_map or {}
        self._event_cache: Dict[Tuple[date, int, int], int] = {}
        self._next_event_id = 1

    def _get_event_id(self, day: date, subject_id: int) -> int:
        key = (day, subject_id, self.class_id)
        if key not in self._event_cache:
            self._event_cache[key] = self._next_event_id
            self._next_event_id += 1
        return self._event_cache[key]

    def _find_period(self, df: pd.DataFrame) -> Tuple[int | None, date | None, date | None]:
        pattern = r"Период:?\s+с\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})\s+по\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})"
        for idx in range(len(df)):
            for col in range(len(df.columns)):
                val = df.iloc[idx, col]
                if isinstance(val, str):
                    m = re.search(pattern, val)
                    if m:
                        start = pd.to_datetime(m.group(1), dayfirst=True).date()
                        end = pd.to_datetime(m.group(2), dayfirst=True).date()
                        return idx, start, end
        return None, None, None

    def _extract_info(self, df: pd.DataFrame, header_idx: int) -> tuple[str, str]:
        """Return academic year and class name from rows above header."""
        academic_year = ""
        class_name = ""
        year_re = re.compile(r"учебный\s*год[:\s]*([\d/\\-]+)", re.I)
        class_re = re.compile(r"класс[:\s]*([^\s]+)", re.I)

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
            if academic_year and class_name:
                break
        return academic_year, class_name

    def parse(self) -> Iterator[ParsedRow]:
        df = pd.read_excel(self.path, header=None)
        period_row, start, _end = self._find_period(df)
        if period_row is None:
            return
        header_row = None
        for idx in range(period_row, min(period_row + 5, len(df))):
            row = df.iloc[idx]
            if any(isinstance(val, str) and "предмет" in val.lower() for val in row):
                header_row = idx
                break
        if header_row is None:
            if period_row + 2 >= len(df):
                return
            date_row = df.iloc[period_row + 1]
            subj_row = df.iloc[period_row + 2]
        else:
            if header_row + 2 >= len(df):
                return
            date_row = df.iloc[header_row + 1]
            subj_row = df.iloc[header_row + 2]

        academic_year, class_name = self._extract_info(df, period_row)
        if not academic_year and start is not None:
            if start.month >= 9:
                y1 = start.year
            else:
                y1 = start.year - 1
            academic_year = f"{y1}/{y1 + 1}"
        headers: List[Tuple[int, date, str, int]] = []
        for col in range(1, len(df.columns)):
            d_raw = date_row[col]
            s_raw = subj_row[col]
            if pd.isna(d_raw) or pd.isna(s_raw):
                continue
            try:
                day = pd.to_datetime(str(d_raw), dayfirst=True).date()
            except Exception:
                continue
            subj_name = str(s_raw).strip()
            if not subj_name:
                continue
            subj_id = self.subject_map.get(subj_name, 0)
            headers.append((col, day, subj_name, subj_id))
        for row_idx in range(period_row + 3, len(df)):
            row = df.iloc[row_idx]
            student = str(row[0]).strip()
            if not student:
                continue
            for col, day, subj_name, subj_id in headers:
                val = row[col]
                if val is None or (isinstance(val, float) and pd.isna(val)):
                    continue
                cell_parts = split_cell(str(val))
                if not cell_parts:
                    continue
                event_id = self._get_event_id(day, subj_id)
                for part in cell_parts:
                    if part in STATUS_CHAR_MAP:
                        status_str = STATUS_CHAR_MAP[part]
                        yield ParsedRow(
                            student_name=student,
                            class_name=class_name,
                            academic_year_name=academic_year,
                            subject_name=subj_name,
                            teacher_name="",
                            lesson_date=day,
                            lesson_index=event_id,
                            grade_value=None,
                            grade_kind=None,
                            term_type=None,
                            term_index=None,
                            attendance_status=status_str,
                            minutes_late=None,
                            comment=None,
                        )
                    else:
                        try:
                            num = float(part.replace(",", "."))
                        except ValueError:
                            continue
                        yield ParsedRow(
                            student_name=student,
                            class_name=class_name,
                            academic_year_name=academic_year,
                            subject_name=subj_name,
                            teacher_name="",
                            lesson_date=day,
                            lesson_index=event_id,
                            grade_value=num,
                            grade_kind=GradeKindEnum.regular.value,
                            term_type=TermTypeEnum.year.value,
                            term_index=1,
                            attendance_status=None,
                            minutes_late=None,
                            comment=None,
                        )
