"""The planted-truth battery.

The 15 items are the artifact's. The handoff's first priority is to REPLACE the weakest of them
with real agent failures that already have a non-zero failure rate on a real agent (the false
impossibility theorem with a published counterexample, the two unsupported "this forces that"
steps, the variance-1 Monte Carlo check). Those artifacts are not in this repository; see the
top-level README. Until they arrive, load them from a file:

    battery.load(extra_path="my-items.json")

Each extra item needs {id, type: true|false|open, statement, truth}, and may carry
{provenance, source_failure} to record that it came from an observed failure rather than a textbook.
"""
from __future__ import annotations
import json, pathlib
import blocks

REQUIRED = ("id", "type", "statement", "truth")
TYPES = ("true", "false", "open")


class BadBatteryItem(ValueError):
    pass


def validate(items: list[dict]) -> None:
    seen = set()
    for it in items:
        for k in REQUIRED:
            if not it.get(k):
                raise BadBatteryItem(f"item {it.get('id', '?')!r} is missing {k!r}")
        if not it["id"].isalnum():
            raise BadBatteryItem(f"id {it['id']!r} must be alphanumeric")
        if it["type"] not in TYPES:
            raise BadBatteryItem(f"item {it['id']!r} has type {it['type']!r}")
        if it["id"] in seen:
            raise BadBatteryItem(f"duplicate id {it['id']!r}")
        seen.add(it["id"])


def load(extra_path: str | pathlib.Path | None = None,
         include_default: bool = True) -> list[dict]:
    items = [dict(p) for p in blocks.BATTERY0] if include_default else []
    for it in items:
        it.setdefault("provenance", "artifact-battery-v0 (textbook-grade; expected to hit ceiling)")
    if extra_path:
        extra = json.loads(pathlib.Path(extra_path).read_text(encoding="utf-8"))
        if not isinstance(extra, list):
            raise BadBatteryItem("extra battery file must be a JSON list")
        for it in extra:
            it.setdefault("provenance", "operator-supplied")
        items += extra
    validate(items)
    return items


def types(items: list[dict]) -> dict[str, str]:
    return {p["id"]: p["type"] for p in items}


def by_id(items: list[dict], pid: str) -> dict:
    return next(p for p in items if p["id"] == pid)
