#!/usr/bin/env python3
"""Cohen's kappa for the blind re-encoding pass (handoff task 2).

Two things need a kappa, and only one of them is a straight categorical rating:

  labels   Two labellers independently assign a transformation (from the closed vocabulary)
           to each held-out after-board. This is a textbook Cohen's kappa. The handoff's
           decision rule: kappa < 0.6 means the five-transformation vocabulary is not
           operational, and THAT IS ITSELF THE P3 RESULT.

  slots    Two encoders independently fill the five before-board slots. Slot contents are
           free text, so there is no automatic agreement measure. An adjudicator codes each
           (case, slot) pair; --template emits the coding sheet. Two adjudicators give a real
           kappa; one gives only an agreement rate, and the tool says so.

Usage
  kappa.py labels   A.json B.json        # {case_id: label} each
  kappa.py slots    coded_A.json [coded_B.json]
  kappa.py template --kind slots|labels  > sheet.json
"""
from __future__ import annotations
import argparse, json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLOT_CODES = ["same", "compatible-but-different", "different", "one-missing"]


def cohen_kappa(pairs: list[tuple[str, str]]) -> tuple[float | None, float, int]:
    """Returns (kappa, observed agreement, n). kappa is None when it is undefined."""
    n = len(pairs)
    if n == 0:
        return None, float("nan"), 0
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    if abs(1 - pe) < 1e-12:
        return None, po, n          # both raters constant: kappa undefined, not 0
    return (po - pe) / (1 - pe), po, n


def report(name: str, pairs: list[tuple[str, str]]) -> float | None:
    k, po, n = cohen_kappa(pairs)
    ks = "undefined (no expected disagreement)" if k is None else f"{k:.3f}"
    print(f"{name}: n = {n}, observed agreement = {po:.1%}, kappa = {ks}")
    dis = [(i, a, b) for (i, (a, b)) in enumerate(pairs) if a != b]
    for i, a, b in dis:
        print(f"    disagreement #{i}: {a!r} vs {b!r}")
    return k


def cmd_labels(a: argparse.Namespace) -> int:
    A = json.loads(a.first.read_text()); B = json.loads(a.second.read_text())
    ids = sorted(set(A) & set(B))
    for missing in sorted(set(A) ^ set(B)):
        print(f"  warning: {missing} labelled by only one labeller", file=sys.stderr)
    k = report("transformation labels", [(A[i], B[i]) for i in ids])
    print()
    if k is None:
        print("VERDICT: kappa undefined. Read the labels before concluding anything.")
        return 0
    if k < 0.6:
        print("VERDICT: kappa < 0.6. The five-transformation vocabulary is NOT OPERATIONAL.")
        print("Per the handoff, report this as the P3 result rather than scoring the procedure.")
        return 0
    print("VERDICT: kappa >= 0.6. The vocabulary is usable; procedure scores may be computed,")
    print("still as lift over the telegraph baseline, never as raw accuracy.")
    return 0


def cmd_slots(a: argparse.Namespace) -> int:
    A = json.loads(a.first.read_text())
    if a.second is None:
        rows = [(c, s, v) for c, slots in A["coding"].items() for s, v in slots.items()]
        agree = sum(1 for *_, v in rows if v == "same")
        print(f"single adjudicator: n = {len(rows)} slots, {agree} coded 'same' "
              f"({agree / max(len(rows), 1):.1%})")
        print("\nThis is an agreement RATE, not a kappa. One adjudicator cannot produce an")
        print("inter-rater statistic. Add a second coding sheet for a real kappa.")
        by = Counter(v for *_, v in rows)
        for code in SLOT_CODES:
            print(f"    {code:>26}: {by.get(code, 0)}")
        return 0
    B = json.loads(a.second.read_text())
    pairs = [(A["coding"][c][s], B["coding"][c][s])
             for c in sorted(set(A["coding"]) & set(B["coding"]))
             for s in sorted(set(A["coding"][c]) & set(B["coding"][c]))]
    report("slot-content adjudication", pairs)
    return 0


def cmd_template(a: argparse.Namespace) -> int:
    ids = sorted(p.name for p in (ROOT / "cases").iterdir() if p.is_dir())
    if a.kind == "labels":
        print(json.dumps({i: "REPLACE-WITH-LABEL" for i in ids}, indent=2))
    else:
        print(json.dumps({
            "adjudicator": "REPLACE",
            "codes": SLOT_CODES,
            "coding": {i: {s: "REPLACE" for s in ("S", "M", "I", "C", "T")} for i in ids},
        }, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("labels"); p.add_argument("first", type=pathlib.Path)
    p.add_argument("second", type=pathlib.Path); p.set_defaults(fn=cmd_labels)
    p = sub.add_parser("slots"); p.add_argument("first", type=pathlib.Path)
    p.add_argument("second", type=pathlib.Path, nargs="?"); p.set_defaults(fn=cmd_slots)
    p = sub.add_parser("template"); p.add_argument("--kind", choices=["slots", "labels"],
                                                   default="slots")
    p.set_defaults(fn=cmd_template)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
