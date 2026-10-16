"""The full Bible text, read from data/bsb.txt. Works fully offline.

The Berean Standard Bible (BSB) is dedicated to the public domain
(https://bereanbible.com), so it can ship with the project. The file is
tab-separated: "Genesis 1:1<TAB>In the beginning...".
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "bsb.txt"
TRANSLATION = "Berean Standard Bible"

_LINE = re.compile(r"^(.+ \d+:\d+)\t(.*)$")
_REFERENCE = re.compile(r"^\s*(.+?)\s+(\d+):(\d+)(?:\s*-\s*(\d+))?\s*$")
# The BSB uses "Psalm" and "Song of Solomon"; accept the other common spellings.
BOOK_ALIASES = {"psalms": "psalm", "song of songs": "song of solomon"}


class VerseNotFoundError(Exception):
    """Raised for unreadable or nonexistent references; message is user-facing."""


@dataclass(frozen=True)
class Verse:
    reference: str      # e.g. "James 1:19" or "Romans 12:9-12"
    text: str
    translation: str = TRANSLATION
    theme: str | None = None  # wisdom theme, set by verses.py
    word: str | None = None   # one-word title for the poster, set by verses.py


@lru_cache(maxsize=1)
def load() -> dict[str, str]:
    """Map "Book C:V" -> text, in canonical order.

    A few verses (e.g. Matthew 17:21) are missing from the oldest manuscripts;
    the BSB keeps their references with empty text.
    """
    try:
        with DATA_FILE.open(encoding="utf-8-sig") as f:
            matches = (_LINE.match(line.rstrip("\r\n")) for line in f)
            return {m.group(1): m.group(2).strip() for m in matches if m}
    except FileNotFoundError as e:
        raise VerseNotFoundError(f"Bible data file is missing: {DATA_FILE}") from e


@lru_cache(maxsize=1)
def _index() -> dict[str, str]:
    """Lowercase reference -> canonical reference, for case-insensitive lookup."""
    return {ref.lower(): ref for ref in load()}


@lru_cache(maxsize=1)
def _non_empty_references() -> tuple[str, ...]:
    return tuple(ref for ref, text in load().items() if text)


def _resolve(reference: str) -> tuple[str, int, int, int]:
    """Parse a reference into (canonical book name, chapter, first verse, last verse)."""
    match = _REFERENCE.match(reference)
    if not match:
        raise VerseNotFoundError(
            f"Can't read {reference!r}. Try a form like \"John 3:16\" or \"Romans 12:9-12\"."
        )
    book, chapter, start, end = match.groups()
    book = " ".join(book.split()).lower()
    book = BOOK_ALIASES.get(book, book)
    chapter, start = int(chapter), int(start)
    end = int(end) if end else start
    if end < start:
        raise VerseNotFoundError(f"Verse range in {reference!r} runs backwards.")

    index = _index()
    keys = [index.get(f"{book} {chapter}:{n}") for n in range(start, end + 1)]
    if None in keys:
        raise VerseNotFoundError(f"Reference not found: {reference!r}")
    return keys[0].rsplit(" ", 1)[0], chapter, start, end


def passage(book: str, chapter: int, start: int = 1, end: int = 176) -> list[tuple[int, str]]:
    """(verse number, text) for each verse in the range that exists and has text.

    The default range covers a whole chapter (the longest, Psalm 119, has 176 verses).
    """
    verses = load()
    lines = ((n, verses.get(f"{book} {chapter}:{n}")) for n in range(start, end + 1))
    return [(n, text) for n, text in lines if text]


def lookup(reference: str) -> Verse:
    """Look up "John 3:16" or a range within one chapter like "Romans 12:9-12"."""
    book, chapter, start, end = _resolve(reference)
    lines = passage(book, chapter, start, end)
    if not lines:
        raise VerseNotFoundError(
            f"{book} {chapter}:{start} isn't in the earliest manuscripts, so the BSB leaves it out."
        )
    canonical = f"{book} {chapter}:{start}" + (f"-{end}" if end != start else "")
    return Verse(canonical, " ".join(text for _, text in lines))


def context(reference: str, radius: int = 2) -> list[tuple[int, str]]:
    """The verses around a reference, within its chapter."""
    book, chapter, start, end = _resolve(reference)
    return passage(book, chapter, max(1, start - radius), end + radius)


def book_of(reference: str) -> str:
    """Canonical book name, e.g. "psalms 23:1" -> "Psalm"."""
    return _resolve(reference)[0]


def random_verse(rng: random.Random, exclude: frozenset[str] = frozenset()) -> Verse:
    """Pick a random non-empty verse; pass a seeded rng for repeatable picks."""
    references = _non_empty_references()
    while True:
        reference = rng.choice(references)
        if reference not in exclude:
            return Verse(reference, load()[reference])
