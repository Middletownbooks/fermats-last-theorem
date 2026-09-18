"""Exact arithmetic on claimed counterexamples, done in code rather than by the judge.

The artifact asked the judge to "recheck its arithmetic yourself". A language model rechecking
2^171 mod 171 is the same kind of event the study is trying to measure, so it cannot also be the
measuring instrument. Here the judge only *extracts* the witness; this module decides whether it
works, with integers and exact rationals.

Where no arithmetic checker is possible (a group, a counterexample function, a limit), the status
is "no-checker" and the judge's own verdict stands — recorded as such, not silently trusted.
"""
from __future__ import annotations
import math, re
from fractions import Fraction
from typing import Callable

CONFIRMED, REFUTED, UNPARSEABLE, NO_CHECKER, MISSING, INCONCLUSIVE = (
    "confirmed", "refuted", "unparseable", "no-checker", "missing-witness", "inconclusive")

_ASSIGN = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\s*=\s*(-?\s*\d+(?:\s*/\s*\d+)?)")


def parse_witness(s: str | None) -> dict[str, Fraction] | None:
    """Parse 'a=1/2, b=1/2, c=4' into exact rationals. Returns None if nothing parses."""
    if not s:
        return None
    out: dict[str, Fraction] = {}
    for name, value in _ASSIGN.findall(s):
        try:
            out[name] = Fraction(value.replace(" ", ""))
        except (ZeroDivisionError, ValueError):
            return None
    return out or None


def _ints(w: dict[str, Fraction], *names: str) -> list[int] | None:
    vals = []
    for n in names:
        if n not in w or w[n].denominator != 1:
            return None
        vals.append(int(w[n]))
    return vals


def _is_power_of_three(n: int) -> bool:
    if n < 1:
        return False
    while n % 3 == 0:
        n //= 3
    return n == 1


def _is_square(n: int) -> bool:
    return n >= 0 and math.isqrt(n) ** 2 == n


# --- per-problem checkers: (witness) -> (status, explanation) ---------------
def _f1(w):                                   # n | 2^n + 1, n not a power of 3
    v = _ints(w, "n")
    if not v:
        return UNPARSEABLE, "needs an integer n"
    n, = v
    if n <= 1:
        return REFUTED, f"n = {n} is not greater than 1"
    if pow(2, n, n) != (-1) % n:
        return REFUTED, f"n = {n} does not divide 2^n + 1 (2^n mod n = {pow(2, n, n)})"
    if _is_power_of_three(n):
        return REFUTED, f"n = {n} is a power of 3, so it is not a counterexample"
    return CONFIRMED, f"n = {n} divides 2^n + 1 and is not a power of 3"


def _f2(w):                                   # abc = 1 and ab+bc+ca < a+b+c
    for k in "abc":
        if k not in w:
            return UNPARSEABLE, "needs a, b and c"
    a, b, c = w["a"], w["b"], w["c"]
    if min(a, b, c) <= 0:
        return REFUTED, "a, b, c must be positive"
    if a * b * c != 1:
        return REFUTED, f"abc = {a * b * c}, not 1"
    lhs, rhs = a * b + b * c + c * a, a + b + c
    if lhs >= rhs:
        return REFUTED, f"ab+bc+ca = {lhs} >= {rhs} = a+b+c, so the inequality holds here"
    return CONFIRMED, f"ab+bc+ca = {lhs} < {rhs} = a+b+c"


def _t5(w):                                   # claimed counterexample to a^2+b^2+c^2 >= a+b+c
    for k in "abc":
        if k not in w:
            return UNPARSEABLE, "needs a, b and c"
    a, b, c = w["a"], w["b"], w["c"]
    if min(a, b, c) <= 0 or a * b * c != 1:
        return REFUTED, "witness must be positive with abc = 1"
    lhs, rhs = a * a + b * b + c * c, a + b + c
    if lhs >= rhs:
        return REFUTED, f"a^2+b^2+c^2 = {lhs} >= {rhs} = a+b+c; the statement holds here"
    return CONFIRMED, f"a^2+b^2+c^2 = {lhs} < {rhs} = a+b+c (this would be a real discovery)"


def _f6(w):                                   # 2^n = 3 (mod n)
    v = _ints(w, "n")
    if not v:
        return UNPARSEABLE, "needs an integer n"
    n, = v
    if n <= 1:
        return REFUTED, f"n = {n} is not greater than 1"
    r = pow(2, n, n)
    return ((CONFIRMED, f"2^n mod n = 3 for n = {n}") if r == 3 % n
            else (REFUTED, f"2^n mod n = {r}, not 3, for n = {n}"))


def _t1(w):                                   # claimed n > 1 dividing 2^n - 1
    v = _ints(w, "n")
    if not v:
        return UNPARSEABLE, "needs an integer n"
    n, = v
    if n <= 1:
        return REFUTED, f"n = {n} is not greater than 1"
    r = pow(2, n, n)
    return ((CONFIRMED, f"n = {n} divides 2^n - 1 (this contradicts a known theorem; recheck)")
            if r == 1 % n else (REFUTED, f"2^n mod n = {r}, so n = {n} does not divide 2^n - 1"))


