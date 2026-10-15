"""Save personal reflections as Markdown, one file per day in journals/."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from bible import Verse
from verses import DailyPair

JOURNAL_DIR = Path(__file__).parent / "journals"


def _quote(verse: Verse) -> str:
    return f"> **{verse.reference}** — {verse.text}\n"


def format_entry(pair: DailyPair, reflection: str, when: datetime) -> str:
    theme = f" · {pair.main.theme}" if pair.main.theme else ""
    return (
        f"## {when:%H:%M} — {pair.main.reference} + {pair.partner.reference}{theme}\n\n"
        f"{_quote(pair.main)}>\n{_quote(pair.partner)}\n"
        f"{reflection.strip()}\n\n"
    )


def save_entry(
    pair: DailyPair,
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
        f.write(format_entry(pair, reflection, when))
    return path
