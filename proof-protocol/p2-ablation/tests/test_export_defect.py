#!/usr/bin/env python3
"""Regression test for DEFECT-1, the judge-2 fallback in the published harness.

The artifact's exportData calls outcome(r, r.j2). outcome() begins `j = j || r.j1`, so on every
row where the second judge did not run, judge 2's exported column is scored FROM JUDGE 1. Rows
that should be blank instead agree with judge 1 by construction, which inflates any inter-judge
agreement computed from the exported CSV toward 1.

This test pins the fixed behaviour and demonstrates the defect it replaces, so a future edit that
reintroduces the fallback fails here.
"""
from __future__ import annotations
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import outcomes  # noqa: E402

TYPE = "false"
# judge 1 says a valid counterexample; judge 2 never ran.
RUN = {"id": "main_F1_X01_1", "phase": "main", "pid": "F1", "arm": "X01",
       "j1": {"return_class": "b", "valid": True}}


def main() -> int:
    bad = []

    # The defect, reproduced exactly: passing the missing judgement through falls back to j1.
    buggy = outcomes.outcome(RUN, TYPE, RUN.get("j2"))
    if buggy is None:
        bad.append("outcome() no longer falls back; the frozen rule was changed, which is a "
                   "re-freeze and must be declared")
    elif buggy != outcomes.outcome(RUN, TYPE, RUN["j1"]):
        bad.append("fallback no longer reproduces judge 1 — unexpected change to the frozen rule")
    else:
        print("ok   frozen rule still falls back to j1 (unchanged, as required)")

    # The fix lives at the call site.
    fixed = outcomes.outcome(RUN, TYPE, RUN["j2"]) if RUN.get("j2") else None
    if fixed is not None:
        bad.append("guarded call site still produced an outcome for an absent judge 2")
    else:
        print("ok   guarded call site yields no judge-2 outcome when judge 2 did not run")

    # And the exporter must use the guarded form.
    src = (pathlib.Path(__file__).resolve().parent.parent / "cli.py").read_text()
    if 'outcomes.outcome(r, types[r["pid"]], r.get("j2"))' in src:
        bad.append("cli.py still exports judge 2 through the unguarded call — DEFECT-1 is back")
    elif 'r["j2"]) if r.get("j2") else None' not in src:
        bad.append("cli.py's judge-2 export is neither the buggy form nor the guarded form")
    else:
        print("ok   cli.py exports judge 2 through the guarded call")

    # What the defect cost: agreement measured off the exported column.
    rows = [dict(RUN, id=f"r{i}") for i in range(10)]
    for r in rows[:5]:                      # half the rows did get a second judge, and it differs
        r["j2"] = {"return_class": "c", "valid": False}
    buggy_agree = sum(1 for r in rows
                      if outcomes.outcome(r, TYPE, r.get("j1")) ==
                         outcomes.outcome(r, TYPE, r.get("j2"))) / len(rows)
    true_agree_rows = [r for r in rows if r.get("j2")]
    true_agree = sum(1 for r in true_agree_rows
                     if outcomes.outcome(r, TYPE, r["j1"]) ==
                        outcomes.outcome(r, TYPE, r["j2"])) / len(true_agree_rows)
    print(f"\n   on 10 rows, 5 with a second judge who disagreed on every one:")
    print(f"     agreement as the published harness would export it : {buggy_agree:.0%}")
    print(f"     agreement over rows that actually have two judges  : {true_agree:.0%}")
    if buggy_agree <= true_agree:
        bad.append("the defect demonstration did not show inflation; rewrite the fixture")

    if bad:
        print("\n" + "\n".join(f"  {b}" for b in bad))
        return 1
    print("\nDEFECT-1 regression test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
