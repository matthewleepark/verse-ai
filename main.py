"""verse-ai command-line entry point.

Usage:
    python main.py                      # today's pair, breakdown, then interactive mode
    python main.py --theme patience     # main verse from one theme
    python main.py --date 2026-12-25    # the pair for a specific day
    python main.py --ref "Proverbs 15:1"
    python main.py --shuffle            # a brand-new random pair right now
    python main.py --once               # breakdown only, no interactive prompt
    python main.py --offline            # never contact Claude
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from datetime import date

from analysis import AnalysisError, VerseCompanion
from bible import Verse, VerseNotFoundError
from interactive import run, stream_print
from verses import THEMES, DailyPair, get_pair


def _format_verse(label: str, verse: Verse) -> str:
    body = textwrap.fill(verse.text, width=72, initial_indent="  ", subsequent_indent="  ")
    return f"{label}: {verse.reference}\n\n{body}\n"


def format_pair(pair: DailyPair) -> str:
    theme = f"  ·  theme: {pair.main.theme}" if pair.main.theme else ""
    return (
        f"{_format_verse('TODAY', pair.main)}\n"
        f"{_format_verse('PAIRED WITH', pair.partner)}\n"
        f"({pair.main.translation}){theme}\n"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="verse-ai", description="A daily verse pair on universal wisdom.")
    parser.add_argument("--theme", choices=THEMES, help="pick the main verse from one theme")
    parser.add_argument("--date", type=date.fromisoformat, help="show the pair for YYYY-MM-DD")
    parser.add_argument("--ref", help='use a specific main verse, e.g. "James 1:19" or "Romans 12:9-12"')
    parser.add_argument("--shuffle", action="store_true", help="a new random pair instead of today's")
    parser.add_argument("--once", action="store_true", help="show the breakdown, then exit")
    parser.add_argument("--offline", action="store_true", help="never contact Claude")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    # Claude's answers can include curly quotes etc.; don't crash on legacy Windows code pages.
    sys.stdout.reconfigure(errors="replace")
    args = parse_args(argv)
    try:
        pair = get_pair(args.date, args.theme, args.ref, args.shuffle)
    except VerseNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    verses_text = format_pair(pair)
    print(verses_text)

    companion = VerseCompanion(pair, offline=args.offline)
    try:
        companion.breakdown(stream_print)
        print("\n")
    except AnalysisError as e:
        # Previously-seen pairs load from the local cache; otherwise carry on without AI.
        print(f"(No breakdown: {e})\n")
        if args.once:
            return 1
    except KeyboardInterrupt:
        print()
        return 130

    if not args.once:
        run(companion, verses_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
