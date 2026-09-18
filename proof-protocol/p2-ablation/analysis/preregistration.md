# Pre-registered analysis for P2

Commit this file, and the hash printed by `python3 cli.py freeze`, **before** the first main-study
run. The six predictions were pre-registered in the artifact; this document pre-registers the
*analysis*, which the artifact did not.

## 1. What the harness reports is not the analysis

`cli.py score` prints difference-of-proportions intervals that treat runs as independent. They are
not independent: every arm sees the same problems, so those intervals are too narrow. They are for
monitoring a run in progress. **They are not the analysis of record.**

## 2. The analysis of record

Primary, on the exported CSV, judge 1's outcome:

~~~
fail ~ A + B + C + D + E + F,  binomial, with a random intercept per problem
~~~

Fitted by `analysis/analyze.py model` (`statsmodels` `BinomialBayesMixedGLM`). Secondary: a GEE
with exchangeable working correlation clustered by problem, reported alongside. Where the two
disagree in sign or significance, both are reported and neither is preferred after the fact.

Factorial arms only. The four control arms (bare, two placebos, the two E+F arms) are **not** in
this model; they are compared directly, as predictions (c), (d) and (e) specify.

## 3. Aliasing — the rule that must not be broken after unblinding

The design is a 2^(6−2) fractional factorial with E = ABC and F = BCD. Its defining relation is

~~~
I = ABCE = BCDF = ADEF
~~~

verified computationally by `tests/test_aliasing.py`, which also confirms that no word of length 1,
2 or 3 is defining — that is what makes the resolution **IV** rather than III — and that each block
is present in exactly 8 of the 16 arms.

- Main effects are clean of two-way interactions.
- **Two-way interactions are aliased with each other**, in these groups:

  | | aliased pair or triple |
  |---|---|
  | 1 | AB = CE |
  | 2 | AC = BE |
  | 3 | AD = EF |
  | 4 | **AE = BC = DF** |
  | 5 | AF = DE |
  | 6 | BD = CF |
  | 7 | BF = CD |

  They will not be fitted, and **no interaction term may be interpreted**. `analyze.py` refuses to
  fit them. Note group 4 in particular: an apparent "substrate × stance" interaction is
  indistinguishable from "decomposition × tags" and from "principles × audit".

Adding an interaction after seeing the data is the most likely way this study produces a false
finding. If an interaction becomes interesting, that is a hypothesis for a new design, not a
result of this one.

## 4. Power

Computed from the design actually run, not recalled: `analysis/analyze.py power --csv runs.csv`.
The inherited rule of thumb is roughly a 30-point shift at ~40 runs per factor level; the tool
recomputes this from the realised design and the observed base rate, inflated by the design effect
from clustering by problem.
It reports runs per factor level, the design effect from clustering by problem, and the smallest
difference detectable at 80% power and α = .05.

The handoff carried an inherited figure — "~40 runs per factor level detects roughly a 30-point
shift". That estimate predates this design. The computed number supersedes it. Whatever it comes
out to: **effects smaller than the detectable difference will read as null, and the write-up must
say that rather than calling them absent.**

## 5. Judge handling, fixed in advance

- All primary tables use **judge 1**. Judge 2 exists to measure agreement, not to be averaged in.
- Report Cohen's κ for the failure outcome and for `scope_executed`.
- **If either κ is below ~0.6, transcripts are read before any table is reported.** This is a stop
  condition, not a caveat to add afterwards.
- Judges are **not blind to arm** and cannot be: the protocol's own tags (`UNENFORCED`,
  `DERIVED HERE`) and the numbered return fields leak the condition into the graded text. Record
  this as a limitation; do not describe the judges as blind.
- Judge 1 and judge 2 default to different model families (Opus, Sonnet). This reduces same-model
  judging bias; it does not remove it, since both are Claude models from one vendor.

## 6. What code decides, and what the judge decides

Where an arithmetic checker exists (`checkers.py`), a claimed counterexample is verified in code
with exact integers and rationals, and that verdict **overrides** the judge's `valid`. The judge
only extracts the witness. Runs where this happened are counted in `cli.py score` and flagged per
row in the CSV (`checker_overrode_j1`).

This changes the *input* to the frozen scoring rules. It does not change the rules. `--no-checkers`
behaviour is available by setting `use_checkers: false` in `study-state.json` for a strict
replication of the artifact.

## 7. Declared deviations from the artifact

The port is behaviourally identical on the frozen scoring rules — `tests/test_fidelity.py` executes
the artifact's own JavaScript and compares every verdict, interval, arm rate and κ. The deviations
below are deliberate and declared, as the handoff requires:

| # | Deviation | Why |
|---|---|---|
| 1 | Placebo text is non-repeating, and length-matched to 10,121 characters from a pool of distinct paragraphs | The artifact cycled ~10 paragraphs; visible repetition weakens the control that prediction (e) turns on |
| 2 | The judge returns one extra field, `claimed_witness`, and its reply is constrained by a JSON schema | Lets code do the arithmetic; removes JSON parse failures |
| 3 | Real token counts from `usage` | The artifact estimated tokens as characters ÷ 4 |
| 4 | Named models and an `effort` setting; optional system prompt | The artifact could only pick a tier |
| 5 | **Temperature is not controlled** | Sampling parameters were removed from the current Claude models; sending one is a 400. `effort` is the nearest control and is recorded per run. Do not report temperature as held constant |

Deviations 1 and 2 change the stimulus and the judge prompt, so the pre-registration hash differs
from the artifact's by construction. That is a **re-freeze**, and this table is the declaration of
it. The six prediction rules themselves are unchanged.

## 8. Stop conditions

- Judge κ below ~0.6 on either measure: read transcripts before reporting.
- The pilot leaves no problem with a bare failure rate in [20%, 80%]: the battery cannot separate
  the arms. Replace the battery rather than running the main study — see `battery.py` and the
  top-level README on the missing real-failure items.
- Three consecutive API failures: the harness pauses itself.
