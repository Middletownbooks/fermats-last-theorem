# What has been measured

**Four** measurements have been completed. They are **finished**, and they supersede parts of what
this repository encoded from the seed. Nothing else in this project has been measured.

Read this before starting any task: both results change what is worth doing.

---

## Step D — the five-transformation vocabulary is not operational

Three raters labelled eight after-boards with one of the five transformations, or "none".

| | |
|---|---|
| **Cohen's κ** | **0.048** |
| Agreement on the label | 20% |
| Recognition of the source problem | 100% |
| Worst case | Three raters gave three different labels to the same Guo–Fang–Lu after-board |

The seed's own stop rule (handoff task 2, bullet 3) was: *"if label κ < 0.6 the vocabulary is not
operational — report that as the P3 result."* It is 0.048.

**This is settled. The five-transformation vocabulary is not operational.** Do not try to rescue it
by adding definitions, and do not add a sixth entry — κ = 0.048 was measured on the five that
already exist, so the catalogue's problem is not that it is too small.

This closes the question `p1-retrodiction/tools/kappa.py` was built to decide. The tool stays: it is
how the next vocabulary, if there is one, gets tested before anyone scores anything with it.

---

## L2 — the blind re-encoding (handoff task 2, now closed)

Five cases from P1 §1.2 — 1 sensitivity, 2 cap set, 5 Kakeya, 8 Spencer, 9 Vinogradov — were
re-encoded by five independent subagents. Each saw only its own case, a date cutoff, and the schema;
none saw the seed's encoding or the held-out after-board. The three calibration items were excluded,
as the seed required.

| measure | result |
|---|---|
| leading leak mechanism agrees | **2 of 5** |
| P1 mechanisms named *anywhere* in the blind table | **6 of 7** |
| `bound` agrees | 3 of 4 comparable (1 void) |
| `state` agrees | 1 of 5 |
| recognition of the superseding work | **5 of 5** |

The two leak agreements are Spencer (UNION BOUND) and Vinogradov (ITERATION COUNT) — the two cases
where the leak is visible in the algebra of the bound itself. Every case admitting more than one
reading got two different readings.

### The load-bearing finding

**2 of 5 leading, but 6 of 7 named anywhere.** The two encoders draw from the same pool of
mechanisms and *rank them differently*. A diagnostic that reads "the leak" reads the ranking, and
**the ranking does not reproduce**.

In cases 1 and 2 the blind encoder does name a multiplicative / product-law mechanism — but attaches
it to a constant, never to the dominant exponent gap, which is where the seed attaches it. That is
the finding that drives the rebuild in `p3-taxonomy/DIAGNOSTIC.md`.

### Known holes in L2 — stated so they are not inherited as facts

- **The pre-registered κ was never measured.** The third rater (provenance hidden, X/Y randomised)
  was not run; all slot marks were made by one non-blind rater. A substitute inter-encoder κ on the
  leading mechanism is 0.286 with a case-resampled 95% CI of **[0.000, 0.667]** at n = 5. Read that
  as **unmeasured, not as a bound.**
- **Case 9 is void through a design error.** Its cutoff was set at 2011-12-31 intending "before
  Wooley", but Wooley's efficient-congruencing paper is arXiv:1101.0574, posted **3 January 2011** —
  eleven months *inside* the cutoff. The two encoders were answering different questions.
  **Date every cutoff from the arXiv posting, never the journal year.**
- **`move` was not comparable on its defining field.** The schema requires
  formula-versus-existence-theorem; the seed's table has no such field.
- **6 of 25 slot-pairs had nothing on one side.** The seed's P1 leaves `composition` empty in cases
  1, 5, 9 and `terminal` empty in 5, 8, 9.

---

## D20 — the two-field κ test: a split result

Three raters, blinded to the rule and to which items were positives, assigned `target_law` and
`bound_law` from the bound and the extremal construction alone. Inputs, filled sheets and verbatim
output: `p3-taxonomy/d20/`. **Read `p3-taxonomy/d20/PROVENANCE.md` first** — partial results were
seen before the full run was assembled, and the scorer's verdict logic was changed afterwards.

