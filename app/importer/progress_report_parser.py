from __future__ import annotations

import re
from datetime import date
from typing import Dict, Iterator, List, Tuple

import pandas as pd

from models.grade import GradeKindEnum, TermTypeEnum
from models.attendance import AttendanceStatusEnum

from .base import BaseParser, ParsedRow
from .constants import STATUS_CHAR_MAP, split_cell

MONTH_MAP = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12,
}


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

    def _find_period_back(
        self, df: pd.DataFrame, start_idx: int
    ) -> Tuple[int | None, date | None, date | None]:
        """Search backwards from ``start_idx`` for a period definition."""
        pattern = r"Период:?\s+с\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})\s+по\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})"
        for idx in range(start_idx, -1, -1):
            for col in range(len(df.columns)):
                val = df.iloc[idx, col]
                if isinstance(val, str):
                    m = re.search(pattern, val)
                    if m:
                        start = pd.to_datetime(m.group(1), dayfirst=True).date()
                        end = pd.to_datetime(m.group(2), dayfirst=True).date()
                        return idx, start, end
        return None, None, None

    def _parse_year_range(self, year: str) -> Tuple[int, int]:
        """Return start and end years for an academic year string."""
        nums = [int(n) for n in re.findall(r"\d+", year)]
        if len(nums) >= 2:
            y1, y2 = nums[0], nums[1]
        elif nums:
            y1 = nums[0]
            y2 = y1 + 1
        else:
            y1 = date.today().year
            y2 = y1 + 1
        if y1 < 100:
            y1 += 2000
        if y2 < 100:
            base = (y1 // 100) * 100
            y2 += base
            if y2 < y1:
                y2 += 100
        return y1, y2

    def _map_dates(
        self, month_row: pd.Series, day_row: pd.Series, academic_year: str
    ) -> Dict[int, date]:
        """Return mapping of column index to actual lesson date."""
        year_start, year_end = self._parse_year_range(academic_year)
        mapping: Dict[int, date] = {}
        current_month: int | None = None
        for col in range(1, len(day_row)):
            m_val = month_row[col]
            if isinstance(m_val, str):
                name = m_val.strip().lower()
                if name in MONTH_MAP:
                    current_month = MONTH_MAP[name]
            d_val = day_row[col]
            if pd.isna(d_val) or current_month is None:
                continue
            try:
                day_num = int(float(d_val))
            except Exception:
                continue
            year = year_start if current_month >= 9 else year_end
            try:
                mapping[col] = date(year, current_month, day_num)
            except Exception:
                continue
        return mapping

    def _get_term_info(self, lesson_date: date) -> Tuple[TermTypeEnum, int]:
        """Return the term type and index for a lesson date.

        Months September-October are mapped to quarter 1, November-December to
        quarter 2, January-March to quarter 3 and April-May to quarter 4. If the
        date falls outside of these ranges, it is treated as a year grade.
        """

        month = lesson_date.month
        if month in (9, 10):
            return TermTypeEnum.quarter, 1
        if month in (11, 12):
            return TermTypeEnum.quarter, 2
        if month in (1, 2, 3):
            return TermTypeEnum.quarter, 3
        if month in (4, 5):
            return TermTypeEnum.quarter, 4
        return TermTypeEnum.year, 1

    def _find_period(
        self, df: pd.DataFrame
    ) -> Tuple[int | None, str | None, date | None, date | None]:
        """Return row index, academic year name and start/end dates."""
        pattern = (
            r"Период:?\s+с\s+(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})\s+по\s+"
            r"(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})"
        )
        for idx in range(len(df)):
            for col in range(len(df.columns)):
                val = df.iloc[idx, col]
                if isinstance(val, str):
                    m = re.search(pattern, val)
                    if m:
                        start = pd.to_datetime(m.group(1), dayfirst=True).date()
                        end = pd.to_datetime(m.group(2), dayfirst=True).date()
                        if start.month >= 9:
                            y1 = start.year
                        else:
                            y1 = start.year - 1
                        year_name = f"{y1}/{y1 + 1}"
                        return idx, year_name, start, end
        return None, None, None, None

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

        has_student_mark = df.apply(
            lambda r: r.astype(str)
            .str.contains("Ученик:", case=False, na=False)
            .any(),
            axis=1,
        ).any()

        if not has_student_mark:
            # old single-table format
            period_row, period_year, start, _end = self._find_period(df)
            if period_row is None:
                return
            header_row = None
            for idx in range(period_row, min(period_row + 5, len(df))):
                row = df.iloc[idx]
                if any(
                    isinstance(val, str) and "предмет" in val.lower() for val in row
                ):
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
            if not academic_year:
                academic_year = period_year or ""
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
                    if val is None or (
                        isinstance(val, float) and pd.isna(val)
                    ):
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
                            tt, ti = self._get_term_info(day)
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
                                term_type=tt.value,
                                term_index=ti,
                                attendance_status=None,
                                minutes_late=None,
                                comment=None,
                            )
            return

        # multi-section format with repeated "Ученик:" rows
        idx = 0
        while idx < len(df):
            student_idx = None
            for j in range(idx, len(df)):
                row = df.iloc[j]
                if any(
                    isinstance(val, str) and "ученик" in val.lower() for val in row
                ):
                    student_idx = j
                    break
            if student_idx is None:
                break

            student_line = df.iloc[student_idx]
            student = ""
            for val in student_line:
                if isinstance(val, str) and "ученик" in val.lower():
                    m = re.search(r"Ученик[:\s]*(.+)", val, re.I)
                    student = m.group(1).strip() if m else val.strip()
                    break

            period_row, start, _end = self._find_period_back(df, student_idx)
            if period_row is None:
                idx = student_idx + 1
                continue

            header_row = None
            for j in range(student_idx, min(student_idx + 10, len(df))):
                row = df.iloc[j]
                if any(
                    isinstance(val, str) and "предмет" in val.lower() for val in row
                ):
                    header_row = j
                    break

            if header_row is None or header_row + 2 >= len(df):
                idx = student_idx + 1
                continue

            academic_year, class_name = self._extract_info(df, period_row)
            if not academic_year and start is not None:
                if start.month >= 9:
                    y1 = start.year
                else:
                    y1 = start.year - 1
                academic_year = f"{y1}/{y1 + 1}"

            month_row = df.iloc[header_row]
            date_row = df.iloc[header_row + 1]
            dates = self._map_dates(month_row, date_row, academic_year)

            row_idx = header_row + 2
            while row_idx < len(df):
                row = df.iloc[row_idx]
                subj_name = str(row[0]).strip()
                if not subj_name:
                    row_idx += 1
                    continue
                low = subj_name.lower()
                if any(k in low for k in ["учебный", "класс", "ученик", "период", "предмет"]):
                    break
                if subj_name in {"Н", "О", "Б", "У"}:
                    row_idx += 1
                    continue
                subj_id = self.subject_map.get(subj_name, 0)
                for col, day in dates.items():
                    val = row[col]
                    if val is None or (
                        isinstance(val, float) and pd.isna(val)
                    ):
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
                            tt, ti = self._get_term_info(day)
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
                                term_type=tt.value,
                                term_index=ti,
                                attendance_status=None,
                                minutes_late=None,
                                comment=None,
                            )
                row_idx += 1
            idx = row_idx
