#!/usr/bin/env python3
"""Render DEBTS.md from debts.json, so the prose cannot drift from the data."""
from __future__ import annotations
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "debts.json").read_text(encoding="utf-8"))

L = ["# Verification debts and the failure register",
     "",
     f"*Generated from `debts.json` by `tools/render_debts.py`. As of {d['as_of']}. "
     "Edit the JSON, not this file.*", ""]

L += ["## Standing caveats", ""]
L += [f"- {g}" for g in d["global"]]
L += ["", "## Debts", "",
      "| id | kind | status | where | claim | what closing it takes |",
      "|---|---|---|---|---|---|"]
for x in d["debts"]:
    claim = x["claim"].replace("|", "\\|")
    action = x["action"].replace("|", "\\|")
    L.append(f"| **{x['id']}** | {x['kind']} | `{x['status']}` | `{x['where']}` | {claim} | {action} |")

blocking = [x for x in d["debts"] if x.get("blocking")]
if blocking:
    L += ["", "### Blocking", ""]
    L += [f"- **{x['id']}** blocks {x['blocking']}." for x in blocking]

L += ["", "## Failure register", "",
      "What was tried, what happened, what it cost.", "",
      "| tried | outcome | cost |", "|---|---|---|"]
for f in d["failure_register"]:
    L.append(f"| {f['tried']} | {f['outcome']} | {f['cost']} |")

L += ["", "## Do not do", ""]
L += [f"{i}. {t}" for i, t in enumerate(d["do_not_do"], 1)]
L += [""]

(ROOT / "DEBTS.md").write_text("\n".join(L), encoding="utf-8")
print(f"DEBTS.md: {len(d['debts'])} debts, "
      f"{sum(1 for x in d['debts'] if x['status'] in ('unverified', 'unadjudicated', 'unvalidated', 'blocked', 'open'))} open")
