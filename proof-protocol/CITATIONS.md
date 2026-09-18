# Citation verification (task 1)

*Generated from `citations.json` by `tools/render_citations.py`. As of 2026-09-18.*

## What could be checked, and what could not

> arxiv.org, export.arxiv.org, api.crossref.org and semanticscholar were EGRESS-BLOCKED from this container; direct curl and WebFetch to arxiv both failed. Web search was the only route, so every row below is verified against secondary sources and abstracts reached through search, not against a fetched PDF. Rows marked COMPUTED were checked by arithmetic here and need no source.

**Standard applied.** A claim is VERIFIED only if a source reached this session states it. Where the source could not be reached, the row says UNVERIFIED rather than accepting the claim.

## Summary

| status | rows |
|---|---|
| VERIFIED | 20 |
| UNVERIFIED | 10 |
| CORRECTED | 1 |
| DISPUTED | 1 |
| PARTIAL | 1 |
| **total** | **33** |

## Rows that changed a claim

These are the ones downstream work must read instead of P1's original.

### C2-batemankatz — CORRECTED

**Where.** `case 2 bound_then`

**Claim as written.** n^{1+eps} (Bateman-Katz 2012)

**What the source says.** Bateman-Katz prove any cap set in F_3^N has size at most C * 3^N / N^{1+eps}.

**Correction.** P1 writes the bound as 'n^{1+eps}', dropping the 3^n. In a column whose neighbouring entry is '3^n/n', that reads as a bound OF SIZE n^{1+eps} rather than a denominator. It is shorthand that becomes an error in context. Field corrected to 3^n/n^{1+eps}.

*Source:* arXiv:1101.5851; JAMS 25(2), 2012

### C5-4n7 — DISPUTED

**Where.** `case 5 bound_then, high-dimensional regime`

**Claim as written.** later about q^{4n/7}

**What the source says.** Katz-Tao 2002 prove a lower bound of 4n/7 + 3/7 on the MINKOWSKI DIMENSION of Kakeya sets in R^n — the EUCLIDEAN problem. The finite-field high-dimensional improvements over (n+2)/2 exist but are not stated anywhere reached this session as an exponent 4n/7 for |K| in F_q^n.

**Correction.** P1 appears to import a Euclidean Minkowski-dimension exponent into a finite-field cardinality bound. The two-regime STRUCTURE that L2 established survives — there is a low-dimensional geometric bound and a high-dimensional arithmetic improvement — but the specific exponent 4n/7 is not verified for F_q^n.

**Consequence.** The n < 14 crossover computed in tools/check_corrections.py is correct AS ARITHMETIC on the two exponents as P1 writes them. If 4n/7 is not the right finite-field exponent, the crossover POINT is an artefact of a misattributed bound, even though the two-regime finding that motivated the schema change does not depend on it. This is the second independent error found in case 5, after the ordering error L2 found.

*Source:* Katz-Tao 2002; Mockenhaupt-Tao arXiv:math/0204234; survey arXiv:2512.09397

## All rows

