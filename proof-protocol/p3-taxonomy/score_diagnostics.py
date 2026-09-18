#!/usr/bin/env python3
"""Apply the leak-free diagnostics mechanically and print their 2x2 tables.

The rules are applied from the structural fields; the `expected` field in diagnostics.json is used
only as a cross-check, so a disagreement between the stated expectation and the computed firing is
reported as an error rather than hidden.
"""
from __future__ import annotations
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
D = json.loads((HERE / "diagnostics.json").read_text(encoding="utf-8"))

# The positive class differs per diagnostic and is recorded explicitly on each item, because
# inferring it from the free-text `truth` string produced a wrong table once already.


def fires_product_law(it: dict) -> str:
    if not it.get("applicable"):
        return "not-applicable"
    return "fire" if it["target_law"] != it["bound_law"] else "no-fire"


def fires_union_bound(it: dict) -> str:
    if not it.get("applicable"):
        return "not-applicable"
    real = it["independence_realisable"] and it["target_requires_simultaneous_control"]
    return "no-fire" if real else "fire"


def score(name: str, block: dict, fn) -> list[str]:
    errs: list[str] = []
    tp = fp = tn = fn_ = 0
    rows, skipped = [], []
    for item_id, it in block["items"].items():
        got = fn(it)
        if got != it["expected"]:
            errs.append(f"{name}/{item_id}: rule computes {got}, file says {it['expected']}")
        truth, cls = it["truth"], it["class"]
        if cls == "excluded":
            skipped.append((item_id, it.get("excluded_reason", "")))
            continue
        if got == "not-applicable":
            rows.append((item_id, "—", truth, "out of domain"))
            continue
        pos = cls == "positive"
        if got == "fire" and pos:
            tp += 1; verdict = "TP"
        elif got == "fire" and not pos:
            fp += 1; verdict = "FALSE POSITIVE"
        elif got == "no-fire" and pos:
            fn_ += 1; verdict = "FALSE NEGATIVE"
        else:
            tn += 1; verdict = "TN"
        rows.append((item_id, got, truth, verdict))

    print(f"\n{'=' * 78}\n{name}\n{'=' * 78}")
    print(f"rule: {block['rule']}")
    print(f"domain: {block['claimed_domain']}")
    print(f"positive class: {block['positive_class']}\n")
    print(f"  {'item':38} {'fires':6} {'truth':26} verdict")
    for r in sorted(rows, key=lambda r: (r[3] == "out of domain", r[0])):
        print(f"  {r[0]:38} {r[1]:6} {r[2]:26} {r[3]}")
    if skipped:
        print("\n  excluded from scoring:")
        for i, why in skipped:
            print(f"    {i}: {why}")
    n_dom = tp + fp + tn + fn_
    print(f"\n  2x2 over the {n_dom} in-domain items (RAW COUNTS, as the rubric requires):")
    print(f"      {'':14}{'positive':>15}{'negative':>20}")
    print(f"      {'fires':14}{tp:>15}{fp:>20}")
    print(f"      {'does not fire':14}{fn_:>15}{tn:>20}")
    print(f"    sensitivity {tp}/{tp + fn_}   specificity {tn}/{tn + fp}   "
          f"false positives {fp}")
    return errs


def main() -> int:
    errs = score("PRODUCT-LAW MATCHING (restated leak-free)", D["product_law"], fires_product_law)
    errs += score("COLLECTIVIZE A UNION BOUND (refined)", D["union_bound"], fires_union_bound)

    print(f"\n{'=' * 78}\nAUXILIARY-WITNESS LIFT\n{'=' * 78}")
    print(f"  {D['auxiliary_witness_lift']['verdict']}: {D['auxiliary_witness_lift']['reason']}")

    print(f"\n{'=' * 78}\nWHAT THIS IS AND IS NOT\n{'=' * 78}")
    print("""  These are RAW COUNTS on ~10 and ~5 in-domain items. Per the seed's own limit, that is a
  counterexample generator, not a rate estimator: near-perfect separation on n=10 is what the
  design can show, and it cannot establish a rate.

  The circularity is REDUCED, NOT REMOVED. The rules are now mechanical, and they read only the
  product operation, the target's law read off the extremal construction, and the bound's law read
  off the formula — all objective and all pre-existing. But the ASSIGNMENT of those laws was made
  by the same instance that restated the rules. What has changed is that the judgement is now
  confined to two closed-vocabulary fields instead of a free-text leak, so it can be inter-rater
  tested the way the leak table was and the five transformations were.

  THE NEXT STEP IS THE ONLY ONE THAT SETTLES THIS: have raters who have not seen these rules assign
  target_law and bound_law blind, from the bound and the extremal construction alone, and compute
  kappa on those two fields. If that kappa clears 0.6 where the transformation label scored 0.048,
  the rebuild has done its job. If it does not, this is one more unreproducible ranking.""")

    if errs:
        print("\nMISMATCHES between the computed rule and the recorded expectation:")
        for e in errs:
            print(f"  {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
