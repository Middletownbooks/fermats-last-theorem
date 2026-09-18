#!/usr/bin/env python3
"""Render LEDGER.md from ledger.json, with a calibration summary."""
from __future__ import annotations
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "ledger.json").read_text(encoding="utf-8"))
P = d["predictions"]
c = Counter(p["status"] for p in P)
settled = [p for p in P if p["status"] in ("correct", "wrong", "partly")]
right = c["correct"]

L = ["# Prediction ledger", "",
     f"*Generated from `ledger.json` by `tools/render_ledger.py`. As of {d['as_of']}.*", "",
     d["purpose"], "",
     "## Calibration", "",
     "| status | n |", "|---|---|"]
for k in ("correct", "partly", "wrong", "unscored", "open"):
    if c[k]:
        L.append(f"| {k} | {c[k]} |")
L += [f"| **total** | **{len(P)}** |", "",
      f"**{len(settled)} of {len(P)} predictions are settled.** Of those, "
      f"**{right} correct, {c['partly']} partly, {c['wrong']} wrong.**", ""]

by_author = Counter(p["by"] for p in P)
L += ["By author:", ""]
for a, n in by_author.most_common():
    sub = [p for p in P if p["by"] == a and p["status"] in ("correct", "wrong", "partly")]
    w = sum(1 for p in sub if p["status"] == "wrong")
    L.append(f"- **{a}** — {n} predictions, {len(sub)} settled, {w} wrong")
L += ["", "## The predictions", "",
      "| id | by | predicted | outcome | status |", "|---|---|---|---|---|"]
for p in P:
    esc = lambda s: str(s).replace("|", "\\|")
    L.append(f"| `{p['id']}` | {p['by']} | {esc(p['predicted'])} | {esc(p['outcome'])} "
             f"| **{p['status']}** |")
L += ["", "## What it cost", ""]
for p in P:
    if p.get("cost") and p["cost"] != "none":
        L.append(f"- **{p['id']}** — {p['cost']}")
L += ["", "## Lessons", ""]
for i, t in enumerate(d["lessons"], 1):
    L.append(f"{i}. {t}")
L += [""]
(ROOT / "LEDGER.md").write_text("\n".join(L), encoding="utf-8")
print(f"LEDGER.md: {len(P)} predictions, {len(settled)} settled, {right} correct, {c['wrong']} wrong")