| id | where | status | claim as written | what the source says |
|---|---|---|---|---|
| `C1-bound` | case 1 bound_then | **VERIFIED** | Delta >= (1/2 - o(1)) log n (Chung-Fueredi-Graham-Seymour 1988) | CFGS 1988 prove that an induced subgraph of Q^n on more than 2^{n-1} vertices has max degree at least (1/2 - o(1)) log_2 n. J. Combin. Theory Ser. A 49(1), 180-187. |
| `C1-after` | case 1 after-board | **VERIFIED** | Huang: signed adjacency with A^2 = nI, interlacing, lambda_1 <= Delta, giving sqrt(n) | Huang 2019 proves every (2^{n-1}+1)-vertex induced subgraph of Q^n has max degree at least sqrt(n), resolving the Sensitivity Conjecture. |
| `C2-meshulam` | case 2 bound_then | **VERIFIED** | 3^n/n (Meshulam 1995) | Meshulam 1995 proved an upper bound of O(3^n/n) for cap sets in F_3^n. |
| `C2-batemankatz` | case 2 bound_then | **CORRECTED** | n^{1+eps} (Bateman-Katz 2012) | Bateman-Katz prove any cap set in F_3^N has size at most C * 3^N / N^{1+eps}. |
| `C2-after` | case 2 after-board | **VERIFIED** | slice rank gives about 2.756^n | Ellenberg-Gijswijt bound the largest cap in F_3^n by O(2.756^n); the exact constant is 3(207+33*sqrt 33)^{1/3}/8. |
| `C3-theta` | case 3 after-board | **VERIFIED (COMPUTED)** | theta(C5) = sqrt 5 | COMPUTED: theta(C_n) = n cos(pi/n)/(1+cos(pi/n)); at n=5 this equals sqrt(5) = 2.2360679774998 to machine precision. |
| `C3-shannon` | case 3 bound_then | **UNVERIFIED** | sqrt 5 <= Theta <= 5/2 (Shannon 1956) | Not separately confirmed this session. |
| `C5-wolff` | case 5 bound_then, low-dimensional regime | **VERIFIED** | \|K\| >~ q^{(n+2)/2} | The finite-field benchmark is \|F\|^{(n+2)/2} for Besicovitch sets, with arithmetic improvements available in dimensions 5 and higher (Katz-Tao; Mockenhaupt-Tao 2004). |
| `C5-4n7` | case 5 bound_then, high-dimensional regime | **DISPUTED** | later about q^{4n/7} | Katz-Tao 2002 prove a lower bound of 4n/7 + 3/7 on the MINKOWSKI DIMENSION of Kakeya sets in R^n — the EUCLIDEAN problem. The finite-field high-dimensional improvements over (n+2)/2 exist but are not stated anywhere reached this session as an exponent 4n/7 for \|K\| in F_q^n. |
| `C5-after` | case 5 after-board | **VERIFIED** | Dvir: \|K\| >= q^n/n! | Dvir 2008 proves a Kakeya set in F_q^n has size at least q^n/n!, by finding a low-degree polynomial vanishing on a small K and deriving a contradiction from the lines it contains. |
| `C6-after` | case 6 after-board | **VERIFIED** | Elekes-Sharir lift plus polynomial partitioning, giving N/log N | Guth-Katz prove N points in R^2 determine at least cN/log N distinct distances, following the Elekes-Sharir set-up (distances to rigid motions to point-line incidences in space) with a polynomial ham-sandwich cell decomposition. |
| `C8-bound` | case 8 bound_then | **VERIFIED** | sqrt(n log n) from uniform random colouring | A random colouring achieves discrepancy Theta(sqrt(n log n)) with high probability. |
| `C8-after` | case 8 after-board | **VERIFIED** | entropy / partial colouring, giving 6 sqrt n | Spencer 1985: for any 0/1 matrix A with n rows and n columns there is x in {-1,1}^n with \|\|Ax\|\|_inf <= 6 sqrt n. |
| `N8` | twin N8 | **VERIFIED** | sqrt(n log(m/n)) is tight, so the log is only partially removable | Spencer's theorem gives discrepancy O(sqrt(n log(m/n + 2))) for m sets on n points. |
| `N1` | twin N1 | **VERIFIED** | dimension log n / eps^2 is proven tight (Larsen-Nelson 2017) | Larsen-Nelson prove any embedding preserving pairwise distances to 1+eps needs m = Omega(eps^{-2} log n), matching JL, and for general (not merely linear) maps. |
| `N2-tight` | twin N2 | **VERIFIED** | tight in general (Komlos-Pach-Woeginger 1992) and for halfspaces in R^4 (Pach-Tardos 2013) | KPW 1992 give almost tight bounds on abstract hypergraphs. Pach-Tardos construct a set system from points in R^4 cut by halfspaces where every eps-net has size at least (1/(9 eps)) log(1/eps). |
| `N2-removable` | twin N2 | **PARTIAL** | removable for halfspaces in R^3 and discs (Matousek-Seidel-Welzl) | O(1/eps)-size nets for halfspaces in R^3 are confirmed (Har-Peled-Kaplan-Sharir, 'eps-Nets for Halfspaces Revisited'), but the attribution to Matousek-Seidel-Welzl was not directly confirmed. |
| `N4` | twin N4 | **VERIFIED** | theta(C7) ~ 3.318 against a lower bound ~3.258 (Polak-Schrijver 2019) | Polak-Schrijver give an independent set of size 367 in the fifth strong power of C7, so Theta(C7) >= 367^{1/5} > 3.2578. COMPUTED here: 367^{1/5} = 3.2578659..., and theta(C7) = 7cos(pi/7)/(1+cos(pi/7)) = 3.3176672.... |
| `N5` | twin N5 | **VERIFIED** | the eps^2 vs eps loss is real even for unique games (Raz 2008, odd-cycle game) | Raz constructs, for every 0 < eps <= 1/2, a game of value <= 1-eps whose n-fold parallel repetition has value >= (1-eps^2)^{O(n)}. The odd cycle game is simultaneously a projection, unique and XOR game, so this settles most variants negatively. |
| `N6` | twin N6 | **VERIFIED** | the answer is n^{1/4}, tight (Roth 1964; Matousek-Spencer 1996) | The discrepancy of arithmetic progressions in [n] is Theta(n^{1/4}): Roth 1964 for the lower bound, Matousek-Spencer 1996 for the matching upper bound by the entropy method. |
| `N7` | twin N7 | **VERIFIED** | R^3 was resolved by a different multi-scale route (Wang-Zahl 2025) | Wang-Zahl, February 2025, 127 pages: every Kakeya set in R^3 has Hausdorff and Minkowski dimension 3. The route is a multiscale analysis of grainy tube configurations, building on their 2022 sticky-Kakeya work — not Dvir's polynomial method. |
| `C14` | control 14 | **VERIFIED** | the board is Cohn-Elkies 2003; the actual board change was Kabatiansky-Levenshtein -> Cohn-Elkies | Cohn-Elkies 2003 gave the first improvement in each dimension since Kabatyanskii-Levenshtein 1978, were the best bounds known for dimensions 4 through 36, and THE AUTHORS THEMSELVES CONJECTURED their approach would settle dimensions 8 and 24. |
| `C15` | control 15 | **VERIFIED** | Kelley-Meka stayed on the density-increment board, giving exp(-c log^{1/12} N) | Kelley-Meka: a 3AP-free A in [N] has \|A\| <= exp(-c (log N)^{1/12}) N. |
| `O3` | battery item O3 | **VERIFIED AS OF 2026-09-18** | x^3 + y^3 + z^3 = 114 is still open | 114 is described as the lowest unsolved case; all n < 100 have known representations after Booker-Sutherland settled 33, 42 and 3, and 114 and 390 remain unsolved with searches ongoing. |
| `C4` | case 4 | **UNVERIFIED** | Weaver KS_2 needs delta <~ 1/log n; MSS interlacing families | Not checked this session. |
| `C7` | case 7 | **UNVERIFIED** | GPY needs theta > 1/2; Bombieri-Vinogradov gives exactly 1/2; Zhang and Maynard after-boards | Not checked this session. |
| `C9` | case 9 | **UNVERIFIED** | s >~ c k^2 log k classical; Wooley efficient congruencing | Not checked this session. The case is void for L2 purposes anyway, through the cutoff design error. The arXiv id 1101.0574 and its 2011-01-03 posting date are taken from the task list and were not independently confirmed here. |
| `C10` | case 10 | **UNVERIFIED** | Fortnow/Feige counterexamples; Raz 1995 and Holenstein 2007 after-boards | Not checked this session. Raz 2008 (N5) was checked and is a different paper. |
| `C11` | case 11 | **UNVERIFIED** | chi <= n-2k+2 (Kneser 1955); Lovasz 1978 neighbourhood complex with Borsuk-Ulam | Not checked this session. |
| `C12` | case 12 | **UNVERIFIED** | Perelman W-entropy and reduced volume give kappa-noncollapsing | Not checked this session. |
| `C13` | case 13 | **UNVERIFIED** | Dinur 2007 graph powering plus alphabet reduction, constant-factor blow-up | Not checked this session. |
| `N3` | twin N3 | **UNVERIFIED** | Behrend excludes power savings; slice rank gives nothing in [N] | Not checked this session. N3 is load-bearing for the rebuilt diagnostic (it is the discriminator against case 2), but the diagnostic's use of it rests on the ABSENCE of a product structure on [N], which is structural and does not depend on Behrend. |
| `C1-gotsman` | case 1 state slot | **UNVERIFIED** | the Gotsman-Linial 1992 reduction | Not checked this session. |

