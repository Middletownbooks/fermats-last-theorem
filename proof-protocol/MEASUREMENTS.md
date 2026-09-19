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

## The N9 audit — the flagship result withdrawn

Full write-up: `p3-taxonomy/d20/N9-audit-result.md`. Every load-bearing computation independently
verified in `p1-retrodiction/tools/check_n9_audit.py` (26 checks).

`DIAGNOSTIC.md` called N9 — case 1 on both sides of Huang's board change — *"the single result most
worth trying to break"*. An adversarial audit by an agent that did not build it broke all three of
its load-bearing points:

1. **The feasible set is not closed under the product.** The constraint is a density threshold and
   density is multiplicative, so the product of two extremal examples occupies a **quarter** of
   Q_{n₁+n₂}, not half. There is no product of extremal examples to read a target law off; the `l2`
   label came from substituting into `⌈√n⌉`. The honest product law is **additive** — Cartesian
   degrees add. **Case 1 and N9 both leave the diagnostic's domain.**
2. **The label is split-dependent and the signal is tiny.** At a 99:1 split, `l2`, `max` and
   `additive` agree to within 10%. `√(n₁+n₂) ≤ √2·√max` always, so the distinction carries **at most
   a factor √2** — and it was being used to flag a polynomial (`log n` vs `√n`) gap.
3. **The example is confounded.** *"Does the lower bound match the upper bound to within a constant
   factor?"* reproduces both verdicts, needs no product-law machinery, and is immune to the rater
   dispute over the counting board's label (debt **D28**).

What survived, and strengthened: the tightness claim. **Integrality** closes the rounding for every
`n` (Δ is an integer, so `Δ ≥ √n ⟺ Δ ≥ ⌈√n⌉`), and **monotonicity** makes CFGS's construction at
perfect squares sufficient everywhere. What was over-claimed: *"nothing further comes off"* conflated
the extremal value with the sensitivity conjecture, whose exponent is open in **[2, 4]**.

**Reduced-domain figures:** 11 items, J = **0.607** against the rule-less baseline's **1.000** —
lift **−0.393**.

**And the pattern that matters most:** the domain condition has now been patched twice, post hoc, each
time by the item that broke it (D23 from N8, D27 from N9). Neither patch is adopted. Two patches from
two items is the signature of a rule being **fitted rather than tested**.

---

## Citation work, second pass — and a structural finding

*Counts in this section are frozen at the end of that pass and are not maintained; the live
state is the generated **Current state** table in `CITATIONS.md`.* As that pass ended:
**28 verified**, 2 corrected, 1 disputed, 2 partial, **4 unverified**, with pasted transcripts
closing C3, C7, C9 and N3 at primary tier. Two changes of substance:

- **C4 closed as a NEGATIVE result.** Neither Weaver nor Marcus–Spielman–Srivastava states the
  threshold `δ ≲ 1/log n`. The number is **dropped** and the sourced log-dimension loss written
  instead. The diagnostic is unaffected: case 4 fires on the *loss*, which is sourced, not the
  *threshold*, which is not.
- **N3 re-attributed.** The exclusion of power savings is **Salem–Spencer 1942**, not Behrend 1946 —
  Behrend is the stronger and still best-known bound, but the exclusion does not need it. The claim
  is also now stated **asymptotically**, with the crossover recorded: N > 10¹⁰ for δ = 0.5 but
  **N > 10²⁴¹** for δ = 0.1.

