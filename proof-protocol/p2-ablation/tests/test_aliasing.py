#!/usr/bin/env python3
"""Verify the fractional factorial's defining relation, rather than taking it on trust.

E = ABC and F = BCD generate the defining relation I = ABCE = BCDF = ADEF. The shortest word has
length 4, so the design is resolution IV: main effects are clean of two-way interactions, but
two-way interactions are aliased WITH EACH OTHER. The pre-registration forbids interpreting them,
and this test is what makes that statement checkable.
"""
from __future__ import annotations
import itertools, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from arms import ARMS, BLOCK_IDS  # noqa: E402

WORDS = ["ABCE", "BCDF", "ADEF"]
FACT = [a for a in ARMS if a.kind == "fact"]


def word_value(arm, word: str) -> int:
    v = 1
    for ch in word:
        v *= arm.lv[ch]
    return v


def main() -> int:
    bad = []
    if len(FACT) != 16:
        bad.append(f"expected 16 factorial arms, found {len(FACT)}")

    for w in WORDS:
        vals = {word_value(a, w) for a in FACT}
        if vals != {1}:
            bad.append(f"{w} is not a defining word: takes values {sorted(vals)}")
        else:
            print(f"ok   {w} = I on all 16 arms")

    # No shorter word is defining, which is what makes the resolution IV rather than III.
    shorter = []
    for k in (1, 2, 3):
        for combo in itertools.combinations(BLOCK_IDS, k):
            w = "".join(combo)
            if {word_value(a, w) for a in FACT} == {1}:
                shorter.append(w)
    if shorter:
        bad.append(f"shorter defining words exist, so the resolution is below IV: {shorter}")
    else:
        print("ok   no defining word of length 1, 2 or 3 — the design is resolution IV")

    # Main effects balanced: each block present in exactly half the arms.
    for b in BLOCK_IDS:
        n = sum(1 for a in FACT if a.lv[b] > 0)
        if n != 8:
            bad.append(f"block {b} is present in {n} arms, not 8 — the design is unbalanced")
    print("ok   every block is present in exactly 8 of 16 arms")

    # The aliasing the pre-registration forbids interpreting: which two-way pairs collide.
    pairs = ["".join(p) for p in itertools.combinations(BLOCK_IDS, 2)]
    groups: dict[tuple, list[str]] = {}
    for p in pairs:
        sig = tuple(word_value(a, p) for a in FACT)
        groups.setdefault(sig, []).append(p)
    aliased = [g for g in groups.values() if len(g) > 1]
    print(f"\n   two-way interactions fall into {len(groups)} distinguishable groups;")
    for g in sorted(aliased):
        print(f"     aliased with each other: {' = '.join(g)}")
    if not aliased:
        bad.append("no two-way aliasing found, which contradicts a resolution IV design")

    if bad:
        print("\n" + "\n".join(f"  {b}" for b in bad))
        return 1
    print("\nAliasing structure confirmed: resolution IV, two-way interactions mutually aliased.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
