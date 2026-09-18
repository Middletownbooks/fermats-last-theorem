#!/usr/bin/env python3
"""Build a provenance-hidden, order-randomised rating sheet for a third rater (L2 re-run, fix 1).

L2's pre-registered kappa was never measured: the third rater was not run, and every slot mark was
made by one NON-BLIND rater who knew which encoding was whose. A rater who knows which column is
the reference cannot produce an inter-rater statistic about it.

This tool removes both leaks:
  * provenance is stripped — encoder names, passes, timestamps, and any field naming a source of
    the encoding itself;
  * the two encodings are presented as X and Y with the assignment RANDOMISED PER CASE, so a rater
    who guesses the pattern on one case learns nothing about the next.

    make_rating_sheet.py build --a enc_fable/ --b enc_blind/ --seed 7 \
                               --out sheet.json --key key.json
    make_rating_sheet.py score --sheet filled.json --key key.json

`build` writes the key to a SEPARATE file. Do not give the rater the key. `score` needs both and
reports Cohen's kappa per slot plus the overall agreement.
"""
from __future__ import annotations
import argparse, json, pathlib, random, sys
from collections import Counter

SLOTS = ["state", "move", "invariant", "composition", "terminal"]
CODES = ["same", "compatible-but-different", "different", "one-missing"]
STRIP = {"encoder", "encoding_pass", "blind_reencoding", "logged_at", "seal", "source",
         "labelled_by", "label_pass", "correction", "verified_by", "provenance"}


def scrub(obj):
    """Remove anything that reveals WHOSE encoding this is."""
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items() if k not in STRIP}
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    return obj


def board_of(enc: dict) -> dict:
    b = enc.get("board") or enc.get("before_board") or {}
    return {s: b.get(s) if isinstance(b, dict) else None for s in SLOTS}


def cmd_build(a) -> int:
    A = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(a.a.glob("*.json"))}
    B = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(a.b.glob("*.json"))}
    ids = sorted(set(A) & set(B))
    if not ids:
        print(f"no case ids in common between {a.a} and {a.b}", file=sys.stderr)
        return 2
    for only in sorted(set(A) ^ set(B)):
        print(f"  warning: {only} is in only one directory and is excluded", file=sys.stderr)

    rng = random.Random(a.seed)
    sheet, key = [], []
    for cid in ids:
        swap = rng.random() < 0.5          # randomised PER CASE, not once for the whole sheet
        x, y = (B[cid], A[cid]) if swap else (A[cid], B[cid])
        sheet.append({
            "case": cid,
            "target": scrub(A[cid]).get("target") or scrub(A[cid]).get("problem"),
            "X": {"board": scrub(board_of(x)), "bound": scrub(x.get("bound") or x.get("bound_regimes") or x.get("bound_then")),
                  "leaks": scrub(x.get("leaks") or x.get("leak"))},
            "Y": {"board": scrub(board_of(y)), "bound": scrub(y.get("bound") or y.get("bound_regimes") or y.get("bound_then")),
                  "leaks": scrub(y.get("leaks") or y.get("leak"))},
            "rate": {s: "REPLACE-WITH-ONE-OF-" + "|".join(CODES) for s in SLOTS},
            "rate_bound": "REPLACE-WITH-ONE-OF-same|compatible-but-different|different|one-missing",
            "rate_leading_leak_mechanism": "REPLACE-WITH-same|different|one-missing",
        })
        key.append({"case": cid, "X": "B" if swap else "A", "Y": "A" if swap else "B"})

    a.out.write_text(json.dumps({
        "instructions": ("For each case, compare encoding X with encoding Y slot by slot. You are "
                         "NOT told which is which, and the assignment differs from case to case. "
                         "Code each slot with one of: " + ", ".join(CODES) + ". Use 'one-missing' "
                         "only when one side is empty; if both are empty, use 'same'."),
        "codes": CODES, "cases": sheet}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    a.key.write_text(json.dumps({"seed": a.seed, "key": key}, indent=2) + "\n", encoding="utf-8")
    print(f"{len(ids)} cases -> {a.out}")
    print(f"key -> {a.key}  (DO NOT give this to the rater)")
    swapped = sum(1 for k in key if k["X"] == "B")
    print(f"X/Y assignment randomised per case: {swapped} of {len(key)} swapped")
    return 0


def kappa(pairs: list[tuple[str, str]]) -> tuple[float | None, float, int]:
    n = len(pairs)
    if not n:
        return None, float("nan"), 0
    po = sum(1 for x, y in pairs if x == y) / n
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    if abs(1 - pe) < 1e-12:
        return None, po, n
    return (po - pe) / (1 - pe), po, n


def cmd_score(a) -> int:
    filled = json.loads(a.sheet.read_text(encoding="utf-8"))
    raters = filled.get("raters")
    if not raters or len(raters) < 2:
        # one rater: report the distribution, and say plainly that it is not a kappa
        rows = [(c["case"], s, c["rate"][s]) for c in filled["cases"] for s in SLOTS]
        unrated = [r for r in rows if str(r[2]).startswith("REPLACE")]
        if unrated:
            print(f"{len(unrated)} of {len(rows)} slot marks are still unfilled")
            return 1
        by = Counter(v for *_, v in rows)
        print(f"ONE rater, {len(rows)} slot marks:")
        for c in CODES:
            print(f"  {c:26} {by.get(c, 0)}")
        agree = by.get("same", 0) / len(rows)
        print(f"\n  'same' rate: {agree:.1%}")
        print("\nThis is an AGREEMENT RATE, not a kappa. One rater cannot produce an inter-rater")
        print("statistic — that was exactly L2's defect. Add a second rater's marks under a")
        print("'raters' key, each a list of case objects in the same order, for a real kappa.")
        return 0
    print(f"{len(raters)} raters\n")
    for s in SLOTS + ["bound", "leading_leak_mechanism"]:
        get = (lambda c, s=s: c["rate"][s]) if s in SLOTS else \
              (lambda c, s=s: c.get("rate_" + s))
        pairs = [(get(raters[0][i]), get(raters[1][i])) for i in range(len(raters[0]))]
        pairs = [(x, y) for x, y in pairs if x and y]
        k, po, n = kappa(pairs)
        ks = "undefined" if k is None else f"{k:.3f}"
        flag = ""
        if k is not None and k < 0.6:
            flag = "  <-- below 0.6"
        print(f"  {s:26} n={n:3}  agreement {po:.1%}  kappa {ks}{flag}")
    print("\nThe stop rule is unchanged: below about 0.6, read the encodings before believing any")
    print("table computed from them.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build")
    p.add_argument("--a", type=pathlib.Path, required=True)
    p.add_argument("--b", type=pathlib.Path, required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("sheet.json"))
    p.add_argument("--key", type=pathlib.Path, default=pathlib.Path("key.json"))
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("score")
    p.add_argument("--sheet", type=pathlib.Path, required=True)
    p.add_argument("--key", type=pathlib.Path)
    p.set_defaults(fn=cmd_score)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
