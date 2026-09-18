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

# Items retired when the repo corpus is swapped in. The rule: retire an item whose correct answer
# is a single named textbook fact with a one-line proof, or a famous named open problem. Those are
# where a capable model sits at ceiling, and an item nothing fails cannot separate arms.
#
# THIS IS A PREDICTION, NOT A MEASUREMENT. It has not been piloted — see README. Whoever runs the
# pilot should report the per-item bare failure rate and re-choose from that, not from this list.
RETIRE_FOR_CORPUS = {
    "T1": "no n>1 divides 2^n-1 — the smallest-prime-factor argument is a standard one-liner",
    "T5": "a^2+b^2+c^2 >= a+b+c under abc=1 — direct AM-GM",
    "F2": "ab+bc+ca >= a+b+c under abc=1 — a small counterexample is easy to find",
    "F3": "exponent-3 groups abelian? — the Heisenberg group over F_3 is the textbook answer",
    "O1": "2^p-1 squarefree — a famous named open problem, so (c) is the easy correct return",
    "O2": "Brocard's problem — likewise famous, likewise an easy correct (c)",
}
CORPUS_PATH = "battery_repo_corpus.json"
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
         include_default: bool = True,
         retire: set[str] | None = None) -> list[dict]:
    items = [dict(p) for p in blocks.BATTERY0] if include_default else []
    if retire:
        items = [p for p in items if p["id"] not in retire]
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
