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

CONFIRMED, REFUTED, UNPARSEABLE, NO_CHECKER, MISSING = (
    "confirmed", "refuted", "unparseable", "no-checker", "missing-witness")

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


CHECKERS: dict[str, Callable] = {
    "F1": _f1, "F2": _f2, "F6": _f6, "T1": _t1, "T5": _t5,
    "O1": _o1, "O2": _o2, "O3": _o3,
}
# F3 (a group), F4 and F7/T2 (limits), F5 (a graph), T3, T4: no arithmetic witness to check.


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
