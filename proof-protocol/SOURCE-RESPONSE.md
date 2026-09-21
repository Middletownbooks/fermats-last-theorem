# Seed document 2 of 2 — the originating response

*Reproduced as received, 2026-09-18. Everything under `p1-retrodiction/`, `p3-taxonomy/` and the
P2 pre-registration derives from this text. Where the encoding had to make a choice this text does
not settle — the names of transformations #3 and #5, the transformation labels for cases 9 and 10 —
the data records `unlabelled` or `null` and `DEBTS.md` records the gap. Nothing was invented to
fill a hole.*

---

Tom, here is the work in priority order, front-loaded so a cutoff costs you the least. Nothing below is **measured**: I can't spawn agents in this environment, so P2 can't be run here. P1 is a usable v0, P2 is a pre-registration ready to execute, P3 is a preliminary scoring that already produces counterexamples, and P4 I decline to write as "justified by measurement". Tags: [R] reasoned, [A] assumed, [K] recalled from literature and not re-fetched this session, so verify citations before relying on them. arXiv:2609.11189 post-dates my knowledge, and I take E3/E4 as given.

## P1. Retrodiction benchmark (v0)

### 1.1 Contamination control

I disagree with the commission's suggested direction [R]. Forced-choice discrimination between the true move and a decoy is still solved by recognition ("cap set → polynomial method"). Decoys written by a contaminated model to be "attractive and wrong" also carry a stylistic tell. Contamination therefore inflates discrimination nearly as much as recall. I propose four layers instead:

- **L1: score the procedure, not the model.** The object under test in P3 is a diagnostic computed from the before-board alone. Where it is mechanical (e.g. "evaluate I on a product vs its factors"), a script or blind rater executes it, and model memory enters only through whoever encoded the case. That relocates contamination to encoding, where it can be controlled.
- **L2: control the encoding.**
  - Before-boards and leak tables may cite only sources dated before the superseding paper.
  - A second encoder, given only those sources, re-encodes blind. Report κ on slot contents and on the transformation label of the after-board. If label κ < 0.6, the five-transformation vocabulary is not operational, which is itself a P3 result.
  - Telegraph baseline: an agent gets the leak table with no procedure and guesses the after-move. The procedure's score is its lift over this baseline, not its raw accuracy.
- **L3: negative twins.** Each positive case is paired where possible with a near neighbour showing the same surface leak, where the transformation provably fails or the factor is provably tight. On twins the memorised famous answer is wrong, so recall hurts rather than helps. Without negatives the benchmark can measure only sensitivity, and a diagnostic that always fired would score perfectly.
  - Decoys are real mathematics only: after-boards swapped from other cases, plus documented failed attempts.
- **L4: recognition probe and prospective arm.**
  - After answering, the agent names the source problem. Scores are stratified by recognised vs unrecognised cases.
  - Anonymisation (renamed objects, names and dates stripped) should be tried. I expect it to fail on famous cases at any abstraction level that still permits computing the diagnostic [A]. Measure this with the probe rather than assume it.
  - The only fully clean estimate is prospective: log the procedure's prediction on new arXiv board-change claims before reading the method section.

**Exclusions.** Banaszczyk, Bansal–Jiang, and Guo–Fang–Lu generated the P3 taxonomy. They are calibration items and are never scored.

### 1.2 Cases: before-board and leak (answers held out in 1.3)

Slots are S (state), M (move), I (invariant), C (composition), T (terminal certificate).

*(The thirteen cases, the fifteen-row table, the two controls and the eight negative twins are
encoded as data in `p1-retrodiction/`. The encoding is one-to-one with this table; see
`cases/*/before.json`, `controls/*.json` and `twins/*.json`.)*

