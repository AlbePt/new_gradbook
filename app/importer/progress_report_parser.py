from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterator, List, Tuple, Any

import pandas as pd

from backend.schemas.grade import GradeCreate
from backend.schemas.attendance import AttendanceCreate
from models.grade import GradeKindEnum, TermTypeEnum
from models.attendance import AttendanceStatusEnum

from .base import BaseParser
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
        pattern = r"Период\s+с\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})\s+по\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})"
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

    def parse(self) -> Iterator[Any]:
        df = pd.read_excel(self.path, header=None)
        period_row, start, end = self._find_period(df)
        if period_row is None:
            return
        # assume next row contains dates, then subjects
        if period_row + 2 >= len(df):
            return
        date_row = df.iloc[period_row + 1]
        subj_row = df.iloc[period_row + 2]
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
                        status = AttendanceStatusEnum(status_str)
                        yield AttendanceCreate.model_construct(
                            date=day,
                            status=status,
                            minutes_late=None,
                            comment=None,
                            student_id=0,
                            lesson_event_id=event_id,
                        )
                    else:
                        try:
                            num = float(part.replace(",", "."))
                        except ValueError:
                            continue
                        yield GradeCreate.model_construct(
                            value=num,
                            date=day,
                            student_id=0,
                            teacher_id=0,
                            subject_id=subj_id,
                            term_type=TermTypeEnum.year,
                            term_index=1,
                            grade_kind=GradeKindEnum.regular,
                            lesson_event_id=event_id,
                        )
