"""verse-ai: a free, offline daily Bible study.

Usage:
    python main.py                      # today's study, then the interactive prompt
    python main.py --theme patience     # a wisdom verse on one theme
    python main.py --date 2026-12-25    # look back at (or ahead to) another day
    python main.py --ref "Romans 12:9-12"
    python main.py --shuffle            # a random verse right now
    python main.py --once               # print today's study and exit
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date

import progress
from bible import VerseNotFoundError
from display import format_header, format_study
from interactive import run
from verses import THEMES, get_verse


def add_verse_options(parser: argparse.ArgumentParser) -> None:
    """Options shared with visual.py for choosing which verse to show."""
    parser.add_argument("--theme", choices=THEMES, help="a wisdom verse on one theme")
    parser.add_argument("--date", type=date.fromisoformat, help="the verse for YYYY-MM-DD")
    parser.add_argument("--ref", help='a specific verse, e.g. "James 1:19" or "Romans 12:9-12"')
    parser.add_argument("--shuffle", action="store_true", help="a random verse instead of today's")


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(errors="replace")
    if os.name == "nt":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("verse-ai")

    parser = argparse.ArgumentParser(prog="verse-ai", description="A free, offline daily Bible study.")
    add_verse_options(parser)
    parser.add_argument("--once", action="store_true", help="print the study, then exit")
    args = parser.parse_args(argv)

    today = date.today()
    day = args.date or today
    tracking = day == today  # streaks only count the real today

    try:
        verse = get_verse(day, args.theme, args.ref, args.shuffle)
    except VerseNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if tracking:
        progress.record(day, verse.reference)
    print(format_header(day, progress.streak(today), progress.studied_on(today), tracking))
    print()
    print(format_study(verse, day))

    if not args.once:
        run(verse, day, tracking)
    return 0


if __name__ == "__main__":
    sys.exit(main())
