#!/usr/bin/env python3
"""Score the second reading of `move_kind` against PREREG_D35.md.

Committed BEFORE the rater's answer exists. Reads two files and nothing else:

  key.json         my codes, the scramble, the self-answering flags (derived)
  verdicts.json    the rater's codes, transcribed verbatim

Usage:  python3 score_d35.py             # scores if verdicts.json exists
        python3 score_d35.py --selftest  # fires the conditions on synthetic data
"""
import json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CODES = {"FORMULA": "formula",
         "EXISTENCE-THEOREM": "existence-theorem",
         "NO MOVE RECORDED": "n/a"}


def kappa(a, b):
    """Cohen's kappa on two equal-length code lists."""
    n = len(a)
    assert n and len(b) == n
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if pe == 1.0:
        return float("nan"), po, pe
    return (po - pe) / (1 - pe), po, pe


def score(key, r2):
    out = []
    ids = list(key["rater1"].keys())
    self_answering = set(key.get("self_answering", {}))
    no_slot = [i for i, p in key["provenance"].items() if p == "no move slot"]

    def pair(subset):
        s = [i for i in ids if i in subset]
        return [key["rater1"][i] for i in s], [r2[i]["code"] for i in s], s

    for label, subset in (("all 17", set(ids)),
                          ("15 non-self-answering", set(ids) - self_answering),
                          ("two-class only (drops n/a on either side)",
                           {i for i in ids
                            if key["rater1"][i] != "n/a" and r2[i]["code"] != "n/a"}
                           - self_answering)):
        a, b, s = pair(subset)
        if len(s) < 2:
            out.append(f"{label}: too few items to score ({len(s)})")
            continue
        k, po, pe = kappa(a, b)
        dis = [i for i, x, y in zip(s, a, b) if x != y]
        out.append(f"{label}: n={len(s)}  agreement {po:.3f}  chance {pe:.3f}  "
                   f"kappa {k:.3f}")
        if dis:
            out.append("    disagreements: " + ", ".join(dis))

    out.append("")
    # E-1
    a, b, s = pair(set(ids) - self_answering)
    k15 = kappa(a, b)[0]
    out.append(f"  E-1: {'PASS' if k15 >= 0.6 else 'FAIL'}  kappa on the 15 = {k15:.3f}")

    # E-2: the two near-identical randomised moves
    ks, sp = "04-kadison-singer", "08-spencer-discrepancy"
    same_r2 = r2[ks]["code"] == r2[sp]["code"]
    out.append(f"  E-2: {'FIRED' if same_r2 else 'did not fire'}  "
               f"rater has {ks}={r2[ks]['code']}, {sp}={r2[sp]['code']}; "
               f"my column splits them ({key['rater1'][ks]} / {key['rater1'][sp]})")

    # E-3
    e3 = all(r2[i]["code"] == "formula" for i in self_answering) if self_answering else None
    out.append(f"  E-3: {'PASS' if e3 else 'FAIL'}  self-answering items "
               f"{sorted(self_answering)} -> "
               f"{[r2[i]['code'] for i in sorted(self_answering)]} (evidence: none)")

    # E-4
    got = {i: r2[i]["code"] for i in no_slot}
    e4 = all(v == "n/a" for v in got.values())
    out.append(f"  E-4: {'PASS' if e4 else 'FAIL'}  no-move-slot items -> {got}")
    filled = [i for i in no_slot if key["rater1"][i] != "n/a"]
    if filled:
        out.append(f"    I filled a slot the source lacks on: {filled} "
                   f"(coverage failure of the record, not a disagreement about mathematics)"
                   if all(got.get(i) == "n/a" for i in filled) else
                   f"    contested no-slot items: {filled}")

    # E-5
    bad = [i for i in ids if key["rater1"][i] != r2[i]["code"]
           and not any(w in r2[i]["reason"].lower() for w in
                       ("move", "comput", "formula", "exist", "assert", "random",
                        "slot", "no move", "construct", "explicit", "operation"))]
    out.append(f"  E-5: {'PASS' if not bad else 'FAIL'}  disagreements whose reason "
               f"names neither the move's shape nor the missing slot: {bad}")

    out.append("")
    if k15 < 0.6:
        out.append("FAILURE CONDITION MET: kappa < 0.6 on the 15. `move_kind` does not "
                   "reproduce; the screen has no measured selectivity and FINDER.md's "
                   "precision figure must be reported as noise until re-run.")
    if same_r2:
        out.append("FAILURE CONDITION MET (E-2): my column splits two items of the same "
                   "form. Per the prereg this is NOT fixed by re-coding one to match the "
                   "rater. Either state the separating criterion before reading the "
                   "rater's reason, or concede both are the same kind -- which costs the "
                   "screen one of its two existence-theorem items.")
    if k15 >= 0.6 and same_r2:
        out.append("This is the outcome the prereg named as likeliest and most "
                   "misleading: high overall agreement coexisting with the binding "
                   "conjunct being unreliable where the screen depends on it. All the "
                   "selectivity lives in the 2-item existence-theorem class.")
    out.append("")
    out.append("This run cannot show the screen works -- only whether the field it turns "
               "on is reproducible.")
    return "\n".join(out)


def load_verdicts(key):
    v = json.load(open(os.path.join(HERE, "verdicts.json")))
    order = key["order_shown_to_rater"]
    out = {}
    for row in v["items"]:
        item = order[int(row["item"]) - 1]
        code = row["code"].strip().upper()
        assert code in CODES, code
        out[item] = {"code": CODES[code], "reason": row.get("reason", "")}
    assert len(out) == len(order), f"{len(out)} of {len(order)} items rated"
    return out


def selftest():
    key = json.load(open(os.path.join(HERE, "key.json")))

    def mk(codes, reason="the move is computed"):
        return {i: {"code": c, "reason": reason} for i, c in codes.items()}

    print("### synthetic A: rater agrees with me everywhere")
    print(score(key, mk(dict(key["rater1"]))))

    print("\n### synthetic B: E-2 fires, no-slot items all declined")
    c = dict(key["rater1"])
    c["04-kadison-singer"] = "formula"
    for i, p in key["provenance"].items():
        if p == "no move slot":
            c[i] = "n/a"
    print(score(key, mk(c, "a random object is sampled, not shown to exist")))

    print("\n### synthetic C: broad disagreement")
    c = {i: ("existence-theorem" if k == "formula" else "formula")
         for i, k in key["rater1"].items()}
    print(score(key, mk(c, "no idea, unfamiliar")))


if __name__ == "__main__":
    key = json.load(open(os.path.join(HERE, "key.json")))
    if "--selftest" in sys.argv:
        selftest()
    elif not os.path.exists(os.path.join(HERE, "verdicts.json")):
        print("verdicts.json not present yet. Harness committed now so the scoring "
              "rule cannot move later.\nRun with --selftest to see the conditions fire.")
    else:
        print(score(key, load_verdicts(key)))
