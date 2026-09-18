# Proof-protocol measurement commission (P1–P4)

A measurement project, seeded 2026-09-18 from a chat instance's response, handoff note and harness
artifact (`SOURCE-RESPONSE.md`, `HANDOFF.md`, `p2-ablation/reference/`). It lives in this repository
for hosting only: it is not part of the Lean development, is not built by `lake`, and nothing under
`proof-protocol/` is imported by `FinalCheck.lean`.

## Status in one line

**Nothing has been measured yet.** This tree converts the seed prose into data, schemas and runnable
code so that it *can* be. Every claim inherited from the seed carries its provenance and its
confidence; nothing was upgraded from "argued" to "measured" in the act of encoding it.

| Part | What it is | State |
|---|---|---|
| **P1** | Retrodiction benchmark: 13 scored cases, 8 negative twins, 2 controls, 3 calibration exclusions | Encoded as data. **Single-encoder, contaminated.** Blind re-encoding (L2) not done. |
| **P2** | Template-ablation study: 20 arms over six clause blocks, planted-truth battery, two judges | Ported to a runnable Python harness. **Never run against a live model.** |
| **P3** | Transformation taxonomy and its scoring | Encoded. Scored once by a contaminated rater. Two of five transformations have **no name in the seed material**. |
| **P4** | The v3 prescription | **Deliberately unwritten.** See "Do not do" below. |

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

## Priority order (from the handoff, unchanged)

1. **Replace the battery's weakest items with real agent failures.** Blocked here: see
   "What this repository does not contain" below.
2. **Blind re-encoding of P1 (L2).** The tree is ready for it; `tools/kappa.py` scores the diff.
   This is the cheapest thing that makes any P3 number mean anything.
3. **Port the harness to a script with a real API key.** Done — `p2-ablation/`. Four of the
   artifact's limits are lifted, one is not (see that README: temperature no longer exists on
   current models).
4. **Pre-register the analysis, not just the predictions.** Done —
   `p2-ablation/analysis/preregistration.md`. Commit it before unblinding.
5. **Verification debts.** Encoded in `debts.json`, all still `unverified`.
6. **Claims the originating instance should attack.** Encoded in `debts.json` as
   `kind: "contested-claim"`.
7. **Do not do.** No v3 before P2 data. No sixth transformation — the catalogue should shrink
   before it grows. No harness results reported with judge κ below ~0.6 without reading
   transcripts first.

## What this repository does not contain

Handoff task 1 says to replace the weakest battery items with the repository's own corpus of real
agent failures — the false impossibility theorem with a published counterexample (E7), the
unsupported "this forces that" steps behind two negative verdicts (E8), the variance-1 Monte Carlo
check (E9). **Those artifacts are not in this repository.** This is the Lean Fermat's Last Theorem
development; a search for them returns nothing. They live wherever the commission's own materials
live.

The slot is built and waiting: `p2-ablation/battery.json` is loaded through
`battery.load(extra_path=...)`, and any file matching `schema/battery-item` is merged in. Until
those three items arrive the battery is 15 textbook-grade statements, which the seed itself expects
to hit ceiling in the pilot. Treat a pilot on the current battery as a dry run of the machinery,
not as a measurement.

## Provenance and confidence tags

Inherited from the seed, and preserved per claim wherever a claim is encoded:

- `[R]` reasoned — argued in the seed, not measured.
- `[A]` assumed.
- `[K]` recalled from literature and **not re-fetched**. Every `[K]` is a row in `debts.json`.
- `[M]` measured — used nowhere yet. Nothing in this tree has earned it.
