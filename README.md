# verse-ai

A command-line study companion. Each day it pairs two Bible verses:

- **Today's verse** is chosen for its wisdom on patience, empathy, conflict resolution, or integrity.
- **Its partner** is picked at random from anywhere in the Bible, giving about 31,000 possible partners each day.

Claude explains the main verse in three parts (Universal Wisdom, Historical Context, Theological Meaning) and then shows how the partner verse connects to it. After that you can ask follow-up questions, get a summary, or write a journal reflection.

## Works offline

The whole Bible is stored in `data/bsb.txt`, so verses never need the internet. Journaling works offline too.

Claude (breakdowns, questions, summaries) needs internet. Each breakdown is saved to `cache/` the first time it's generated, so a pair you've seen before shows its breakdown offline. If you're offline or have no API key, the app tells you and keeps working without AI.

## Setup (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For the AI features, get an API key from https://console.anthropic.com and run:

```powershell
setx ANTHROPIC_API_KEY "sk-ant-..."
```

`setx` only applies to new terminals, so open one afterwards. Never commit your key.

## Usage

```powershell
python main.py                        # today's pair + breakdown, then interactive mode
python main.py --theme empathy        # main verse from one theme
python main.py --shuffle              # a brand-new random pair
python main.py --ref "Romans 12:9-12" # choose the main verse (ranges work)
python main.py --date 2026-12-25      # the pair for another day
python main.py --once                 # breakdown only
python main.py --offline              # never contact Claude
```

In interactive mode, type any question, or one of these commands: `summary`, `journal`, `verse`, `help`, `quit`.
Journal entries go in `journals/YYYY-MM-DD.md`, one file per day.

## Tests

```powershell
python -m unittest discover tests
```

The tests fake Claude, so they need neither internet nor an API key.

## Why not the NIV?

The NIV is copyrighted by Biblica, and its license doesn't allow bundling the full text. The Berean Standard Bible is a modern translation that reads similarly, and it has been dedicated to the public domain, so it can ship with the project.

## Credits

Bible text: the Berean Standard Bible (BSB), public domain, from [bereanbible.com](https://bereanbible.com).
