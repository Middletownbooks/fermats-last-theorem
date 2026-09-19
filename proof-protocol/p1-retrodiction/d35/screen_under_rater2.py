#!/usr/bin/env python3
"""What the transformable-board screen does if rater 2's `move_kind` column is used.

D35 measured that the field does not reproduce (kappa 0.430 on the 15 codable-and-not-
self-answering items). The consequence is not abstract: the screen FIRES on
`move_kind == "existence-theorem"`, so a column that calls six items existence-theorem
instead of two is a different screen. This recomputes precision and yield under both
columns, using the SAME tightness assignments and the same board-changed truth.

Run from anywhere. Read-only. Imports finder.py so the screen's own logic is not
re-implemented here.
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "tools")
spec = importlib.util.spec_from_file_location("finder", os.path.join(TOOLS, "finder.py"))
finder = importlib.util.module_from_spec(spec)
sys.modules["finder"] = finder
spec.loader.exec_module(finder)

CODES = {"FORMULA": "formula", "EXISTENCE-THEOREM": "existence-theorem",
         "NO MOVE RECORDED": "n/a"}


def rater2_column():
    key = json.load(open(os.path.join(HERE, "key.json")))
    v = json.load(open(os.path.join(HERE, "verdicts.json")))
    order = key["order_shown_to_rater"]
    return {order[int(r["item"]) - 1]: CODES[r["code"].strip().upper()] for r in v["items"]}


def run(items, tight, column, label):
    tp = fp = tn = fn = na = 0
    fires = []
    for i, r in sorted(items.items()):
        mk, t = column.get(i), tight.get(i)
        if mk in (None, "n/a") or t is None:
            na += 1
            continue
        f = (mk == "existence-theorem") and (t is False)
        if f:
            fires.append(i)
        tp += f and r["board_changed"]
        fp += f and not r["board_changed"]
        fn += (not f) and r["board_changed"]
        tn += (not f) and not r["board_changed"]
    n = tp + fp + tn + fn
    prec = tp / (tp + fp) if tp + fp else None
    print(f"  {label}")
    print(f"    applicable to {n} of {len(items)}; not-applicable {na}")
    print(f"    fires on {len(fires)}: {', '.join(fires) or 'none'}")
    print(f"    PRECISION {tp}/{tp+fp} = "
          f"{'n/a' if prec is None else format(prec, '.3f')}   "
          f"(TP {tp} FP {fp} TN {tn} FN {fn})")
    return set(fires), n, prec


def main():
    items, tight = finder.load_items(), finder.tightness()
    mine = {i: r["move_kind"] for i, r in items.items()}
    theirs = rater2_column()

    print("=== the screen under each column, same tightness, same truth\n")
    f1, n1, p1 = run(items, tight, mine, "rater 1 (the committed column)")
    print()
    f2, n2, p2 = run(items, tight, theirs, "rater 2 (blind, D35)")

    print("\n=== what changed\n")
    print(f"  fires only under rater 1: {sorted(f1 - f2) or 'none'}")
    print(f"  fires only under rater 2: {sorted(f2 - f1) or 'none'}")
    print(f"  fires under both:         {sorted(f1 & f2) or 'none'}")
    print(f"  applicability: {n1} items -> {n2} items")
    ec1 = sum(1 for v in mine.values() if v == "existence-theorem")
    ec2 = sum(1 for v in theirs.values() if v == "existence-theorem")
    print(f"  existence-theorem class: {ec1} of 17 -> {ec2} of 17")
    print()
    print("  The precision figure survives numerically -- every fire under either column is")
    print("  a case whose board changed, because ALL 13 CASES ARE SUCCESSES (D26). That is")
    print("  the point: with no negative in the scored set, precision cannot fall, so it was")
    print("  never the number carrying the screen. What the column controls is the YIELD and")
    print("  therefore how much of a person's time the screen spends, and that is what moved.")
    print()
    print("  Read the two columns' disagreements, not their precisions: all six are")
    print("  rater 1 = formula against rater 2 = existence-theorem or no-move-recorded.")
    print("  A one-directional disagreement is a systematic criterion difference, not noise.")


if __name__ == "__main__":
    main()
