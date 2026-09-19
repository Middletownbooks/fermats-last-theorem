# Proof-protocol measurement commission (P1–P4)

A measurement project, seeded 2026-09-18 from a chat instance's response, handoff note and harness
artifact (`SOURCE-RESPONSE.md`, `HANDOFF.md`, `p2-ablation/reference/`). It lives in this repository
for hosting only: it is not part of the Lean development, is not built by `lake`, and nothing under
`proof-protocol/` is imported by `FinalCheck.lean`.

## Status in one line

**Two things have been measured, and both were negative.** Read `MEASUREMENTS.md` first. Everything
else here is an instrument, not a result.

| | measured | result |
|---|---|---|
| **Step D** | label κ over the five transformations | **κ = 0.048.** The vocabulary is not operational. Settled. |
| **L2** | blind re-encoding, 5 cases | **2 of 5** leading leak mechanisms agree, but **6 of 7** are named somewhere. The leak field does not reproduce; `bound` does (3 of 4). |
| **D20** | two-field κ, 3 blind raters | fields reproduce (**+0.811**, **+0.755**); the **rule** built on them does not, at +0.618 [+0.220, +0.904]; the zero-false-positive claim **failed**. |
| **Baseline** | rule-less rater vs the diagnostic | the rater scores **J = 1.000** against the diagnostic's **0.607** — lift **−0.393** — with **11/11 recognition**. |
| **N9 audit** | adversarial attack on the flagship claim | **broken.** The feasible set is not closed under the product, the label is split-dependent, and the verdicts are reproduced by a simpler bound-strength test. Case 1 and N9 leave the domain. |

> ### The result that reframes everything else
>
> **The retrospective arm is saturated by recall.** A rater with no rule, given the same item,
> separates positives from twins perfectly, and names every problem while doing it. So no
> retrospective 2×2 in this tree measures whether a diagnostic *works* — only whether it is
> self-consistent, against a baseline that beats it. `p1-retrodiction/prospective/` is now not one
> instrument among several; it is the only one. See `p3-taxonomy/BASELINE.md`.
>
> **One partial answer, found while sourcing a control.** A *ceiling statement* — practitioners
> saying in print, before the outcome exists, that their board cannot reach the known truth, with
> a number on both sides — is the one retrospective structure whose label is not our own
> hindsight. Two are registered in `p1-retrodiction/CEILINGS.md`, one of them still open. Two
> items are an instrument, not a measurement, and the register is kept strictly separate from the
> prospective arm's counts.
>
> **And a number for the other route.** `p1-retrodiction/PAIRS.md`: five contemporaneous
> within-problem pairs scored perfectly would clear α = 0.05, eight would survive one miss, and
> one is in hand. Four candidates are ranked with what each needs and how each might fail.

| Part | What it is | State |
|---|---|---|
| **P1** | Retrodiction benchmark: 13 cases, **20 negative twins**, **3 controls**, 3 calibration exclusions | Encoded as data. Cases 2, 5, 8, 9 **corrected**. Citation state is generated in `CITATIONS.md`; **the last unsourced control is closed** (15, at primary tier), and control 16 arrived with the case 7 split. **Still single-encoder**; L2 found real errors but its own κ was never measured. |
| **P2** | Template-ablation study: 20 arms, planted-truth battery, two judges | Ported, fidelity-tested against the artifact's own JavaScript, and **one defect in the published instrument found and fixed** (`p2-ablation/DEFECTS.md`). Repo corpus R1–R6 swapped in with machine-verified ground truths. **Never run against a live model — no API key here.** |
| **P3** | The diagnostic | The five-transformation catalogue is **dead** (κ = 0.048). Rebuilt on the fields that reproduce: `p3-taxonomy/DIAGNOSTIC.md`. Zero false positives over 14 negatives, and one principled false negative that splits the catalogue. |
| **P4** | The v3 prescription | **Still deliberately unwritten.** |

### The one test that would settle the rebuild

The rebuilt diagnostic's only judgement calls are two closed-vocabulary fields, `target_law` and
`bound_law`. Have raters who have not seen the rules assign them blind and compute κ against the
measured **0.048** baseline. That is debt **D20**, and it is a smaller experiment than a full
re-encoding.

## What each directory is

~~~
p1-retrodiction/    cases/ twins/ controls/ calibration/  — the before-boards a scored agent may see
                    heldout/                              — after-boards and labels. NEVER shown to a scored agent.
                    schema/                               — JSON Schema for both halves
                    tools/                                — validate.py, pack.py, kappa.py
