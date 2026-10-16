"""Today's verse as an interactive poster: Jesus stays still while the sea moves.

Builds web/today.html from web/template.html and opens it in your browser.
Everything (all the daily verses, the artwork and the font) is embedded in the
page, so it works offline and you can browse days without running Python again.

Usage:
    python visual.py                      # today's verse
    python visual.py --date 2026-12-25
    python visual.py --ref "Matthew 14:31"
    python visual.py --theme patience
    python visual.py --shuffle
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import webbrowser
from datetime import date
from pathlib import Path

import bible
import study
from bible import Verse, VerseNotFoundError
from verses import daily_list, get_verse

WEB_DIR = Path(__file__).parent / "web"
ASSETS = WEB_DIR / "assets"
OUTPUT = WEB_DIR / "today.html"


def _data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _verse_info(reference: str, word: str) -> dict:
    """Everything the poster shows for one verse, including the About panel."""
    verse = bible.lookup(reference)
    first, _, last = verse.reference.rsplit(":", 1)[1].partition("-")
    return {
        "ref": verse.reference,
        "word": word,
        "text": verse.text,
        "book": bible.book_of(verse.reference),
        "context": bible.context(verse.reference, radius=2),
        "range": [int(first), int(last or first)],
    }


def build(verse: Verse, day: date, output: Path = OUTPUT) -> Path:
    daily = [_verse_info(e["ref"], e["word"]) for e in daily_list()]
    notes = {e["ref"]: study.notes_for(e["ref"]) for e in daily_list() if study.notes_for(e["ref"])}
    if study.notes_for(verse.reference):
        notes[verse.reference] = study.notes_for(verse.reference)
    data = {
        "start": _verse_info(verse.reference, verse.word or "FAITH"),
        "startDate": day.isoformat(),
        "startOrdinal": day.toordinal(),
        "startIsToday": day == date.today(),
        "daily": daily,
        "notes": notes,
        "books": study.all_books(),
        "translation": verse.translation,
        "image": _data_uri(ASSETS / "schnorr-1860.jpg", "image/jpeg"),
        "font": _data_uri(ASSETS / "BodoniModa.ttf", "font/ttf"),
    }
    # "</" inside a <script> block could end it early, so escape it.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (WEB_DIR / "template.html").read_text(encoding="utf-8")
    output.write_text(template.replace("/*__VERSE_DATA__*/null", payload, 1), encoding="utf-8")
    return output


def open_poster(verse: Verse, day: date) -> Path:
    page = build(verse, day)
    webbrowser.open(page.as_uri())
    return page


def _show_error(message: str) -> None:
    """Print, and also pop up a dialog: the desktop shortcut runs without a console."""
    if sys.stderr:
        print(f"error: {message}", file=sys.stderr)
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, message, "verse-ai", 0x10)


def main(argv: list[str] | None = None) -> int:
    from main import add_verse_options

    parser = argparse.ArgumentParser(prog="visual", description="Open today's verse as an interactive poster.")
    add_verse_options(parser)
    parser.add_argument("--no-open", action="store_true", help="build the page without opening it")
    args = parser.parse_args(argv)

    day = args.date or date.today()
    try:
        verse = get_verse(day, args.theme, args.ref, args.shuffle)
        page = build(verse, day)
    except (VerseNotFoundError, OSError) as e:
        _show_error(str(e))
        return 1
    if not args.no_open:
        webbrowser.open(page.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
