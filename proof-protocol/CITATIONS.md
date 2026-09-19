# Citation verification (task 1)

*Generated from `citations.json` by `tools/render_citations.py`. As of 2026-09-19.*

## What could be checked, and what could not

> arxiv.org, export.arxiv.org, api.crossref.org and semanticscholar were EGRESS-BLOCKED from this container; direct curl and WebFetch to arxiv both failed. Web search was the only route, so every row below is verified against secondary sources and abstracts reached through search, not against a fetched PDF. Rows marked COMPUTED were checked by arithmetic here and need no source.

**Standard applied.** A claim is VERIFIED only if a source reached this session states it. Where the source could not be reached, the row says UNVERIFIED rather than accepting the claim.

## Summary

| status | rows |
|---|---|
| VERIFIED | 36 |
| CORRECTED | 2 |
| PARTIAL | 2 |
| UNVERIFIED | 2 |
| DISPUTED | 1 |
| SEARCH | 1 |
| **total** | **44** |

## Current state (last row per id)

The table above counts **every row ever written**, including superseded ones: 44 rows cover 41 distinct claims, because 3 ids recur (`C10`, `C12`, `C15`) where a later pass superseded an earlier row instead of rewriting it. Counting the latest row per id:

| status | claims |
|---|---|
| VERIFIED | 35 |
| CORRECTED | 2 |
| PARTIAL | 2 |
| DISPUTED | 1 |
| SEARCH | 1 |
| **distinct claims** | **41** |

**Still UNVERIFIED:** none. **Below fetched-primary tier:** `C10`, `C12`, `N2-removable`. Two VERIFIED twin rows, `N16` and `N20`, rest on STANDARD-tier claims and say so.

## Rows that changed a claim

These are the ones downstream work must read instead of P1's original.

### C2-batemankatz — CORRECTED

**Where.** `case 2 bound_then`

**Claim as written.** n^{1+eps} (Bateman-Katz 2012)

**What the source says.** Bateman-Katz prove any cap set in F_3^N has size at most C * 3^N / N^{1+eps}.

**Correction.** P1 writes the bound as 'n^{1+eps}', dropping the 3^n. In a column whose neighbouring entry is '3^n/n', that reads as a bound OF SIZE n^{1+eps} rather than a denominator. It is shorthand that becomes an error in context. Field corrected to 3^n/n^{1+eps}.

*Source:* arXiv:1101.5851; JAMS 25(2), 2012; publication data corroborated from primary (Bloom-Sisask ref [1]): J. Amer. Math. Soc. 25 (2012), no. 2, 585-613

### C5-4n7 — DISPUTED

**Where.** `case 5 bound_then, high-dimensional regime`

**Claim as written.** later about q^{4n/7}

**What the source says.** Katz-Tao 2002 prove a lower bound of 4n/7 + 3/7 on the MINKOWSKI DIMENSION of Kakeya sets in R^n — the EUCLIDEAN problem. The finite-field high-dimensional improvements over (n+2)/2 exist but are not stated anywhere reached this session as an exponent 4n/7 for |K| in F_q^n.

**Correction.** P1 appears to import a Euclidean Minkowski-dimension exponent into a finite-field cardinality bound. The two-regime STRUCTURE that L2 established survives — there is a low-dimensional geometric bound and a high-dimensional arithmetic improvement — but the specific exponent 4n/7 is not verified for F_q^n.

**Consequence.** The n < 14 crossover computed in tools/check_corrections.py is correct AS ARITHMETIC on the two exponents as P1 writes them. If 4n/7 is not the right finite-field exponent, the crossover POINT is an artefact of a misattributed bound, even though the two-regime finding that motivated the schema change does not depend on it. This is the second independent error found in case 5, after the ordering error L2 found.

*Source:* Katz-Tao 2002; Mockenhaupt-Tao arXiv:math/0204234; survey arXiv:2512.09397

### C4 — CORRECTED

**Where.** `case 4`

**Claim as written.** Weaver KS_2 needs delta <~ 1/log n; MSS interlacing families

**What the source says.** NEITHER Weaver (math/0209078) NOR Marcus-Spielman-Srivastava (1306.3969) states the threshold delta <~ 1/log n. A negative result, and the flagged remedy applies.

