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
| `web/template.html` | Full-screen WebGL2 page, "The Fourth Watch": an engraving printed in darkness, lit by one light. The shader:<br>• prints the engraved sea and sky (16 painter-ordered wave rows hatched with `engrave()`, a horizontal-line sky with clouds and rays from `uSun`) onto a night light field `L`: charcoal, a crimson-amber dusk band and hot horizon line, the halo behind Jesus, and a path of light on the water<br>• lights the woodcut figures (cut out with the `FIGURE` polygon) from the halo down, with a darken-only feathered edge so there's no halo or box<br>• adds a soft bloom, one anamorphic streak, static grain and a light-biased vignette; `pk` tightens glows on phones<br>• shows click and mouse ripples as fine rings (`uRipples`)<br>DOM overlays:<br>• the verse set directly on the sea in bone EB Garamond, with a gold Cormorant initial and an invisible radial scrim (`.caption::before`)<br>• the gold-leaf title, gilded per `.ch`, fitted with `fitTitle()`<br>• small-caps text controls, a Context drawer (C) and a dark Share card |
| `web/assets/` | The Schnorr von Carolsfeld 1860 woodcut (public domain), plus EB Garamond and Cormorant Garamond (OFL) |

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
- **Changing the artwork:** re-trace `FIGURE`, `ART_HORIZON` and `JESUS_HEAD` in `web/template.html` for the new image. The drawn horizon is aligned to `ART_HORIZON` inside the placed figure. Data has to be embedded as data URIs because Chrome blocks `file://` images in WebGL.
- **Checking the poster:** run `node tools/browser_check.mjs` after `python visual.py --no-open`. It drives headless Edge over the DevTools protocol, using `?lowres` because SwiftShader is CPU-bound. Other testing switches are `?nograin`, `?t=SECONDS`, `?ripple=X,Y` and `?panel`. `window.verseAI` exposes `state()`, `verseFor()`, `shareCard()` and `freezeAt(ms)`; `freezeAt` holds every animation at an exact time, for filmstrips.
- **Verse transitions (`go()`):**
  - `offset` changes synchronously, so Context, Share and the `#date` hash always match the displayed verse. Only the visuals animate.
  - The outgoing `.heading` and `.caption` are cloned into `.ghost` layers (`pointer-events: none`). New title letters are revealed in the direction of travel. Forward: the ghost scales up and the letters come from 0.8. Backward: the ghost scales down and the letters come from 1.2.
  - The caption swap is sequential, so two passages never overlap.
  - On a second click within 500 ms, `reuseGhosts()` keeps the outgoing copies the reader is still looking at (it commits their mid-fade styles) rather than flashing the half-revealed in-between verse; otherwise `settleTransition()` finishes the previous transition.
  - A `SAFETY_MS` (1.9 s) timer forces the end state if the browser stalls. `freezeAt()` pauses that timer.
  - The title ghost is gone by 420 ms and the new letters start at 360 ms, so two words never blend into one.
  - The scene glides via `uTravel`, `uPulse`, `uProgress`, `uDir` and `uMood` over `TRAVEL_MS`.
  - Reduced motion gives 160 ms opacity-only fades, and CSS transitions are disabled.
- **Style:** reverent and scriptural: an engraving printed in darkness, lit by one light. Charcoal, bone, warm gold, crimson only as hairline rules, classic serif type. The user's dark-theme request supersedes the earlier parchment look. Never comic styles, halftone dots or stepped animation. Avoid boxes around the verse, glassmorphism, pure #000/#fff, faux italics (both fonts are roman-only), and particles.
- **Capitalizing verses:** `displayText()` capitalizes a verse that starts mid-sentence (e.g. Proverbs 3:6 "in all your ways"), so the drop cap reads correctly. Use it for the caption, the copied text and the share card alike.
- **"Today":** the real date from the viewer's clock (`localIsoToday()`), never the day the page was built or opened on. A page built for today (`startIsToday`) that is opened on a later day moves to the real today; a page built with `--date` stays on that date unless `#date` says otherwise.
- **Gitignored:** `journals/`, `progress.json`, `.venv/`, `web/today.html`.
