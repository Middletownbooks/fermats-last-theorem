# Prediction ledger

*Generated from `ledger.json` by `tools/render_ledger.py`. As of 2026-09-18.*

Every prediction this programme has made, and how it turned out. MEASUREMENTS.md records what was measured; this records what was EXPECTED, so the next instance's judgement is calibratable instead of confident. Rendered to LEDGER.md by tools/render_ledger.py.

## Calibration

| status | n |
|---|---|
| correct | 4 |
| partly | 5 |
| wrong | 7 |
| unscored | 2 |
| open | 1 |
| **total** | **19** |

**16 of 19 predictions are settled.** Of those, **4 correct, 5 partly, 7 wrong.**

By author:

- **seed** — 10 predictions, 9 settled, 2 wrong
- **this session** — 8 predictions, 6 settled, 4 wrong
- **L2** — 1 predictions, 1 settled, 1 wrong

## The predictions

| id | by | predicted | outcome | status |
|---|---|---|---|---|
| `P-01` | seed | Transformations #3 and #5 are probably artefacts of the originating trio; the catalogue should shrink before it grows. | correct, and understated. Step D measured label kappa = 0.048 across ALL FIVE entries, not just two. The vocabulary is not operational. | **correct** |
| `P-02` | seed | Forced-choice discrimination fails as a contamination control because it is still solved by recognition. | correct, three times over. Recognition measured at 100% (step D), 5 of 5 (L2), and 13 of 13 (the rule-less baseline). | **correct** |
| `P-03` | seed | L4: anonymisation will fail on famous cases at any abstraction level that still permits computing the diagnostic. Only a prospective arm gives a clean estimate. | correct. The rule-less baseline named every one of 13 problems from a deliberately abstracted description and scored PERFECTLY (J = 1.000). | **correct** |
| `P-04` | seed | De-tensorize, as stated, is the right shape. | wrong. It fires the opposite way on cases 2 and 3, and the seed itself caught this in its own P3 pass. | **wrong** |
| `P-05` | seed | Product-law matching should replace de-tensorize. Flagged by the seed itself as circular: derived from the cases it was scored on. | partly. Restated leak-free it separates positives from twins (J = 0.675 against chance J = 0), but it LOSES to a rule-less rater by 0.325, and it takes a false positive on N8 that exposed a domain defect. | **partly** |
| `P-06` | seed | Against E5(b): the better discriminator is whether the existence guarantee is strictly cheaper than the target. Flagged n = 3 and the same circularity. | scored. The ORIGINAL criterion is refuted as a disqualifying condition (2 of 10 successes had existence-theorem moves) but untestable as a discriminator, because all P1 cases are successes. The REPLACEMENT is DROPPED: no metric for 'cheaper' is stated, so it is not computable — the same standard that dropped auxiliary-witness lift. | **wrong** |
| `P-07` | seed | Many of the 15 textbook battery items will hit ceiling in the pilot. | not yet scored — the pilot needs an API key. The cost estimate shows the full study is ~$109, so this is not blocked by money. | **unscored** |
| `P-08` | seed | 2 of 15 headline results (sphere packing, Kelley-Meka) were better play on an unchanged board, so the programme's hypothesis should carry that denominator. | upheld. ADJ-14 confirmed the sphere-packing reclassification from sources: Cohn-Elkies 2003 was itself the board change over Kabatyanskii-Levenshtein, and Cohn and Elkies conjectured their own board would settle dimensions 8 and 24. | **correct** |
| `P-09` | seed | Case 9 (Vinogradov): the pre-Wooley bound and the log-k-rounds leak, flagged [K, medium confidence]. | the flag was warranted but for the wrong reason. The bound is correct for the classical method; the CUTOFF DATE was wrong — Wooley is arXiv:1101.0574, posted eleven months inside it. The case was voided. | **partly** |
| `P-10` | seed | Case 5 (Kakeya): the pre-Dvir exponent, flagged as the shakiest citation. | the flag was right and the error was WORSE than flagged. Not a wrong exponent but (a) a missing regime — (n+2)/2 > 4n/7 exactly when n < 14 — and (b) a probable Euclidean/finite-field conflation, since 4n/7 is Katz-Tao's Minkowski-dimension bound. | **partly** |
| `P-11` | L2 | L2-1 (its own pre-registered prediction). | FAILED on both halves. It survives only if PARTIAL is counted with AGREE. It was scored as failed. | **wrong** |
| `P-12` | this session | The rebuilt diagnostic takes zero false positives over eight negatives. | WRONG, and withdrawn. Three blind raters unanimously assigned N8 max/l2 where I had additive/additive; I checked and they were right. Corrected specificity 7/8. | **wrong** |
| `P-13` | this session | Moving the judgement onto two closed-vocabulary fields will make it reproduce where the free-text leak did not. | correct on the fields: Fleiss kappa +0.811 and +0.755 against the measured 0.048 baseline. NOT correct on the rule built from them: +0.618 with CI [+0.220, +0.904]. | **partly** |
| `P-14` | this session | Implicitly, that the retrospective 2x2 measured something about the diagnostic. | WRONG. A rule-less rater scores J = 1.000 against the diagnostic's 0.675 — lift of -0.325 — with 13/13 recognition. The retrospective arm is saturated by recall and cannot measure a diagnostic's value at all. | **wrong** |
| `P-15` | this session | Six named textbook battery items will ceiling and are the right ones to retire. | not scored — no pilot. The list is labelled a prediction in battery.py and should be scored against the measured per-item rates when a key exists. | **unscored** |
| `P-16` | this session | Erdos distinct distances in R^3 is a clean negative twin because Guth-Katz does not transfer. | wrong. A search found a recent claim of N^{2/3-o(1)} in R^3. The candidate was rejected before it entered the set. | **wrong** |
| `P-17` | this session | The P2 study's budget would be the binding constraint on its power. | wrong. The full study is ~$109 and the configured design already detects 19.4 points against a 30-point target. The binding constraint is the DESIGN EFFECT from having few problems, which more runs cannot fix. | **wrong** |
| `P-18` | this session | Five sealed prospective predictions: 2607.21517 no-fire, 2609.15025 fire, 2608.14454 not-applicable, 2608.30273 no-fire, 2606.12181 fire. | open. All five await resolution. | **open** |
| `P-19` | this session | D9 could be scored mechanically once schema v2 made formula-vs-existence its own field. | half right. The original criterion became scoreable; the replacement did not, and the corpus turned out to contain no failures to score either against. | **partly** |