p2-ablation/        blocks.py arms.py outcomes.py ...     — the harness, ported from the browser artifact
                    tests/                                — including a differential test against the original JavaScript
                    analysis/                             — the pre-registered analysis (mixed-effects, not the harness's own intervals)
                    reference/                            — the original artifact, preserved verbatim
p3-taxonomy/        taxonomy.json                         — the five transformations, two of them unnamed
DEBTS.md debts.json                                       — every recalled citation and unverified claim, as data
~~~

## The one structural rule

`p1-retrodiction/heldout/` holds the answers. A scored agent must never see it.
`tools/pack.py` is the only supported way to build what an agent is shown; it reads `cases/` and
refuses to open `heldout/` at all. `tools/validate.py` fails the tree if an after-board string
appears in a before-board, or if a before-board cites a source dated on or after its superseding
paper. Run both before any scoring round:

~~~sh
python3 proof-protocol/p1-retrodiction/tools/validate.py
python3 proof-protocol/p1-retrodiction/tools/pack.py --id 01-sensitivity
~~~

## Task status

| # | Task | State |
|---|---|---|
| 1 | Verify the citation layer | **Three passes done; counts are generated, not typed** — see the *Current state* table in `CITATIONS.md` (from `tools/citation_status.py`). Two errors found and one claim dropped as unsourced; both reclassifications adjudicated; **one row is still UNVERIFIED** (`C1-gotsman`). Every egress route is blocked for the whole session, so every primary-tier closure came from a pasted transcript: C3, C7, C9, N3, C15. |
| 2 | Fix and port the harness | **Done.** DEFECT-1 fixed and recorded; fidelity test runs the artifact's own JavaScript; non-repeating placebos; two judge families; exact arithmetic in code. |
| 3 | Replace the battery's weakest items | **Corpus in, ground truths machine-verified. Pilot not run** — no API key here, so the retirement list is a labelled prediction. |
| 4 | Rebuild the diagnostic on fields that reproduce | **Done.** `p3-taxonomy/DIAGNOSTIC.md`. |
| 5 | Grow the negative twins | **8 → 20**, and — more importantly — **6 of the 8 "standard" twins verified**, leaving 2 declared. Every twin now carries a re-check date. One candidate rejected and recorded. |
| 6 | Pre-register the analysis | **Done**, with the defining relation `I = ABCE = BCDF = ADEF` verified computationally and the alias groups listed. |
| 7 | Start the prospective arm | **Done.** Five sealed predictions; blinding is structural. Resolution procedure now written, `resolve` gated on seal verification, not-applicable rate promoted to a first-class number (**20%**). |
| 8 | Re-run L2 properly | **Instrument built** — all four design fixes. Deliberately **not run**: D20 was the cheap version of the same question and its answer is split. |
| — | **D20** closed | Inputs, three filled rater sheets and verbatim output in `p3-taxonomy/d20/`. Provenance disclosed in `d20/PROVENANCE.md` — **not a fresh run**. |
| — | **Baseline** run | `p3-taxonomy/BASELINE.md`. The finding above. |
| — | **D9** closed | `p3-taxonomy/D9-ADJUDICATION.md`. The E5(b) replacement is **dropped**, not rescued. |
| — | **Cost estimate** | `p2-ablation/analysis/cost_estimate.txt`. Full study ≈ **$109**, and it *reaches* its power target. Budget was never the constraint; the design effect from having few problems is. |
| — | **Prediction ledger** | `LEDGER.md`. 19 predictions, 16 settled: **4 correct, 5 partly, 7 wrong**. |

## Do not do

1. No v3 before P2 data exists.
2. **No sixth transformation, and no rescue of the five.** κ = 0.048 was measured on the catalogue
   that exists; its problem is not that it is too small.
3. No harness results with judge κ below ~0.6 without reading transcripts first.
4. Never score the three calibration items.
5. **Never interpret a two-way interaction** in the P2 factorial. The aliases are verified and listed.
6. No unregistered collapse to rescue a failed prediction.
7. Do not reuse L2's original five blind encodings; they would contaminate new raters.
8. Do not log a prospective prediction after glancing at a method section.

## The repo corpus (previously blocked, now closed)

The six real-failure battery items **arrived** and are in `p2-ablation/battery_repo_corpus.json`.
Every checkable number in their ground truths was verified by exact computation before anything was
wired to them (`p2-ablation/tools/verify_corpus.py`): 48 counterexamples below 400, 8,977 primes
with M ≡ 1 mod 3 throughout, zero mismatches over q = 1..800, and an explicit verified counterexample
for the sieve item. All six check out as supplied.

`python3 cli.py battery --swap-in-corpus` swaps them in and retires six textbook items by a stated
rule. **That retirement list is a prediction, not a measurement** — the pilot needs an API key this
container does not have.

## Provenance and confidence tags

Inherited from the seed, and preserved per claim wherever a claim is encoded:

- `[R]` reasoned — argued in the seed, not measured.
- `[A]` assumed.
- `[K]` recalled from literature and **not re-fetched**. Every `[K]` is a row in `debts.json`.
- `[M]` measured — used nowhere yet. Nothing in this tree has earned it.
