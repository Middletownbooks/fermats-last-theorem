#!/usr/bin/env python3
"""
Apply the FROZEN promotion rule to Round 2 condition A, then split the result by
whether Round 3 can form it.

The rule is quoted from `termform2/round1_manifest.json` and applied
mechanically, with no hand selection -- the same discipline, and the same parser,
as `termform2/promote.py`. The prior round here is Round 2's condition A at the
honoured budget (`termform2/round2b_A.json`), whose certified set is its 13
untargeted library matches plus the 5 targets it reached.

The split is by BODY SIZE: a formed term `least(k: body)` or `count(k: body)` is
formable at body budget b iff `size(body) <= b`, recursively for any named unit
inside the body. Round 3 runs b = 3, so terms needing a size-5 body are
candidates for the carried vocabulary. The claim that they are unreachable is
NOT taken from this arithmetic -- `certificate.py` proves it by exhaustive
enumeration before any condition is scored.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T2 = HERE.parent / "termform2"
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(T2))

from language import show, size                              # noqa: E402
from promote import named_units, parse                       # noqa: E402

BODY_BUDGET = 3


# --- reach analysis over the PRINTED form, where `<...>` still marks a unit ----
# DEFECT FOUND AND FIXED BEFORE ANY CONDITION WAS RUN. The first version of this
# file walked the parsed tuple, in which `parse` has already dropped the `<>`
# markers, so a named unit was charged its EXPANDED size inside its parent's
# body. Formation does the opposite: a stage-1 unit enters stage 2 as a size-1
# leaf, so `count(k: (k % <spf>))` has body size 3, not 6, and IS formable at
# budget 3. The bug made six formable terms look out of reach. Recorded here
# rather than silently corrected, in the manner of Report P section 13.

def _split_units(body):
    """Return (body with each top-level `<...>` replaced by a single token,
    list of the unit definitions)."""
    out, units, d, start = [], [], 0, None
    for i, c in enumerate(body):
        if c == "<":
            if d == 0:
                start = i
            d += 1
        elif c == ">":
            d -= 1
            if d == 0:
                units.append(body[start + 1:i])
                out.append("U")
                continue
        if d == 0:
            out.append(c)
    return "".join(out), units


def _size_with_units_as_leaves(body):
    """Size of a quantifier body, counting each named unit as a single leaf.

    Sizes: an atom is 1, a binary operation is 1 + a + b. The body is a printed
    infix expression, so the count is (number of leaves) + (number of operators)
    = 2 * leaves - 1 for a binary tree.
    """
    masked, _ = _split_units(body)
    leaves = 0
    i = 0
    while i < len(masked):
        c = masked[i]
        if c == "U":
            leaves += 1
            i += 1
        elif c.isdigit():
            leaves += 1
            while i < len(masked) and masked[i].isdigit():
                i += 1
        elif c in "nk":
            leaves += 1
            i += 1
        else:
            i += 1
    return 2 * leaves - 1 if leaves else 0


def wrappers(printed):
    """Every `least(k: ...)` / `count(k: ...)` in `printed`, outermost first,
    as (wrapper name, body string)."""
    out = []
    i = 0
    while True:
        j = min([x for x in (printed.find("least(k: ", i), printed.find("count(k: ", i))
                 if x >= 0] or [-1])
        if j < 0:
            return out
        name = printed[j:j + 5]
        k = j + len("least(k: ")
        d = 1
        while k < len(printed) and d:
            if printed[k] == "(":
                d += 1
            elif printed[k] == ")":
                d -= 1
                if d == 0:
                    break
            k += 1
        out.append((name, printed[j + len("least(k: "):k]))
        i = j + 1


def body_sizes(printed):
    """Body sizes of every quantifier in the printed term, units as leaves."""
    return [_size_with_units_as_leaves(b) for _, b in wrappers(printed)]


def formable_at(printed, b):
    """Formable at body budget b iff every quantifier body, with named units
    counted as size-1 leaves, is within b. A unit's own body is one of the
    bodies listed, so the condition is checked at every depth at once."""
    return all(s <= b for s in body_sizes(printed))


def main():
    a = json.loads((T2 / "round2b_A.json").read_text())
    man = json.loads((T2 / "round1_manifest.json").read_text())
    rule = man["promotion_rule_for_round_2"]

    certified = []
    for name, rec in sorted(a["untargeted"].items()):
        certified.append({"term": rec["term"], "target": "untargeted:" + name})
    for name, rec in sorted(a["targets"].items()):
        if rec.get("reached"):
            certified.append({"term": rec["selected_term"], "target": "target:" + name})

    promoted, prov, seen = [], [], set()

    def add(printed, why, target):
        t = parse(printed)
        assert show(t) == printed.replace("<", "").replace(">", ""), (show(t), printed)
        key = repr(t)
        if key in seen:
            for p in prov:
                if p["term"] == show(t) and target not in p["from"]:
                    p["from"].append(target)
            return
        seen.add(key)
        promoted.append(t)
        prov.append({"term": show(t), "printed_with_units": printed,
                     "expanded_size": size(t),
                     "body_sizes": body_sizes(printed),
                     "formable_at_body_3": formable_at(printed, BODY_BUDGET),
                     "reason": why, "from": [target]})

    for c in certified:
        add(c["term"], "certified Round-2-A term", c["target"])
    for c in certified:
        for u in named_units(c["term"]):
            add(u, "named unit inside a certified term", c["target"])

    out_of_reach = [p for p in prov if not p["formable_at_body_3"]]
    in_reach = [p for p in prov if p["formable_at_body_3"]]
    out = {
        "label": "PROMOTED_FROM_ROUND2A",
        "promotion_rule": rule,
        "applied_by": "termform3/promote3.py",
        "prior_round": "termform2/round2b_A.json (condition A, honoured budget)",
        "body_budget_of_receiving_round": BODY_BUDGET,
        "count": len(promoted),
        "count_out_of_reach": len(out_of_reach),
        "count_in_reach": len(in_reach),
        "terms": prov,
        "term_tuples": [repr(t) for t in promoted],
        "out_of_reach_tuples": [repr(parse(p["term"])) for p in out_of_reach],
        "note": ("Body sizes are arithmetic, not evidence. certificate.py proves "
                 "unreachability by exhaustive enumeration before any condition "
                 "is scored, and strikes anything that turns out formable."),
    }
    (HERE / "promoted3.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("promoted %d terms: %d out of reach at body budget %d, %d in reach\n"
          % (len(promoted), len(out_of_reach), BODY_BUDGET, len(in_reach)))
    for p in prov:
        flag = "IN REACH " if p["formable_at_body_3"] else "OUT      "
        print("  %s bodies=%-10s exp.size %2d  %s"
              % (flag, str(p["body_sizes"]), p["expanded_size"], p["term"][:60]))


if __name__ == "__main__":
    main()