## What it cost

- **P-01** — none — it protected against a sixth entry being added
- **P-03** — none — and it is the finding the whole programme now rests on
- **P-04** — the entry was replaced by product-law matching, which then had its own problems
- **P-05** — one withdrawn headline claim; one new open debt (D23)
- **P-06** — the replacement is dropped rather than carried; it also exposed D26, that the corpus cannot test any success-versus-failure criterion at all
- **P-07** — none yet
- **P-09** — one of five L2 cases voided, a fifth of that sample
- **P-10** — a schema change (multi-regime bound) that turned out to be needed anyway
- **P-11** — none — scoring it honestly is what makes the rest of L2 readable
- **P-12** — one retracted headline; it exposed D23, which is worth more than the claim was
- **P-13** — none — and the field/rule gap is itself a finding
- **P-14** — every retrospective 2x2 in the tree is downgraded to self-consistency; this is the largest single correction the programme has made
- **P-15** — none; it is a free pre-registered forecast
- **P-16** — none — caught at vetting; recorded in twins/REJECTED.json so it is not re-proposed
- **P-17** — none — it redirects the fix from buying runs to enlarging the battery
- **P-18** — none yet; this is the only uncontaminated instrument in the programme
- **P-19** — none — the attempt is what surfaced D26

## Lessons

1. Every flag the seed raised about its own citations was warranted, and in two of two cases the error was WORSE than flagged. A self-flagged low-confidence claim should be treated as probably wrong, not probably imprecise.
2. Three of the four wrong predictions made this session were mine, and two were caught only by an external check — three blind raters on N8, and a rule-less rater on the baseline. Self-scoring found the vocabulary bug; it did not find either of the substantive errors.
3. The predictions that held up best were the seed's about CONTAMINATION. The ones that failed worst were everyone's about DIAGNOSTIC VALUE. That asymmetry is the programme's central result so far: it is much easier to establish that a measurement is confounded than to establish that a procedure helps.
4. No prediction in this programme has yet been settled by a retrospective 2x2. They were settled by a dating check, an arithmetic check, a unanimous rater disagreement, and a baseline.
5. Twice now a criterion has been dropped for the same reason: no computable diagnostic (auxiliary-witness lift, and the E5(b) replacement). Both were phrased as insights rather than as procedures. A criterion that cannot say what it reads off the page is not a criterion, and the catalogue has shrunk from five transformations plus two proposals to two tested rules.
