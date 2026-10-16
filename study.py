"""Offline study content: notes for the wisdom verses, book background,
reflection questions, and the daily reading plan. All stored in data/*.json.
"""

from __future__ import annotations

import json
from datetime import date
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Proverbs has 31 chapters, one for each day of the month.
READING_BOOK = "Proverbs"


@lru_cache(maxsize=None)
def _load(name: str) -> dict:
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def notes_for(reference: str) -> dict[str, str] | None:
    """Study notes ({wisdom, context, meaning}) for a curated verse, else None."""
    return _load("study_notes.json").get(reference)


def book_info(book: str) -> dict[str, str] | None:
    """Background for a book of the Bible: {type, author, date, about}."""
    return _load("books.json").get(book)


def all_books() -> dict[str, dict[str, str]]:
    return _load("books.json")


def reflection_question(theme: str | None, day: date) -> str:
    """One question per day, rotating through the theme's list."""
    questions = _load("reflections.json")
    pool = questions.get(theme or "", questions["general"])
    return pool[day.toordinal() % len(pool)]


def reading_for(day: date) -> tuple[str, int]:
    """Today's reading: the Proverbs chapter matching the day of the month."""
    return READING_BOOK, day.day
