# Verification debts and the failure register

*Generated from `debts.json` by `tools/render_debts.py`. As of 2026-09-18 (second pass: step D, L2, tasks 1-8). Edit the JSON, not this file.*

## Standing caveats

- Step D measured label kappa = 0.048 and L2 measured 2-of-5 leak agreement. Both are FINISHED. See MEASUREMENTS.md before reading anything else here.
- Of P1's citation layer, 20 rows are now VERIFIED and 10 remain UNVERIFIED. See CITATIONS.md; arxiv.org, Crossref and Semantic Scholar are egress-blocked from this container, so web search was the only route and no PDF was fetched.
- arXiv:2609.11189 post-dates the seed instance's knowledge and was taken on trust; commission items E3 and E4 were taken as given.

## Debts

| id | kind | status | where | claim | what closing it takes |
|---|---|---|---|---|---|
| **D1** | citation | `unverified` | `p1-retrodiction/cases/09-vinogradov-mean-value/` | The pre-Wooley bound is s >~ c*k^2*log k, and the leak is that each congruencing iteration recovers a fixed fraction of the defect so about log k rounds are needed. | Still not fetched. Note the case is VOID for L2 purposes through the cutoff design error, so this debt no longer blocks anything downstream. |
| **D2** | citation | `resolved-as-error` | `p1-retrodiction/cases/05-finite-field-kakeya/` | The best pre-Dvir exponent was about q^{4n/7}. | CLOSED by finding the error. CITATIONS.md row C5-4n7: 4n/7 + 3/7 is Katz-Tao's EUCLIDEAN Minkowski-dimension bound; no source states it for \|K\| in F_q^n. The seed's low confidence was warranted. The two-regime structure survives; the exponent does not. |
| **D3** | citation | `verified` | `p1-retrodiction/cases/01-sensitivity/` | Chung-Fueredi-Graham-Seymour 1988 gives Delta >= (1/2 - o(1)) log n. | CLOSED. CFGS 1988 give (1/2 - o(1)) log_2 n — note base 2, which P1 left unstated — and themselves construct the matching ceil(sqrt n) example. |
| **D4** | citation | `verified` | `p1-retrodiction/twins/N4-shannon-capacity-c7.json` | Polak-Schrijver 2019 give a lower bound of about 3.258 for Theta(C7), against theta(C7) about 3.318. | CLOSED. Polak-Schrijver: 367^(1/5) > 3.2578 (IPL 143, 2019). theta(C7) = 3.3176672 computed here. Both figures confirmed. |
| **D5** | dated-fact | `verified-but-dated` | `p2-ablation/blocks.json (battery item O3)` | x^3 + y^3 + z^3 = 114 has no known integer solution and the problem is open. | Verified today: 114 is described as the lowest unsolved case. STILL A DATED FACT — re-check on the day of freezing. |
| **D6** | reclassification | `adjudicated-upheld` | `p1-retrodiction/controls/14-sphere-packing-8-24.json` | Sphere packing in dimensions 8 and 24 is NOT a board change. The board is Cohn-Elkies 2003; Viazovska supplied the terminal certificate on that board, and numerics had already shown it was tight. The actual board change was Kabatiansky-Levenshtein -> Cohn-Elkies. | CLOSED. CITATIONS.md ADJ-14. Cohn-Elkies 2003 was itself the first improvement since Kabatyanskii-Levenshtein 1978, and Cohn and Elkies themselves conjectured their board would settle dimensions 8 and 24. Supported by sources now, not argument. |
| **D7** | reclassification | `adjudicated-upheld` | `p1-retrodiction/cases/13-pcp-weak/` | PCP is demoted to fit-testing only, because its 'before' was a successful proof rather than a failing bound. | CLOSED. CITATIONS.md ADJ-13. Noted that the rebuilt diagnostic WOULD fire on it, which is evidence the item is well-formed, not that it should be scored. |
| **D8** | contested-claim | `addressed-in-part` | `p3-taxonomy/taxonomy.json -> candidate_replacements` | 'Product-law matching' should replace 'de-tensorize': compute how the target behaves on the product construction of the extremal family, and require the invariant to obey the same law. | Restated leak-free in p3-taxonomy/DIAGNOSTIC.md and tested against 13 in-domain items with zero false positives. Circularity is REDUCED, not removed: the rules are mechanical but the assignment of laws is still mine. The remaining test is D20. |
| **D9** | contested-claim | `unvalidated` | `SOURCE-RESPONSE.md, P3 item 7` | Against E5(b): the better discriminator is whether the existence guarantee is strictly cheaper than the target, not formula versus existence. Banaszczyk's move, Marcus-Spielman-Srivastava and Dvir all rest on existence statements and all succeed. | n = 3, and it has the same flaw as the criterion it replaces: derived from the cases that motivated it. |
| **D10** | contested-claim | `measured` | `p1-retrodiction/README.md -> contamination control` | Forced-choice discrimination fails as a contamination control, because it is still solved by recognition; the four-layer alternative (score the procedure, negative twins, telegraph baseline, recognition probe, prospective arm) is better. | CLOSED as a question. Step D measured 100% recognition and L2 measured 5 of 5, on encoders that were trying to comply. The seed's concern was correct and cutoff discipline does not fix it. The prospective arm (p1-retrodiction/prospective/) is the only remaining route. |
| **D11** | contested-claim | `upheld` | `p1-retrodiction/README.md -> base rate` | 2 of 15 headline results (Viazovska, Kelley-Meka) were better play on an unchanged board, so the programme's core hypothesis should carry that denominator. | D6 adjudicated in favour, so the denominator stands: 2 of 15 headline results were better play on an unchanged board. |
| **D12** | gap | `superseded` | `p3-taxonomy/taxonomy.json` | Transformations #3 and #5 have NO NAME anywhere in the seed material; they are referenced only by number. #3 is fitted weakly by one case and #5 by none. | Moot. Step D measured kappa = 0.048 on the five-entry catalogue, so the vocabulary is not operational and the entries' names no longer matter. auxiliary-witness-lift has been DROPPED; the rebuild in DIAGNOSTIC.md replaces the rest. Do not recover the names; do not add a sixth. |
| **D13** | method-limit | `acknowledged` | `p2-ablation/analysis/preregistration.md §5` | Judges cannot be blinded to arm: the protocol's own tags and the numbered return fields leak the condition into the graded text. | Record it as a limitation in the write-up. Do not describe the judges as blind. Not fixable within this design. |
| **D14** | method-limit | `acknowledged` | `p2-ablation/config.py` | Temperature cannot be controlled: sampling parameters were removed from the current Claude models and sending one returns a 400. | Report `effort` instead, which is recorded per run. Do not report temperature as held constant. This is a change in the world since the handoff was written, not an omission. |
| **D15** | missing-input | `closed` | `p2-ablation/battery.py` | Handoff task 1 - replace the weakest battery items with the repository's own real agent failures (E7 the false impossibility theorem with a published counterexample, E8 the two unsupported 'this forces that' steps, E9 the variance-1 Monte Carlo check). | CLOSED. The corpus was supplied as R1-R6 and every checkable number in its ground truths was verified by exact computation (p2-ablation/tools/verify_corpus.py): 48 counterexamples below 400, 8,977 primes, zero mismatches over q = 1..800. Swapped in via `cli.py battery --swap-in-corpus`. |
| **D16** | method-limit | `addressed-in-part` | `p1-retrodiction/` | P1 v0 is single-encoder and contaminated: one model encoded all 23 items while knowing every answer. | L2 ran on five cases and found real errors, but its own pre-registered kappa was never measured (D22) and case 9 was void. The re-run instrument with all four design fixes is built: p1-retrodiction/L2-RERUN.md. |
| **D17** | instrument-defect | `fixed-and-recorded` | `p2-ablation/DEFECTS.md` | DEFECT-1: the published harness's exportData calls outcome(r, r.j2), and outcome() opens `j = j \|\| r.j1`, so judge 2's exported column is scored from judge 1 on every row where the second judge did not run. | Fixed at the call site (the frozen rule is untouched) and pinned by tests/test_export_defect.py. Recorded as a PRE-FREEZE defect: it changes what the published instrument would have reported, and belongs in the write-up as such. |
| **D18** | not-run | `blocked` | `p2-ablation` | The pilot has not been run, so no per-item failure rate exists. | No ANTHROPIC_API_KEY and no `ant` CLI in this container. The retirement list in battery.py is a PREDICTION and is labelled one. Run `cli.py pilot` with a key and re-choose the retired items from the measured rates. |
| **D19** | citation | `unverified` | `CITATIONS.md` | Ten citation rows remain unverified: cases 4, 7, 9, 10, 11, 12, 13, twin N3, the Gotsman-Linial reduction, and Shannon's 5/2 upper bound. | Needs an environment where arxiv.org is reachable. Declared rather than assumed — none is presented as checked. |
| **D20** | the-test-that-settles-it | `open` | `p3-taxonomy/DIAGNOSTIC.md` | The rebuilt diagnostic's only judgement calls are two closed-vocabulary fields, target_law and bound_law. | Have raters who have NOT seen the rules assign those two fields blind, from the bound and the extremal construction alone, and compute kappa against the measured 0.048 baseline. kappa >= 0.6 means the judgement was moved onto a field that reproduces; below it, this is one more unreproducible ranking and must be reported as such. This is a smaller experiment than a full re-encoding and it tests the thing that matters. |
| **D21** | coverage | `partial` | `p1-retrodiction/twins/` | Twenty negatives against a target of ~25, and 8 of the 20 are STANDARD rather than fetched. | Three further candidates were dropped because their tightness could not be verified here. One candidate was REJECTED outright and recorded (twins/REJECTED.json): Erdos distinct distances in R^3 is no longer open. Twin candidates decay, so every twin needs a re-check date. |
| **D22** | unmeasured | `open` | `MEASUREMENTS.md` | L2's pre-registered kappa was never measured; the substitute 0.286 [0.000, 0.667] at n = 5 is unmeasured, not a bound. | The instrument is built (tools/make_rating_sheet.py, schema v2). Use fresh cases and fresh encoders; do NOT reuse the original five blind encodings. |

