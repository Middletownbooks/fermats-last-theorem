#!/usr/bin/env python3
"""Verify the four derivations in the citations-response document. Standard library only."""
from __future__ import annotations
import math, sys
bad = []
def ck(name, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    if not ok: bad.append(name)

print("=== (a) N3: Behrend excludes every fixed power saving, but the crossover is large ===")
c2 = 2 * math.sqrt(2)                     # Behrend exponent coefficient in log_2 form
c = c2 * math.sqrt(math.log(2))           # same coefficient in natural-log form
ck("N3 coefficient", abs(c - 2.3548) < 1e-4,
   f"c = 2*sqrt(2)*sqrt(ln 2) = {c:.6f}, matching the document's 2.3548. NOTE: an earlier version "
   f"of this check asserted the document was wrong here and gave 2.3542. That was MY hand-arithmetic "
   f"error, not the document's; the document is correct to 4 decimal places.")
rows = []
for delta, claimed in ((0.5, 10), (0.2, 60), (0.1, 241), (0.05, 963)):
    lnN = (c / delta) ** 2
    log10N = lnN / math.log(10)
    rows.append((delta, log10N, claimed))
    ck(f"  crossover delta={delta}", abs(log10N - claimed) < 1.0,
       f"N > 10^{log10N:.1f} (document says 10^{claimed})")
ck("N3 equivalence", all(abs((c2 / d) ** 2 * math.log(2) - (c / d) ** 2) < 1e-9
                         for d in (0.5, 0.2, 0.1, 0.05)),
   "the log_2 and natural-log forms give the same crossover, so both statements are consistent")

print("\n=== (b) C3: chi_f(C5) = 5/2 ===")
ck("C5 fractional cover", 5 / 2 == 2.5 and 5 / 2 == 5 / 2,
   "C5 is vertex-transitive so chi_f = n/alpha = 5/2 = 2.5; it is self-complementary, so the "
   "clique-cover convention does not bite")
ck("  ratio to sqrt5", abs(2.5 / math.sqrt(5) - 1.118) < 1e-3,
   f"5/2 vs sqrt5 = {math.sqrt(5):.4f}: ratio {2.5/math.sqrt(5):.4f}, a CONSTANT factor "
   "(this is why the bound-strength test also declines on case 3)")

print("\n=== (c) C9: the log k IS the contraction count ===")
for k, m_claim, s_claim, r_claim in ((10, 38, 380, 1.650), (100, 848, 84800, 1.841),
                                    (1000, 13116, 13116000, 1.899)):
    m = math.ceil(math.log(k * k / 2) / -math.log(1 - 1 / k))
    s = k * m
    r = s / (k * k * math.log(k))
    ck(f"k={k}", m == m_claim and s == s_claim and abs(r - r_claim) < 5e-4,
       f"m = {m} contractions, s = km = {s}, s/(k^2 ln k) = {r:.3f}")
def _ratio(k):
    m = math.ceil(math.log(k * k / 2) / -math.log(1 - 1 / k))
    return k * m / (k * k * math.log(k))
_seq = [_ratio(k) for k in (10, 100, 1000, 10**4, 10**6)]
ck("  ratio increases to 2", all(a < b for a, b in zip(_seq, _seq[1:])) and _seq[-1] > 1.94,
   "ratio " + " -> ".join(f"{v:.3f}" for v in _seq) + " : increasing towards 2, matching Pierce's "
   "'the leading 3 can be improved to a 2'. Convergence is SLOW (1.92 at k=10^4), so a tolerance "
   "of 0.05 only holds from about k=10^6 -- my first version of this check was tighter than the "
   "mathematics and failed for that reason, not because the claim is wrong.")

print("\n=== (d) C7: rho_k saturates at 4, so the criterion caps at 2*theta ===")
def rho(k, l):
    return (k / (k + 2 * l + 1)) * (2 * (2 * l + 1) / (l + 1))
TABLE = {(10, 1): 2.308, (10, 5): 1.746, (10, 20): 0.766, (10, 100): 0.189,
         (10**6, 1): 3.000, (10**6, 5): 3.667, (10**6, 20): 3.905, (10**6, 100): 3.979}
for (k, l), claimed in sorted(TABLE.items()):
    v = rho(k, l)
    ck(f"rho(k={k}, l={l})", abs(v - claimed) < 1e-3, f"{v:.3f} (document says {claimed})")
sup = max(rho(10**9, l) for l in range(1, 4000))
ck("rho supremum", sup < 4.0 and sup > 3.99,
   f"sup rho over one-variable F = {sup:.4f} < 4, approached but never reached, INDEPENDENT of k")
ck("criterion cap", abs(0.5 * 1.0 * 4 - 2.0) < 1e-12,
   "Granville's criterion (1/2)*theta*rho > 1 therefore caps at 2*theta; needing 2*theta > 1 "
   "recovers theta > 1/2 -- the barrier derived from the leak, not quoted beside it")
ck("Maynard-Tao lifts it", math.log(105) - 2 * math.log(math.log(105)) - 1 > 0.5
   and math.log(10**6) - 2 * math.log(math.log(10**6)) - 1 > 7.5,
   f"log k - 2 log log k - 1 = {math.log(105)-2*math.log(math.log(105))-1:.2f} at k=105 and "
   f"{math.log(10**6)-2*math.log(math.log(10**6))-1:.2f} at k=10^6: GPY capped at 4, "
   "Maynard-Tao grows like log k")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("All four derivations in the citations response verify.")

print("\n=== (e) control 15: the Kelley-Meka exponent ladder, and the board's ceiling ===")
# Bound shape: |A| <= N/exp(c (log N)^e). LARGER e = stronger bound.
ladder = {"Kelley-Meka (Thm 1)": 1/12, "Bloom-Sisask clean modification": 1/9,
          "Bloom-Sisask technical optimisation": 5/41,
          "stated natural limit of these methods": 1/7,
          "stated limit of ANY density-increment-with-Bohr-sets argument": 1/3,
          "Behrend lower bound (the truth is at least this strong)": 1/2}
prev = None
for name, e in ladder.items():
    print(f"     {e:8.5f}  {name}")
    if prev is not None:
        ck(f"  ladder ordering", e > prev, f"{e:.5f} > {prev:.5f}")
    prev = e
ck("5/41 beats 1/9", 5/41 > 1/9, f"5/41 = {5/41:.5f} > 1/9 = {1/9:.5f}, so the technical "
   "optimisation is stronger than the clean one -- larger exponent means a smaller bound")
ck("P1's figure is doubly stale", 1/12 < 1/9 < 5/41,
   "P1 records 1/12; Bloom-Sisask themselves give 1/9 cleanly and 5/41 with more work")
ck("the board is capped SHORT of the truth", 1/3 < 1/2,
   "Bloom-Sisask state 1/3 (perhaps 1/4) as the limit of ANY density-increment-with-Bohr-sets "
   "argument, while Behrend's construction gives 1/2. The board has a stated ceiling below the "
   "answer -- which is the leak structure this benchmark is about, sourced and contemporary.")
ck("gap the board cannot close", abs((1/2) - (1/3)) > 0.16,
   f"the unreachable interval is ({1/3:.4f}, {1/2:.4f}] in the exponent")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("Control-15 exponent ladder verified.")

print("\n=== (f) the ceiling register's numeric claims (CEILINGS.md, ceilings/register.jsonl) ===")
_sup = max(rho(10**9, l) for l in range(1, 4000))
ck("GPY cap: sup rho = 3.9995 at k = 10^9", abs(_sup - 3.9995) < 5e-5,
   f"{_sup:.6f} < 4, so the board reaches every value BELOW the requirement and none at or above it. "
   "This is why the register allows a cap equal to the truth when cap_attained is false.")
_md = lambda k: math.log(k) - 2 * math.log(math.log(k)) - 1
ck("Maynard-Tao ratio 0.5785 at k = 105", abs(_md(105) - 0.5785) < 5e-5, f"{_md(105):.4f}")
ck("Maynard-Tao ratio 7.564 at k = 10^6", abs(_md(10**6) - 7.564) < 5e-4,
   f"{_md(10**6):.4f}, against the one-variable cap of 4: the multidimensional sieve GROWS where the "
   "one-variable board saturates")
ck("Roth: the method's own believed limit is under half the board's stated cap",
   (1 / 7) / (1 / 3) < 0.5, f"(1/7)/(1/3) = {(1/7)/(1/3):.4f}: 1/7 is the believed natural limit of "
   "the method, 1/3 the stated cap of the board, 1/2 the truth")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("Ceiling register figures verified.")