| | κ (Fleiss, 3 raters) | 95% CI | 0.6 stop rule |
|---|---|---|---|
| transformation label (step D) | **0.048** | — | failed |
| `target_law` | **+0.811** | [+0.570, +1.000] | pass |
| `bound_law` | **+0.755** | [+0.494, +1.000] | pass |
| **the firing decision the rule uses** | **+0.618** | **[+0.220, +0.904]** | pass, barely |

**Passed:** moving the judgement onto two closed-vocabulary fields raised κ roughly sixteenfold over
the transformation label. That was the rebuild's central bet.

**Failed:** the zero-false-positive claim. **All three raters fire on N8**, unanimously against my
reference; I checked the mathematics and they are right. `DIAGNOSTIC.md`'s "0 false positives over 8
negatives" is **withdrawn** and the corrected specificity is 7/8.

**The finding that outranks both:** the rule reproduces (0.618) markedly worse than its inputs
(0.755–0.811), because it consumes the *difference* of two labels and disagreement concentrates
where they are close. And N8 exposes a defect in the rule's **domain condition** — it admits
operations that move both coordinates of a two-parameter family. Every case the diagnostic gets
right is single-parameter; its false positive is the two-parameter one (debt **D23**).

---

## The baseline — the retrospective arm is saturated by recall

Full write-up: `p3-taxonomy/BASELINE.md`. Inputs and output: `p3-taxonomy/baseline/`.

The rebuilt diagnostic's 2×2s were raw accuracies, which this programme's rules forbid. Scored
against a baseline, with Youden's J:

| | J |
|---|---|
| fire on everything / fire on nothing / coin flip | **0.000** by construction |
| product-law matching | **+0.675** |
| **a rule-less rater, same item, asked only "was this bound superseded?"** | **+1.000** |

**Lift of the diagnostic over the rule-less rater: −0.325.** It is worse than no diagnostic. The
rater got 5/5 positives and 8/8 negatives, and its **recognition probe came back 13 of 13** — it
named every problem and was recalling, not inferring.

**Consequence, and it is the most important sentence in this file:** a contaminated rater ceilings
this benchmark perfectly, so **the retrospective arm cannot measure a diagnostic's value at all.**
Every retrospective 2×2 here is a weaker version of recall. This is step D's 100% and L2's 5-of-5
reproduced a third time, with the cost finally made explicit — and it is the seed's L4 claim,
*"the only fully clean estimate is prospective"*, measured rather than argued.

What survives: the twins still falsify (N8 caught the domain defect D23), D20's field κ still
measures encoding reproducibility, and `p1-retrodiction/prospective/` is now not one instrument
among several but the only one.

---

## Corrections to P1 that are established

### Case 5 (Kakeya) — the seed's flagged debt was real, and worse than flagged

P1 gives the before-bound as "|K| ≳ q^{(n+2)/2}, later ≈ q^{4n/7}", ordering them as though 4n/7
superseded Wolff's exponent. **It does not, uniformly:**

~~~
(n+2)/2 > 4n/7   ⟺   7n + 14 > 8n   ⟺   n < 14
~~~

At n = 13, (n+2)/2 = 7.500 against 4n/7 = 7.429; they meet exactly at n = 14. **At the 2008 cutoff
Wolff's bound was still the best known in every dimension below 14.** No single exponent dominated
uniformly in n. (Verified in `p1-retrodiction/tools/check_corrections.py`.)

The consequence is structural, not bibliographic: **the two regimes leak differently.** The blind
encoder split them — UNION BOUND for Wolff's (n+2)/2 (the bush argument double-counts incidences
with no use of structure in the direction set), FEASIBILITY THEOREM for 4n/7 (Bourgain–Katz–Tao
supplies only a qualitative sum-product exponent).

**A single-regime `bound` field forces a single leak where there are two.** That is a schema defect,
and it is the first thing the corrected schema fixes.

### Case 9 (Vinogradov) — the seed's `[K, medium confidence]` flag was warranted for the wrong reason

The bound s ≳ c·k² log k is correct for the classical method. The fault was in the cutoff date, not
in the seed's recall.

### Case 8 (Spencer) — an outright `move` disagreement, and it is real mathematics

The seed's move is "uniform random colouring", one shot. The blind encoder's is "colour one more
point, taking the smaller Chernoff potential" — the sequential Erdős–Selfridge derandomisation. Both
reach √(n log n); **they are not the same board**, and one of them has no composition step at all.

If you re-encode anything, expect this class of divergence and **record which board you mean**.
