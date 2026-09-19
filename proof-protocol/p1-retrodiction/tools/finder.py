#!/usr/bin/env python3
"""The transformable-board screen: which boards are candidates for the move the
Banaszczyk / Bansal-Jiang / Guo-Fang-Lu trio made?

Run from `proof-protocol/`. Read-only.

The trio that generated this project's taxonomy made one move: a bound whose proof
ASSERTS that a good object exists gets re-proved by an argument that PRODUCES one.
This screen asks, from before-side fields only, whether a board is in position for
that move. Both inputs are recorded before any transformation exists, so the screen
is PROSPECTIVE -- and being mechanical, it cannot do what D25's rule-less rater did,
because it never sees the problem's name.

    S1  move_kind == "existence-theorem"      the move asserts, it does not construct
    S2  the best known bound is NOT tight to a constant against the best known
        construction                           (D28's one-line test, J = +0.750 on 14 items)
    fire iff S1 and S2

A FINDER IS SCORED ON PRECISION AND YIELD, NOT ON SENSITIVITY. Its job is to
propose candidates worth a person's time, so a false positive is expensive and a
miss is not; reporting Youden's J here would be a category error, and the
not-applicable rate is a first-class number, exactly as `prospective.py` says of the
diagnostic.
"""
from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
P3 = ROOT.parent / "p3-taxonomy"


def load_items():
    out = {}
    for d in sorted((ROOT / "cases").iterdir()):
        if not d.is_dir():
            continue
        b = json.loads((d / "before.json").read_text(encoding="utf-8"))
        h = json.loads((ROOT / "heldout" / (d.name + ".json")).read_text(encoding="utf-8"))
        out[b["id"]] = {"kind": "case", "move_kind": (b.get("move_kind") or {}).get("kind"),
                        "board_changed": True, "after": h["after_board"][:70]}
    for p in sorted((ROOT / "controls").glob("*.json")):
        c = json.loads(p.read_text(encoding="utf-8"))
        out[c["id"]] = {"kind": "control", "move_kind": (c.get("move_kind") or {}).get("kind"),
                        "board_changed": (c.get("level") or {}).get("axis") == "input-level",
                        "after": c["what_happened"][:70]}
    return out


def tightness():
    d = json.loads((P3 / "d28_bound_strength.json").read_text(encoding="utf-8"))
    return {k: v["tight_to_constant"] for k, v in d["assignments"].items()}


def ceilings():
    p = ROOT / "ceilings" / "register.jsonl"
    if not p.exists():
        return {}
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("phase") == "register":
            out[r["id"]] = r["ceiling"].get("cap")
    return out


def main() -> int:
    items, tight, ceil = load_items(), tightness(), ceilings()
    print("=== the screen, applied to every item that has both inputs\n")
    print(f"  {'item':34} {'move':18} {'tight?':8} {'fires':6} board changed")
    tp = fp = tn = fn = na = 0
    fires = []
    for i, r in sorted(items.items()):
        mk, t = r["move_kind"], tight.get(i)
        if mk in (None, "n/a") or t is None:
            na += 1
            print(f"  {i:34} {str(mk):18} {'--':8} {'N/A':6} (one input missing)")
            continue
        f = (mk == "existence-theorem") and (t is False)
        if f:
            fires.append(i)
        tp += f and r["board_changed"]
        fp += f and not r["board_changed"]
        fn += (not f) and r["board_changed"]
        tn += (not f) and not r["board_changed"]
        print(f"  {i:34} {mk:18} {str(t):8} {('FIRE' if f else '-'):6} {r['board_changed']}")

    n = tp + fp + tn + fn
    prec = tp / (tp + fp) if tp + fp else None
    print(f"\n  applicable to {n} of {len(items)} items; NOT-APPLICABLE on {na} "
          f"({na / len(items):.0%}) for want of a move slot or a tightness assignment")
    print(f"  fires on {len(fires)}: {', '.join(fires) or 'none'}")
    print(f"  PRECISION {tp}/{tp + fp} = {prec if prec is None else format(prec, '.3f')}"
          f"   (TP {tp}  FP {fp}  TN {tn}  FN {fn})")
    print("\n  Sensitivity is deliberately not reported as a figure of merit: every one of "
          "the 13\n  cases is a success whose board changed (D26), so a screen that fired on all "
          "of them\n  would score perfectly and propose nothing. What a finder owes is that its "
          "fires are\n  worth reading.")

    print("\n=== what the two fires have in common, which is the pattern the trio named\n")
    for i in fires:
        print(f"  {i}\n     after: {items[i]['after']}...")
    print("\n  Both are 'the move asserts a good object exists, and the bound is loose':\n"
          "  case 2's large Fourier coefficient and case 4's random partition. Both were then\n"
          "  re-proved by an argument that PRODUCES the object -- slice rank, interlacing\n"
          "  families. Case 4 is the corpus's own instance of the trio's move: "
          "Marcus-Spielman-Srivastava\n  did to Weaver's conjecture what Bansal-Jiang did to Banaszczyk's theorem.")

    if ceil:
        print("\n=== second, independent screen: a sourced ceiling on the board (CEILINGS.md)\n")
        for k, v in sorted(ceil.items()):
            print(f"  {k:34} cap {v}")
        print("\n  This one needs no fields at all -- only a practitioner saying in print, before\n"
              "  the fact, that the board is capped short of the truth. It is the strongest\n"
              "  evidence available and the rarest: two instances after a full pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
