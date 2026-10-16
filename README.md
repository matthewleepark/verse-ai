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

Double-click **verse-ai poster**, or run `python visual.py`. It shows a woodcut of Jesus catching Peter on the sea, with the day's title word set in tall serif letters behind Jesus and the verse beneath.

| Do this | What happens |
|---|---|
| Click the water | Ripples spread out from that point |
| Move the mouse over the sea | A gentle wake follows the pointer |
| ← / → or the ‹ › buttons | The previous or next day's verse |
| T or **Today** | Back to today |
| I or **About** | Study notes, the passage around the verse, and background on the book |
| Space | Pause or resume the waves |

Only the sea moves. A hand-traced outline keeps Jesus, Peter and the boat perfectly still. The page has every day's verse, the artwork and the font built in, so it works offline and you can browse days without running Python again.

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
| `web/template.html` | The poster (WebGL water, ripples, controls) |
| `visual.py` | Fills the poster with the verses and opens it |

Your journal and streak stay on your computer and are never uploaded.

## Tests

```powershell
python -m unittest discover tests
```

## Why not the NIV?

The NIV is copyrighted by Biblica, and its license doesn't allow bundling the full text. The Berean Standard Bible is a modern translation that reads similarly, and it has been dedicated to the public domain, so it can ship with the project.

## Credits

- **Bible text:** the Berean Standard Bible (BSB), public domain, from [bereanbible.com](https://bereanbible.com).
- **Artwork:** "Jesus Rescues the Sinking Peter", a woodcut by Julius Schnorr von Carolsfeld from *Die Bibel in Bildern* (1860). Public domain, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Schnorr_von_Carolsfeld_Bibel_in_Bildern_1860_194.png).
- **Font:** [Bodoni Moda](https://github.com/indestructible-type/Bodoni), SIL Open Font License 1.1 (see `web/assets/BodoniModa-OFL.txt`).
