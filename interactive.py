"""Interactive prompt for the daily study: read, context, journal, history, poster."""

from __future__ import annotations

from datetime import date

import bible
import progress
import study
from bible import Verse
from display import format_history, format_passage, format_study, format_verse, verse_range
from journal import save_entry

HELP = """\
Commands:
  read       today's chapter of Proverbs (counts toward your streak)
  context    the verses around today's verse
  journal    write a reflection (saved to journals/, counts toward your streak)
  poster     open today's verse as an animated poster in your browser
  history    your streak and past days
  study      show today's study again
  help       show this list
  quit       exit
"""


def read_reflection() -> str:
    print("Write your reflection. Press Enter on an empty line to finish.\n")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


def run(verse: Verse, day: date, tracking: bool) -> None:
    """tracking=False when looking back at another day: nothing counts toward the streak."""

    def mark(**flags: bool) -> None:
        if not tracking:
            return
        already_counted = progress.studied_on(day)
        progress.record(day, verse.reference, **flags)
        if not already_counted:
            n = progress.streak(day)
            print(f"Today counts! Streak: {n} day{'s' * (n != 1)}.\n")

    print(HELP)
    while True:
        try:
            # Windows PowerShell prefixes piped input with a byte-order mark.
            command = input("verse-ai> ").strip().lstrip("﻿").lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not command:
            continue
        if command in {"quit", "exit", "q"}:
            return
        if command == "help":
            print(HELP)
        elif command == "study":
            print(format_study(verse, day))
        elif command == "verse":
            print(format_verse(verse))
        elif command == "read":
            book, chapter = study.reading_for(day)
            print(f"\n{book.upper()} {chapter}\n")
            print(format_passage(bible.passage(book, chapter)))
            print()
            mark(read=True)
        elif command == "context":
            print(f"\n{verse.reference} in context\n")
            print(format_passage(bible.context(verse.reference, radius=4), verse_range(verse.reference)))
            print()
        elif command == "journal":
            try:
                reflection = read_reflection()
            except (EOFError, KeyboardInterrupt):
                print("\nJournal entry cancelled.\n")
                continue
            if not reflection:
                print("Nothing written, so nothing saved.\n")
                continue
            path = save_entry(verse, reflection)
            print(f"Saved to {path}")
            mark(journaled=True)
        elif command == "poster":
            import visual  # only needed for this command
            visual.open_poster(verse, day)
            print("Opened the poster in your browser.\n")
        elif command == "history":
            print(format_history(progress.history(), progress.streak(date.today())))
        else:
            print(f"Unknown command {command!r}. Type 'help' to see the commands.\n")
