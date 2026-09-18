#!/usr/bin/env python3
"""Baselines for the rebuilt diagnostic (task 2). Raw accuracy is not a permitted unit here.

p1-retrodiction/README.md, inherited from the seed: "scores are lift over the telegraph baseline,
never raw accuracy." DIAGNOSTIC.md's 2x2s are raw accuracies, so they are stated in a unit the
programme forbids. This computes what they should be stated against.

The seed's telegraph baseline was "the leak table with no procedure". The rebuilt diagnostic reads
NO leak table, so that exact arm does not apply. Three baselines are used instead, and the choice is
stated here BEFORE any of them is run:

  B0  fire on everything in domain        free, exact, a floor
  B1  fire on nothing in domain           free, exact, the other floor
  B2  a rater given the same neutral item and asked ONLY "did this board change?",
      with no rule, no vocabulary and no mention that a rule exists

B0 and B1 are floors that any non-trivial rule should clear; clearing them is necessary, not
impressive. B2 is the baseline that decides whether the diagnostic ADDS anything, and it is the
direct analogue of the seed's telegraph arm: same information, no procedure.

Scored with Youden's J = sensitivity + specificity - 1, because it is the accuracy measure that a
constant rule cannot game: B0 and B1 both score J = 0 by construction, whatever the class balance.
    baseline.py trivial
    baseline.py score --rater baseline/raterX.json --key d20/law_key.json
"""
from __future__ import annotations
import argparse, json, pathlib, random, sys

HERE = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((HERE / "diagnostics.json").read_text(encoding="utf-8"))
ITEMS = {k: v for k, v in D["product_law"]["items"].items()
         if v.get("applicable") and v.get("class") in ("positive", "negative")}


def confusion(fires: dict[str, bool]) -> dict:
    tp = fp = tn = fn = 0
    fps = []
    for k, v in ITEMS.items():
        pos = v["class"] == "positive"
        f = fires.get(k, False)
        if f and pos:
            tp += 1
        elif f:
            fp += 1; fps.append(k)
        elif pos:
            fn += 1
        else:
            tn += 1
    sens = tp / (tp + fn) if tp + fn else float("nan")
    spec = tn / (tn + fp) if tn + fp else float("nan")
    return {"tp": tp, "fn": fn, "fp": fp, "tn": tn, "sens": sens, "spec": spec,
            "J": sens + spec - 1, "fps": fps}


def show(name: str, c: dict) -> None:
    print(f"  {name:34} TP {c['tp']}  FN {c['fn']}  FP {c['fp']}  TN {c['tn']}   "
          f"sens {c['sens']:.3f}  spec {c['spec']:.3f}   J = {c['J']:+.3f}")


def diagnostic_fires() -> dict[str, bool]:
    return {k: v["target_law"] != v["bound_law"] for k, v in ITEMS.items()}


def cmd_trivial(a) -> int:
    n_pos = sum(1 for v in ITEMS.values() if v["class"] == "positive")
    print(f"{len(ITEMS)} in-domain items: {n_pos} positive, {len(ITEMS) - n_pos} negative\n")
    show("B0  fire on everything", confusion({k: True for k in ITEMS}))
    show("B1  fire on nothing", confusion({k: False for k in ITEMS}))
    rng = random.Random(0)
    Js = [confusion({k: rng.random() < 0.5 for k in ITEMS})["J"] for _ in range(20000)]
    Js.sort()
    print(f"  {'B1b coin flip (20k trials)':34} mean J = {sum(Js)/len(Js):+.3f}   "
          f"95% of trials in [{Js[500]:+.3f}, {Js[-500]:+.3f}]")
    print()
    show("product-law matching", confusion(diagnostic_fires()))
    d = confusion(diagnostic_fires())["J"]
    print(f"\n  LIFT over B0/B1 (both J = 0 by construction): {d:+.3f}")
    print("\n  Clearing a constant rule is NECESSARY, NOT IMPRESSIVE. A coin flip also scores J = 0")
    print("  in expectation, and its spread above shows what 13 items can produce by chance alone:")
    print(f"  {sum(1 for j in Js if j >= d) / len(Js):.2%} of coin flips reach J >= {d:+.3f}.")
    print("\n  The baseline that decides whether the diagnostic ADDS anything is B2, the rule-less")
    print("  rater. Run it with `baseline.py score`.")
    return 0


def cmd_score(a) -> int:
    key = {r["key"]: r["id"] for r in json.loads(a.key.read_text())["key"]}
    raw = a.rater.read_text(encoding="utf-8")
    ans = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
    fires, recog = {}, {}
    for k, v in ans.items():
        rid = key.get(k)
        if rid in ITEMS:
            fires[rid] = str(v["board_changed"]).lower() in ("true", "yes")
            recog[rid] = v.get("recognised_problem") or ""
    print(f"B2 rule-less rater: {a.rater.stem}, {len(fires)} in-domain items scored\n")
    b2 = confusion(fires)
    dg = confusion(diagnostic_fires())
    show("B2  rule-less rater", b2)
    show("product-law matching", dg)
    print(f"\n  LIFT of the diagnostic over B2: {dg['J'] - b2['J']:+.3f} "
          f"(J {dg['J']:+.3f} vs {b2['J']:+.3f})")
    named = sum(1 for v in recog.values() if v and v.lower() not in ("", "no", "none", "unknown"))
    print(f"\n  RECOGNITION PROBE: the rater named a source problem on {named}/{len(recog)} items.")
    if named / max(len(recog), 1) > 0.5:
        print("  The baseline is substantially recognition, not inference. That is the L4 finding,")
        print("  and it means B2 is an UPPER bound on what a clean baseline would score — so the")
        print("  lift computed above is a LOWER bound on the diagnostic's true lift.")
    if b2["J"] >= dg["J"]:
        print("\n  THE DIAGNOSTIC DOES NOT BEAT THE BASELINE. A rater with no rule, given the same")
        print("  item, separates positives from twins at least as well. That is the finding, and it")
        print("  matters more than the 2x2.")
    print("\n  n = 1 rater. This is a single observation on 13 items, not a rate.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("trivial").set_defaults(fn=cmd_trivial)
    p = sub.add_parser("score")
    p.add_argument("--rater", type=pathlib.Path, required=True)
    p.add_argument("--key", type=pathlib.Path, required=True)
    p.set_defaults(fn=cmd_score)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
