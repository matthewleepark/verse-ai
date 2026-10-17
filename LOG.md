# Build Log, Artifact 2: verse-ai

Tools: Claude Code (building), Claude chat (planning). Repo: https://github.com/matthewleepark/verse-ai. Date: 2026-10-16

Rebuilt from the git history (`git log --reverse --stat` and `git show`), not the README. "unknown" means the history doesn't show it.

## Commits

### dcaf459 · Oct 14, 22:54 · "Initial commit"
- Done: Created the repo on GitHub with a one-line README.md.
- Planned / Checked / Problems: unknown

### 7632956 · Oct 14, 22:57 · "Add verse-ai CLI: daily verse pairs with Claude breakdowns"
- Planned (from the commit message): an offline Bible, a daily pair of verses, a Claude breakdown saved for offline use, an interactive mode with a journal, and tests.
- Done: Built the command-line app (main.py, bible.py, verses.py, interactive.py, journal.py) and added the full Berean Standard Bible (data/bsb.txt, 31,105 lines). analysis.py called the Claude API, and cache.py saved breakdowns.
- Changed: 17 files, +32,170 lines, including 4 test files.
- Checked / Problems: unknown

### 5854fdb · Oct 15, 20:32 · "Offline daily verse with interactive poster"
- Done:
  - Removed the Claude feature (deleted analysis.py and cache.py).
  - Switched to one verse per day, with 416 daily verses (data/daily_verses.json).
  - Added study notes, book background and reflection questions.
  - Added a streak (progress.py) and a Proverbs reading plan (study.py).
  - Added the first browser poster (visual.py, web/template.html) with a public-domain 1860 woodcut.
  - Added Desktop shortcuts (make_shortcut.ps1).
- Changed: 31 files, +2,403 / −622, with 3 new test files.
- Planned / Checked / Problems: unknown

### f239f20 · Oct 16, 05:12 · "Cinematic verse transitions, sharing, and navigation fixes"
- Done: Restyled the poster in a comic-book style (Bangers and Comic Neue fonts). Added verse-to-verse transitions, a share image, swipe and keyboard navigation, and a browser test (tools/browser_check.mjs).
- Changed: 11 files, +1,504 / −379.
- Problems: the message mentions "navigation fixes", but what they fixed is unknown.
- Planned / Checked: unknown

### deb2661 · Oct 16, 07:21 · "Engraved scripture style for the poster"
- Done: Replaced the comic style with a light parchment, engraved-Bible look (EB Garamond and Cormorant Garamond fonts).
- Changed: 12 files, +386 / −334.
- Planned / Checked / Problems: unknown

### 035285e · Oct 16, 08:59 · "Dark cinematic design for the poster"
- Done: Made the poster dark: a night sea lit by one light behind Jesus.
- Changed: 3 files, +485 / −280.
- Planned / Checked / Problems: unknown

### 1cbc018 · Oct 16, 21:52 · "Dark cinematic design: fixes from review"
- Done (from the code comments):
  - readable title and buttons
  - the verse no longer runs into the figure
  - a gold first letter
  - a fixed Context panel overlap
  - balanced quotation marks
  - short verses shown larger
  - reduced-motion support
  - smoother fast clicks
- Changed: 2 files, +257 / −58.
- Checked (run by Claude Code on Oct 16):
  - `python -m unittest discover tests` → 50 tests, OK
  - `python main.py --date 2026-10-14` → showed 1 Peter 4:8 ("LOVE")
  - `python visual.py --no-open` → poster built
  - `node tools/browser_check.mjs` → 35/35 checks passed
- Planned / Problems: unknown

### 0d4a7ff · Oct 16, 22:34 · "Ignore .env files"
- Done: Added `.env` back to .gitignore.
- Checked: `git check-ignore .env` confirmed it's ignored.

### 9f6388a, b301816, 94635e9, fd14eb2 · Oct 16 · LOG.md commits
- Done: Wrote this log, rewrote it to match my portfolio log, then added my hand changes and decisions.

## Changes I made by hand

- Created the verse-ai repo on GitHub.
- Ran the commit and push commands myself.
- Tested the poster in my browser and reported the Context panel overlapping the buttons.
- Shared three reference posters for the poster style.

## Decisions

1. Why did you remove the Claude breakdowns and make the app fully offline?
   - I made the app fully offline because I don't have usage credits and can't rely on them. Keeping it offline, so it works automatically with or without internet, felt like the best way to learn and be efficient.
2. Why did you go from a pair of verses each day to one verse?
   - Pairing verses each day felt overwhelming, with a lot of information to cover. Having one verse leaves room for more ideas and thoughts about that passage.
3. Why the Berean Standard Bible?
   - I had to use the Berean Standard Bible because of copyright.
4. Why did the poster go comic → parchment → dark?
   - The comic style felt a little unprofessional, and the message didn't really come through.
5. What did you leave out on purpose?
   - I left out any distractions that could take the focus away from the passage.

## Issues

- `.env` was dropped from .gitignore in 5854fdb and added back in 0d4a7ff. No .env file was ever committed.
- Some commits bundle several steps (5854fdb did four things at once), so the steps in between aren't in the history.
- Commit messages don't say how changes were tested, so most "Checked" lines are unknown.
- An old local `master` branch has only the initial commit. It isn't on GitHub.
