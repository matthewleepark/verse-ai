"""Save personal reflections as Markdown, one file per day in journals/."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bible import Verse

JOURNAL_DIR = Path(__file__).parent / "journals"


def format_entry(verse: Verse, reflection: str, when: datetime) -> str:
    word = f" · {verse.word}" if verse.word else ""
    return (
        f"## {when:%H:%M} — {verse.reference}{word}\n\n"
        f"> {verse.text}\n"
        f"> — *{verse.translation}*\n\n"
        f"{reflection.strip()}\n\n"
    )


def save_entry(
    verse: Verse,
    reflection: str,
    when: datetime | None = None,
    folder: Path = JOURNAL_DIR,
) -> Path:
    """Append a reflection to journals/YYYY-MM-DD.md and return the file path."""
    if not reflection.strip():
        raise ValueError("Reflection is empty.")
    when = when or datetime.now()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{when:%Y-%m-%d}.md"
    is_new = not path.exists()
    with path.open("a", encoding="utf-8") as f:
        if is_new:
            f.write(f"# Journal — {when:%A, %B %d, %Y}\n\n")
        f.write(format_entry(verse, reflection, when))
    return path
