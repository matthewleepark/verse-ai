"""Choosing each day's pair: a curated wisdom verse + a random partner verse.

The wisdom verse keeps every day on theme; the partner comes from anywhere in
the Bible (~31,000 verses), so the combinations practically never repeat.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, replace
from datetime import date

from bible import Verse, lookup, random_verse

WISDOM_VERSES: dict[str, list[str]] = {
    "patience": [
        "James 1:19",
        "Proverbs 14:29",
        "Proverbs 16:32",
        "Proverbs 19:11",
        "Ecclesiastes 7:8",
        "Romans 12:12",
        "Galatians 6:9",
        "Colossians 3:12",
        "James 5:7",
        "Psalm 37:7",
    ],
    "empathy": [
        "Romans 12:15",
        "Galatians 6:2",
        "Philippians 2:4",
        "Luke 6:31",
        "1 Peter 3:8",
        "Ephesians 4:32",
        "Proverbs 31:8",
        "Matthew 25:40",
        "Hebrews 13:3",
        "1 John 3:17",
    ],
    "conflict resolution": [
        "Proverbs 15:1",
        "Proverbs 15:18",
        "Proverbs 17:14",
        "Proverbs 20:3",
        "Matthew 5:9",
        "Matthew 5:24",
        "Matthew 18:15",
        "Romans 12:18",
        "Ephesians 4:26",
        "Colossians 3:13",
    ],
    "integrity": [
        "Proverbs 10:9",
        "Proverbs 11:3",
        "Proverbs 12:22",
        "Proverbs 20:7",
        "Proverbs 22:1",
        "Psalm 15:2",
        "Micah 6:8",
        "Luke 16:10",
        "Matthew 5:37",
        "Titus 2:7",
    ],
}

THEMES = list(WISDOM_VERSES)


@dataclass(frozen=True)
class DailyPair:
    main: Verse     # the wisdom verse (or the one asked for with --ref)
    partner: Verse  # random verse from anywhere in the Bible


def _pool(theme: str | None) -> list[tuple[str, str]]:
    if theme is None:
        return [(t, ref) for t, refs in WISDOM_VERSES.items() for ref in refs]
    if theme not in WISDOM_VERSES:
        raise ValueError(f"Unknown theme {theme!r}. Choose from: {', '.join(THEMES)}")
    return [(theme, ref) for ref in WISDOM_VERSES[theme]]


def pick_reference(day: date | None = None, theme: str | None = None) -> tuple[str, str]:
    """Deterministically pick (theme, reference) for a given day."""
    day = day or date.today()
    pool = _pool(theme)
    return pool[day.toordinal() % len(pool)]


def get_pair(
    day: date | None = None,
    theme: str | None = None,
    reference: str | None = None,
    shuffle: bool = False,
) -> DailyPair:
    """Build the day's pair. Same day -> same pair, unless shuffle=True."""
    day = day or date.today()
    rng = random.Random() if shuffle else random.Random(day.toordinal())
    if reference:
        main = lookup(reference)
    else:
        chosen_theme, ref = rng.choice(_pool(theme)) if shuffle else pick_reference(day, theme)
        main = replace(lookup(ref), theme=chosen_theme)
    partner = random_verse(rng, exclude=frozenset({main.reference}))
    return DailyPair(main, partner)
