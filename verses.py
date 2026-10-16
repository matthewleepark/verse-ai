"""Choosing each day's verse.

data/daily_verses.json lists 415 verses, each with a one-word title for the
poster. Day N of the calendar gets entry N % 415, so the verse changes every
day and doesn't repeat for over a year. The 40 wisdom verses below (which have
study notes) are part of that list and can also be picked by theme.
"""

from __future__ import annotations

import json
import random
from dataclasses import replace
from datetime import date
from functools import lru_cache
from pathlib import Path

from bible import Verse, lookup

DAILY_FILE = Path(__file__).parent / "data" / "daily_verses.json"

WISDOM_VERSES: dict[str, list[str]] = {
    "patience": [
        "James 1:19",
        "Proverbs 14:29",
        "Proverbs 16:32",
        "Proverbs 19:11",
        "Ecclesiastes 7:8",
        "Romans 12:12",
        "Galatians 6:9",
        "Colossians 3:12",
        "James 5:7",
        "Psalm 37:7",
    ],
    "empathy": [
        "Romans 12:15",
        "Galatians 6:2",
        "Philippians 2:4",
        "Luke 6:31",
        "1 Peter 3:8",
        "Ephesians 4:32",
        "Proverbs 31:8",
        "Matthew 25:40",
        "Hebrews 13:3",
        "1 John 3:17",
    ],
    "conflict resolution": [
        "Proverbs 15:1",
        "Proverbs 15:18",
        "Proverbs 17:14",
        "Proverbs 20:3",
        "Matthew 5:9",
        "Matthew 5:24",
        "Matthew 18:15",
        "Romans 12:18",
        "Ephesians 4:26",
        "Colossians 3:13",
    ],
    "integrity": [
        "Proverbs 10:9",
        "Proverbs 11:3",
        "Proverbs 12:22",
        "Proverbs 20:7",
        "Proverbs 22:1",
        "Psalm 15:2",
        "Micah 6:8",
        "Luke 16:10",
        "Matthew 5:37",
        "Titus 2:7",
    ],
}

THEMES = list(WISDOM_VERSES)


@lru_cache(maxsize=1)
def daily_list() -> list[dict[str, str]]:
    """[{"ref": "Isaiah 43:2", "word": "WATERS"}, ...] in calendar order."""
    with DAILY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _words() -> dict[str, str]:
    return {entry["ref"]: entry["word"] for entry in daily_list()}


def theme_of(reference: str) -> str | None:
    return next((t for t, refs in WISDOM_VERSES.items() if reference in refs), None)


def entry_for(day: date) -> dict[str, str]:
    entries = daily_list()
    return entries[day.toordinal() % len(entries)]


def pick_reference(day: date | None = None, theme: str | None = None) -> str:
    """The day's reference: from the daily list, or from one wisdom theme."""
    day = day or date.today()
    if theme is None:
        return entry_for(day)["ref"]
    if theme not in WISDOM_VERSES:
        raise ValueError(f"Unknown theme {theme!r}. Choose from: {', '.join(THEMES)}")
    refs = WISDOM_VERSES[theme]
    return refs[day.toordinal() % len(refs)]


def get_verse(
    day: date | None = None,
    theme: str | None = None,
    reference: str | None = None,
    shuffle: bool = False,
) -> Verse:
    """The verse to study. Same day -> same verse, unless shuffle=True."""
    if reference:
        verse = lookup(reference)
    elif shuffle:
        pool = WISDOM_VERSES[theme] if theme else [e["ref"] for e in daily_list()]
        verse = lookup(random.choice(pool))
    else:
        verse = lookup(pick_reference(day, theme))
    return replace(
        verse,
        theme=theme_of(verse.reference),
        word=_words().get(verse.reference, "FAITH"),
    )