## Refinements worth carrying

- **C1-bound** — The logarithm is base 2, which P1 leaves unstated. CFGS ALSO construct a (2^{n-1}+1)-vertex induced subgraph with max degree ceil(sqrt n) — so the sqrt(n) target came from their own matching construction, which is exactly the extremal-construction input the rebuilt diagnostic reads.
- **C2-batemankatz** — Dating: arXiv:1101.5851 was posted January 2011; JAMS published April 2012 (electronic November 2011). Under the arXiv-dating rule adopted after the case 9 error, this work dates to 2011, not 2012.
- **C2-after** — COMPUTED here: the exact constant is 2.7551046..., so 2.756 is correct as an upper bound but is not the constant itself. P1's 'approximately 2.756^n' is sound as written.
- **N2-tight** — Kupavskii-Mustafa-Pach later generalised the Pach-Tardos construction to halfspaces in R^d for every d >= 4.
- **C15** — NEW SINCE THE SEED: Bloom-Sisask improved the exponent from 1/12 to 1/9 a few months later (arXiv:2309.02353). The control's status is unaffected — both stayed on the same board — but the figure in P1 is no longer the record.

## Adjudications

The two reclassifications the seed asked to have settled. These are arguments, not citations, and are adjudicated on the record.

### ADJ-14 — Sphere packing moved from board-change to same-board control

