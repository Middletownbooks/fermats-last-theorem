#!/usr/bin/env python3
"""Score the two-field kappa test (debt D20) — the test that decides whether the rebuild worked.

Step D measured kappa = 0.048 for the five-transformation LABEL. The rebuilt diagnostic moved the
judgement onto two closed-vocabulary fields, target_law and bound_law, on the argument that those
reproduce where the leak table does not. This scores that argument.

    score_law_kappa.py --key d20/law_key.json --raters d20/raterA.json d20/raterB.json d20/raterC.json

Three things are reported, and the verdict requires all three. An earlier version of this scorer
declared success on the FIELD kappa alone, which was too generous: the diagnostic does not consume
the fields, it consumes the firing decision derived from them, and a negative twin that fires is a
false positive whatever the field agreement is.

  1. field agreement   pairwise Cohen and Fleiss kappa on target_law and bound_law
  2. the rule          Fleiss kappa on the IMPLIED FIRING DECISION (target_law != bound_law)
  3. the claim         false positives on negatives, per rater, against the recorded truth

Intervals are bootstrap percentiles over ITEMS (case-resampled), matching how L2's substitute kappa
was reported. With 14 items they are wide, and that is the point of printing them.
"""
from __future__ import annotations
import argparse, itertools, json, pathlib, random, statistics, sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ["target_law", "bound_law"]
LAWS = ["multiplicative", "additive", "l2", "max", "none"]
BASELINE, THRESHOLD, BOOT = 0.048, 0.6, 4000


def cohen(pairs):
    n = len(pairs)
    if not n:
        return None, float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    return (None if abs(1 - pe) < 1e-12 else (po - pe) / (1 - pe)), po


def fleiss(rows):
    """rows[i] = labels given to item i by each rater."""
    if not rows:
        return None
    n = len(rows[0])
    if n < 2 or any(len(r) != n for r in rows):
        return None
    cats = sorted({c for r in rows for c in r})
    col, P = Counter(), []
    for r in rows:
        cnt = Counter(r)
        col.update(cnt)
        P.append((sum(v * v for v in cnt.values()) - n) / (n * (n - 1)))
    total = len(rows) * n
    pe = sum((col[c] / total) ** 2 for c in cats)
    pbar = sum(P) / len(P)
    return None if abs(1 - pe) < 1e-12 else (pbar - pe) / (1 - pe)


def boot_ci(rows, seed=0):
    """Case-resampled bootstrap percentile interval for Fleiss kappa."""
    rng = random.Random(seed)
    ks = []
    for _ in range(BOOT):
        s = [rows[rng.randrange(len(rows))] for _ in rows]
        k = fleiss(s)
        if k is not None:
            ks.append(k)
    if len(ks) < BOOT * 0.5:
        return None, None
    ks.sort()
    return ks[int(0.025 * len(ks))], ks[int(0.975 * len(ks)) - 1]


