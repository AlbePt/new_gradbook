STATUS_CHAR_MAP = {
    "Н": "absent",
    "Б": "sick",
    "У": "excused",
    "О": "late",
}


def split_cell(value: str) -> list[str]:
    return [part.strip() for part in str(value).split("/") if part and part.strip()]


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