| # | Problem | Bound then | Leak |
|---|---|---|---|
| 1 | Sensitivity | Δ ≥ (½−o(1))log n (Chung–Füredi–Graham–Seymour 1988); conjectured √n | Counting controls mean degree, not max. The unsigned spectrum of Q_n is n−2k, additive under Cartesian product, so the median eigenvalue is ≈0 and interlacing is empty. |
| 2 | Cap set | 3^n/n (Meshulam 1995); n^{1+ε} (Bateman–Katz 2012) | The per-step gain δ² combined with the additive cost of one dimension per step forces δ ≳ 1/n. The invariant composes additively, while the target is supermultiplicative under products, so the truth has form c^n. |
| 3 | Shannon capacity Θ(C5) | √5 ≤ Θ ≤ 5/2 (Shannon 1956) | The LP sees only cliques (edges, for C5), so it is loose on odd cycles. Its product law is correct; its value is wrong. |
| 4 | Kadison–Singer (Weaver KS₂) | Needs δ ≲ 1/log n | The factor n in tr exp gives log n. It is tight on direct sums of independent blocks. |
| 5 | Finite-field Kakeya | \|K\| ≳ q^{(n+2)/2}, later ≈q^{4n/7} | Cauchy–Schwarz sees pairwise line interactions only, which caps the exponent near n/2. |
| 6 | Erdős distinct distances | N^{0.864} (Katz–Tardos 2004) | Circle incidence bounds are weaker than line bounds. The exponent stays stuck below 1. |
| 7 | Small prime gaps | GPY: needs θ > ½; Bombieri–Vinogradov gives exactly ½ | Weights are a one-dimensional function of the product. The ratio saturates at 2θ·(1+o(1)) regardless of k. |
| 8 | Spencer set discrepancy | √(n log n) | √log n comes from the union bound over sets. |
| 9 | Vinogradov mean value | s ≳ c·k² log k (classical). [K, medium confidence] | Each iteration recovers a fixed fraction of the defect, so ~log k rounds are needed. |
| 10 | Parallel repetition | The conjectured invariant is false (Fortnow/Feige counterexamples) | Game value is not multiplicative. Provers correlate across coordinates. |
| 11 | Kneser conjecture | χ ≤ n−2k+2 known (Kneser 1955); no matching lower bound | No factor. Counting cannot see the obstruction, which is qualitative. |
| 12 | Geometrization | The programme was blocked at singularities | No control on collapsing at singular times, so the cigar soliton cannot be excluded. Qualitative. |
| 13 | PCP (weak case) | Gap amplifies but instance size grows as n^k | Size is multiplicative in the exponent under product. *Flag: the theorem was already proved. Use for P3 fit-testing only.* |

**Controls, where there was no board change and "change the board" is the wrong call:**

- **14. Sphere packing in dimensions 8 and 24.** I reclassify this candidate [R, K]. The board is Cohn–Elkies 2003. Viazovska supplied the terminal certificate on that board, and numerics had already shown it was tight. The actual board change was Kabatiansky–Levenshtein → Cohn–Elkies. As a control it tests for false board-change alarms when the board is right and the certificate is merely hard.
- **15. Roth in [N] (Kelley–Meka 2023).** The work stayed on the density-increment board and improved the play (sifting/higher energies), giving exp(−c log^{1/12} N).

**Negative twins, where the leak is real or the famous fix fails:**

- **N1 (twin of case 8). Johnson–Lindenstrauss.** A union over n² pairs gives dimension log n/ε², proven tight (Larsen–Nelson 2017).
- **N2. ε-nets.** A union over ranges gives (d/ε)log(1/ε). Tight in general (Komlós–Pach–Woeginger 1992) and for halfspaces in R⁴ (Pach–Tardos 2013); removable for halfspaces in R³ and discs (Matoušek–Seidel–Welzl). A within-problem matched pair.
- **N3 (twin of case 2). 3AP-free sets in [N].** Behrend excludes power savings. Slice rank gives nothing.
- **N4 (twin of case 3). Θ(C7).** The same after-board does not close it: ϑ(C7)≈3.318 vs lower bound ≈3.258 (Polak–Schrijver 2019). Still open.
- **N5 (twin of case 10). Strong parallel repetition.** The ε² vs ε loss is real even for unique games (Raz 2008, odd-cycle game).
- **N6. Discrepancy of arithmetic progressions.** The answer is n^{1/4}, tight (Roth 1964; Matoušek–Spencer 1996). No board change can beat it.
- **N7 (twin of case 5). Euclidean Kakeya.** Dvir's method does not transfer. R³ was resolved by a different multi-scale route (Wang–Zahl 2025).
- **N8 (twin of case 8). Discrepancy with m ≫ n sets.** √(n log(m/n)) is tight, so the log is only partially removable.

