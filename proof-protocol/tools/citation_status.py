#!/usr/bin/env python3
"""One place that computes what the citation layer actually says.

citations.json APPENDS a superseding row rather than rewriting history, so three ids recur
(C15, C10, C12) and any count over raw rows double-counts them. Two views are therefore
distinct and both are wanted:

  * rows_view   -- every row ever written, which is what the CITATIONS.md summary has always
                   shown and is kept so published numbers do not move under the reader;
  * latest_view -- the LAST row per id, which is the layer's current state and the only view
                   a prose sentence about "what is still open" may be written from.

Typed counts have now been wrong in both directions in this tree: D19's action text
undercounted by omitting C1-gotsman, and its replacement overcounted by calling C10 and C12
UNVERIFIED after later rows had moved them to SEARCH and PARTIAL. Both are recorded in D19.
Counts that can be derived are derived here and nowhere else.
"""
from __future__ import annotations
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent

# A row's status string may carry a qualifier ("VERIFIED (COMPUTED)"); the tier is the first word.
def tier(status: str) -> str:
    return status.split()[0]


def load(root: pathlib.Path | None = None) -> dict:
    root = root or ROOT
    d = json.loads((root / "citations.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    latest: dict[str, dict] = {}
    for r in rows:                      # later rows supersede earlier ones with the same id
        latest[r["id"]] = r
    return {
        "as_of": d["as_of"],
        "rows": rows,
        "latest": latest,
        "recurring": sorted(i for i, n in Counter(r["id"] for r in rows).items() if n > 1),
        "rows_view": Counter(tier(r["status"]) for r in rows),
        "latest_view": Counter(tier(r["status"]) for r in latest.values()),
        "unverified": sorted(i for i, r in latest.items() if tier(r["status"]) == "UNVERIFIED"),
        "below_primary": sorted(i for i, r in latest.items()
                                if tier(r["status"]) in ("SEARCH", "PARTIAL")),
    }


def caveat(st: dict) -> str:
    """The standing caveat in debts.json, generated rather than typed."""
    lv = ", ".join(f"{v} {k}" for k, v in sorted(st["latest_view"].items(), key=lambda kv: -kv[1]))
    return (
        f"Of P1's citation layer, {len(st['rows'])} rows cover {len(st['latest'])} distinct claims "
        f"({len(st['recurring'])} ids recur because a later pass supersedes an earlier row rather "
        f"than rewriting it: {', '.join(st['recurring'])}). By latest row per id: {lv}. Still "
        f"UNVERIFIED: {', '.join(st['unverified']) or 'none'}. Below fetched-primary tier: "
        f"{', '.join(st['below_primary']) or 'none'}. Egress stayed blocked for the whole session "
        f"-- no PDF was ever fetched -- so every closure at PRIMARY tier came from a transcript "
        f"pasted in by the user, which this project counts as a fetched primary source (C3, C7, C9, "
        f"N3, C15). Two VERIFIED twin rows, N16 and N20, still rest on STANDARD-tier claims and say "
        f"so. See CITATIONS.md."
    )


if __name__ == "__main__":
    st = load()
    print(f"rows {len(st['rows'])}  distinct ids {len(st['latest'])}  recurring {st['recurring']}")
    print("rows_view  ", dict(st["rows_view"]))
    print("latest_view", dict(st["latest_view"]))
    print("unverified ", st["unverified"])
    print("below_primary", st["below_primary"])
    print()
    print(caveat(st))
