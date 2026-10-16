"""Formatting for everything the app prints. Pure functions that return strings."""

from __future__ import annotations

import textwrap
from datetime import date

import bible
import study
from bible import Verse
from progress import DayRecord

WIDTH = 72
RULE = "=" * WIDTH


def wrap(text: str, indent: str = "  ") -> str:
    return textwrap.fill(text, width=WIDTH, initial_indent=indent, subsequent_indent=indent)


def format_passage(lines: list[tuple[int, str]], highlight: range | None = None) -> str:
    """Numbered verses; verses in `highlight` are marked with '>'."""
    out = []
    for n, text in lines:
        marker = ">" if highlight and n in highlight else " "
        out.append(textwrap.fill(
            text, width=WIDTH, initial_indent=f"{marker}{n:>3}  ", subsequent_indent="      "
        ))
    return "\n".join(out)


def format_book(book: str) -> str:
    info = study.book_info(book)
    if not info:
        return ""
    name = "Psalms" if book == "Psalm" else book  # BSB references say "Psalm 23:1"
    return wrap(
        f"About {name} ({info['type']}): {info['about']} "
        f"Author: {info['author']}. Date: {info['date']}."
    )


def format_header(day: date, streak: int, studied_today: bool, tracking: bool) -> str:
    title = f"  verse-ai  ·  {day:%A, %B} {day.day}, {day.year}"
    if not tracking:
        status = "  (Looking back at another day; streaks only count today.)"
    elif studied_today:
        status = f"  Streak: {streak} day{'s' * (streak != 1)}  ·  today is done!"
    elif streak:
        status = f"  Streak: {streak} day{'s' * (streak != 1)}  ·  read or journal today to keep it going"
    else:
        status = "  Start a streak: type 'read' or 'journal' today."
    return f"{RULE}\n{title}\n{status}\n{RULE}"


def verse_range(reference: str) -> range:
    """Verse numbers covered by a canonical reference: "John 3:16-18" -> 16..18."""
    verses = reference.rsplit(":", 1)[1]
    first, _, last = verses.partition("-")
    return range(int(first), int(last or first) + 1)


def format_verse(verse: Verse) -> str:
    word = f"  ·  {verse.word}" if verse.word else ""
    return f"TODAY'S VERSE{word}\n{verse.reference}\n\n{wrap(verse.text)}\n"


def format_study(verse: Verse, day: date) -> str:
    """The full daily study screen (everything below the header)."""
    sections = [format_verse(verse).rstrip()]

    notes = study.notes_for(verse.reference)
    if notes:
        for title, key in (("UNIVERSAL WISDOM", "wisdom"),
                           ("HISTORICAL CONTEXT", "context"),
                           ("THEOLOGICAL MEANING", "meaning")):
            sections.append(f"{title}\n{wrap(notes[key])}")
    else:
        # No written notes: show the verse's surroundings and its book instead.
        passage = format_passage(bible.context(verse.reference), verse_range(verse.reference))
        sections.append(f"IN CONTEXT\n{passage}")
        sections.append(f"ABOUT THE BOOK\n{format_book(bible.book_of(verse.reference))}")

    sections.append(f"REFLECT\n{wrap(study.reflection_question(verse.theme, day))}")

    book, chapter = study.reading_for(day)
    sections.append(f"TODAY'S READING: {book} {chapter}  (type 'read')")
    return "\n\n".join(sections) + "\n"


def format_history(records: list[DayRecord], streak: int, limit: int = 14) -> str:
    if not records:
        return "No history yet. Your studied days will show up here.\n"
    lines = [f"Current streak: {streak} day{'s' * (streak != 1)}", ""]
    for r in records[:limit]:
        done = ", ".join(x for x, ok in (("read", r.read), ("journaled", r.journaled)) if ok)
        lines.append(f"  {r.day:%a %b %d}  {r.reference:<22} [{done or 'not studied'}]")
    lines.append("")
    lines.append("Revisit a day with:  --date YYYY-MM-DD  (or --ref for a specific verse)")
    return "\n".join(lines) + "\n"