**The structural finding: case 7 splits into a contemporaneous within-problem pair.** Maynard–Tao
changed the board and kept the old input (Granville: *"one can avoid having to prove any difficult new
results about primes in arithmetic progressions"*); Zhang left the sieve alone and improved the input.
So **7a is the positive and Zhang becomes control 16** — one problem, one year, two teams, one
changing the board and one not, **with the counterfactual actually run**. Controls go 2 → 3.

This matters beyond bookkeeping. **D25 found that a rule-less rater ceilings the benchmark because it
only has to *name* the problem.** A contemporaneous within-problem pair is the one structure recall
cannot crack: both halves are "bounded prime gaps, 2013", so a rater must separate them *on
mechanism*. That is the most promising response to D25 that does not require waiting for the
prospective arm (debt **D31**).

Carried with it, honestly: Zhang is **not** simply better play. He changed the *equidistribution*
board one level down — smooth moduli, factored modulus, Graham–Ringrose. So control 16 is a
**level-(n−1) board change feeding an unchanged level-n board**, a third category the catalogue never
had (debt **D30**). The control is valid only with the level stated.

---

## Citation work, third pass — the last open control closes, and the board has a stated ceiling

One pasted transcript, arXiv:2302.07211v3 (Bloom–Sisask, *The Kelley–Meka bounds for sets free of
three-term arithmetic progressions*), closed the only unsourced **control** in the benchmark and
carried four more rows with it. Live counts are the generated table in `CITATIONS.md`; the standing
caveat in `DEBTS.md` is generated from the same function.

**Control 15 verified on its own terms (D29 closed).** The exposition breaks Kelley–Meka into five
steps and names the fifth **"Density increment"** — *"there is an affine subspace V of codimension
O(L(α)⁴L(γ)⁴) on which A has density at least (1 + 1/100)α … This density increment condition can now
be iteratively applied."* So the board P1 assigns to the control is the board the primary source says
the argument runs on, and the new play is Steps 1–4 (Hölder lifting, unbalancing, dependent random
choice, almost-periodicity), described by the authors as *"mostly physical-based methods, rather than
the Fourier-based methods that have dominated the study of three-term progressions thus far."* A
change of technique on an unchanged board is exactly what this control tests for.

**P1's exponent is doubly stale, and the source says so in one paragraph.** Larger exponent = stronger
bound, for `|A| ≤ exp(−c(log N)^e)N`:

| e | value | what it is |
|---|---|---|
| 1/12 | 0.08333 | Kelley–Meka Theorem 1 — the figure P1 records |
| 1/9 | 0.11111 | Bloom–Sisask, *"a relatively clean argument (the only modification required is to the almost-periodicity part)"* |
| 5/41 | 0.12195 | after *"a further tedious lengthy technical optimisation"* |
| 1/7 | 0.14286 | *"the natural limit of these methods, in that achieving anything better will require significant new ideas"* |
| **1/3** | **0.33333** | **the stated limit of _any_ density-increment-with-Bohr-sets argument** (*"or perhaps even 1/4"*) |
| 1/2 | 0.50000 | Behrend's construction — so the truth is at least this strong |

Ordering and both gaps are verified in `p1-retrodiction/tools/check_citations_response.py` §(e). One
trap is recorded rather than smoothed over: **1/7 appears twice with different referents** — it is the
improved *finite-field* exponent of Theorem 2, and separately the believed limit of Theorem 1 over the
integers. Reading one for the other puts a finite-field exponent on the integer ladder.

**The finding worth more than the row (D32).** The interval **(1/3, 1/2] is unreachable from this
board on the practitioners' own account**, stated in print, contemporaneously, about a live problem.
Every leak in P1's retrospective corpus is one *we* identified after the board was left — which is the
contamination D25 showed the retrospective arm cannot escape. This is a leak identified **before** the
board was left, by the people playing on it, with the cap and the truth both quantified. It does not
reclassify control 15: a stated ceiling predicts the board will have to be left, and in 2023 it was
not, so the control still reads must-not-fire. What it does is name the shape of item the benchmark
actually needs, and the search for more of that shape now outranks adding twins.

**Three smaller things.** Twin N3's load-bearing half is now a quoted primary claim rather than our
inference — *"there is no known analogue of the polynomial method for the integer problem, so
achieving strong bounds for the integer problem via this method is out of reach"*. The N3 refinement's
"first improvement to Behrend since 1946" needed a qualifier, and it was my phrasing that needed it:
Elkin (2011) and Green–Wolf (2010) are small improvements, to the lower-order factor rather than to
(log N)^{1/2}. And "sifting" — the item's own word for Step 3 — is Kelley–Meka's term, which the
exposition names *dependent random choice*; "higher energies" was dropped from the item, because the
source uses the word "energy" nowhere but in a reference title.

**What was built from the finding, and what the second instance did to it.** The ceiling register
(`p1-retrodiction/CEILINGS.md`, sealed data in `ceilings/register.jsonl`, tool `tools/ceilings.py`)
holds **two** entries, not the one anecdote D32 was opened on. The second — GPY's one-dimensional
sieve, whose ρ_k(F) saturates at 4 for every *k*, so under Bombieri–Vinogradov the criterion caps at
exactly the value it must exceed — was **already in this repository** and cost no new source. It then
broke three of the register's assumptions at once: a cap can be an *unattained supremum* (the tool now
allows `cap == truth` with `cap_attained: false` and a boundary note, rather than fudging 3.999); the
truth a cap falls short of may be a *conjecture* rather than a theorem, which is a second axis; and a
resolution must state the **level** at which a board changed, because Zhang beat the θ > 1/2
requirement without touching the capped sieve (D30). Sharpest of all: **neither diagnostic reads both
instances.** Product-law matching is *silent* on the Roth entry — no product structure in [N], which
is twin N3's claim — while the D28 one-line test fires; and the D28 test has nothing to read on GPY,
because that cap is on a criterion rather than on a bound against a construction. That is the third
independent appearance of the surplus-machinery finding. Figures checked in
`check_citations_response.py` §(f); the register's first amendment corrects one of my own figures
inside a sealed record, by appending rather than editing.

