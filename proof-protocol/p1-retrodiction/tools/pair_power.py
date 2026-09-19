#!/usr/bin/env python3
"""How many contemporaneous within-problem pairs would a usable measurement need?

D31 recorded that the case 7 pair was deliberately NOT run, because n = 2 produces a number that
cannot be interpreted. This says what n WOULD be enough, before any collecting effort is spent.

The design: each pair is one problem in one period, with two teams, one of which changed the board
and one of which did not. A rater sees both halves and must say which is which. Under recall alone
the rater cannot use the problem's identity -- both halves ARE the problem -- so chance is 1/2 per
pair and the test is an exact one-sided sign test.
"""
from __future__ import annotations
from math import comb

ALPHA = 0.05


def p_value(k: int, n: int) -> float:
    """P(X >= k) for X ~ Binomial(n, 1/2): the one-sided sign test."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def main() -> None:
    print("exact one-sided sign test against chance = 1/2 per pair, alpha = 0.05\n")
    print(f"  {'n pairs':>8} {'all correct':>12} {'one miss':>10}  smallest n that clears alpha")
    best_clean = best_one_miss = None
    for n in range(2, 13):
        clean, one = p_value(n, n), p_value(n - 1, n)
        if best_clean is None and clean <= ALPHA:
            best_clean = n
        if best_one_miss is None and one <= ALPHA:
            best_one_miss = n
        print(f"  {n:>8} {clean:>12.4f} {one:>10.4f}")
    print(f"\n  {best_clean} pairs, scored perfectly, clear alpha = {ALPHA} (p = "
          f"{p_value(best_clean, best_clean):.4f}).")
    print(f"  {best_one_miss} pairs are needed to still clear it after ONE miss (p = "
          f"{p_value(best_one_miss - 1, best_one_miss):.4f}); at n = {best_one_miss - 1} one miss "
          f"gives p = {p_value(best_one_miss - 2, best_one_miss - 1):.4f} and fails.")
    print("\n  So the collecting target is 5 pairs to say anything at all and 8 to survive a single")
    print("  disagreement. ONE discrimination pair is in hand -- case 7a (Maynard-Tao, board")
    print("  changed) against control 16 (Zhang, level-n board unchanged). The Roth 2023 pair")
    print("  (control 15, Kelley-Meka, against control 17, Bloom-Sisask) does NOT count toward the")
    print("  five: both halves are must-not-fire, so there is no 'which is which' to score. It tests")
    print("  specificity inside one problem-period instead, a different number. Every")
    print("  discrimination pair must be a PAIR: same period, two teams, one board change and one")
    print("  not. See PAIRS.md.")
    print("\n  Note what this does NOT buy. The sign test measures whether a rater can separate the")
    print("  halves; it does not measure whether the DIAGNOSTIC adds anything, because the D25")
    print("  baseline rater must be run on the same pairs and beaten. A pair set that a rule-less")
    print("  rater also separates 8/8 is another D25, not an answer to it.")


if __name__ == "__main__":
    main()
