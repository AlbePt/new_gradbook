STATUS_CHAR_MAP = {
    "Н": "absent",
    "Б": "sick",
    "У": "excused",
    "О": "late",
}


import re


def split_cell(value: str) -> list[str]:
    """Return list of parts from a cell value.

    The original implementation only split on ``/`` which meant values like
    ``"О 2"`` were parsed as a single token. We now split on both ``/`` and
    whitespace so that mixed values are handled correctly.
    """

    parts = re.split(r"[\s/]+", str(value))
    return [part.strip() for part in parts if part and part.strip()]


from dataclasses import dataclass, field
from typing import List


@dataclass
class ImportSummary:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)

    def __iadd__(self, other: "ImportSummary") -> "ImportSummary":
        self.created += other.created
        self.updated += other.updated
        self.skipped += other.skipped
        self.errors.extend(other.errors)
        return self
