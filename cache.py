"""Saved breakdowns, so a pair you've already seen works offline (and costs nothing)."""

from __future__ import annotations

import json
from pathlib import Path

CACHE_FILE = Path(__file__).parent / "cache" / "breakdowns.json"


def _key(main_ref: str, partner_ref: str) -> str:
    return f"{main_ref} | {partner_ref}"


def _read(path: Path) -> dict[str, str]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_breakdown(main_ref: str, partner_ref: str, path: Path = CACHE_FILE) -> str | None:
    return _read(path).get(_key(main_ref, partner_ref))


def save_breakdown(main_ref: str, partner_ref: str, text: str, path: Path = CACHE_FILE) -> None:
    data = _read(path)
    data[_key(main_ref, partner_ref)] = text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
