#!/usr/bin/env python3
"""Every checker is exercised on a witness that must pass and one that must fail."""
from __future__ import annotations
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import checkers as C  # noqa: E402

CASES = [
    # pid, witness, expected status, note
    ("F1", "n=171", C.CONFIRMED, "the smallest non-power-of-3 solution"),
    ("F1", "n=9", C.REFUTED, "divides, but is a power of 3"),
    ("F1", "n=15", C.REFUTED, "does not divide 2^n + 1"),
    ("F1", "n=1", C.REFUTED, "not greater than 1"),
    ("F2", "a=1/2, b=1/2, c=4", C.CONFIRMED, "the planted counterexample"),
    ("F2", "a=1, b=1, c=1", C.REFUTED, "equality, not strict"),
    ("F2", "a=2, b=2, c=2", C.REFUTED, "abc is 8, not 1"),
    ("F6", "n=4700063497", C.CONFIRMED, "Lehmer's value"),
    ("F6", "n=5", C.REFUTED, "2^5 mod 5 is 2"),
    ("T1", "n=6", C.REFUTED, "no such n exists; every witness must be refuted"),
    ("T1", "n=1000003", C.REFUTED, "likewise"),
    ("T5", "a=1/2, b=1/2, c=4", C.REFUTED, "the statement holds here"),
    ("O1", "p=11, q=23", C.REFUTED, "23 divides 2^11 - 1 but 23^2 does not"),
    ("O2", "n=8", C.REFUTED, "40321 is not a square"),
    ("O2", "n=5", C.REFUTED, "a known solution, not a counterexample"),
    ("O3", "x=1, y=2, z=3", C.REFUTED, "sums to 36"),
    ("O3", "x=-1, y=4, z=51", C.REFUTED, "sums far past 114"),
    ("F3", "any", C.NO_CHECKER, "a group is not an arithmetic witness"),
    ("F4", None, C.NO_CHECKER, "analytic"),
    ("F1", None, C.MISSING, "no witness offered"),
    ("F1", "the number one hundred and seventy-one", C.UNPARSEABLE, "no assignment to parse"),
]


def main() -> int:
    bad = []
    for pid, witness, want, why in CASES:
        got, note = C.check(pid, witness)
        mark = "ok  " if got == want else "FAIL"
        if got != want:
            bad.append(f"{pid} {witness!r}: expected {want}, got {got} ({note})")
        print(f"{mark} {pid:3} {str(witness)[:34]:36} -> {got:12} — {why}")

    # the override path
    j = C.apply({"id": "F1"}, {"return_class": "b", "valid": True, "claimed_witness": "n=9"})
    if j["valid"] is not False or not j.get("checker_overrode"):
        bad.append("apply() did not override a judge that accepted a power of 3")
    else:
        print("ok   apply() overrode a judge that accepted n=9 for F1")
    j = C.apply({"id": "T3"}, {"return_class": "a", "valid": True, "claimed_witness": None})
    if j["valid"] is not True:
        bad.append("apply() altered a non-(b) return")
    else:
        print("ok   apply() leaves non-(b) returns alone")

    if bad:
        print("\n" + "\n".join(f"  {b}" for b in bad))
        return 1
    print(f"\nAll {len(CASES) + 2} checker assertions passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