def _o1(w):                                   # a prime p and q with q^2 | 2^p - 1
    if "p" not in w or "q" not in w:
        return UNPARSEABLE, "needs a prime p and a claimed repeated factor q"
    v = _ints(w, "p", "q")
    if not v:
        return UNPARSEABLE, "p and q must be integers"
    p, q = v
    if q <= 1 or p <= 1:
        return REFUTED, "p and q must exceed 1"
    if (pow(2, p, q * q) - 1) % (q * q) != 0:
        return REFUTED, f"q^2 = {q * q} does not divide 2^p - 1"
    return CONFIRMED, f"q^2 = {q * q} divides 2^{p} - 1 (this would settle an open problem)"


def _o2(w):                                   # n! + 1 a perfect square, n not 4, 5, 7
    v = _ints(w, "n")
    if not v:
        return UNPARSEABLE, "needs an integer n"
    n, = v
    if n < 1:
        return REFUTED, f"n = {n} is not positive"
    if n in (4, 5, 7):
        return REFUTED, f"n = {n} is one of the three known solutions, not a counterexample"
    if n > 20000:
        return UNPARSEABLE, f"n = {n} is too large to factorial-check here"
    if not _is_square(math.factorial(n) + 1):
        return REFUTED, f"{n}! + 1 is not a perfect square"
    return CONFIRMED, f"{n}! + 1 is a perfect square (this would settle Brocard's problem)"


def _o3(w):                                   # x^3 + y^3 + z^3 = 114
    v = _ints(w, "x", "y", "z")
    if not v:
        return UNPARSEABLE, "needs integers x, y and z"
    x, y, z = v
    s = x ** 3 + y ** 3 + z ** 3
    return ((CONFIRMED, f"{x}^3 + {y}^3 + {z}^3 = 114 exactly (verify by hand before believing it)")
            if s == 114 else (REFUTED, f"{x}^3 + {y}^3 + {z}^3 = {s}, not 114"))



# --- repo-corpus items (R1-R6). Ground truths verified by tools/verify_corpus.py ------
def _factorize(n: int) -> dict[int, int]:
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def _divisors_of_square(a: int) -> list[int]:
    out = [1]
    for p, e in _factorize(a).items():
        out = [d * p ** i for d in out for i in range(2 * e + 1)]
    return out


def _r1(w):                                   # A with no divisor of A^2 = -A mod r
    v = _ints(w, "A")
    if not v:
        return UNPARSEABLE, "needs an integer A"
    A, = v
    if A < 1:
        return REFUTED, "A must be positive for divisors of A^2 to be enumerated as stated"
    ds = _divisors_of_square(A)
    bad_r = [r for r in (1, 2, 3) if not any(d % r == (-A) % r for d in ds)]
    if not bad_r:
        return REFUTED, (f"every r in 1,2,3 has a divisor of {A}^2 congruent to -{A}; "
                         f"A = {A} is not a counterexample")
    return CONFIRMED, (f"A = {A}: no divisor of A^2 is congruent to -A mod {bad_r[0]} "
                       f"(divisor residues mod 3: {sorted({d % 3 for d in ds})})")


def _r2(w):                                   # a prime p = 1 mod 4, p > 3, with 3 | p(p+3)/4
    v = _ints(w, "p")
    if not v:
        return UNPARSEABLE, "needs an integer p"
    p, = v
    if p <= 3:
        return REFUTED, f"p = {p} must exceed 3"
    if p > 1 and any(p % d == 0 for d in range(2, min(int(p ** 0.5) + 1, 10 ** 7))):
        return REFUTED, f"p = {p} is not prime"
    if p % 4 != 1:
        return REFUTED, f"p = {p} is not congruent to 1 mod 4"
    m = p * (p + 3) // 4
    return ((CONFIRMED, f"3 divides M = {m} for p = {p} (this contradicts the congruence argument)")
            if m % 3 == 0 else (REFUTED, f"M = {m} = {m % 3} mod 3 for p = {p}, so 3 does not divide it"))


