"""Interactive prompt: ask follow-ups, get a summary, or write a journal entry.

Journaling and re-showing the verses work offline; questions need Claude.
"""

from __future__ import annotations

from analysis import AnalysisError, VerseCompanion
from journal import save_entry

HELP = """\
Commands:
  <any question>   ask about today's verses (needs internet)
  summary          quick summary of the pair and this conversation (needs internet)
  journal          write a reflection (saved to journals/)
  verse            show today's verses again
  help             show this list
  quit             exit
"""


def stream_print(chunk: str) -> None:
    print(chunk, end="", flush=True)


def read_reflection() -> str:
    print("Write your reflection. Press Enter on an empty line to finish.\n")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


def run(companion: VerseCompanion, verses_text: str) -> None:
    print(HELP)
    while True:
        try:
            # Windows PowerShell prefixes piped input with a byte-order mark.
            command = input("verse-ai> ").strip().lstrip("﻿")
        except (EOFError, KeyboardInterrupt):
            print()
            return

        lowered = command.lower()
        if not command:
            continue
        if lowered in {"quit", "exit", "q"}:
            return
        if lowered == "help":
            print(HELP)
        elif lowered in {"verse", "verses"}:
            print(verses_text)
        elif lowered == "journal":
            try:
                reflection = read_reflection()
            except (EOFError, KeyboardInterrupt):
                print("\nJournal entry cancelled.\n")
                continue
            if not reflection:
                print("Nothing written, so nothing saved.\n")
                continue
            path = save_entry(companion.pair, reflection)
            print(f"Saved to {path}\n")
        elif lowered == "summary":
            respond(lambda: companion.summary(stream_print))
        else:
            respond(lambda: companion.ask(command, stream_print))


def respond(call) -> None:
    """Run one streamed Claude turn, keeping the prompt alive on errors or Ctrl+C."""
    print()
    try:
        call()
    except AnalysisError as e:
        print(f"\n{e}")
    except KeyboardInterrupt:
        print("\n(interrupted)")
    print("\n")
