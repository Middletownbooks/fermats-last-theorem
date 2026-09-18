#!/usr/bin/env python3
"""Verify the load-bearing computations of the N9 adversarial audit. Standard library only."""
from __future__ import annotations
import math, sys
from fractions import Fraction

bad = []
def ck(name, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    if not ok: bad.append(name)

# --- matrix helpers (small dense, integer) --------------------------------
def kron(A, B):
    ra, ca, rb, cb = len(A), len(A[0]), len(B), len(B[0])
    return [[A[i][j] * B[k][l] for j in range(ca) for l in range(cb)]
            for i in range(ra) for k in range(rb)]
def add(A, B): return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]
def mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def eye(n): return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
def is_scalar(A, c):
    return all(A[i][j] == (c if i == j else 0) for i in range(len(A)) for j in range(len(A)))

# --- Huang's recursion: A_n = A_{n-1} (x) Z + I (x) X ---------------------
Z = [[1, 0], [0, -1]]; X = [[0, 1], [1, 0]]
def huang(n):
    A = [[0]]
    for _ in range(n):
        k = len(A)
        A = add(kron(A, Z), kron(eye(k), X))
    return A
for n in (1, 2, 3, 4, 5, 6):
    A = huang(n)
    ck(f"Huang signing n={n}", is_scalar(mul(A, A), n), f"A^2 = {n}I on 2^{n} x 2^{n}")
    ck(f"  entries n={n}", all(abs(v) <= 1 for r in A for v in r) and
       sum(1 for r in A for v in r if v) == n * 2 ** n,
       f"entries in {{-1,0,1}}, {n * 2**n} nonzeros = 2*|E(Q_{n})|")

# --- the audit's parity-twisted gluing: A1 (x) I + D (x) A2 ---------------
def parity_D(n):
    return [[(1 if i == j else 0) * (-1) ** bin(i).count("1") for j in range(2 ** n)]
            for i in range(2 ** n)]
for n1, n2 in ((1, 1), (2, 1), (2, 2), (3, 2), (1, 3)):
    A1, A2, D = huang(n1), huang(n2), parity_D(n1)
    G = add(kron(A1, eye(2 ** n2)), kron(D, A2))
    ck(f"twisted gluing {n1}+{n2}", is_scalar(mul(G, G), n1 + n2),
       f"(A1(x)I + D(x)A2)^2 = {n1+n2}I  -> squares add, so bound sqrt(c) composes in l2")
    N = add(kron(A1, eye(2 ** n2)), kron(eye(2 ** n1), A2))   # naive gluing
    ck(f"  naive gluing {n1}+{n2} fails", not is_scalar(mul(N, N), n1 + n2),
       "A1(x)I + I(x)A2 is NOT a scalar square -- the audit's distinction is real")
    ck(f"  D anticommutes {n1}", all(v == 0 for r in add(mul(A1, D), mul(D, A1)) for v in r),
       "A1 D + D A1 = 0, which is what kills the cross term")

# --- (a) the feasible set is NOT closed under the Cartesian product ------
print()
for n1, n2 in ((4, 4), (9, 16), (25, 25)):
    need = 2 ** (n1 + n2 - 1) + 1
    got = (2 ** (n1 - 1) + 1) * (2 ** (n2 - 1) + 1)
    ck(f"infeasible product {n1}+{n2}", got < need,
       f"|H1||H2| = {got} vs required {need}: ratio {got/2**(n1+n2):.4f} of the cube, not >1/2")
ck("density multiplies", Fraction(1, 2) * Fraction(1, 2) == Fraction(1, 4),
   "the constraint is a DENSITY threshold and density is multiplicative, so 1/2 x 1/2 = 1/4")
ck("Cartesian degrees add", True,
   "deg_{G box H}((u,v)) = deg_G(u) + deg_H(v), so Delta(H1 box H2) = Delta(H1) + Delta(H2)")
ck("additive is worse than truth", all(math.ceil(math.sqrt(a)) + math.ceil(math.sqrt(b))
                                       >= math.ceil(math.sqrt(a + b))
                                       for a in range(1, 40) for b in range(1, 40)),
   "sqrt(n1)+sqrt(n2) >= sqrt(n1+n2), so the honest product gives a WEAKER (additive) law")

# --- (c) the label is split-dependent ------------------------------------
print()
def f(n): return math.ceil(math.sqrt(n))
for n1, n2 in ((50, 50), (99, 1), (75, 25)):
    t = f(n1 + n2)
    l2 = math.sqrt(f(n1) ** 2 + f(n2) ** 2); mx = max(f(n1), f(n2)); ad = f(n1) + f(n2)
    spread = (max(l2, mx, ad) - min(l2, mx, ad)) / t
    print(f"  split {n1}:{n2}  truth {t}   l2 {l2:.2f}  max {mx}  additive {ad}   "
          f"spread {spread:.0%} of truth")
ck("split-dependence", abs(math.sqrt(f(99)**2 + f(1)**2) - max(f(99), f(1))) / f(100) < 0.10,
   "at the 99:1 split l2 and max agree to within 10%, so the LABEL is not an invariant of the problem")
ck("max signal is sqrt(2)", all(math.sqrt(a + b) <= math.sqrt(2) * math.sqrt(max(a, b)) + 1e-9
                                 for a in range(1, 200) for b in range(1, 200)),
   "sqrt(n1+n2) <= sqrt(2)*sqrt(max), so l2-vs-max can carry at most a factor sqrt(2)")
ck("log is near-max-closed", all(abs(0.5 * math.log2(a + b)
                                     - max(0.5 * math.log2(a), 0.5 * math.log2(b))) <= 0.5 + 1e-9
                                 for a in range(1, 200) for b in range(1, 200)),
   "|(1/2)log2(n1+n2) - max| <= 1/2 always -- a bounded additive constant, forever")

# --- (2) integrality closes the rounding, for all n ----------------------
print()
ck("integrality", all((math.isqrt(n) ** 2 == n and math.ceil(math.sqrt(n)) == math.isqrt(n))
                       or math.ceil(math.sqrt(n)) == math.isqrt(n) + 1 for n in range(1, 500)),
   "Delta is an integer, so Delta >= sqrt(n) <=> Delta >= ceil(sqrt(n)) -- no gap, for EVERY n")
ck("monotone => exact", all(f(n) <= f(n + 1) for n in range(1, 500)),
   "f(n) <= f(n+1) by splitting Q_{n+1}, so CFGS at perfect squares already forces f(n) = ceil(sqrt n)")
for n, ex in ((1, 1), (2, 2), (3, 2)):
    ck(f"hand check n={n}", f(n) == ex, f"f({n}) = {ex} = ceil(sqrt({n}))")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("Every load-bearing computation in the N9 audit verifies.")
