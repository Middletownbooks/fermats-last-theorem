#!/usr/bin/env python3
"""What the level axis says once every item carries it (debt D30).

Run from `proof-protocol/`. Read-only: it reports, and exits 1 if an item is missing the field, so it
can be used as a gate alongside tools/validate.py.

The axis was added because control 16 is only a valid control with the level stated -- Zhang left the
GPY sieve untouched and improved what it consumes. Once every item carries the field, three things
fall out that no single item shows, and they are printed below.
"""
from __future__ import annotations
import json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path("p1-retrodiction")
LEVELS = ["same-level", "input-level", "reduction-level", "substrate", "none", "unclear"]


def items() -> list[tuple[str, str, dict]]:
    out = []
    for p in sorted((ROOT / "heldout").glob("*.json")):
        out.append((p.stem, "case", json.loads(p.read_text(encoding="utf-8"))))
    for p in sorted((ROOT / "controls").glob("*.json")):
        out.append((p.stem, "control", json.loads(p.read_text(encoding="utf-8"))))
    return out


def main() -> int:
    rows = items()
    missing = [i for i, _, d in rows if (d.get("level") or {}).get("axis") not in LEVELS]
    dist = Counter((d["level"]["axis"] if not missing else "?") for _, _, d in rows
                   if (d.get("level") or {}).get("axis") in LEVELS)
    print(f"{len(rows)} scoreable items ({sum(1 for _, k, _ in rows if k == 'case')} cases, "
          f"{sum(1 for _, k, _ in rows if k == 'control')} controls)\n")
    for k in LEVELS:
        if dist[k]:
            print(f"  {k:16} {dist[k]:2}   " +
                  ", ".join(i for i, _, d in rows if d.get("level", {}).get("axis") == k))
    print()

    conf = Counter(d["level"]["confidence"].split("-")[0] for _, _, d in rows
                   if (d.get("level") or {}).get("axis") in LEVELS)
    print(f"  confidence: {dict(conf)}")
    med = [i for i, _, d in rows if d.get("level", {}).get("confidence") == "medium"]
    print(f"  the two at the weakest boundary (same-level vs reduction-level): {', '.join(med)}")

    print("""
  THREE THINGS THE AXIS SHOWS THAT NO SINGLE ITEM DOES

  1. The corpus is 10 of 13 SAME-LEVEL. Only one item in the whole tree changes an input and
     leaves the board (control 16), and it is a CONTROL, not a case. So the level axis is, on
     current material, almost constant on the positives -- which means it cannot discriminate
     positives from controls on its own, and must not be sold as if it could. What it does is stop
     control 16 from being mislabelled, which is what D30 asked for and all it asked for.

  2. Case 7 and control 16 are exact complements, and that is why the pair works. 7a changed the
     level-n board and consumed the same input ('one can avoid having to prove any difficult new
     results about primes in arithmetic progressions'); Zhang changed the input and left the
     level-n board. One problem, one year, two teams, opposite entries on this axis.

  3. The corpus contains a two-level stack it never encoded: case 13's old board CONSUMED case
     10's object -- PCP amplification by parallel repetition -- and Dinur's change removed that
     dependence rather than improving it. So one of the thirteen positives is a same-level change
     that ELIMINATED a level below. One instance is not a category, so no axis value was added for
     it; it is recorded in case 13's basis field.

  WHAT THIS PASS IS NOT. Single-encoder and unvalidated, like the v0 transformation labels. The one
  reason to expect better than kappa = 0.048 is D20: closed-vocabulary FIELDS reproduced at +0.811
  and +0.755 while the rule built on them did not, and this is a field. That is a reason for
  optimism, not evidence. The test is the D20 instrument over these 17 items with raters who have
  not seen taxonomy.json -- one field, so cheaper than D20 was.""")
    if missing:
        print(f"\n  ERROR: {len(missing)} item(s) missing level.axis: {', '.join(missing)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
