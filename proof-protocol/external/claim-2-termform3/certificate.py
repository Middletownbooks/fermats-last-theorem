#!/usr/bin/env python3
"""
PREREG section 3 — prove, before any condition is scored, that the carried terms
are NOT formable by the receiving round's own formation stage at body budget 3.

The proof is exhaustive rather than analytic: run the receiving round's formation
exactly as the conditions will run it (two stages, bodies capped at 3, units from
stage 1 available in stage 2), with the caps raised far past the space's size and
the beam off, and assert that no formed term has a carried term's value vector on
TRAIN.

Anything that turns out to be formable is STRUCK from the carried set and the
strike is recorded -- the check Report P's leakage audit performed too late to
protect target T3.
"""
import ast
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
T2 = HERE.parent / "termform2"
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(T2))

import synth3 as S                                           # noqa: E402
from round2 import TRAIN                                     # noqa: E402

BODY_BUDGET = 3
BIG = 10 ** 9


def formed_at_budget(b):
    """Every term the receiving round's formation can produce at body budget b,
    exhaustively. Mirrors synth3.form_leaves with size1 = size2 = b, caps off."""
    S.reset()
    grid = [(o, k) for o in TRAIN for k in range(1, min(o, 6) + 1)]
    envs = {i: {"n": n, "k": k} for i, (n, k) in enumerate(grid)}
    idx = list(range(len(grid)))
    b1, _, trunc1 = S.enumerate_terms(["n", "k"], idx, b, env_for=lambda i: envs[i],
                                      cap=BIG, tag="cert1")
    formed = {}

    def wrap_all(bodies):
        for body in bodies:
            for w in ("least", "count"):
                t = (w, body)
                try:
                    v = tuple(S.ev(t, {"n": o}) for o in TRAIN)
                except Exception:
                    continue
                formed.setdefault(v, t)

    wrap_all(b1.values())
    stage1 = len(formed)
    units = [S.leaf(t, TRAIN) for t in formed.values()]
    b2, _, trunc2 = S.enumerate_terms(["n", "k"], idx, b, extra_leaves=units,
                                      ops=["mod", "div", "sub", "mul", "pow", "add"],
                                      env_for=lambda i: envs[i], cap=BIG, tag="cert2")
    wrap_all(b2.values())
    return formed, {"stage1_formed": stage1, "stage2_formed_total": len(formed),
                    "stage1_body_classes": len(b1), "stage2_body_classes": len(b2),
                    "truncated_stage1": trunc1, "truncated_stage2": trunc2,
                    "bodies_exhausted": not (trunc1 or trunc2)}


def main():
    t0 = time.time()
    prom = json.loads((HERE / "promoted3.json").read_text())
    carried = [(p["term"], ast.literal_eval(r)) for p, r in
               zip([q for q in prom["terms"] if not q["formable_at_body_3"]],
                   prom["out_of_reach_tuples"])]
    formed, stats = formed_at_budget(BODY_BUDGET)
    print("formation at body budget %d, exhaustive: %s" % (BODY_BUDGET, stats), flush=True)

    S.reset()
    rows, struck = [], []
    for printed, t in carried:
        try:
            v = tuple(S.ev(t, {"n": o}) for o in TRAIN)
        except Exception:
            rows.append({"term": printed, "status": "UNEVALUABLE"})
            continue
        hit = formed.get(v)
        rec = {"term": printed, "value_vector_head": list(v[:8]),
               "formable_at_budget_3": hit is not None}
        if hit is not None:
            rec["formed_as"] = S.show(hit)
            struck.append(printed)
        rows.append(rec)
        print("  %-9s %s" % ("STRUCK" if hit is not None else "out of reach", printed[:62]),
              flush=True)

    out = {"label": "CERTIFICATE",
           "question": "is each carried term formable by the receiving round at body budget 3?",
           "method": ("the receiving round's own two-stage formation, bodies capped at 3, "
                      "caps raised to 1e9 and the beam off, so the body space is exhausted"),
           "body_budget": BODY_BUDGET,
           "formation_stats": stats,
           "carried_candidates": len(carried),
           "certified_out_of_reach": [r["term"] for r in rows if r.get("formable_at_budget_3") is False],
           "struck_because_formable": struck,
           "rows": rows,
           "seconds": round(time.time() - t0, 1)}
    (HERE / "certificate.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("\n%d of %d certified out of reach; %d struck (%.0fs)"
          % (len(out["certified_out_of_reach"]), len(carried), len(struck), out["seconds"]))


if __name__ == "__main__":
    main()
