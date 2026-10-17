# Build Log, Artifact 2: verse-ai

Tools: Claude Code (building), Claude chat (planning). Repo: https://github.com/matthewleepark/verse-ai. Date: 2026-10-16

This log was rebuilt from the git history (`git log --reverse --date=iso --stat` and `git show` on the main files at each commit), not from the README. "unknown" means the history doesn't show it.

## dcaf459 · 2026-10-14 22:54:32 -0700 · "Initial commit"

- Planned: unknown
- Done: Created the repo with a one-line README.md.
- Changed: README.md (1 file, +1 line)
- Checked: unknown
- Problems and fixes: unknown

## 7632956 · 2026-10-14 22:57:10 -0700 · "Add verse-ai CLI: daily verse pairs with Claude breakdowns"

- Planned: The commit message lists the plan:
  - bundle the full Berean Standard Bible for offline use
  - pair a wisdom verse with a random partner verse each day
  - a Claude breakdown (Universal Wisdom, Historical Context, Theological Meaning, The Connection), cached so pairs already seen work offline
  - an interactive mode for questions, summaries and journaling
  - unit tests with a faked Claude client
- Done:
  - Added the command-line app: main.py, bible.py, verses.py, interactive.py and journal.py.
  - Added the full Bible text in data/bsb.txt (31,105 lines).
  - analysis.py called the Claude API (`MODEL = "claude-opus-5-5"`), and cache.py saved breakdowns locally.
- Changed: 17 files, +32,170 / −1
  - New code: .gitignore, CLAUDE.md, analysis.py, bible.py, cache.py, data/bsb.txt, interactive.py, journal.py, main.py, requirements.txt, verses.py
  - New tests: test_analysis.py, test_bible.py, test_journal.py, test_verses.py
- Checked: unknown. Tests were added, but whether they were run at the time is unknown.
- Problems and fixes: unknown

## 5854fdb · 2026-10-15 20:32:15 -0700 · "Offline daily verse with interactive poster"

- Planned: unknown
- Done:
  - Removed the Claude feature (deleted analysis.py, cache.py and test_analysis.py).
  - Switched from a verse pair to one verse per day (`get_verse()` in verses.py, with 416 daily verses in data/daily_verses.json).
  - Added written study notes, book background and reflection questions (data/*.json).
  - Added a streak and history (progress.py), a Proverbs reading plan (study.py), and screen layout (display.py). The commands are now read, context, journal, poster and history.
  - Added the first browser poster (visual.py, web/template.html): Bodoni Moda font, a public-domain 1860 woodcut (web/assets/schnorr-1860.jpg), and an "About" panel.
  - Added make_shortcut.ps1 for Desktop and Start-menu shortcuts.
- Changed: 31 files, +2,403 / −622
- Checked: unknown. New tests were added (test_progress.py, test_study.py, test_visual.py), but whether they were run at the time is unknown.
- Problems and fixes: unknown

## f239f20 · 2026-10-16 05:12:49 -0700 · "Cinematic verse transitions, sharing, and navigation fixes"

- Planned: unknown
- Done:
  - Restyled the poster with comic-book fonts (Bangers and Comic Neue replaced Bodoni Moda).
  - Added verse transitions, a share image (`shareCard()`) and swipe/keyboard navigation in web/template.html.
  - Added an automated browser test, tools/browser_check.mjs (364 lines).
- Changed: 11 files, +1,504 / −379
- Checked: unknown. The browser test was added, but whether it was run at the time is unknown.
- Problems and fixes: The message says "navigation fixes". What was fixed is unknown.

## deb2661 · 2026-10-16 07:21:04 -0700 · "Engraved scripture style for the poster"

- Planned: unknown
- Done: Replaced the comic style with a light parchment, engraved-Bible style, using the EB Garamond and Cormorant Garamond fonts.
- Changed: 12 files, +386 / −334 (web/template.html, visual.py, tools/browser_check.mjs, tests/test_visual.py, README.md, CLAUDE.md, fonts)
- Checked: unknown
- Problems and fixes: unknown

## 035285e · 2026-10-16 08:59:58 -0700 · "Dark cinematic design for the poster"

- Planned: unknown
- Done: Changed the poster to a dark design. The template describes it as "The Fourth Watch": an engraving printed in darkness, lit by one light.
- Changed: 3 files, +485 / −280 (web/template.html, README.md, CLAUDE.md)
- Checked: unknown
- Problems and fixes: unknown

## 1cbc018 · 2026-10-16 21:52:28 -0700 · "Dark cinematic design: fixes from review"

- Planned: The message says the changes came from a review. What the review found is described only by the code comments listed below.
- Done: The new code comments describe these fixes:
  - shadow behind the title and buttons so they stay readable
  - room for letter tails in the gold title (like the J)
  - the verse stops before the figure
  - a gold first letter with a hanging quotation mark
  - a minimum size for the reference
  - a solid band at the top of the Context panel so scrolled text doesn't run behind the buttons
  - balanced quotation marks
  - short verses grow and long ones shrink
  - reduced-motion handling
  - smoother fast double clicks
- Changed: 2 files, +257 / −58 (web/template.html, CLAUDE.md)
- Checked (Claude Code ran these on 2026-10-16 with this commit checked out):
  - `python -m unittest discover tests` → "Ran 50 tests in 0.718s, OK"
  - `python main.py --date 2026-10-14` → showed the study for Wednesday, October 14, 2026 (1 Peter 4:8, "LOVE"), then exited on `quit`
  - `python visual.py --no-open` → built web/today.html, exit code 0
  - `node tools/browser_check.mjs` → "35/35 checks passed"
- Problems and fixes: unknown, beyond the fixes listed above

## 9f6388a · 2026-10-16 22:27:51 -0700 · "Add LOG.md for Artifact 2"

- Planned: unknown
- Done: Added the first version of this log, rebuilt from git history.
- Changed: LOG.md (1 file, +117 lines)
- Checked: `git log --oneline` showed the commit at the top.
- Problems and fixes: Its layout didn't match my portfolio log, so the log was rewritten in this format.

## 0d4a7ff · 2026-10-16 22:34:52 -0700 · "Ignore .env files"

- Planned: unknown
- Done: Added `.env` back to .gitignore.
- Changed: .gitignore (1 line)
- Checked: Created an empty .env file, ran `git check-ignore .env`, which printed `.env` (so it's ignored), then deleted the test file.
- Problems and fixes: Fixes the gap described under Issues.

## Changes I made by hand

- Created the verse-ai repo on GitHub.
- Ran the commit and push commands myself (GitHub has everything up to 1cbc018).
- Tested the poster in my browser and reported the Context panel overlapping the buttons.
- Shared three reference posters for the poster style.

## Decisions

Questions for me to answer:

1. Why did you remove the Claude breakdowns (7632956) and make the app fully offline (5854fdb)?
2. Why did you go from a pair of verses each day to one verse?
3. Why the Berean Standard Bible?
4. Why add a browser poster next to the command-line app?
5. Why did the poster go comic → parchment → dark (f239f20, deb2661, 035285e)?
6. What did you leave out on purpose?

## Issues

- `.env` was in .gitignore at 7632956, dropped in 5854fdb, and added back in 0d4a7ff. No .env file was ever committed (checked with `git log --all --name-only`).
- Some commits bundle several steps, so the steps in between aren't in the history. For example, 5854fdb removes the AI feature, switches to one verse a day, adds the study features and adds the poster, all in one commit.
- The commit messages don't say how changes were tested. The "Checked" lines are mostly "unknown" for that reason.
- There's an old local branch called `master` with only the initial commit. It isn't on GitHub.
