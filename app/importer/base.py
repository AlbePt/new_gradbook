from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Iterator, Optional, List


@dataclass
class ParsedRow:
    """Container for raw data parsed from import files."""

    student_name: str
    class_name: str
    subject_name: str
    teacher_name: str
    lesson_date: date
    lesson_index: Optional[int] = None
    grade_value: Optional[float] = None
    grade_kind: Optional[str] = None
    term_type: Optional[str] = None
    term_index: Optional[int] = None
    attendance_status: Optional[str] = None
    minutes_late: Optional[int] = None
    comment: Optional[str] = None


class BaseParser(ABC):
    """Abstract base parser for import files."""

    @abstractmethod
    def parse(self) -> Iterator[ParsedRow]:
        """Yield parsed rows from a file."""

    def iter_batches(self, size: int = 500) -> Iterator[List[ParsedRow]]:
        """Yield parsed rows in batches."""
        batch: List[ParsedRow] = []
        for row in self.parse():
            batch.append(row)
            if len(batch) >= size:
                yield batch
                batch = []
        if batch:
            yield batch
