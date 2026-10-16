# verse-ai

A free, offline daily Bible study. It needs no internet, no account and no API key.

**A new verse every day.** verse-ai steps through a list of 416 well-known verses, one per day, so the verse changes daily and doesn't repeat for more than a year. Each verse has a one-word title (HOPE, STILLNESS, COURAGE, WATERS...). It comes in two forms:

- **The poster:** an interactive picture in your browser. Jesus stands still while the sea around him keeps moving.
- **The study app:** a command-line companion with study notes, a daily reading, a journal and a streak.

## Getting started (Windows)

1. Install Python 3.10 or newer from https://python.org.
2. In the project folder, run once:
   ```powershell
   python -m venv .venv
   powershell -ExecutionPolicy Bypass -File make_shortcut.ps1
   ```
3. Two icons appear on your Desktop and in the Start menu: **verse-ai poster** and **verse-ai**.

## The poster

Double-click **verse-ai poster**, or run `python visual.py`. It opens full screen in your browser. A woodcut of Jesus catching Peter stands in the middle of a comic-book sea: rows of inked waves with foam, spray and halftone shading, light rays behind Jesus, storm clouds and rain. The waves move in small steps, like hand-drawn animation. The day's title word appears in big comic lettering, and the verse sits in a caption box.

| Do this | What happens |
|---|---|
| Click the water | A splash: droplets fly up and rings spread out |
| Move the mouse over the sea | Small rings follow the pointer |
| ← / → (or the ‹ › buttons, which show the dates) | The previous or next day's verse |
| Swipe left / right on a touchscreen | The next / previous day's verse |
| T or **Today** | Back to today's verse (always the real date) |
| C or **Context** | A side panel with the surrounding passage, study notes and background on the book |
| **Share** | Copy the verse as text, or save a share-card image of it |
| Space | Pause or resume the waves |

**Moving between days** is a short, directional transition:

- **Going forward:** the old title drifts toward you and dissolves while the next one rises out of the depth, letter by letter from left to right.
- **Going back:** the old title recedes into the distance while the previous one comes forward, letter by letter from right to left.
- **The scene:** it glides in the direction of travel, with near waves moving more than far ones, as a soft band of light and a few motes sweep across. Each verse has its own sky, and the sky blends from one to the next.
- **The verse text:** it only crossfades with a small slide, so it stays easy to read.

If your system is set to reduce motion, verse changes become a short fade.

The day you're viewing is kept in the page address (for example `today.html#2026-10-20`), so reloading keeps your place. Browsing never changes which verse belongs to today.

The sea and sky are drawn live, so they fill any screen shape. The woodcut figures stay perfectly still. The page has every day's verse, the artwork and the fonts built in, so it works offline and you can browse days without running Python again.

## The study app

Double-click **verse-ai**, or run `python main.py`. Each day shows the verse with study notes. The 40 wisdom verses have written notes (Universal Wisdom, Historical Context, Theological Meaning); every other verse shows its surrounding passage and background on its book. You also get a reflection question and a daily chapter of Proverbs.

| Command | What it does |
|---|---|
| `read` | Today's chapter of Proverbs (counts toward your streak) |
| `context` | The verses around today's verse |
| `journal` | Write a reflection, saved to `journals/YYYY-MM-DD.md` (counts toward your streak) |
| `poster` | Open today's verse as the poster |
| `history` | Your streak and past days |
| `study` / `help` / `quit` | Show the study again / list the commands / exit |

## Options (for both `main.py` and `visual.py`)

```powershell
--date 2026-12-25        # the verse for another day
--ref "Romans 12:9-12"   # any verse or passage
--theme patience         # a wisdom verse on patience, empathy, conflict resolution or integrity
--shuffle                # a random verse right now
```

## Files

| File | Role |
|---|---|
| `data/bsb.txt` | The full Berean Standard Bible |
| `data/daily_verses.json` | The 416 daily verses and their title words |
| `data/study_notes.json` | Study notes for the 40 wisdom verses |
| `data/books.json` | Background on all 66 books |
| `web/template.html` | The poster (WebGL comic sea and sky, splashes, controls, Context panel) |
| `visual.py` | Fills the poster with the verses and opens it |

Your journal and streak stay on your computer and are never uploaded.

## Tests

```powershell
python -m unittest discover tests
```

There is also an end-to-end check that drives the poster in a real (headless) Microsoft Edge. It needs Node.js 22 or newer. It tests forward and backward transitions, rapid clicks, Today, keyboard, Context and Share staying in sync, reduced motion, and a phone layout with swipes:

```powershell
python visual.py --no-open
node tools/browser_check.mjs
```

## Why not the NIV?

The NIV is copyrighted by Biblica, and its license doesn't allow bundling the full text. The Berean Standard Bible is a modern translation that reads similarly, and it has been dedicated to the public domain, so it can ship with the project.

## Credits

- **Bible text:** the Berean Standard Bible (BSB), public domain, from [bereanbible.com](https://bereanbible.com).
- **Artwork:** "Jesus Rescues the Sinking Peter", a woodcut by Julius Schnorr von Carolsfeld from *Die Bibel in Bildern* (1860). Public domain, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Schnorr_von_Carolsfeld_Bibel_in_Bildern_1860_194.png).
- **Fonts:** [Bangers](https://github.com/googlefonts/bangers) and [Comic Neue](https://github.com/crozynski/comicneue), both under the SIL Open Font License 1.1 (see `web/assets/*-OFL.txt`).