**A bookkeeping failure, recorded because this project records them.** Closing the row exposed that
**D19's prose had been wrong twice in opposite directions**: first it listed four open citation rows
and omitted a fifth the data had always carried (`C1-gotsman`), then my replacement called three rows
UNVERIFIED when later rows had moved two of them to SEARCH and PARTIAL. Reading the sentence caught
neither; a derived count caught both at once. Counts now come from `tools/citation_status.py`, the
`DEBTS.md` caveat and the `CITATIONS.md` current-state table are generated from it, and
`tools/check_consistency.py` fails the tree if any of it drifts again — including a stale render or a
reference to a debt that does not exist.

---

## How many within-problem pairs would be enough (D31), and two counting corrections

**The pair route now has a number attached.** Each contemporaneous within-problem pair is one binary
decision at chance 1/2, so the test is an exact one-sided sign test (`p1-retrodiction/tools/pair_power.py`):
**five pairs scored perfectly clear α = 0.05** (p = 0.0312) and **eight are needed to survive one
miss** (p = 0.0352; at seven, one miss gives 0.0625 and fails). One discrimination pair is in hand —
case 7a against control 16. `p1-retrodiction/PAIRS.md` ranks four candidates, each with the document
that would settle it *and the way it might fail*, and rejects two (cap set 2016: both halves changed
the board; sphere packing 2016: neither did, and they share an author).

The arithmetic is stated rather than buried: **one pair in hand, four candidates, at most three of
which survive their stated risks, against a floor of five.** This route does not reach the floor on
current material. It is still the cheaper route to be wrong about — a failed candidate costs one
transcript, a failed prospective prediction costs months of waiting.

One pair is available **now** with no new source: Roth 2023, Kelley–Meka against Bloom–Sisask days
later on the same board, both must-not-fire. It does not count toward the five — with no "which is
which" there is nothing to score — but it measures *specificity inside one problem-period*, and the
authors' own words make the encoding clean.

**Two counting corrections, both the same class of error as D19's.**

1. **The debt count in `DEBTS.md` was wrong, and wrong in the flattering direction.** It was inferred
   from each debt's status *string*, so when a status stopped reading "open" while the work was still
   live — D19, D31, D32 — the number silently fell. It read **6 open when 13 were live**. Every debt
   now carries an explicit `state` of `open`, `closed` or `standing`, the count is rendered from that
   field, and `tools/check_consistency.py` fails the tree if a debt lacks one. Current state: **13
   open, 16 closed, 4 standing.**
2. **`standing` is a new category, and it is not a dodge.** Four debts are limitations that cannot be
   closed and must not be counted as work: judges that cannot be blinded to arm (D13), a sampling
   parameter the current models no longer have (D14), a retrospective arm saturated by recall (D25),
   and a corpus with no failed board changes (D26). Counting those as open work would make the
   backlog look permanently worse; counting them as closed would make it look solved. They are
   neither.

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
