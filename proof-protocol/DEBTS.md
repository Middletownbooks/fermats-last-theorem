# Verification debts and the failure register

*Generated from `debts.json` by `tools/render_debts.py`. As of 2026-09-18. Edit the JSON, not this file.*

## Standing caveats

- All P1 citations were RECALLED by the seed instance, not fetched. Every sources_before entry in p1-retrodiction/ carries verified: false. Treat the whole citation layer as unverified, not just the rows singled out below.
- arXiv:2609.11189 post-dates the seed instance's knowledge and was taken on trust; commission items E3 and E4 were taken as given.

## Debts

| id | kind | status | where | claim | what closing it takes |
|---|---|---|---|---|---|
| **D1** | citation | `unverified` | `p1-retrodiction/cases/09-vinogradov-mean-value/` | The pre-Wooley bound is s >~ c*k^2*log k, and the leak is that each congruencing iteration recovers a fixed fraction of the defect so about log k rounds are needed. | Fetch Wooley 2012 and a pre-2012 statement of the classical bound. The seed flagged both the bound and the leak as medium confidence. |
| **D2** | citation | `unverified` | `p1-retrodiction/cases/05-finite-field-kakeya/` | The best pre-Dvir exponent was about q^{4n/7}. | Fetch the pre-2008 record. The seed wrote this with low confidence. |
| **D3** | citation | `unverified` | `p1-retrodiction/cases/01-sensitivity/` | Chung-Fueredi-Graham-Seymour 1988 gives Delta >= (1/2 - o(1)) log n. | Fetch the 1988 paper and confirm the constant. |
| **D4** | citation | `unverified` | `p1-retrodiction/twins/N4-shannon-capacity-c7.json` | Polak-Schrijver 2019 give a lower bound of about 3.258 for Theta(C7), against theta(C7) about 3.318. | Fetch Polak-Schrijver 2019 and confirm both numbers. |
| **D5** | dated-fact | `unverified` | `p2-ablation/blocks.json (battery item O3)` | x^3 + y^3 + z^3 = 114 has no known integer solution and the problem is open. | RE-CHECK ON THE DAY OF FREEZING. This is a moving target: 33 and 42 both fell recently. If it has been solved, the item's type changes from open to true and its ground truth is wrong. |
| **D6** | reclassification | `unadjudicated` | `p1-retrodiction/controls/14-sphere-packing-8-24.json` | Sphere packing in dimensions 8 and 24 is NOT a board change. The board is Cohn-Elkies 2003; Viazovska supplied the terminal certificate on that board, and numerics had already shown it was tight. The actual board change was Kabatiansky-Levenshtein -> Cohn-Elkies. | Adjudicate. If this is wrong, the control set loses half its members and the 'false board-change alarm' arm of the rubric is untestable. |
| **D7** | reclassification | `unadjudicated` | `p1-retrodiction/cases/13-pcp-weak/` | PCP is demoted to fit-testing only, because its 'before' was a successful proof rather than a failing bound. | Adjudicate. The case is flagged fit-testing-only in the data and must not be scored as a prediction until this is settled. |
| **D8** | contested-claim | `unvalidated` | `p3-taxonomy/taxonomy.json -> candidate_replacements` | 'Product-law matching' should replace 'de-tensorize': compute how the target behaves on the product construction of the extremal family, and require the invariant to obey the same law. | Needs cases chosen by someone who has NOT seen the hypothesis. The seed derived it from the same cases it then scored it on. Until then it is a guess, and the seed said so. |
| **D9** | contested-claim | `unvalidated` | `SOURCE-RESPONSE.md, P3 item 7` | Against E5(b): the better discriminator is whether the existence guarantee is strictly cheaper than the target, not formula versus existence. Banaszczyk's move, Marcus-Spielman-Srivastava and Dvir all rest on existence statements and all succeed. | n = 3, and it has the same flaw as the criterion it replaces: derived from the cases that motivated it. |
| **D10** | contested-claim | `unvalidated` | `p1-retrodiction/README.md -> contamination control` | Forced-choice discrimination fails as a contamination control, because it is still solved by recognition; the four-layer alternative (score the procedure, negative twins, telegraph baseline, recognition probe, prospective arm) is better. | Argued, not validated. The seed states that the prospective arm is the only fully clean estimate. Nothing has been measured. |
| **D11** | contested-claim | `open` | `p1-retrodiction/README.md -> base rate` | 2 of 15 headline results (Viazovska, Kelley-Meka) were better play on an unchanged board, so the programme's core hypothesis should carry that denominator. | Depends on D6. Small count, but the base rate is not zero. |
| **D12** | gap | `open` | `p3-taxonomy/taxonomy.json` | Transformations #3 and #5 have NO NAME anywhere in the seed material; they are referenced only by number. #3 is fitted weakly by one case and #5 by none. | Recover the names from the commission's catalogue, or drop both entries. DO NOT INVENT NAMES. Handoff task 7 says the catalogue should shrink before it grows. |
| **D13** | method-limit | `acknowledged` | `p2-ablation/analysis/preregistration.md §5` | Judges cannot be blinded to arm: the protocol's own tags and the numbered return fields leak the condition into the graded text. | Record it as a limitation in the write-up. Do not describe the judges as blind. Not fixable within this design. |
| **D14** | method-limit | `acknowledged` | `p2-ablation/config.py` | Temperature cannot be controlled: sampling parameters were removed from the current Claude models and sending one returns a 400. | Report `effort` instead, which is recorded per run. Do not report temperature as held constant. This is a change in the world since the handoff was written, not an omission. |
| **D15** | missing-input | `blocked` | `p2-ablation/battery.py` | Handoff task 1 - replace the weakest battery items with the repository's own real agent failures (E7 the false impossibility theorem with a published counterexample, E8 the two unsupported 'this forces that' steps, E9 the variance-1 Monte Carlo check). | Those artifacts are NOT in this repository, which is the Lean Fermat's Last Theorem development. Supply them as a JSON file and load with battery.load(extra_path=...). Until then the battery is textbook-grade and is expected to hit ceiling. |
| **D16** | method-limit | `acknowledged` | `p1-retrodiction/` | P1 v0 is single-encoder and contaminated: one model encoded all 23 items while knowing every answer. | Handoff task 2, the blind re-encoding, is the cheapest thing that makes any P3 number mean anything. The tree and tools are ready for it; it has not been run. |

### Blocking

- **D5** blocks p2-ablation freeze.
- **D15** blocks the whole point of P2's battery.

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

## Do not do

1. Do not write v3 before P2 data exists. The v3 hypotheses are already encoded as arms: if (c) and (d) hold, v3 is a return form with about six computed-content fields and the named-failure-principles block becomes a footnote.
2. Do not add a sixth transformation. #3 and #5 fit almost nothing; the catalogue should shrink before it grows.
3. Do not report harness results with judge kappa below about 0.6 without reading transcripts first.
4. Do not score the three calibration items (Banaszczyk, Bansal-Jiang, Guo-Fang-Lu). They generated the taxonomy.
5. Do not interpret two-way interactions in the P2 factorial: resolution IV aliases them with each other.
