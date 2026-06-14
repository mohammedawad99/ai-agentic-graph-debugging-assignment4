"""Token/size accounting for the graph-guided workflow.

Single estimation method, consistent with the Stage 8 baseline (D-011):
    estimated_tokens = characters / 4   (an estimate, NOT exact API tokenization)
"""

from __future__ import annotations

from dataclasses import dataclass, field

TOKEN_METHOD = "estimated_tokens = characters / 4  (approximation; NOT exact API tokenization)"


def estimate_tokens(characters: int) -> int:
    """Estimate tokens from a character count (chars / 4, rounded)."""
    return round(characters / 4)


@dataclass
class ReadRecord:
    """One tracked context read (graphify / obsidian / source)."""

    path: str
    source_type: str  # "graphify" | "obsidian" | "source"
    reason: str
    characters: int
    start_line: int | None = None
    end_line: int | None = None

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "source_type": self.source_type,
            "reason": self.reason,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "characters": self.characters,
            "estimated_tokens_chars_div_4": estimate_tokens(self.characters),
        }


@dataclass
class MetricsAccumulator:
    """Collect read records and summarize totals."""

    records: list[ReadRecord] = field(default_factory=list)

    def add(self, record: ReadRecord) -> ReadRecord:
        self.records.append(record)
        return record

    @property
    def total_characters(self) -> int:
        return sum(r.characters for r in self.records)

    @property
    def files(self) -> set[str]:
        return {r.path for r in self.records}

    def summary(self) -> dict:
        chars = self.total_characters
        return {
            "method": TOKEN_METHOD,
            "total_files_read": len(self.files),
            "total_text_units_read": len(self.records),
            "total_characters_read": chars,
            "estimated_tokens": estimate_tokens(chars),
            "records": [r.as_dict() for r in self.records],
        }
