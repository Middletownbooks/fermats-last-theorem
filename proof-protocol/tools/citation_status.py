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


# The per-source flags inside the ITEM files are a second place where prose can drift from data --
# D33 was opened when control 14's three sources all said verified: false while row C14 stood
# VERIFIED. These counts are derived here so no document has to type them.
ITEM_GLOBS = ("cases/*/before.json", "twins/*.json", "controls/*.json")
SKIP_STEMS = {"REJECTED"}


def item_flags(root: pathlib.Path | None = None) -> dict:
    root = (root or ROOT) / "p1-retrodiction"
    n = true = 0
    n_unrowed = [0]                     # flags, which can exceed the number of FILES they sit in
    tiers: Counter = Counter()
    unrowed_true: list[str] = []
    for g in ITEM_GLOBS:
        for f in sorted(root.glob(g)):
            if f.stem in SKIP_STEMS:
                continue
            stack = [json.loads(f.read_text(encoding="utf-8"))]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    if "cite" in cur and "verified" in cur:
                        n += 1
                        true += bool(cur["verified"])
                        tiers[str(cur.get("tier", "NONE")).split()[0]] += 1
                        if cur["verified"] and cur.get("citation_row") is None:
                            unrowed_true.append(f.parent.name if f.name == "before.json" else f.stem)
                            n_unrowed[0] += 1
                    stack.extend(cur.values())
                elif isinstance(cur, list):
                    stack.extend(cur)
    return {"n": n, "verified": true, "tiers": tiers, "unrowed_true": sorted(set(unrowed_true)),
            "n_unrowed_true": n_unrowed[0]}


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


def item_caveat(fl: dict) -> str:
    t = ", ".join(f"{v} {k}" for k, v in sorted(fl["tiers"].items(), key=lambda kv: -kv[1]))
    return (
        f"Inside the ITEM files, {fl['n']} per-source flags now each name the citations.json row they "
        f"stand on, or state that no row covers them: {fl['verified']} read verified, "
        f"{fl['n'] - fl['verified']} do not, by tier {t}. "
        f"{fl['n_unrowed_true']} flags across {len(fl['unrowed_true'])} twins read verified on a "
        f"DECLARED basis with no row at all ({', '.join(fl['unrowed_true']) or 'none'}), which is "
        f"recorded rather than swept. "
        f"tools/check_consistency.py fails the tree if a flag reads verified without a row whose "
        f"status is VERIFIED or CORRECTED, or if any flag lacks a stated basis. Debt D33."
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
    print()
    print(item_caveat(item_flags()))
