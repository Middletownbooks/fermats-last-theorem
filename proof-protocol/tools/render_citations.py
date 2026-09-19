#!/usr/bin/env python3
"""Render CITATIONS.md from citations.json so the prose cannot drift from the data."""
from __future__ import annotations
import json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import citation_status                                   # noqa: E402

d = json.loads((ROOT / "citations.json").read_text(encoding="utf-8"))
rows = d["rows"]
c = Counter(r["status"].split()[0] for r in rows)
st = citation_status.load(ROOT)

L = ["# Citation verification (task 1)", "",
     f"*Generated from `citations.json` by `tools/render_citations.py`. As of {d['as_of']}.*", "",
     "## What could be checked, and what could not", "",
     f"> {d['environment']}", "", f"**Standard applied.** {d['standard']}", "",
     "## Summary", "",
     "| status | rows |", "|---|---|"]
for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
    L.append(f"| {k} | {v} |")
L += [f"| **total** | **{len(rows)}** |", ""]

# Rows are APPENDED when a later pass supersedes an earlier one, so the table above counts some
# claims twice. The current state is the last row per id, and it is the only view a sentence about
# what is still open may be written from. See tools/citation_status.py and debt D19.
L += ["## Current state (last row per id)", "",
      f"The table above counts **every row ever written**, including superseded ones: "
      f"{len(rows)} rows cover {len(st['latest'])} distinct claims, because "
      f"{len(st['recurring'])} ids recur ({', '.join(f'`{i}`' for i in st['recurring'])}) where a "
      f"later pass superseded an earlier row instead of rewriting it. Counting the latest row per id:",
      "", "| status | claims |", "|---|---|"]
for k, v in sorted(st["latest_view"].items(), key=lambda kv: -kv[1]):
    L.append(f"| {k} | {v} |")
L += [f"| **distinct claims** | **{len(st['latest'])}** |", "",
      f"**Still UNVERIFIED:** {', '.join(f'`{i}`' for i in st['unverified']) or 'none'}. "
      f"**Below fetched-primary tier:** {', '.join(f'`{i}`' for i in st['below_primary']) or 'none'}. "
      f"Two VERIFIED twin rows, `N16` and `N20`, rest on STANDARD-tier claims and say so.", ""]

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
