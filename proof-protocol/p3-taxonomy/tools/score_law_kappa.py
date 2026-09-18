#!/usr/bin/env python3
"""Score the two-field kappa test (debt D20) — the test that decides whether the rebuild worked.

Step D measured kappa = 0.048 for the five-transformation LABEL. The rebuilt diagnostic moved the
judgement onto two closed-vocabulary fields, target_law and bound_law, on the argument that those
reproduce where the leak table does not. This scores that argument.

    score_law_kappa.py --key key.json --raters A.json B.json C.json

Reports, per field:
  * pairwise Cohen's kappa for every pair of raters;
  * Fleiss' kappa across all raters (the right statistic for three or more);
  * the agreement rate;
and then the thing that actually matters: whether each rater's IMPLIED FIRING DECISION
(target_law != bound_law) matches the reference assignment, item by item.

A high kappa on the two fields with low agreement on the firing decision would mean the fields
reproduce but the rule built on them does not. Both are reported; neither is assumed.
"""
from __future__ import annotations
import argparse, itertools, json, pathlib, sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ["target_law", "bound_law"]
LAWS = ["multiplicative", "additive", "l2", "max", "none"]
BASELINE = 0.048
THRESHOLD = 0.6


def cohen(pairs: list[tuple[str, str]]) -> tuple[float | None, float, int]:
    n = len(pairs)
    if not n:
        return None, float("nan"), 0
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    if abs(1 - pe) < 1e-12:
        return None, po, n
    return (po - pe) / (1 - pe), po, n


def fleiss(rows: list[list[str]]) -> float | None:
    """rows[i] = the labels given to item i by each rater."""
    if not rows:
        return None
    n = len(rows[0])
    if n < 2 or any(len(r) != n for r in rows):
        return None
    cats = sorted({c for r in rows for c in r})
    P = []
    col = Counter()
    for r in rows:
        cnt = Counter(r)
        col.update(cnt)
        P.append((sum(v * v for v in cnt.values()) - n) / (n * (n - 1)))
    total = len(rows) * n
    pj = [col[c] / total for c in cats]
    pbar = sum(P) / len(P)
    pe = sum(p * p for p in pj)
    if abs(1 - pe) < 1e-12:
        return None
    return (pbar - pe) / (1 - pe)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", type=pathlib.Path, required=True)
    ap.add_argument("--raters", type=pathlib.Path, nargs="+", required=True)
    a = ap.parse_args()

    key = {r["key"]: r["id"] for r in json.loads(a.key.read_text())["key"]}
    raters = []
    for p in a.raters:
        txt = p.read_text(encoding="utf-8").strip()
        i, j = txt.find("{"), txt.rfind("}")
        raters.append((p.stem, json.loads(txt[i:j + 1])))

    ref_all = json.loads((HERE / "diagnostics.json").read_text())["product_law"]["items"]
    items = sorted(key)
    bad = []
    for name, r in raters:
        for it in items:
            for f in FIELDS:
                v = (r.get(it) or {}).get(f)
                if v not in LAWS:
                    bad.append(f"{name}/{it}/{f} = {v!r} is not in the vocabulary")
    if bad:
        print("\n".join(f"  {b}" for b in bad[:20]))
        return 1

    print(f"{len(raters)} raters, {len(items)} items, vocabulary of {len(LAWS)}\n")
    for f in FIELDS:
        print(f"=== {f} ===")
        for (n1, r1), (n2, r2) in itertools.combinations(raters, 2):
            k, po, n = cohen([(r1[i][f], r2[i][f]) for i in items])
            ks = "undefined" if k is None else f"{k:+.3f}"
            print(f"  {n1} vs {n2:14} n={n:3}  agreement {po:5.1%}  Cohen kappa {ks}")
        fk = fleiss([[r[i][f] for _, r in raters] for i in items])
        print(f"  {'Fleiss kappa (all raters)':34} {'undefined' if fk is None else f'{fk:+.3f}'}\n")

    # the implied firing decision, which is what the diagnostic actually uses
    print("=== implied firing decision (target_law != bound_law) ===")
    print(f"  {'item':34} {'reference':10} " + " ".join(f"{n[:8]:>9}" for n, _ in raters))
    agree_all = 0
    for it in items:
        rid = key[it]
        ref = ref_all[rid]
        ref_fire = "fire" if ref["target_law"] != ref["bound_law"] else "no-fire"
        cells, oks = [], []
        for _, r in raters:
            f = "fire" if r[it]["target_law"] != r[it]["bound_law"] else "no-fire"
            cells.append(f)
            oks.append(f == ref_fire)
        if all(oks):
            agree_all += 1
        mark = "" if all(oks) else "   <-- differs"
        print(f"  {rid[:34]:34} {ref_fire:10} " + " ".join(f"{c:>9}" for c in cells) + mark)
    print(f"\n  all raters match the reference firing decision on {agree_all}/{len(items)} items")

    fk_pair = [fleiss([[("fire" if r[i]["target_law"] != r[i]["bound_law"] else "no-fire")
                        for _, r in raters] for i in items])]
    print(f"  Fleiss kappa on the firing decision itself: "
          f"{'undefined' if fk_pair[0] is None else f'{fk_pair[0]:+.3f}'}")

    print(f"\n=== verdict against the measured baseline ===")
    ks = [fleiss([[r[i][f] for _, r in raters] for i in items]) for f in FIELDS]
    worst = min([k for k in ks if k is not None], default=None)
    print(f"  transformation label (step D, measured): kappa = {BASELINE}")
    if worst is None:
        print("  law fields: kappa undefined — raters were constant. Read the assignments.")
    elif worst >= THRESHOLD:
        print(f"  law fields: worst kappa = {worst:+.3f} >= {THRESHOLD}")
        print("  The judgement WAS moved onto a field that reproduces. The rebuild did its job on\n"
              "  this evidence; it remains a small n, and raters share one fixed encoding.")
    else:
        print(f"  law fields: worst kappa = {worst:+.3f} < {THRESHOLD}")
        print("  NOT operational at the stop rule. Report this as the result rather than defending\n"
              "  the rebuild: it would be one more unreproducible ranking, on a shorter vocabulary.")
    print("\n  LIMIT, stated rather than buried: the raters share ONE fixed encoding of the inputs,\n"
          "  written by the same instance that wrote the rules. This measures rater agreement GIVEN\n"
          "  that encoding, not encoder-plus-rater agreement. It is strictly weaker than L2's design\n"
          "  and strictly stronger than no measurement at all.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