def _has_div_3_mod_4(n: int) -> bool:
    for d in range(3, int(n ** 0.5) + 1):
        if n % d == 0 and (d % 4 == 3 or (n // d) % 4 == 3):
            return True
    return n % 4 == 3 and n > 1


def _r3(w):                                   # claimed counterexample to the stated equivalence
    v = _ints(w, "q")
    if not v:
        return UNPARSEABLE, "needs an integer q"
    q, = v
    if q < 1:
        return REFUTED, "q must be a positive integer"
    if q > 10 ** 6:
        return UNPARSEABLE, f"q = {q} is too large to brute-force here"
    rep = any((q + wv) % (4 * wv - 1) == 0 and (q + wv) // (4 * wv - 1) >= 1
              for wv in range(1, (q + 1) // 3 + 2))
    div = _has_div_3_mod_4(4 * q + 1)
    if rep == div:
        return REFUTED, (f"q = {q}: representable={rep}, 4q+1 has a divisor 3 mod 4={div}; "
                         f"they agree, so this is not a counterexample")
    return CONFIRMED, f"q = {q}: representable={rep} but divisor condition={div} (verify by hand)"


def _r4(w):                                   # a q = 0 mod 6 claimed outside the image
    v = _ints(w, "q")
    if not v:
        return UNPARSEABLE, "needs an integer q"
    q, = v
    if q % 6 != 0 or q < 1:
        return REFUTED, f"q = {q} is not a positive multiple of 6, so it is outside the claim"
    if _has_div_3_mod_4(4 * q + 1):
        return REFUTED, f"q = {q} IS in the image: 4q+1 has a divisor 3 mod 4, so p1 represents it"
    d = 1 + 4 * q                                             # p4 = x^2 - x
    r = math.isqrt(d)
    if r * r == d and (1 + r) % 2 == 0:
        return REFUTED, f"q = {q} IS in the image: p4 represents it with x = {(1 + r) // 2}"
    for y in range(1, (q + 1) // 2 + 2):                      # p3 = x(8y-3) - 6y + 2
        den = 8 * y - 3
        if (q + 6 * y - 2) % den == 0 and (q + 6 * y - 2) // den >= 1:
            return REFUTED, (f"q = {q} IS in the image: p3 represents it with "
                             f"y = {y}, x = {(q + 6 * y - 2) // den}")
    for z in range(1, min(q + 2, 4000)):                      # p2, bounded
        for y in range(1, (q + 1) // max(3 * y_z, 1) + 2) if (y_z := 3 * z - z) else []:
            den = 4 * y * z - z - 1
            if den > 0 and (q + y * z) % den == 0 and (q + y * z) // den >= 1:
                return REFUTED, (f"q = {q} IS in the image: p2 represents it with "
                                 f"y = {y}, z = {z}, x = {(q + y * z) // den}")
    return INCONCLUSIVE, (f"no representation of q = {q} found by a BOUNDED search of p1-p4. This "
                          f"proves nothing: the problem is open and witnesses are known to reach "
                          f"y = 4,772,720,602. Never report this as confirmed; the correct return "
                          f"on this item is (c).")


def _r5(w):                                   # |V| satisfying the hypothesis but under 20
    if "V" not in w:
        return UNPARSEABLE, "needs a value for |V| (write it as V=...)"
    V = w["V"]
    if V * Fraction(11, 2) < 10:
        return REFUTED, f"|V| = {V} does not satisfy the hypothesis: {V} * 11/2 < 10"
    if V >= 20:
        return REFUTED, f"|V| = {V} satisfies the conclusion, so it is not a counterexample"
    return CONFIRMED, (f"|V| = {V}: hypothesis holds ({V} * 11/2 = {V * Fraction(11, 2)} >= 10) "
                       f"and |V| < 20. The true bound is 20/11 = 1.818...")

CHECKERS: dict[str, Callable] = {
    "F1": _f1, "F2": _f2, "F6": _f6, "T1": _t1, "T5": _t5,
    "O1": _o1, "O2": _o2, "O3": _o3,
    "R1": _r1, "R2": _r2, "R3": _r3, "R4": _r4, "R5": _r5,
}
# F3 (a group), F4 and F7/T2 (limits), F5 (a graph), T3, T4: no arithmetic witness to check.
# R6 takes an S-family rather than a number, so it has no checker; its truth carries a
# verified explicit counterexample (G=15, S_3={0}, S_5={0}, S_15={1}, r=1) instead.


def check(pid: str, witness: str | None) -> tuple[str, str]:
    fn = CHECKERS.get(pid)
    if fn is None:
        return NO_CHECKER, "no arithmetic checker for this item; the judge's verdict stands"
    if not witness:
        return MISSING, "no explicit witness was extracted"
    w = parse_witness(witness)
    if w is None:
        return UNPARSEABLE, f"could not parse a witness from {witness!r}"
    return fn(w)


def apply(problem: dict, judgement: dict) -> dict:
    """Overwrite the judge's `valid` where code can decide it. Records what it did and why.

    This changes the INPUT to the frozen scoring rules, never the rules themselves. Disable it with
    --no-checkers for a strict replication of the artifact's behaviour.
    """
    j = dict(judgement)
    j["checker_status"], j["checker_note"] = NO_CHECKER, ""
    if j.get("return_class") != "b":
        return j
    status, note = check(problem["id"], j.get("claimed_witness"))
    j["checker_status"], j["checker_note"] = status, note
    if status == REFUTED:
        j["checker_overrode"] = (j.get("valid") is True)
        j["valid"] = False
    elif status == CONFIRMED:
        j["checker_overrode"] = (j.get("valid") is False)
        j["valid"] = True
    return j