def fmt(k):
    return "undefined" if k is None else f"{k:+.3f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", type=pathlib.Path, required=True)
    ap.add_argument("--raters", type=pathlib.Path, nargs="+", required=True)
    a = ap.parse_args()

    key = {r["key"]: r["id"] for r in json.loads(a.key.read_text())["key"]}
    raters = []
    for p in a.raters:
        t = p.read_text(encoding="utf-8")
        raters.append((p.stem, json.loads(t[t.find("{"):t.rfind("}") + 1])))
    items = sorted(key)
    ref = json.loads((HERE / "diagnostics.json").read_text())["product_law"]["items"]

    bad = [f"{n}/{i}/{f}={(r.get(i) or {}).get(f)!r}" for n, r in raters for i in items
           for f in FIELDS if (r.get(i) or {}).get(f) not in LAWS]
    if bad:
        print("vocabulary violations: " + ", ".join(bad[:10]))
        return 1

    print(f"{len(raters)} raters, {len(items)} items, vocabulary of {len(LAWS)}")
    print(f"bootstrap: {BOOT} case-resamples, 95% percentile intervals\n")

    print("=" * 78 + "\n1. FIELD AGREEMENT\n" + "=" * 78)
    field_k = {}
    for f in FIELDS:
        print(f"\n  {f}")
        for (n1, r1), (n2, r2) in itertools.combinations(raters, 2):
            k, po = cohen([(r1[i][f], r2[i][f]) for i in items])
            print(f"    {n1} vs {n2:10}  agreement {po:5.1%}  Cohen kappa {fmt(k)}")
        rows = [[r[i][f] for _, r in raters] for i in items]
        k = fleiss(rows)
        lo, hi = boot_ci(rows, seed=1)
        field_k[f] = k
        ci = "" if lo is None else f"  95% CI [{lo:+.3f}, {hi:+.3f}]"
        print(f"    {'Fleiss (all raters)':24} {fmt(k)}{ci}")

    print("\n" + "=" * 78 + "\n2. THE RULE: implied firing decision (target_law != bound_law)\n"
          + "=" * 78)
    print(f"\n  {'item':34} {'reference':10} " + " ".join(f"{n[:7]:>8}" for n, _ in raters))
    fire_rows, all_match = [], 0
    for i in items:
        rid = key[i]
        rf = "fire" if ref[rid]["target_law"] != ref[rid]["bound_law"] else "no-fire"
        cells = ["fire" if r[i]["target_law"] != r[i]["bound_law"] else "no-fire"
                 for _, r in raters]
        fire_rows.append(cells)
        ok = all(c == rf for c in cells)
        all_match += ok
        print(f"  {rid[:34]:34} {rf:10} " + " ".join(f"{c:>8}" for c in cells)
              + ("" if ok else "   <-- differs"))
    fk = fleiss(fire_rows)
    lo, hi = boot_ci(fire_rows, seed=2)
    ci = "" if lo is None else f"  95% CI [{lo:+.3f}, {hi:+.3f}]"
    print(f"\n  all raters match the reference on {all_match}/{len(items)} items")
    print(f"  Fleiss kappa on the firing decision: {fmt(fk)}{ci}")

    print("\n" + "=" * 78 + "\n3. THE CLAIM: false positives on negatives, per rater\n" + "=" * 78)
    print("\n  DIAGNOSTIC.md claims zero false positives. That claim was computed from MY law\n"
          "  assignments. Here it is recomputed from each rater's.\n")
    print(f"  {'rater':10} {'TP':>4} {'FN':>4} {'FP':>4} {'TN':>4}   false positives on")
    fp_any = {}
    for n, r in raters:
        tp = fn = fp = tn = 0
        fps = []
        for i in items:
            rid = key[i]
            cls = ref[rid].get("class")
            if cls == "excluded":
                continue
            f_ = r[i]["target_law"] != r[i]["bound_law"]
            pos = cls == "positive"
            if f_ and pos:
                tp += 1
            elif f_:
                fp += 1
                fps.append(rid)
            elif pos:
                fn += 1
            else:
                tn += 1
        fp_any[n] = fps
        print(f"  {n:10} {tp:>4} {fn:>4} {fp:>4} {tn:>4}   {', '.join(fps) or '-'}")
    union = sorted({x for v in fp_any.values() for x in v})

    print("\n" + "=" * 78 + "\nVERDICT\n" + "=" * 78)
    worst_field = min([k for k in field_k.values() if k is not None], default=None)
    print(f"\n  baseline, transformation label (step D, measured):  kappa = {BASELINE}")
    print(f"  field agreement, worst of the two fields:           {fmt(worst_field)}")
    print(f"  the firing decision the diagnostic actually uses:   {fmt(fk)}")
    print(f"  negatives that fired for at least one rater:        "
          f"{', '.join(union) if union else 'none'}\n")

    fields_ok = worst_field is not None and worst_field >= THRESHOLD
    rule_ok = fk is not None and fk >= THRESHOLD
    claim_ok = not union

    print(f"  [{'PASS' if fields_ok else 'FAIL'}] fields reproduce at the {THRESHOLD} stop rule")
    print(f"  [{'PASS' if rule_ok else 'FAIL'}] the rule built on them reproduces")
    print(f"  [{'PASS' if claim_ok else 'FAIL'}] the zero-false-positive claim survives "
          f"independent assignment")

    if fields_ok and rule_ok and claim_ok:
        print("\n  The rebuild is supported on this evidence.")
    elif fields_ok and not rule_ok:
        print("\n  SPLIT RESULT. The fields reproduce far better than the transformation label did,\n"
              "  so moving the judgement onto them was a real improvement. But the DIFFERENCE of\n"
              "  two well-agreed fields does not itself reproduce at the stop rule: raters who\n"
              "  agree on the labels can still disagree on whether they differ, because\n"
              "  disagreement concentrates on exactly the items where the two labels are close.\n"
              "  Report this, do not defend the rebuild with the field kappa alone.")
    elif not fields_ok:
        print("\n  NOT operational at the stop rule. The judgement moved from one unreproducible\n"
              "  field to another, which DIAGNOSTIC.md commits to reporting rather than defending.")
    if not claim_ok:
        print(f"\n  The zero-false-positive claim in DIAGNOSTIC.md DOES NOT SURVIVE. Under at least\n"
              f"  one independent assignment the diagnostic fires on {len(union)} negative(s): "
              f"{', '.join(union)}.\n  That figure must not be quoted without this qualification.")

    print("\n  LIMITS, stated rather than buried:")
    print("   * 14 items, 5 categories, 3 raters. The intervals above are wide by construction.")
    print("   * The raters share ONE fixed encoding of the inputs, written by the same instance\n"
          "     that wrote the rules. This measures rater agreement GIVEN that encoding, not\n"
          "     encoder-plus-rater agreement. Weaker than L2's design; stronger than no measurement.")
    print("   * The reference column is my own assignment, so 'differs' means differs from me,\n"
          "     not necessarily wrong. Where all three raters agree against me, I am the outlier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
