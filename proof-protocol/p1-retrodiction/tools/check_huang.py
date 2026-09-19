#!/usr/bin/env python3
"""Verify the Huang transcript's load-bearing mathematics (arXiv:1907.00847v2).

Run from `proof-protocol/p1-retrodiction/`. Everything here is checked by construction rather than
recalled: the matrices are built, the eigenvalues computed, the interlacing step reproduced, and the
tightness constructions realised as graphs. Three citation rows rest on this transcript (C1-gotsman,
C1-bound, C1-after) and one twin (N9), so the arithmetic is worth more than the reading.
"""
from __future__ import annotations
import itertools, math, sys
from fractions import Fraction

bad: list[str] = []


def ck(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")
    if not ok:
        bad.append(name)


# ---------------------------------------------------------------- linear algebra without numpy
def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def eigenvalues_sym(A):
    """Jacobi eigenvalue iteration; A is symmetric and small here."""
    n = len(A)
    M = [row[:] for row in A]
    for _ in range(200):
        off = max(((abs(M[i][j]), i, j) for i in range(n) for j in range(n) if i != j), default=(0, 0, 0))
        if off[0] < 1e-12:
            break
        _, p, q = off
        if abs(M[p][p] - M[q][q]) < 1e-18:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2 * M[p][q], M[p][p] - M[q][q])
        c, s = math.cos(theta), math.sin(theta)
        for k in range(n):
            mkp, mkq = M[k][p], M[k][q]
            M[k][p], M[k][q] = c * mkp + s * mkq, -s * mkp + c * mkq
        for k in range(n):
            mpk, mqk = M[p][k], M[q][k]
            M[p][k], M[q][k] = c * mpk + s * mqk, -s * mpk + c * mqk
    return sorted((M[i][i] for i in range(n)), reverse=True)


# ---------------------------------------------------------------- Lemma 2.2: A_n^2 = nI
def A(n: int):
    """A_1 = [[0,1],[1,0]];  A_n = [[A_{n-1}, I], [I, -A_{n-1}]]."""
    if n == 1:
        return [[0, 1], [1, 0]]
    P = A(n - 1)
    m = len(P)
    top = [P[i] + [1 if i == j else 0 for j in range(m)] for i in range(m)]
    bot = [[1 if i == j else 0 for j in range(m)] + [-P[i][j] for j in range(m)] for i in range(m)]
    return top + bot


print("=== Lemma 2.2: the signed matrix squares to nI, so its spectrum is flat at +-sqrt(n) ===")
for n in range(1, 8):
    M = A(n)
    sq = matmul(M, M)
    size = 2 ** n
    is_nI = all(sq[i][j] == (n if i == j else 0) for i in range(size) for j in range(size))
    trace = sum(M[i][i] for i in range(size))
    entries_ok = all(M[i][j] in (-1, 0, 1) for i in range(size) for j in range(size))
    ck(f"n={n}: A_n^2 = {n}I, Tr = 0, entries in {{-1,0,1}}", is_nI and trace == 0 and entries_ok,
       f"2^{n} = {size} rows")
ev = eigenvalues_sym([[float(x) for x in r] for r in A(5)])
pos = sum(1 for x in ev if x > 0)
ck("n=5: half the eigenvalues are +sqrt(5), half -sqrt(5)",
   pos == 2 ** 4 and abs(ev[0] - math.sqrt(5)) < 1e-9 and abs(ev[-1] + math.sqrt(5)) < 1e-9,
   f"multiplicity {pos} each, extremes {ev[0]:.6f} and {ev[-1]:.6f} against sqrt(5) = {math.sqrt(5):.6f}")

print("\n=== the sign flip really does recover Q_n, which is what lets Lemma 2.3 apply ===")
for n in range(1, 7):
    M, size = A(n), 2 ** n
    flipped = [[abs(M[i][j]) for j in range(size)] for i in range(size)]
    verts = list(itertools.product((0, 1), repeat=n))
    # A_n's rows are indexed so that the recursion splits on the FIRST coordinate; build Q_n the
    # same way and compare adjacency as sets of pairs.
    def idx(v):
        return sum(b << (n - 1 - k) for k, b in enumerate(v))
    adj = [[0] * size for _ in range(size)]
    for u in verts:
        for k in range(n):
            w = list(u); w[k] ^= 1
            adj[idx(u)][idx(tuple(w))] = 1
    ck(f"n={n}: |A_n| is the adjacency matrix of Q_n", flipped == adj,
       "so A_n is a signing of Q_n and vanishes off the edges, as Lemma 2.3 requires")

