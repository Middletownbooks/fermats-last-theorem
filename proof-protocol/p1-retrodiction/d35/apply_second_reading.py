#!/usr/bin/env python3
"""Write D35's second reading into the record, beside my column and not over it.

Each item's `move_kind` gains a `second_reading` block DERIVED from d35/verdicts.json:
the blind rater's code, its one-line reason, and whether the two readings agree. My
`kind` is left exactly as it was -- overwriting it would destroy the only measurement of
it that exists, and would leave a field that looks single-rater again.

Idempotent. Run from anywhere: `python3 apply_second_reading.py`.
"""
import glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CODES = {"FORMULA": "formula", "EXISTENCE-THEOREM": "existence-theorem",
         "NO MOVE RECORDED": "n/a"}


def main():
    key = json.load(open(os.path.join(HERE, "key.json")))
    verd = json.load(open(os.path.join(HERE, "verdicts.json")))
    order = key["order_shown_to_rater"]
    second = {}
    for row in verd["items"]:
        second[order[int(row["item"]) - 1]] = row

    files = sorted(glob.glob(os.path.join(ROOT, "cases", "*", "before.json"))) + \
            sorted(glob.glob(os.path.join(ROOT, "controls", "*.json")))
    changed = 0
    for f in files:
        d = json.load(open(f))
        row = second[d["id"]]
        mk = d.get("move_kind")
        assert mk is not None, d["id"]
        code = CODES[row["code"].strip().upper()]
        block = {
            "rater": "D35 rater 2, blind: sheet text only, tools forbidden",
            "kind": code,
            "reason": row["reason"],
            "agrees_with_first": code == mk.get("kind"),
            "run": "p1-retrodiction/d35 (PREREG_D35.md, verdicts.json, REPORT_D35.md)",
        }
        if "rater_confidence" in row:
            block["rater_confidence"] = row["rater_confidence"]
        if d["id"] in key.get("self_answering", {}):
            block["caveat"] = ("the shown text contains its own answer ("
                               + ", ".join(key["self_answering"][d["id"]])
                               + "), so agreement here is not evidence")
        if key["provenance"][d["id"]] == "no move slot":
            block["caveat"] = ("the record has NO move slot for this item; the rater was "
                              "shown the rest of the board and declined, which is a "
                              "coverage failure of the record where my column filled it")
        if mk.get("second_reading") == block:
            continue
        mk["second_reading"] = block
        json.dump(d, open(f, "w"), indent=1, ensure_ascii=False)
        open(f, "a").write("\n")
        changed += 1

    agree = sum(1 for f in files
                if json.load(open(f))["move_kind"]["second_reading"]["agrees_with_first"])
    print(f"second reading written to {changed} file(s); {agree}/17 agree with the first")


if __name__ == "__main__":
    main()