### 1.3 Held-out answers (keep separate from anything a scored agent sees)

*(Encoded in `p1-retrodiction/heldout/`, which `p1-retrodiction/tools/pack.py` is structurally unable to read.)*

| # | After-board | Source |
|---|---|---|
| 1 | Signed adjacency matrix with A²=nI, so squares add under product and the spectrum is flat at ±√n; Cauchy interlacing; λ₁ ≤ Δ. | Huang, arXiv:1907.00847 |
| 2 | One-shot slice-rank/polynomial bound with no iteration: the diagonal tensor has rank \|A\| ≤ 3·#{monomials of degree ≤ 2n/3} ≈ 2.756^n. | Croot–Lev–Pach 1605.01506; Ellenberg–Gijswijt 1605.09223; Tao's slice-rank formulation |
| 3 | ϑ via orthonormal representations. Multiplicative via tensor product of vectors, and ϑ(C5)=√5. | Lovász 1979 |
| 4 | Interlacing families: the expected characteristic polynomial is real-rooted, a barrier argument bounds its largest root, and some partition does at least as well. The largest root of a direct sum is the max over blocks, so it is dimension-free. | Marcus–Spielman–Srivastava 1306.3969 |
| 5 | A nonzero polynomial of degree < q vanishes on K if K is small. It vanishes on whole lines, hence at infinity in all directions, hence is zero. \|K\| ≥ q^n/n!. | Dvir 0803.2336 |
| 6 | Elekes–Sharir lift (distances → rigid motions → lines in R³) plus polynomial partitioning, giving N/log N. | Guth–Katz 1011.4105 |
| 7 | Two distinct answers; the rubric must accept either. | |
| 7a | Multidimensional weights λ_{d₁…d_k}, where the ratio grows like log k. | Maynard 1311.4600 |
| 7b | Breaking θ=½ for smooth moduli. | Zhang 2013 |
| 8 | Entropy/partial colouring, giving 6√n. | Spencer 1985 |
| 9 | Efficient congruencing, or ℓ² decoupling. | Wooley 2012; Bourgain–Demeter–Guth 1512.01565 |
| 10 | Information-theoretic embedding: conditioning on winning a subset, with per-coordinate relative entropy. | Raz 1995; Holenstein 2007 |
| 11 | Neighbourhood complex with Borsuk–Ulam. | Lovász 1978 |
| 12 | Same move, new monotone invariants: W-entropy and reduced volume give κ-noncollapsing. | Perelman math/0211159 |
| 13 | Graph powering on expanders plus alphabet reduction, with constant-factor size blowup. | Dinur 2007 |

### 1.4 Rubric

- **R1, per-diagnostic 2×2.** Fire or no-fire (from the before-block only) against the outcome label. Report raw counts. Positives are cases where the transformation is the blind-encoded label. Negatives are twins where it is blocked.
- **R2, lift.** Compare top-1 transformation choice and twin verdicts ("this leak is real") between procedure-equipped and table-only agents.
- **R3.** Recognition-stratified scores.
- **R4.** Encoder κ.

**The benchmark can detect:** diagnostics that fire on tight leaks (N1, N2, N6, N8); direction errors (cases 2 and 3); historical changes fitting no transformation; false board-change alarms (14, 15).

**The benchmark cannot detect:**
- *Rates.* With ~13 positives and 8 negatives, only near-perfect separation reaches significance. It is a counterexample generator, not a rate estimator.
- *PPV in the wild.* Cases are survivorship-selected famous successes.
- *Generative validity.* Huang did not work from a leak table, and retrodictive fit does not imply that the procedure helps find boards.
- *Hindsight in my encoding.* This v0 is single-encoder and contaminated. L2 has not been done.

## P3, preliminary (single contaminated rater, [R] throughout)

P3 comes ahead of P2 here because it is the part I can complete. P2's pre-registration follows and should still run first.

