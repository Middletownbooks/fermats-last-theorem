#!/usr/bin/env python3
"""Emit the blind rater bundle for the two-field kappa test (debt D20).

The rater assigns target_law and bound_law ONLY. It must not see:
  * the firing rule, or that any rule exists;
  * which items are positives and which are negative twins;
  * the recorded expectation, truth, class, or my own evidence text, which says things like
    "so squares add" and would hand over the answer.

What it sees: the problem, the product operation, the bound formula and its mechanism, and the
extremal construction, written without naming a law. Items are shuffled and re-keyed so positives
and twins are not separable by position.
"""
from __future__ import annotations
import argparse, json, pathlib, random, sys

HERE = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((HERE / "diagnostics.json").read_text(encoding="utf-8"))
FORBIDDEN = {"expected", "truth", "class", "note", "target_law", "bound_law",
             "target_evidence", "bound_evidence", "excluded_reason"}
# Ids encode verdicts ("N9-huang-tightness"), so problem names are written out
# explicitly rather than derived from the id. This leak was found by the check below.
LEAK_WORDS = ("tight", "removable", "fire", "twin", "positive", "negative",
              "board change", "diagnostic")

INSTRUCTIONS = """You are classifying how two quantities behave under a product operation.

For each item you are given: a problem, a PRODUCT OPERATION on instances of it, a BOUND (the best
known result of its shape, with the mechanism that produces it), and an EXTREMAL CONSTRUCTION (the
best known examples).

Assign two labels from this closed vocabulary:

  multiplicative  T(I1 (x) I2) = T(I1) * T(I2)          -- grows like c^n
  additive        T(I1 (x) I2) = T(I1) + T(I2)          -- grows like c*n
  l2              T(I1 (x) I2)^2 = T(I1)^2 + T(I2)^2    -- grows like sqrt(n)
  max             T(I1 (x) I2) = max(T(I1), T(I2))      -- flat in n
  none            no law of these shapes

  target_law : how the TRUE quantity behaves under the product operation. Read it off the
               EXTREMAL CONSTRUCTION -- take the product of the extremal examples and see what
               happens to the quantity.
  bound_law  : how the BOUND behaves under the same product operation. Read it off the FORMULA and
               the mechanism that produces it.

These are independent judgements; they may agree or differ, and nothing follows from either.
Answer with a JSON object mapping each item key to {"target_law": ..., "bound_law": ...,
"why_target": "<one sentence>", "why_bound": "<one sentence>"}. Use only the five labels."""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--key-out", type=pathlib.Path)
    a = ap.parse_args()

    items = []
    for iid, it in D["product_law"]["items"].items():
        if not it.get("applicable") or "neutral" not in it:
            continue
        n = it["neutral"]
        items.append({"_id": iid, "problem": n["problem_name"],
                      "product_operation": it["operation"],
                      "bound": n["bound_formula"], "bound_mechanism": n["bound_mechanism"],
                      "extremal_construction": n["extremal_construction"]})
    rng = random.Random(a.seed)
    rng.shuffle(items)
    key = []
    for n, it in enumerate(items, 1):
        k = f"item_{n:02d}"
        key.append({"key": k, "id": it.pop("_id")})
        it["item"] = k

    blob = json.dumps(items).lower()
    for it in items:
        leaked = FORBIDDEN & set(it)
        if leaked:
            print(f"LEAK: forbidden field {leaked}", file=sys.stderr)
            return 2
    for w in LEAK_WORDS:
        if w in blob:
            print(f"LEAK: the word {w!r} appears in the rater bundle", file=sys.stderr)
            return 2
    print(json.dumps({"instructions": INSTRUCTIONS, "vocabulary": D["law_meanings"],
                      "items": items}, indent=2, ensure_ascii=False))
    if a.key_out:
        a.key_out.write_text(json.dumps({"seed": a.seed, "key": key}, indent=2) + "\n")
        print(f"key -> {a.key_out} (not for the rater)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