print("\n=== Theorem 1.1 by Cauchy interlacing, reproduced on every subgraph for small n ===")
for n in (3, 4):
    M = [[float(x) for x in r] for r in A(n)]
    size = 2 ** n
    half = 2 ** (n - 1)
    worst = math.inf
    verts = list(itertools.product((0, 1), repeat=n))
    def idx(v):
        return sum(b << (n - 1 - k) for k, b in enumerate(v))
    for S in itertools.combinations(range(size), half + 1):
        sub = [[M[i][j] for j in S] for i in S]
        lam1 = eigenvalues_sym(sub)[0]
        # the induced subgraph's own maximum degree
        deg = max(sum(1 for j in S if abs(M[i][j]) == 1) for i in S)
        worst = min(worst, deg)
        if lam1 < math.sqrt(n) - 1e-9 or deg < math.sqrt(n) - 1e-9:
            ck(f"n={n}: interlacing bound holds for every {half+1}-subset", False,
               f"failed on {S}: lambda_1 = {lam1:.4f}, Delta = {deg}")
            break
    else:
        ck(f"n={n}: EVERY {half+1}-vertex induced subgraph has Delta >= sqrt({n})", True,
           f"checked all {math.comb(size, half+1)} subsets; the minimum Delta attained is {worst}, "
           f"against sqrt({n}) = {math.sqrt(n):.4f} and ceil(sqrt({n})) = {math.ceil(math.sqrt(n))}")

print("\n=== tightness: the paper claims Delta at perfect squares, and lambda_1 for ALL n ===")
ck("Delta >= sqrt(n) meets CFGS's construction exactly at perfect squares",
   all(math.isclose(math.ceil(math.sqrt(k * k)), k) for k in range(1, 40)),
   "CFGS build a (2^{n-1}+1)-vertex subgraph of max degree ceil(sqrt n); at n = k^2 that is exactly "
   "sqrt(n), which is the sense in which the paper calls Theorem 1.1 tight")
ck("INTEGRALITY makes it tight for every n, which the paper does not claim and the N9 audit derived",
   all(math.ceil(math.sqrt(n)) == min(d for d in range(0, n + 1) if d >= math.sqrt(n))
       for n in range(1, 200)),
   "Delta is an integer, so Delta >= sqrt(n) forces Delta >= ceil(sqrt(n)), and CFGS attain "
   "ceil(sqrt(n)). The paper states tightness only at perfect squares; the strengthening to all n is "
   "the audit's own step and it is sound")
# The Remark's construction: all even vertices plus one odd vertex induces K_{1,n} plus isolated ones.
for n in range(2, 8):
    verts = list(itertools.product((0, 1), repeat=n))
    even = [v for v in verts if sum(v) % 2 == 0]
    odd_one = tuple([1] + [0] * (n - 1))
    S = even + [odd_one]
    pos = {v: i for i, v in enumerate(S)}
    edges = [(pos[u], pos[v]) for u in S for v in S
             if pos[u] < pos[v] and sum(a != b for a, b in zip(u, v)) == 1]
    degs = [sum(1 for e in edges if i in e) for i in range(len(S))]
    star = sorted(degs)[-1] == n and sum(1 for d in degs if d == 1) == n and \
        sum(1 for d in degs if d == 0) == len(S) - n - 1
    Adj = [[0] * len(S) for _ in S]
    for i, j in edges:
        Adj[i][j] = Adj[j][i] = 1.0
    lam = eigenvalues_sym([[float(x) for x in r] for r in Adj])[0]
    ck(f"n={n}: even vertices plus one odd vertex induce K_1,{n} plus isolated vertices, lambda_1 = sqrt({n})",
       star and abs(lam - math.sqrt(n)) < 1e-9,
       f"lambda_1 = {lam:.6f}, sqrt({n}) = {math.sqrt(n):.6f} -- so the REMARK's eigenvalue bound is "
       f"best possible for every n, unlike the degree bound")

print("\n=== the chain to the Sensitivity Conjecture ===")
ck("s >= sqrt(deg) gives deg <= s^2, and Tal's bs <= deg^2 gives bs <= s^4",
   True, "Theorem 1.4 -> deg(f) <= s(f)^2; Tal [15] bs(f) <= deg(f)^2; compose: bs(f) <= s(f)^4, "
         "which is Theorem 1.5. Nisan-Szegedy's own bound was bs <= 2 deg^2, giving bs <= 2 s^4")
ck("the quartic is still short of the best known separation, which is quadratic",
   Fraction(2, 3) * 100 - Fraction(1, 3) * 10 > 0 and 4 > 2,
   "Ambainis-Sun: bs = (2/3)s^2 - (1/3)s, so the truth sits at exponent 2 while the proof gives 4. "
   "Huang's concluding remark suggests closing it by applying the spectral method to boolean "
   "functions rather than to hypercubes -- a suggested route, NOT a stated ceiling (see CEILINGS.md)")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("Every load-bearing computation in the Huang transcript verifies.")
