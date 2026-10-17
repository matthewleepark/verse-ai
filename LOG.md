# verse-ai — Development Log

**Project:** verse-ai, a daily Bible verse study app (Python command-line app plus a browser poster)
**Log written:** 2026-10-16

> This log was reconstructed from the git history (`git log --reverse --stat` and `git show` on the main files at each commit). It was not written at the time of each change, and it does not use the README as a source. Anything git can't show is marked "unknown".

---

## Commits

### 1. `dcaf459` — 2026-10-14 22:54:32 -0700 — "Initial commit"

- **Planned:** unknown
- **Done:** Created the repository on GitHub with a one-line `README.md`.
- **Changed:** `README.md` (1 file, +1 line)
- **Checked by:** unknown
- **Problems and fixes:** unknown

### 2. `7632956` — 2026-10-14 22:57:10 -0700 — "Add verse-ai CLI: daily verse pairs with Claude breakdowns"

- **Planned:** unknown. The commit message lists the goals: bundle the full Berean Standard Bible for offline use, pair a curated wisdom verse with a random partner verse each day, add a Claude-written breakdown that is cached locally, an interactive mode, and unit tests with a faked Claude client.
- **Done:**
  - Added the first working command-line app: `main.py`, `bible.py`, `verses.py`, `interactive.py` and `journal.py`.
  - Added the full BSB text in `data/bsb.txt`, which is 31,105 lines.
  - `analysis.py` called the Claude API (`MODEL = "claude-opus-5-5"`, with `fallbacks="default"`), and `cache.py` stored breakdowns locally.
- **Changed:** 17 files, +32,170 / −1. New: `.gitignore`, `CLAUDE.md`, `analysis.py`, `bible.py`, `cache.py`, `data/bsb.txt`, `interactive.py`, `journal.py`, `main.py`, `requirements.txt`, `verses.py`, and `tests/` (`test_analysis.py`, `test_bible.py`, `test_journal.py`, `test_verses.py`).
- **Checked by:** Unit tests were added in `tests/`. Whether they were run before this commit is unknown.
- **Problems and fixes:** unknown

### 3. `5854fdb` — 2026-10-15 20:32:15 -0700 — "Offline daily verse with interactive poster"

- **Planned:** unknown
- **Done:**
  - Removed the Claude AI feature: deleted `analysis.py`, `cache.py` and `tests/test_analysis.py`.
  - Replaced the daily verse pair with a single verse per day: `verses.py` now has `get_verse()`, plus a list of 416 daily verses in `data/daily_verses.json`.
  - Added offline study content: `data/study_notes.json`, `data/books.json` and `data/reflections.json`.
  - Added study-app features: a streak and history (`progress.py`), a Proverbs reading plan and study content (`study.py`), and screen formatting (`display.py`). The interactive commands are now `read`, `context`, `journal`, `poster` and `history`.
  - Added the first browser poster: `visual.py` and `web/template.html`, set in the Bodoni Moda font, with a public-domain 1860 woodcut (`web/assets/schnorr-1860.jpg`) and an "About" panel.
  - Added `make_shortcut.ps1` for Desktop and Start-menu shortcuts.
- **Changed:** 31 files, +2,403 / −622.
- **Checked by:** New tests `tests/test_progress.py`, `tests/test_study.py` and `tests/test_visual.py`, with updates to the others. Whether they were run before this commit is unknown.
- **Problems and fixes:** unknown. This one commit contains several separate changes at once (removing the AI, switching to one verse a day, the study features, the poster), so the steps in between aren't visible in git.

### 4. `f239f20` — 2026-10-16 05:12:49 -0700 — "Cinematic verse transitions, sharing, and navigation fixes"

- **Planned:** unknown
- **Done:**
  - Restyled the poster with comic-book fonts: replaced Bodoni Moda with Bangers and Comic Neue.
  - Reworked `web/template.html` (+1,347 lines changed): verse-to-verse transitions, a share feature (`shareCard()`), and swipe and keyboard navigation.
  - Added an automated browser test, `tools/browser_check.mjs` (364 lines).
- **Changed:** 11 files, +1,504 / −379. Added `tools/browser_check.mjs`, `web/assets/Bangers-Regular.ttf`, `web/assets/ComicNeue-Bold.ttf` and their license files; removed the Bodoni Moda font.
- **Checked by:** `tools/browser_check.mjs` was added in this commit, and `tests/test_visual.py` was updated. Whether either was run before this commit is unknown.
- **Problems and fixes:** The message mentions "navigation fixes". Which problems were fixed is unknown from git alone.

### 5. `deb2661` — 2026-10-16 07:21:04 -0700 — "Engraved scripture style for the poster"

- **Planned:** unknown
- **Done:** Replaced the comic style with a light parchment, engraved-Bible style: the template defines `--parchment` and `--vellum` colours, and the comic fonts were swapped for EB Garamond and Cormorant Garamond.
- **Changed:** 12 files, +386 / −334. `web/template.html`, `visual.py`, `tools/browser_check.mjs`, `tests/test_visual.py`, `README.md`, `CLAUDE.md`, and the font files.
- **Checked by:** `tools/browser_check.mjs` and `tests/test_visual.py` were updated. Whether they were run before this commit is unknown.
- **Problems and fixes:** unknown

### 6. `035285e` — 2026-10-16 08:59:58 -0700 — "Dark cinematic design for the poster"

- **Planned:** unknown
- **Done:** Changed the poster to a dark design, described in the template as `"The Fourth Watch": an engraving printed in darkness, lit by one light`, with a `--night: #0b0a0b` background.
- **Changed:** 3 files, +485 / −280: `web/template.html`, `README.md` and `CLAUDE.md`.
- **Checked by:** unknown
- **Problems and fixes:** unknown

### 7. `1cbc018` — 2026-10-16 21:52:28 -0700 — "Dark cinematic design: fixes from review"

- **Planned:** unknown. The message says the changes came from a review.
- **Done:** The code comments added in this commit describe these fixes:
  - Shadow pools behind the title and controls so they stay readable.
  - Room for letter tails in the gold title, such as the tail of J.
  - The verse stops short of the figure.
  - A real gold initial plus a hanging quotation mark.
  - A minimum size for the reference.
  - A solid band at the top of the Context drawer so scrolled text doesn't run behind the buttons.
  - Balancing quotation marks on verses that start or end mid-quote.
  - Short verses grow and long ones shrink.
  - Title fitting that measures the letters.
  - Reduced-motion handling.
  - Smoother handling of fast second clicks during a transition.
- **Changed:** 2 files, +257 / −58: `web/template.html` and `CLAUDE.md`.
- **Checked by:** unknown from git
- **Problems and fixes:** The problems are the ones the code comments name above. Who found them, and how, is unknown from git.

---

## Process

- **Claude chat** handled planning.
- **Claude Code** handled building.

## Manual changes by me

<!-- Fill this in yourself: anything you wrote, edited, or decided by hand. -->

## Decisions

These are questions for me (the student) to answer. They weren't guessed from the code.

1. Why did the app move from Claude-generated breakdowns (commit 2) to a fully offline app with written study notes (commit 3)?
   - Answer:
2. Why did the daily verse change from a pair of verses (commit 2) to a single verse each day (commit 3)?
   - Answer:
3. Why use the Berean Standard Bible (BSB) as the translation?
   - Answer:
4. Why add a browser poster alongside the command-line app?
   - Answer:
5. Why did the poster go comic → parchment → dark (commits 4, 5 and 6)? What did you dislike about each earlier style?
   - Answer:
6. What did you decide to leave out or postpone, such as the phone-layout fixes?
   - Answer:
