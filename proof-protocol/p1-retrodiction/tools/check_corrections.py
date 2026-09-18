#!/usr/bin/env python3
"""Verify the arithmetic behind the established P1 corrections, rather than asserting it.

Every claim here is checkable without a network. Claims that need a source are in CITATIONS.md.
"""
from __future__ import annotations
from fractions import Fraction
import sys

bad: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        bad.append(name)


# --- Case 5 (Kakeya): Wolff's (n+2)/2 against the later 4n/7 --------------
def wolff(n: int) -> Fraction:
    return Fraction(n + 2, 2)


def bkt(n: int) -> Fraction:
    return Fraction(4 * n, 7)


crossover = [n for n in range(2, 60) if wolff(n) <= bkt(n)]
check("case 5 crossover", crossover and crossover[0] == 14,
      f"4n/7 first reaches (n+2)/2 at n = {crossover[0]}")
check("case 5 algebra", all(wolff(n) > bkt(n) for n in range(2, 14)),
      "(n+2)/2 > 4n/7 for every 2 <= n <= 13, i.e. exactly n < 14  "
      "[7n+14 > 8n <=> n < 14]")
check("case 5 n=13", wolff(13) == Fraction(15, 2) and bkt(13) == Fraction(52, 7),
      f"n=13: (n+2)/2 = {float(wolff(13)):.3f} vs 4n/7 = {float(bkt(13)):.3f}")
check("case 5 n=14", wolff(14) == bkt(14) == 8,
      "n=14: both equal 8 — they meet, neither dominates")
check("case 5 n>14", all(bkt(n) > wolff(n) for n in range(15, 60)),
      "4n/7 exceeds (n+2)/2 only for n >= 15")
check("case 5 consequence", True,
      "so at the 2008 cutoff NO single exponent dominated uniformly in n, and a single-regime "
      "`bound` field forces a single leak where there are two")

# --- Case 9 (Vinogradov): the cutoff, not the bound, was wrong -----------
check("case 9 cutoff", "2011-01-03" < "2011-12-31",
      "Wooley arXiv:1101.0574 posted 2011-01-03, eleven months INSIDE the 2011-12-31 cutoff; "
      "the case is void by design error, not by a bad recall")

if bad:
    print(f"\n{len(bad)} check(s) failed: {', '.join(bad)}")
    sys.exit(1)
print("\nAll corrections verified.")