### Blocking

- **D5** blocks p2-ablation freeze.
- **D15** blocks the whole point of P2's battery.
- **D18** blocks tasks 3 and 6 both need pilot data.
- **D20** blocks any claim that the rebuild succeeded.

## Failure register

What was tried, what happened, what it cost.

| tried | outcome | cost |
|---|---|---|
| Forced-choice discrimination as the contamination control | Rejected on argument; not tested | reasoning only |
| Sphere packing as a board-change case | Reclassified as a same-board control | reasoning only |
| PCP as a scoreable case | Demoted to fit-testing only | reasoning only |
| Running P2 in chat | Impossible (no agent substrate); a browser harness was built instead | one artifact |
| Raw-API harness with token counts (in the browser) | Blocked by the published-page runtime; fell back to a sampling capability | lost O5 precision — now recovered by the Python port |
| Live integration test of the harness | Not done; logic tested against mocks only (600 simulated runs) | — |
| Controlling temperature in the Python port | Not possible: the parameter was removed from the current models | one design assumption; `effort` recorded instead |
| Sourcing the real-failure battery items from this repository | Not present here; the slot is built and empty | P2's first priority remains blocked |
| Erdos distinct distances in R^3 as a negative twin | REJECTED — a recent paper claims N^{2/3-o(1)}, so it is not open | one search; the candidate is recorded so it is not proposed again |
| Reading arXiv directly to verify citations | Egress-blocked; web search was the only route and no PDF was fetched | 10 of 33 citation rows remain unverified |
| Running the P2 pilot | No API key in the container; the battery retirement list stays a prediction | tasks 3 and 6 still lack pilot data |
| Scoring both rebuilt diagnostics against one positive-class vocabulary | Wrong table — cases 4 and 8 came out as false positives when 'the log is removable' IS the positive class. Each item now carries an explicit class field | one wrong table, caught and corrected before it was written up |

## Do not do

1. Do not write template v3 before P2 data exists. The v3 hypotheses are already encoded as arms.
2. Do not add a sixth transformation, and do not try to rescue the five. Step D measured kappa = 0.048 on the catalogue that exists; its problem is not that it is too small.
3. Do not report harness results with judge kappa below about 0.6 without reading transcripts first.
4. Do not score the three calibration items (Banaszczyk, Bansal-Jiang, Guo-Fang-Lu).
5. Do not interpret two-way interactions in the P2 factorial. The aliases are verified and listed in analysis/preregistration.md: AB=CE, AC=BE, AD=EF, AE=BC=DF, AF=DE, BD=CF, BF=CD.
6. Do not rescue a failed prediction with an unregistered collapse. L2's prediction L2-1 failed on both halves and survives only if PARTIAL is counted with AGREE; it was scored as failed. Keep that standard.
7. Do not treat P1's numbers as verified beyond the 20 rows CITATIONS.md marks VERIFIED.
8. Do not reuse L2's five original blind encodings in a re-run; they would contaminate new raters.
9. Do not log a prospective prediction after glancing at a method section. One unsealed prediction and that arm is worth no more than the retrospective cases.
