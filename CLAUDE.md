# verse-ai

A school project: a free, fully offline daily Bible study. It shows one verse per day, with no pairing or matching. There are two front ends: an interactive browser poster (`visual.py`) and a CLI study app (`main.py`) with notes, a daily Proverbs reading, a journal and a streak. There is no AI and no network use, by design.

## Commands

```
.\.venv\Scripts\python.exe visual.py          # build + open today's poster
.\.venv\Scripts\python.exe main.py            # today's study + interactive prompt
.\.venv\Scripts\python.exe -m unittest discover tests
powershell -ExecutionPolicy Bypass -File make_shortcut.ps1   # Desktop + Start menu shortcuts
```

Python 3.13 in `.venv`, standard library only (no third-party packages).

## Layout

| File | Role |
|---|---|
| `data/bsb.txt` | The full Berean Standard Bible (public domain), tab-separated `Book C:V<TAB>text`, 31,102 verses |
| `data/daily_verses.json` | 416 `{ref, word}` entries. Day `d` shows entry `d.toordinal() % 416`, so there are no repeats for over a year. `word` is the poster title. |
| `data/study_notes.json` | `{wisdom, context, meaning}` notes for the 40 wisdom verses |
| `data/books.json` | `{type, author, date, about}` for all 66 books |
| `data/reflections.json` | Questions for each theme, plus `general` |
| `bible.py` | Loads the text. `lookup()`, `passage()`, `context()`, `book_of()`, `random_verse()`. `Verse` has `theme` and `word`. |
| `verses.py` | `daily_list()`, `WISDOM_VERSES` (by theme), and `get_verse(day, theme, reference, shuffle)` |
| `study.py` | Reads the JSON content; `reading_for(day)` returns Proverbs at the day-of-month chapter |
| `progress.py` | `progress.json`: each day's reference plus `read`/`journaled` flags; streak and history |
| `display.py` | Pure formatting functions that return strings |
| `interactive.py` | The REPL: `read`, `context`, `journal`, `poster`, `history`, `study`, `help`, `quit` |
| `journal.py` | Appends Markdown reflections to `journals/YYYY-MM-DD.md` |
| `main.py` | argparse entry point. `add_verse_options()` is shared with `visual.py`. |
| `visual.py` | Builds `web/today.html` from `web/template.html`, embedding the whole daily list (with context and book) plus notes, books, artwork and font so the page can browse days offline |
| `web/template.html` | WebGL2 poster: the shader ripples only the water, with click and mouse ripples (`uRipples`). `FIGURE` is a hand-traced polygon that keeps Jesus, Peter and the boat still. Controls: arrow keys or ‹ › for days, T for today, I for the About panel, Space to pause. |
| `web/assets/` | The Schnorr von Carolsfeld 1860 woodcut (public domain) and Bodoni Moda (OFL) |

## Conventions

- **No network:** keep the app fully offline. Don't add API calls or third-party dependencies.
- **One verse per day:** no partner verses or pairing.
- **Day rule:** the poster's JavaScript must use the same rule as `get_verse()`: `(ordinal + offset) % length`. `tests/test_visual.py` checks this.
- **Translation:** don't add copyrighted translations such as the NIV, ESV, or NLT; their licenses forbid bundling the full text.
- **Book names and missing verses:** the BSB spells books "Psalm" and "Song of Solomon", and `BOOK_ALIASES` handles the other spellings. A handful of verses that aren't in the earliest manuscripts (e.g. Matthew 17:21) have empty text. `passage()` skips them, and `lookup()` raises an error for them.
- **Daily list rules:** every entry must exist in the BSB, be unique, and have an uppercase `word`. All 40 wisdom verses must be in it. Tests enforce all of this.
- **Adding a wisdom verse:** it needs entries in `WISDOM_VERSES`, `data/study_notes.json` and `data/daily_verses.json`.
- **Study notes tone:** accurate, attributed to traditions ("Christian tradition...", "Jewish tradition..."), flagging scholarly debate where it exists, and never preachy.
- **Streaks:** a day counts when `read` or `journaled` is true. Only the real today is tracked; `--date` views of other days never touch `progress.json`.
- **Poster artwork:** only use public-domain artwork or openly licensed fonts. The images the user shared as inspiration are other people's designs.
- **Changing the artwork:** re-trace `FIGURE` and `HORIZON` in `web/template.html` for the new image. Data has to be embedded as data URIs because Chrome blocks `file://` images in WebGL.
- **Checking the poster:** use headless Edge (`--use-angle=swiftshader --enable-unsafe-swiftshader`) with the testing switches `?nograin`, `?t=SECONDS`, `?ripple=X,Y` and `?panel`. Inside `FIGURE`, frames must be pixel-identical; the open sea must differ.
- **Gitignored:** `journals/`, `progress.json`, `.venv/`, `web/today.html`.