**Correction.** The number is DROPPED from case 4's bound_then and replaced by the sourced statement: the matrix-Chernoff / random-partition route loses a factor logarithmic in the dimension, and interlacing families remove it. Keeping a figure no source states is exactly the defect C2 and C5 already were. The diagnostic is unaffected -- case 4 fires on the LOSS, which is sourced, not the THRESHOLD, which is not.

*Source:* Weaver math/0209078; MSS 1306.3969

## All rows

| id | where | status | claim as written | what the source says |
|---|---|---|---|---|
| `C1-bound` | case 1 bound_then | **VERIFIED** | Delta >= (1/2 - o(1)) log n (Chung-Fueredi-Graham-Seymour 1988) | CFGS 1988 prove that an induced subgraph of Q^n on more than 2^{n-1} vertices has max degree at least (1/2 - o(1)) log_2 n. J. Combin. Theory Ser. A 49(1), 180-187. |
| `C1-after` | case 1 after-board | **VERIFIED** | Huang: signed adjacency with A^2 = nI, interlacing, lambda_1 <= Delta, giving sqrt(n) | Huang 2019 proves every (2^{n-1}+1)-vertex induced subgraph of Q^n has max degree at least sqrt(n), resolving the Sensitivity Conjecture. |
| `C2-meshulam` | case 2 bound_then | **VERIFIED** | 3^n/n (Meshulam 1995) | Meshulam 1995 proved an upper bound of O(3^n/n) for cap sets in F_3^n. |
| `C2-batemankatz` | case 2 bound_then | **CORRECTED** | n^{1+eps} (Bateman-Katz 2012) | Bateman-Katz prove any cap set in F_3^N has size at most C * 3^N / N^{1+eps}. |
| `C2-after` | case 2 after-board | **VERIFIED** | slice rank gives about 2.756^n | Ellenberg-Gijswijt bound the largest cap in F_3^n by O(2.756^n); the exact constant is 3(207+33*sqrt 33)^{1/3}/8. |
| `C3-theta` | case 3 after-board | **VERIFIED (COMPUTED)** | theta(C5) = sqrt 5 | COMPUTED: theta(C_n) = n cos(pi/n)/(1+cos(pi/n)); at n=5 this equals sqrt(5) = 2.2360679774998 to machine precision. |
| `C3-shannon` | case 3 bound_then | **VERIFIED** | sqrt 5 <= Theta <= 5/2 (Shannon 1956) | Shannon determined Theta(G) for all graphs on at most SIX vertices except C5, proved Theta(C5) >= sqrt5 via the explicit independent set {t(1,2) : t in Z_5}, and THE 5/2 UPPER BOUND IS HIS OWN, by what is now called the fractional clique covering number. The before-board needs no change. |
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
| `C4` | case 4 | **CORRECTED** | Weaver KS_2 needs delta <~ 1/log n; MSS interlacing families | NEITHER Weaver (math/0209078) NOR Marcus-Spielman-Srivastava (1306.3969) states the threshold delta <~ 1/log n. A negative result, and the flagged remedy applies. |
| `C7` | case 7 | **VERIFIED** | GPY needs theta > 1/2; Bombieri-Vinogradov gives exactly 1/2; Zhang and Maynard after-boards | Granville, arXiv:1410.8400v1, verifies every field verbatim or in substance: the sieve weights, the ratio criterion, two primes in the tuple, and theta > 1/2 against Bombieri-Vinogradov's exactly 1/2. |
| `C9` | case 9 | **VERIFIED** | s >~ c k^2 log k classical; Wooley efficient congruencing | Pierce, arXiv:1707.00119, confirms the classical shape and gives eta_{s,k} = (1/2)k^2(1-1/k)^{[s/k]} with s >= 3k^2(log k + O(log log k)), the leading 3 improvable to 2; Wooley's 1992 thesis gives the constant 1. Wooley's efficient congruencing is confirmed as arXiv:1101.0574, 3 January 2011, Annals 175(3) 1575-1627. |
| `C10` | case 10 | **UNVERIFIED** | Fortnow/Feige counterexamples; Raz 1995 and Holenstein 2007 after-boards | Not checked this session. Raz 2008 (N5) was checked and is a different paper. |
| `C11` | case 11 | **VERIFIED** | chi <= n-2k+2 (Kneser 1955); Lovasz 1978 neighbourhood complex with Borsuk-Ulam | Lovasz 1978 proves chi(KG(n,k)) = n-2k+2 via the neighbourhood complex: N(KG(n,k)) is (n-2k-1)-connected, and Borsuk-Ulam turns that connectivity into an obstruction to colouring. Both the Kneser 1955 upper bound and the Lovasz after-board are as P1 states them. |
| `C12` | case 12 | **UNVERIFIED** | Perelman W-entropy and reduced volume give kappa-noncollapsing | Not checked this session. |
| `C13` | case 13 | **VERIFIED** | Dinur 2007 graph powering plus alphabet reduction, constant-factor blow-up | Dinur 2007 amplifies the unsatisfiability factor by a factor of 2 per round while blowing up instance size by at most a CONSTANT factor, using a zig-zag-inspired preprocessing into a constant-degree expander, graph powering, and alphabet reduction. Exactly the P1 after-board. |
| `N3` | twin N3 | **VERIFIED** | Behrend excludes power savings; slice rank gives nothing in [N] | Peluse, arXiv:2206.10037: SALEM-SPENCER (1942) constructed 3AP-free subsets of [N] of density exp(-log N/log log N), 'showing that the true order of magnitude of r_3(N) is larger than N^{1-eps} for any fixed eps > 0'. Behrend (1946) gives the stronger, still essentially best-known Omega(N/exp(C sqrt(log N))). |
| `C1-gotsman` | case 1 state slot | **VERIFIED** | the Gotsman-Linial 1992 reduction | CLOSED FROM PRIMARY. Huang arXiv:1907.00847v2 states it as Theorem 1.3, attributed to Gotsman and Linial [9] and proved by them 'using Fourier analysis': for any MONOTONE h: N -> R, the following are equivalent -- (a) for any induced subgraph H of Q_n with \|V(H)\| != 2^{n-1}, Gamma(H) >= h(n), where Gamma(H) = max{Delta(H), Delta(Q_n - H)}; (b) for any boolean function f, s(f) >= h(deg(f)). Huang then takes h(n) = sqrt(n), 'since one of H and Q_n - H must contain at least 2^{n-1} + 1 vertices, and the maximum degree Delta is monotone'. Publication data from the same reference list: J. Combin. Theory Ser. A 61(1) (1992), 142-146. |
| `TWINS-batch2` | p1-retrodiction/twins/ | **VERIFIED** | Eight twins carried their tightness claim as STANDARD rather than fetched. | Six upgraded to verified this session: N11 (max of n Gaussians, asymptotically tight), N12 (Raab-Steger 1998, tight upper AND lower bounds), N13 (E[T] = n*H_n, verified by exact computation rather than citation), N17 (Alon-Boppana, attained by Lubotzky-Phillips-Sarnak and Margulis Ramanujan families), N18 (Szemeredi-Trotter, Elekes construction; except for the constant it cannot be improved), N19 (Sauer-Shelah, attained exactly by downward-closed systems). |
| `C10` | case 10 | **SEARCH** | Fortnow then Feige counterexamples; Raz 1995 / Holenstein 2007 after-boards | Search reaches it in substance, including the Fortnow-then-Feige ordering the row asserts (Feige-Verbitsky 2002 the simpler example), Raz's sub-exponential decay and Holenstein's simplification. The primaries are largely pre-arXiv, so a transcript is unlikely to improve it. |
| `C12` | case 12 | **PARTIAL** | Perelman W-entropy and reduced volume give kappa-noncollapsing | Bibliographic record confirmed (math/0211159, 11 Nov 2002); the cigar-soliton obstruction and the entropy-plus-reduced-distance remedy corroborated from a secondary source. |
| `C2-after-split` | heldout/02-cap-set | **VERIFIED** | P1 credited Croot-Lev-Pach and Ellenberg-Gijswijt jointly for the cap-set after-board. | Peluse: CLP proved a bound for (Z/4Z)^n (O(3.61^n), improving Sanders); EG ADAPTED THE METHOD to prove the cap-set theorem. CLP supplied the method, EG the theorem. |
| `C15` | controls/15-roth-kelley-meka.json | **VERIFIED** | Kelley-Meka stayed on the density-increment board, giving exp(-c log^{1/12} N). | CLOSED FROM PRIMARY. Bloom-Sisask arXiv:2302.07211v3 is an exposition of Kelley-Meka that breaks the argument into five steps and names the fifth 'Density increment': 'If <mu_A * mu_A, mu_C> <= 1/2, then there is an affine subspace V of codimension O(L(alpha)^4 L(gamma)^4) on which A has density at least (1 + 1/100) alpha ... This density increment condition can now be iteratively applied.' The board P1 assigns to control 15 is the one the primary source says the argument runs on. Theorem 1 is stated with exponent 1/12, as P1 records. |
| `C15-ladder` | controls/15-roth-kelley-meka.json exponent_ladder | **VERIFIED** | NEW ROW. The exponent record for r_3(N) around Kelley-Meka, largest exponent = strongest bound. | 1/12 Kelley-Meka Thm 1; 1/9 Bloom-Sisask clean modification ('the only modification required is to the almost-periodicity part'); 5/41 after technical optimisation; 1/7 'the natural limit of these methods, in that achieving anything better will require significant new ideas'; 1/3 (perhaps 1/4) the limit of any density-increment-with-Bohr-sets argument; 1/2 from Behrend's construction, which is where the truth is at least. Ordering and the two gaps checked in check_citations_response.py section (e). |
| `C15-ceiling` | controls/15-roth-kelley-meka.json board_ceiling | **VERIFIED** | NEW ROW. The density-increment board has a stated ceiling below the known truth. | Bloom-Sisask: 'an exponent of 1/3 (or perhaps even 1/4) seems to be the limit of any argument that uses any sort of "density increment" argument with Bohr sets (whether using Kelley-Meka ideas or a more traditional Fourier analytic approach)', against Behrend's 1/2. The interval (1/3, 1/2] in the exponent is, on the practitioners' own account, unreachable from this board. |
| `N3-polynomial-method` | twin N3, the load-bearing half | **VERIFIED** | N3's discriminator against case 2 is the ABSENCE of a slice-rank/polynomial-method route in [N]. Previously carried as structural reasoning, not as a sourced statement. | Bloom-Sisask state it outright: 'Unfortunately, however, there is no known analogue of the polynomial method for the integer problem, so achieving strong bounds for the integer problem via this method is out of reach.' They also give the contrast N3 needs: in F_q^n the polynomial method gives \|A\| <= q^{n-cn} (Ellenberg-Gijswijt), stronger than Kelley-Meka's q^{n-cn^{1/9}}, while over the integers the Kelley-Meka route is the one that generalises. |
| `N3-behrend-improvements` | twin N3 refinement | **VERIFIED** | The N3 refinement recorded arXiv:2406.12290 as 'the first quasipolynomial improvement to Behrend since 1946', which reads as though nothing happened in between. | Bloom-Sisask: Behrend [2] (PNAS 32 (1946), 331-332) gives exp(-c (log N)^{1/2}) N, and 'small improvements have also been established by Elkin [9] (Israel J. Math. 184 (2011), 93-128) and Green and Wolf [13] (Additive number theory, 141-144, Springer 2010)'. |
| `C1-tightness` | twin N9 (Huang tightness) and controls on the N9 audit | **VERIFIED** | NEW ROW. In what sense Huang's sqrt(n) is tight. | The paper claims two DIFFERENT tightness statements, and they differ in scope. Theorem 1.1: 'Moreover this inequality is tight when n is a perfect square' -- the degree bound meets CFGS's ceil(sqrt n) construction exactly at n = k^2. The Remark: lambda_1(H) >= sqrt(n) strengthens Theorem 1.1, and THAT inequality 'is best possible for all n', witnessed by taking all even vertices of Q_n plus one odd vertex, which induces a star K_{1,n} plus isolated vertices with lambda_1 exactly sqrt(n). Verified by construction for n = 2..7 in tools/check_huang.py. |
| `C1-chain` | case 1, the route from the cube bound to the Sensitivity Conjecture | **VERIFIED** | NEW ROW. What Huang's theorem has to be combined with to settle the conjecture. | Theorem 1.4: s(f) >= sqrt(deg(f)), which 'confirms a conjecture of Gotsman and Linial' and is tight for the AND-of-ORs function. Then bs(f) <= deg(f)^2 -- Nisan-Szegedy's bs <= 2 deg(f)^2 improved by Tal -- gives Theorem 1.5, bs(f) <= s(f)^4. Before Huang the best upper bound was EXPONENTIAL in s(f): Kenyon-Kutin's bs(f) = O(e^{s(f)} sqrt(s(f))). |

