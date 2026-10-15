# verse-ai

A Python CLI for a school project. Each day it pairs a curated "universal wisdom" verse (patience, empathy, conflict resolution, integrity) with a random partner verse from the whole Bible. Claude explains the pair, and an interactive mode handles follow-up questions, summaries, and journal entries. Everything except Claude works offline.

## Commands

```
.\.venv\Scripts\python.exe main.py            # pair + breakdown + interactive mode
.\.venv\Scripts\python.exe main.py --offline  # never contact Claude
.\.venv\Scripts\python.exe -m unittest discover tests
```

Python 3.13 in `.venv`. The only dependency is `anthropic`. The AI features need `ANTHROPIC_API_KEY`.

## Layout

| File | Role |
|---|---|
| `data/bsb.txt` | The full Berean Standard Bible (public domain), tab-separated `Book C:V<TAB>text`, 31,102 verses |
| `bible.py` | Loads the data file; `lookup()` for single verses or ranges in one chapter; `random_verse()` |
| `verses.py` | Curated `WISDOM_VERSES` and `get_pair()` → `DailyPair(main, partner)`. Same day → same pair, seeded by `date.toordinal()`. |
| `analysis.py` | `VerseCompanion`: one Claude conversation per pair, with `breakdown()`, `ask()`, and `summary()`, all streamed |
| `cache.py` | Saves breakdowns to `cache/breakdowns.json`, keyed by the pair's references |
| `interactive.py` | The REPL: questions, `summary`, `journal`, `verse`, `help`, `quit` |
| `journal.py` | Appends Markdown reflections, quoting both verses, to `journals/YYYY-MM-DD.md` |
| `main.py` | argparse entry point |
| `tests/` | `unittest`; Claude is faked (`FakeClient`). Bible tests read the real data file. |

## Conventions

- **Translation:** don't add copyrighted translations such as the NIV, ESV, or NLT; their licenses forbid bundling the full text. BSB, WEB, and KJV are public domain.
- **Book names and missing verses:** the BSB spells books "Psalm" and "Song of Solomon", and `BOOK_ALIASES` maps the other spellings. A handful of verses that aren't in the earliest manuscripts (e.g. Matthew 17:21) have empty text. `random_verse` skips them, and `lookup` raises an error for them.
- **Adding wisdom verses:** add them to `WISDOM_VERSES`. A test checks that every entry exists in the data file.
- **Offline behavior:** expected failures raise `VerseNotFoundError` or `AnalysisError`, and their messages are full, user-facing sentences. An `AnalysisError` never ends the session; the app carries on without AI.
- **Claude usage**, all in `analysis.py`:
  - Model `claude-opus-5-5`, effort `medium`, called through `client.beta.messages.stream`.
  - `fallbacks="default"` (beta `server-side-fallback-2026-07-01`) handles safety declines.
  - Both verses live in the system prompt, so the system prompt never changes during a session.
  - The conversation is append-only. The only edit is popping an unanswered user turn after an error.
  - A cached breakdown is replayed as the first exchange, as plain text.
  - Output goes to a plain terminal, so the prompts ask for no Markdown.
- **Tone:** respectful and educational. Theological claims are attributed to traditions, and the partner connection is honest rather than forced.
- **Gitignored:** `journals/` (personal writing), `cache/`, and `.venv/`.