1. **De-tensorize has the wrong shape as stated.** It fires correctly on case 4 (direct sums) and loosely on case 13. On cases 2 and 3 the needed move runs the opposite way: progress required an invariant that is multiplicative, because the target quantity itself is (super)multiplicative. Case 1 changes the product law from additive to Pythagorean. Proposed replacement, not a sixth entry: **product-law matching** — compute how the target behaves on the product construction of the extremal family, and require the invariant to obey the same law. E4 then becomes the special case where the target is flat. Caveat: I derived this from the same cases I scored it on. It needs fresh cases.
2. **Collectivize-a-union-bound has poor specificity.** Correct on cases 8 and 4. It fires and fails on N1, N2 (general), and N8. Candidate refinement: ask whether an instance in the class makes the m bad events near-independent. If it does, the log is real. This is untested.
3. **Auxiliary-witness lift** fits cases 1, 3, and 5, but it has no stated diagnostic and fits almost anything post hoc. It has near-zero discriminating power, which is the programme's own E9 criticism applied to the programme.
4. **Transformations #3 and #5.** Only case 2 fits #3, and only weakly (it abolishes the iteration entirely). Nothing fits #5. I suspect both are artefacts of the Komlós trio.
5. **Cases fitting none of the five:** case 6 lifts the state through the move's symmetry group; case 7a enlarges the dimension of the move space, de-collectivizing, which is the reverse of #4; case 11 is a category change; case 12 is "same move, new invariant", exactly E4's shape, but no entry says how to find the invariant.
6. **Against the programme's hypothesis.** 2 of 15 headline results (cases 14 and 15) were better play on the same board. It is a small count, but the base rate is not zero.
7. **Disagreement with E5(b).** Banaszczyk's move is itself an existence lemma. Case 4 is pure existence, and case 5 gets existence from dimension counting. All three succeed. The better discriminator is probably whether the existence guarantee is strictly cheaper than the target, not formula versus existence.

## P2. Pre-registration (not run)

**Battery.** Problems with planted ground truth, of three kinds: (i) statement pairs, one true and one subtly false with a small known counterexample, the agent asked to prove them; (ii) true statements with a tempting invalid route; (iii) open problems where only return-condition (c) is correct. Pilot: 3 bare runs per problem. Keep only problems with bare failure in [20%, 80%], per E10.

**Arms.** A 2^(6−2) fractional factorial (16 arms) over six clause blocks: A §0 substrate honesty; B §1 decomposition/scale; C §3 tags and diagnosis; D §4 named failure principles; E §5 content-not-verdict; F §7 coverage/validity/scope. §6, §8 and §9 are held fixed at N=1. Four further arms: bare; length-matched irrelevant placebo (formatting rules); length-matched generic-rigour exhortation; and a **schema arm**, with the same E+F content delivered as mandatory return fields rather than prose. Size: roughly 12 problems × 16 arms × 2 reps plus controls, about 450 runs, blind double-judged with κ.

**Outcomes (yes/no).** O1: false (a) returned on a false or open item. O2: clause executed, defined by a content marker — e.g. SCOPE CHECK counts as executed iff a named neighbouring statement and the expression the mechanism produces there both appear. O3: the executed check was discriminating, meaning its value would have differed if the claim were false. O4: a verdict reported without content. O5: tokens.

**Predictions, to be scored as written.**
- (a) Block D has no O1 effect beyond the generic-rigour placebo.
- (b) Block E lowers both O4 and O1.
- (c) Under prose delivery, SCOPE CHECK is executed in fewer than 50% of runs, and in more than 80% under the schema arm.
- (d) E+F alone matches full v2.1 on O1 at half the tokens or less.
- (e) The generic-rigour placebo recovers at least half of the full template's O1 effect.
- (f) Block A changes labelling but not O1.

## P4 and the failure register

I am not writing v3, because a v3 written now would be one more prescription. The schema arm and predictions (a) to (f) are the v3 hypotheses. If (c) and (d) hold, v3 is a return form with around six computed-content fields, and §4 shrinks to a footnote.

Tried and dropped: forced-choice discrimination as the contamination control (rejected, 1.1); sphere packing as a board change (reclassified as a control); PCP as a scoreable case (demoted); running P2 here (no agent substrate).

For next steps, I can build the P2 harness as an artifact that runs the arms through the API from your browser, which makes the ablation affordable. If a cheaper first step is needed, the L2 blind re-encoding of P1 comes first.