**Verdict: UPHELD, and now supported by sources rather than argument alone**

Two facts settle it. (1) Cohn-Elkies 2003 was itself the first improvement in each dimension since Kabatyanskii-Levenshtein 1978 — so the board change in this problem is KL -> Cohn-Elkies, exactly as the seed reclassified it. (2) Cohn and Elkies THEMSELVES conjectured that their approach would solve dimensions 8 and 24, which is the documentary form of the seed's claim that numerics had already shown the board was tight. Viazovska supplied the certificate on a board that was known to be right. As a control this item tests for false board-change alarms, and the rebuilt diagnostic correctly does not fire on it.

### ADJ-13 — PCP demoted to fit-testing only

**Verdict: UPHELD on the stated ground**

This is a definitional argument, not a citation, so it is adjudicated rather than verified. The seed's ground holds: the before-board was a SUCCESSFUL proof — parallel repetition did amplify the gap — and the defect was size blow-up n^k, not a failing bound. The benchmark scores predictions about bounds that failed, so the item does not belong among the scored positives. Noted for the record: the rebuilt diagnostic WOULD fire on it (target law additive, bound law multiplicative), which is evidence the item is well-formed, not evidence it should be scored.

## Unverified, and staying that way until someone has network access

Declaring what could not be checked is part of the deliverable.

- **C3-shannon** (`case 3 bound_then`) — sqrt 5 <= Theta <= 5/2 (Shannon 1956)
- **C4** (`case 4`) — Weaver KS_2 needs delta <~ 1/log n; MSS interlacing families
- **C7** (`case 7`) — GPY needs theta > 1/2; Bombieri-Vinogradov gives exactly 1/2; Zhang and Maynard after-boards
- **C9** (`case 9`) — s >~ c k^2 log k classical; Wooley efficient congruencing
- **C10** (`case 10`) — Fortnow/Feige counterexamples; Raz 1995 and Holenstein 2007 after-boards
- **C11** (`case 11`) — chi <= n-2k+2 (Kneser 1955); Lovasz 1978 neighbourhood complex with Borsuk-Ulam
- **C12** (`case 12`) — Perelman W-entropy and reduced volume give kappa-noncollapsing
- **C13** (`case 13`) — Dinur 2007 graph powering plus alphabet reduction, constant-factor blow-up
- **N3** (`twin N3`) — Behrend excludes power savings; slice rank gives nothing in [N]
- **C1-gotsman** (`case 1 state slot`) — the Gotsman-Linial 1992 reduction
