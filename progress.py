"""Study history and streaks, saved locally in progress.json.

A day counts as "studied" once you finish the reading or write a journal entry.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

PROGRESS_FILE = Path(__file__).parent / "progress.json"


@dataclass(frozen=True)
class DayRecord:
    day: date
    reference: str
    read: bool = False
    journaled: bool = False

    @property
    def studied(self) -> bool:
        return self.read or self.journaled


def _read(path: Path) -> dict[str, dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def record(
    day: date,
    reference: str,
    *,
    read: bool = False,
    journaled: bool = False,
    path: Path = PROGRESS_FILE,
) -> None:
    """Save the day's verse; read/journaled flags only ever turn on, never off."""
    data = _read(path)
    entry = data.get(day.isoformat(), {})
    data[day.isoformat()] = {
        "reference": reference,
        "read": entry.get("read", False) or read,
        "journaled": entry.get("journaled", False) or journaled,
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def history(path: Path = PROGRESS_FILE) -> list[DayRecord]:
    """All recorded days, newest first."""
    return [
        DayRecord(date.fromisoformat(d), e.get("reference", "?"), e["read"], e["journaled"])
        for d, e in sorted(_read(path).items(), reverse=True)
    ]


def streak(today: date, path: Path = PROGRESS_FILE) -> int:
    """Consecutive studied days ending today (or yesterday, if today isn't done yet)."""
    studied = {r.day for r in history(path) if r.studied}
    day = today if today in studied else today - timedelta(days=1)
    count = 0
    while day in studied:
        count += 1
        day -= timedelta(days=1)
    return count


def studied_on(day: date, path: Path = PROGRESS_FILE) -> bool:
    return any(r.day == day and r.studied for r in history(path))
