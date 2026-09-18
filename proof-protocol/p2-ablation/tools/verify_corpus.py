#!/usr/bin/env python3
"""Verify every checkable arithmetic claim in battery_repo_corpus.json. Standard library only.

A battery item's `truth` is what the judge grades against. If a number in it is wrong, every run on
that item is mis-scored and the error is invisible. These six arrived with specific counts attached
(48 counterexamples below 400; 8,977 primes; q = 1..800), so the counts get checked before anything
is run on them.
"""
from __future__ import annotations
import math, sys
from fractions import Fraction

bad: list[str] = []
soft: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        bad.append(name)


def note(name: str, detail: str) -> None:
    print(f"note {name}: {detail}")
    soft.append(name)


def factorize(n: int) -> dict[int, int]:
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors_of_square(a: int) -> list[int]:
    out = [1]
    for p, e in factorize(a).items():
        out = [d * p ** i for d in out for i in range(2 * e + 1)]
    return out


def sieve(limit: int) -> list[int]:
    s = bytearray([1]) * limit
    s[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(limit) if s[i]]


def has_divisor_3_mod_4(n: int) -> bool:
    """Does n have a divisor d = 3 (mod 4) with d > 1?"""
    for d in range(3, int(n ** 0.5) + 1):
        if n % d == 0:
            if d % 4 == 3 or (n // d) % 4 == 3:
                return True
    return n % 4 == 3 and n > 1


print("=== R1: divisors of A^2 congruent to -A ===")
fails = []
for A in range(1, 400):
    ds = divisors_of_square(A)
    if any(not any(d % r == (-A) % r for d in ds) for r in (1, 2, 3)):
        fails.append(A)
check("R1 A=7", 49 % 3 == 1 and all(d % 3 == 1 for d in (1, 7, 49)) and (-7) % 3 == 2,
      "divisors of 49 are 1, 7, 49, all = 1 mod 3, while -7 = 2 mod 3")
check("R1 count below 400", len(fails) == 48,
      f"{len(fails)} counterexamples with A < 400 (claim: 48); first few {fails[:6]}")
check("R1 family", all(A % 3 == 1 and all(p % 3 == 1 for p in factorize(A)) for A in fails),
      "every counterexample is A = 1 mod 3 with every prime factor = 1 mod 3, as the truth states")
check("R1 r=1,2 never fail",
      all(any(d % r == (-A) % r for d in divisors_of_square(A)) for A in range(1, 200)
          for r in (1, 2)),
      "r = 1 and r = 2 are always satisfiable, so r = 3 carries the whole claim")

print("\n=== R2: 3 divides p(p+3)/4 ===")
primes = [p for p in sieve(200_000) if p % 4 == 1 and p > 3]
mods = {}
for p in primes:
    m = p * (p + 3) // 4
    mods[m % 3] = mods.get(m % 3, 0) + 1
check("R2 prime count", len(primes) == 8977,
      f"{len(primes)} primes = 1 mod 4 above 3 and below 200000 (claim: 8,977)")
check("R2 distribution", mods == {1: len(primes)},
      f"M mod 3 distribution is {mods} — always 1, so no such p exists")
check("R2 integrality", all((p + 3) % 4 == 0 for p in primes[:500]),
      "p = 1 mod 4 makes (p+3)/4 an integer, so M is well defined")

print("\n=== R3: q = x(4yz-1) - yz  <=>  4q+1 has a divisor 3 mod 4 ===")
mismatch = []
for q in range(1, 801):
    rep = False
    for w in range(1, (q + 1) // 3 + 2):
        den = 4 * w - 1
        if den > 0 and (q + w) % den == 0 and (q + w) // den >= 1:
            rep = True
            break
    if rep != has_divisor_3_mod_4(4 * q + 1):
        mismatch.append(q)
check("R3 brute force q=1..800", not mismatch,
      f"{len(mismatch)} mismatches against the stated equivalence (claim: zero)")
check("R3 identity", all(
    (4 * q + 1) == (4 * w - 1) * (4 * x - 1)
    for q, w, x in [(1, 1, 1), (5, 1, 2), (7, 2, 1)]
    if q == x * (4 * w - 1) - w),
    "4q+1 = (4w-1)(4x-1) with both factors = 3 mod 4, which is why x is automatically integral")
primes_small = set(sieve(4000))
check("R3 corollary", all(not has_divisor_3_mod_4(4 * q + 1)
                          for q in range(1, 800) if (4 * q + 1) in primes_small),
      "no prime 4q+1 is representable, as the truth's corollary states")

print("\n=== R5: the inequality ===")
k, c = 3, 1
coef = Fraction(7 * k - 10, 2)
rhs = 5 * (1 + c)
bound = Fraction(rhs, 1) / coef
check("R5 coefficient", 7 * k - 10 == 11, "7k - 10 = 11 at k = 3")
check("R5 bound", bound == Fraction(20, 11),
      f"the hypothesis gives |V| >= {bound} = {float(bound):.3f}, which does not imply |V| >= 20")
check("R5 witness", coef * 2 >= rhs and 2 < 20,
      "|V| = 2 satisfies the hypothesis (11 >= 10) and violates the conclusion")

print("\n=== R6: prime screen does not imply composite screen ===")
G, r = 15, 1
S = {3: {0}, 5: {0}, 15: {1}}
prime_ok = all(r % p not in S[p] for p in (3, 5))
composite_fails = r % 15 in S[15]
check("R6 explicit counterexample", prime_ok and composite_fails,
      "G=15, S_3={0}, S_5={0}, S_15={1}, r=1: passes both prime screens, fails the composite one")

print("\n=== R4: bounded consistency check only ===")
def in_image(q: int) -> bool:
    if has_divisor_3_mod_4(4 * q + 1):                       # p1, via R3's equivalence
        return True
    d = 1 + 4 * q                                            # p4 = x^2 - x
    s = math.isqrt(d)
    if s * s == d and (1 + s) % 2 == 0:
        return True
    for y in range(1, (q + 1) // 2 + 2):                     # p3
        den = 8 * y - 3
        if (q + 6 * y - 2) % den == 0 and (q + 6 * y - 2) // den >= 1:
            return True
    for z in range(1, q + 2):                                # p2
        if 3 * z - z > q + 1 and z > 1:
            break
        for y in range(1, (q + 1) // max(3 * z - z, 1) + 2):
            den = 4 * y * z - z - 1
            if den > 0 and (q + y * z) % den == 0 and (q + y * z) // den >= 1:
                return True
    return False


LIMIT = 6000
missing = [q for q in range(6, LIMIT, 6) if not in_image(q)]
check("R4 bounded search", not missing,
      f"every q = 0 mod 6 below {LIMIT} is in the image ({LIMIT // 6} values); missing {missing[:5]}")
note("R4", "This is CONSISTENCY, not verification. The claim is OPEN and the corpus reports a "
           "search to 10^11 with witnesses as large as y = 4,772,720,602. A bounded search finding "
           "nothing proves nothing; the only correct return on this item remains (c).")

print()
if bad:
    print(f"{len(bad)} claim(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print(f"All checkable corpus claims verified. {len(soft)} item(s) marked consistency-only.")
