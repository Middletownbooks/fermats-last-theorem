# P1 — Retrodiction benchmark (v0)

Does a diagnostic computed from a problem's *before*-board predict that the board had to change,
and predict how? This directory holds the boards, the answers, and the machinery that keeps them
apart.

**State: single-encoder and contaminated.** One model encoded all 23 items while knowing every
answer. Layer L2 below has not been run. Until it is, a P3 score computed on this tree measures the
encoder, not the procedure.

## Contamination control: four layers

The commission proposed forced-choice discrimination between the true move and a decoy. The seed
**rejects** that [R]: forced choice is still solved by recognition ("cap set → polynomial method"),
and decoys written by a contaminated model to be attractive-and-wrong carry a stylistic tell, so
contamination inflates discrimination nearly as much as recall. In its place:

**L1 — score the procedure, not the model.** The object under test is a diagnostic computed from
the before-board alone. Where it is mechanical ("evaluate I on a product against its factors"), a
script or a blind rater executes it, and model memory enters only through whoever encoded the case.
That relocates contamination to encoding, where it can be controlled.

**L2 — control the encoding.** *Not done.* Three requirements:
- before-boards and leak tables may cite only sources dated before the superseding paper
  (`tools/validate.py` enforces this);
- a second encoder, given only those sources, re-encodes blind; report κ on slot contents and on
  the after-board's transformation label (`tools/kappa.py`);
- **if label κ < 0.6 the five-transformation vocabulary is not operational, and that is itself the
  P3 result** — not a reason to retry until it clears.

**L3 — negative twins.** Each positive is paired, where possible, with a near neighbour showing the
same surface leak where the transformation provably fails or the factor is provably tight. On a
twin the memorised famous answer is *wrong*, so recall hurts instead of helping. Without negatives
the benchmark measures only sensitivity, and a diagnostic that always fires would score perfectly.
Decoys are real mathematics only: after-boards swapped between cases, plus documented failed
attempts.

**L4 — recognition probe and prospective arm.** After answering, the agent names the source
problem; scores are stratified by recognised against unrecognised. `tools/pack.py --anonymise`
strips names, dates and citations — the seed *expects this to fail* on famous cases at any
abstraction level that still permits computing the diagnostic [A], and says to measure it with the
probe rather than assume it. The only fully clean estimate is prospective: log the procedure's
prediction on new arXiv board-change claims **before** reading the method section.

## Contents

| Set | n | Role |
|---|---|---|
| `cases/` | 13 | Positives: historical board changes. Case 13 (PCP) is flagged `fit-testing-only` — its "before" was a successful proof, not a failing bound. |
| `twins/` | 8 | Negatives: same surface leak, but the leak is real or the famous fix does not transfer. |
| `controls/` | 2 | No board change happened. A diagnostic that fires here has raised a false alarm. |
| `calibration/` | 3 | Banaszczyk, Bansal–Jiang, Guo–Fang–Lu. **Never scored.** They generated the taxonomy. |
| `heldout/` | 13 | After-boards and labels. **Never shown to a scored agent.** |

Two reclassifications the seed made and flagged for adjudication (`../DEBTS.md`): sphere packing
moved from board-change to same-board control (the board is Cohn–Elkies 2003; Viazovska supplied
the certificate), and PCP was demoted to fit-testing only.

## Running a round

~~~sh
python3 tools/validate.py                                  # structural guard; run first, every time
python3 tools/pack.py --set mixed --seed 7 --key-out /tmp/key.json   # what the agent sees
python3 tools/pack.py --set mixed --seed 7 --telegraph     # the baseline arm
python3 tools/kappa.py template --kind labels > labels_B.json
python3 tools/kappa.py labels labels_A.json labels_B.json
~~~

`pack.py` shuffles positives, twins and controls together under opaque ids (`I01`, `I02`, …) so the
agent cannot tell a twin from a case by position, and writes the key to a separate file. It is
structurally unable to read `heldout/`.

## Rubric

- **R1 — per-diagnostic 2×2.** Fire or no-fire, computed from the before-block only, against the
  outcome label. **Report raw counts.** Positives are cases where the transformation is the
  blind-encoded label; negatives are twins where it is blocked.
- **R2 — lift.** Compare top-1 transformation choice and twin verdicts ("this leak is real")
  between procedure-equipped and table-only agents. **The procedure's score is its lift over the
  telegraph baseline, never its raw accuracy.**
- **R3 — recognition-stratified scores.**
- **R4 — encoder κ.**

## What this benchmark can and cannot detect

**Can:** diagnostics that fire on tight leaks (N1, N2, N6, N8); direction errors (cases 2 and 3);
historical changes fitting no transformation; false board-change alarms (controls 14, 15).

**Cannot:**
- *Rates.* With ~13 positives and 8 negatives, only near-perfect separation reaches significance.
  This is a **counterexample generator, not a rate estimator.**
- *PPV in the wild.* Cases are survivorship-selected famous successes.
- *Generative validity.* Huang did not work from a leak table. Retrodictive fit does not imply the
  procedure helps *find* boards.
- *Hindsight in this encoding.* v0 is single-encoder and contaminated. L2 has not been done.

## A base rate the programme should carry

2 of 15 headline results in this set (Viazovska, Kelley–Meka) were better play on an **unchanged**
board. Small count, but the base rate is not zero.
