#!/usr/bin/env python3
"""The pre-registered analysis. Read analysis/preregistration.md before running this.

    python3 analysis/analyze.py describe --csv runs.csv
    python3 analysis/analyze.py power    --csv runs.csv
    python3 analysis/analyze.py model    --csv runs.csv        (needs statsmodels)

The harness's own intervals treat runs as independent. They are not: every arm sees the same
problems, so those intervals are too narrow and are for monitoring only. The analysis of record is
the mixed-effects logistic regression below.

Resolution IV: main effects are clean of two-way interactions, but two-way interactions are
ALIASED WITH EACH OTHER. This program will not fit them, and you should not interpret them.
"""
from __future__ import annotations
import argparse, csv, math, pathlib, sys
from collections import defaultdict

BLOCKS = ["A", "B", "C", "D", "E", "F"]
Z_975, Z_80 = 1.959963985, 0.841621234


def load(path: str, phase: str = "main") -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["phase"] == phase]
    keep = [r for r in rows if r["arm_kind"] == "fact" and r["fail_j1"] != ""]
    if not keep:
        raise SystemExit(f"no factorial runs with a judge-1 outcome in {path}")
    return keep


def describe(rows: list[dict]) -> None:
    n = len(rows)
    probs = sorted({r["problem"] for r in rows})
    print(f"{n} factorial runs over {len(probs)} problems, "
          f"{len({r['arm'] for r in rows})} arms\n")
    print(f"{'blk':4} {'n present':>10} {'n absent':>9} {'fail present':>13} {'fail absent':>12} "
          f"{'crude diff':>11}")
    for b in BLOCKS:
        on = [r for r in rows if r[b] == "1"]
        off = [r for r in rows if r[b] == "0"]
        p1 = sum(int(r["fail_j1"]) for r in on) / len(on) if on else float("nan")
        p0 = sum(int(r["fail_j1"]) for r in off) / len(off) if off else float("nan")
        print(f"{b:4} {len(on):>10} {len(off):>9} {p1:>12.1%} {p0:>11.1%} "
              f"{(p1 - p0) * 100:>+10.1f}")
    print("\nper problem (clustering is why the crude intervals are too narrow):")
    by = defaultdict(list)
    for r in rows:
        by[r["problem"]].append(int(r["fail_j1"]))
    for p in probs:
        v = by[p]
        print(f"  {p:5} n={len(v):>4}  failure {sum(v) / len(v):>6.1%}")


def _n_for(delta: float, base: float, deff: float) -> float:
    """Runs per level needed to detect `delta` at alpha .05, power .80, inflated by `deff`."""
    p1, p2 = base, max(min(base + delta, 0.999), 0.001)
    pbar = (p1 + p2) / 2
    num = (Z_975 * math.sqrt(2 * pbar * (1 - pbar)) +
           Z_80 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return deff * num / (delta ** 2)


def power(rows: list[dict], icc: float) -> None:
    per_level = min(len({r["id"] for r in rows if r[b] == "1"}) for b in BLOCKS)
    n_problems = len({r["problem"] for r in rows})
    m = per_level / max(n_problems, 1)                   # runs per problem per level
    deff = 1 + (m - 1) * icc
    base = sum(int(r["fail_j1"]) for r in rows) / len(rows)
    print(f"runs per factor level : {per_level}")
    print(f"problems              : {n_problems}  ({m:.1f} runs per problem per level)")
    print(f"assumed ICC           : {icc}  -> design effect {deff:.2f}")
    print(f"observed base failure : {base:.1%}\n")
    lo, hi = 0.005, 0.60
    for _ in range(80):                                  # bisect for the detectable difference
        mid = (lo + hi) / 2
        if _n_for(mid, base, deff) > per_level:
            lo = mid
        else:
            hi = mid
    print(f"smallest difference detectable at 80% power, alpha .05: "
          f"{hi * 100:.1f} percentage points")
    print("\nAnything smaller than that will read as null. Say so in the write-up rather than "
          "calling a small effect absent.")
    print("The handoff inherited a figure of '~40 runs per factor level detects roughly a 30-point "
          "shift'. That was an estimate made before this design existed; the numbers above come "
          "from the design actually run and supersede it.")


def model(rows: list[dict]) -> None:
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.api as sm
        from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    except ModuleNotFoundError:
        raise SystemExit(
            "The mixed-effects fit needs numpy, pandas and statsmodels:\n"
            "    pip install -r requirements.txt\n"
            "`describe` and `power` run without them.")

    df = pd.DataFrame([{**{b: int(r[b]) for b in BLOCKS},
                        "fail": int(r["fail_j1"]), "problem": r["problem"]} for r in rows])
    formula = "fail ~ " + " + ".join(BLOCKS)
    print(f"PRIMARY: {formula} + (1 | problem), binomial, variational Bayes\n")
    m = BinomialBayesMixedGLM.from_formula(formula, {"problem": "0 + C(problem)"}, df).fit_vb()
    print(m.summary())
    print("\nSECONDARY: GEE, exchangeable working correlation, clustered by problem\n")
    g = sm.GEE.from_formula(formula, groups="problem", data=df,
                            family=sm.families.Binomial(),
                            cov_struct=sm.cov_struct.Exchangeable()).fit()
    print(g.summary())
    print("\nTwo-way interactions are aliased with each other under resolution IV and are not "
          "fitted. Do not add them to this formula.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["describe", "power", "model"])
    ap.add_argument("--csv", required=True)
    ap.add_argument("--phase", default="main")
    ap.add_argument("--icc", type=float, default=0.10,
                    help="intra-problem correlation assumed for the design effect")
    a = ap.parse_args()
    rows = load(a.csv, a.phase)
    {"describe": lambda: describe(rows),
     "power": lambda: power(rows, a.icc),
     "model": lambda: model(rows)}[a.cmd]()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:   # piping into head is not an error
        sys.stderr.close()
        sys.exit(0)