## Refinements worth carrying

- **C1-bound** — The logarithm is base 2, which P1 leaves unstated. CFGS ALSO construct a (2^{n-1}+1)-vertex induced subgraph with max degree ceil(sqrt n) — so the sqrt(n) target came from their own matching construction, which is exactly the extremal-construction input the rebuilt diagnostic reads. CONFIRMED FROM PRIMARY: Huang's introduction states CFGS's bound as '(1/2 - o(1)) log_2 n' with the base explicit, for induced subgraphs of MORE THAN 2^{n-1} vertices, and states their matching construction as a (2^{n-1}+1)-vertex induced subgraph of maximum degree ceil(sqrt n). Both halves of this row are now primary-tier, including the base-2 reading that P1 left unstated.
- **C1-after** — VERIFIED BY CONSTRUCTION, not only by citation: tools/check_huang.py builds A_n by Huang's recursion for n = 1..7 and confirms A_n^2 = nI exactly, trace 0, entries in {-1,0,1}, spectrum flat at +-sqrt(n) with multiplicity 2^{n-1} each, and that flipping the signs recovers the adjacency matrix of Q_n (which is what lets Lemma 2.3 apply). It then reproduces Theorem 1.1 exhaustively at n = 3 and n = 4: all 56 and all 11,440 (2^{n-1}+1)-vertex induced subgraphs have Delta >= sqrt(n).
- **C2-batemankatz** — Dating: arXiv:1101.5851 was posted January 2011; JAMS published April 2012 (electronic November 2011). Under the arXiv-dating rule adopted after the case 9 error, this work dates to 2011, not 2012.
- **C2-after** — COMPUTED here: the exact constant is 2.7551046..., so 2.756 is correct as an upper bound but is not the constant itself. P1's 'approximately 2.756^n' is sound as written.
- **C3-shannon** — A search snippet relayed earlier said FIVE vertices; the transcript says six. Use six. Load-bearing and it holds: case 3 is the one principled false negative precisely because chi_f is multiplicative under the strong product and merely not tight -- and chi_f(C5) = 5/2 is COMPUTED here (vertex-transitive, n/alpha), ratio 1.118 to sqrt5, a constant factor.
- **N2-tight** — Kupavskii-Mustafa-Pach later generalised the Pach-Tardos construction to halfspaces in R^d for every d >= 4.
- **C15** — NEW SINCE THE SEED: Bloom-Sisask improved the exponent from 1/12 to 1/9 a few months later (arXiv:2309.02353). The control's status is unaffected — both stayed on the same board — but the figure in P1 is no longer the record. FROM PRIMARY: the 1/9 improvement is announced in arXiv:2302.07211 ITSELF ('we will detail these improvements in a separate forthcoming note'), together with 5/41. This row credited the improvement to arXiv:2309.02353, the promised note; the announcement is earlier than that row implies.
- **C7** — Three additions. (1) The invariant's threshold is not literally 1: Prop. 6.3 gives rho(F) > 4h unconditionally, > 2h under Elliott-Halberstam. (2) bound_then named only theta, but D = [d_1,d_2] <= R^2 binds the sieve as R < x^{1/4-o(1)}, which sec. 4.2 calls 'an important barrier' -- the same barrier from two sides, and a field naming one loses the form in which it bites, exactly as case 5's single-regime field lost a dimension range. (3) Two EMPTY slots are now filled: move = Selberg's explicit formula lambda(d) = mu(d)G(log d/log R), composition = multiplicativity of omega. The leak is DERIVED: rho_k caps at 4 independent of k, so the criterion caps at 2*theta and theta > 1/2 follows.
- **C9** — The leak is now a DEMONSTRATION rather than a claim: each block of k variables multiplies the defect by a fixed fraction, so burning k^2/2 to O(1) needs ~k log(k^2/2) contractions and s ~ 2k^2 log k. THE log k IS THE CONTRACTION COUNT. Case 9 was one of only two cases where L2's encoders agreed on the leading mechanism, and this is why. D1 CLOSES.
- **N3** — The exclusion is ASYMPTOTIC and the crossover is large: N > 10^10 for delta = 0.5 but N > 10^241 for delta = 0.1 (derived and verified here). The item now says so. Also logged: arXiv:2406.12290 is the first quasipolynomial improvement to Behrend since 1946 -- it does not change N3's status, but it is the class of event that rejected the Erdos-R^3 candidate.
- **TWINS-batch2** — N16 (matrix-multiplication exponent) and N20 (Kovari-Sos-Turan) remain STANDARD and are declared so. Every twin now carries a recheck_by date, per D21 — twin candidates decay, as the rejected Erdos-R^3 candidate showed.
- **C2-after-split** — Same transcript confirms Meshulam O(3^n/n), Bateman-Katz O(3^n/n^{1+c}), Edel Omega(2.217^n), EG O(2.756^n).
- **C15** — P1's exponent 1/12 is DOUBLY STALE and the primary source says so in one paragraph: 1/9 'with a relatively clean argument', then 5/41 after 'a further tedious lengthy technical optimisation'. The control's status is unaffected -- every one of these stayed on the density-increment board -- but the figure in the item is not the record. Full ladder in row C15-ladder and in the item's exponent_ladder block.
- **C15-ladder** — TRAP RECORDED: 1/7 occurs twice in the source with different referents. Theorem 2 (the F_q^n model case) improves from 1/9 to 1/7 under the same modification; 1/7 in Theorem 1 (the integers) is the believed natural limit. Reading one for the other would put a finite-field exponent on the integer ladder.
- **C15-ceiling** — This is the benchmark's own subject matter stated by the people on the board, contemporaneously, about a live problem -- not reconstructed by us after the fact. It does NOT reclassify control 15: a stated ceiling predicts the board will have to be left, and what happened in 2023 is that it was not. Debt D32.
- **N3-polynomial-method** — This upgrades the part of N3 the rebuilt diagnostic actually leans on. The N3 row's own note said the diagnostic's use of N3 'rests on the ABSENCE of a product structure on [N], which is structural and does not depend on Behrend' -- that absence is now a quoted primary claim rather than our inference.
- **N3-behrend-improvements** — The claim N3 needs -- Behrend's shape excludes power savings, and is still essentially best-known -- is untouched: Elkin and Green-Wolf improve the lower-order factor, not the (log N)^{1/2}. But 'since 1946' needed the qualifier, and it was my phrasing that needed it, not the source's.
- **C1-tightness** — THE N9 AUDIT DERIVED MORE THAN THE PAPER STATES, and the derivation is sound. The audit concluded tightness for ALL n from integrality plus monotonicity: Delta is an integer, so Delta >= sqrt(n) forces Delta >= ceil(sqrt(n)), and CFGS attain ceil(sqrt(n)). The paper only claims the perfect-square case for Delta. So the audit's step is a strengthening of the published statement rather than a reading of it, and it should be cited as ours -- checked for n = 1..200.
- **C1-chain** — The quartic is still short of the truth: the best known separation is quadratic, bs(f) = (2/3)s(f)^2 - (1/3)s(f) (Ambainis-Sun). Huang's concluding remark suggests closing the gap 'by directly applying the spectral method to boolean functions instead of to the hypercubes'. That is a SUGGESTED ROUTE, not a stated ceiling, and CEILINGS.md records it as a rejected candidate with that reason.

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

- **C10** (`case 10`) — Fortnow/Feige counterexamples; Raz 1995 and Holenstein 2007 after-boards
- **C12** (`case 12`) — Perelman W-entropy and reduced volume give kappa-noncollapsing
