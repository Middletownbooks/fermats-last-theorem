#!/usr/bin/env python3
"""Render CITATIONS.md from citations.json so the prose cannot drift from the data."""
from __future__ import annotations
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "citations.json").read_text(encoding="utf-8"))
rows = d["rows"]
c = Counter(r["status"].split()[0] for r in rows)

L = ["# Citation verification (task 1)", "",
     f"*Generated from `citations.json` by `tools/render_citations.py`. As of {d['as_of']}.*", "",
     "## What could be checked, and what could not", "",
     f"> {d['environment']}", "", f"**Standard applied.** {d['standard']}", "",
     "## Summary", "",
     "| status | rows |", "|---|---|"]
for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
    L.append(f"| {k} | {v} |")
L += [f"| **total** | **{len(rows)}** |", ""]

changed = [r for r in rows if r["status"].startswith(("CORRECTED", "DISPUTED"))]
if changed:
    L += ["## Rows that changed a claim", "",
          "These are the ones downstream work must read instead of P1's original.", ""]
    for r in changed:
        L += [f"### {r['id']} — {r['status']}", "",
              f"**Where.** `{r['where']}`", "",
              f"**Claim as written.** {r['claim']}", "",
              f"**What the source says.** {r['found']}", ""]
        if r.get("correction"):
            L += [f"**Correction.** {r['correction']}", ""]
        if r.get("consequence"):
            L += [f"**Consequence.** {r['consequence']}", ""]
        if r.get("source"):
            L += [f"*Source:* {r['source']}", ""]

L += ["## All rows", "",
      "| id | where | status | claim as written | what the source says |",
      "|---|---|---|---|---|"]
for r in rows:
    esc = lambda s: str(s or "").replace("|", "\\|")
    L.append(f"| `{r['id']}` | {esc(r['where'])} | **{r['status']}** | {esc(r['claim'])} | "
             f"{esc(r.get('found') or r.get('note') or '—')} |")

L += ["", "## Refinements worth carrying", ""]
for r in rows:
    if r.get("refinement"):
        L.append(f"- **{r['id']}** — {r['refinement']}")

L += ["", "## Adjudications", "",
      "The two reclassifications the seed asked to have settled. These are arguments, not "
      "citations, and are adjudicated on the record.", ""]
for a in d["adjudications"]:
    L += [f"### {a['id']} — {a['subject']}", "", f"**Verdict: {a['verdict']}**", "",
          a["reasoning"], ""]

L += ["## Unverified, and staying that way until someone has network access", "",
      "Declaring what could not be checked is part of the deliverable.", ""]
for r in rows:
    if r["status"] == "UNVERIFIED":
        L.append(f"- **{r['id']}** (`{r['where']}`) — {r['claim']}")
L += [""]
(ROOT / "CITATIONS.md").write_text("\n".join(L), encoding="utf-8")
print(f"CITATIONS.md: {len(rows)} rows, {dict(c)}")
