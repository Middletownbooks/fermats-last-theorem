# P3 — The transformation taxonomy and its scoring

`taxonomy.json` is the catalogue. This file is the seed's preliminary scoring of it.

> ## SUPERSEDED IN PART — read `../MEASUREMENTS.md` first
>
> **Step D has since measured label κ = 0.048** (three raters, eight after-boards, 100%
> recognition, 20% agreement). The seed's own stop rule was κ < 0.6. **The five-transformation
> vocabulary is not operational, and that is the P3 result.** Finding 4 below anticipated it for
> two entries; the measurement extends it to the catalogue.
>
> **The rebuild is in `DIAGNOSTIC.md`.** Findings 1, 2 and 3 below are superseded by it: product-law
> matching has been restated to read no leak table, the union-bound refinement has been corrected
> and tested, and auxiliary-witness lift has been **dropped**. The preliminary findings are kept
> below as the record of what was thought before either measurement existed.
>
> **One contaminated rater. [R] throughout.** The scoring below was produced by the same instance
> that encoded P1, while knowing every answer, in a single pass with no second labeller. Its own
> summary of its status: this is a counterexample generator, not a measurement. **Nothing here has
> a κ**, because `second_blind_label` is `null` on all thirteen held-out answers.
>
> If the blind re-encoding (handoff task 2) returns label κ < 0.6, the five-transformation
> vocabulary is **not operational**, and *that* is the P3 result — not any of the findings below.

## The seven preliminary findings

**1. "De-tensorize" has the wrong shape as stated.** It fires correctly on case 4 (direct sums)
and loosely on case 13. On cases 2 and 3 the needed move runs the *opposite* way: progress required
an invariant that is **multiplicative**, because the target quantity itself is (super)multiplicative.
Case 1 changes the product law from additive to Pythagorean.

Proposed replacement — **not a sixth entry** — is *product-law matching*: compute how the target
behaves on the product construction of the extremal family, and require the invariant to obey the
same law. E4 then becomes the special case where the target is flat.

*Caveat the seed stated itself:* this was derived from the same cases it was then scored on. It
needs fresh cases chosen by someone who has not seen the hypothesis. Until then it is a guess
(debt **D8**).

**2. "Collectivize a union bound" has poor specificity.** Correct on cases 8 and 4. It fires and
fails on N1, N2 (general) and N8. Candidate refinement, **untested**: ask whether some instance in
the class makes the m bad events near-independent; if it does, the log is real.

**3. "Auxiliary-witness lift" fits cases 1, 3 and 5 — and almost anything else.** It has no stated
diagnostic and near-zero discriminating power. This is the programme's own E9 criticism applied to
the programme.

**4. Transformations #3 and #5 are probably artefacts.** Only case 2 fits #3, and only weakly — it
abolishes the iteration entirely. Nothing fits #5. Both are suspected artefacts of the Komlós trio
that generated the catalogue. **Neither has a name anywhere in the seed material** (debt **D12**):
do not invent one.

**5. Four cases fit none of the five.**

| Case | What actually happened |
|---|---|
| 6, Erdős distinct distances | Lifts the state through the move's symmetry group |
| 7a, small prime gaps | Enlarges the dimension of the move space — it *de-collectivizes*, the reverse of #4 |
| 11, Kneser | A category change |
| 12, Geometrization | "Same move, new invariant" — exactly E4's shape, but no entry says how to *find* the invariant |

**6. Against the programme's hypothesis.** 2 of 15 headline results — sphere packing in dimensions
8 and 24, and Kelley–Meka — were better play on an **unchanged** board. A small count, but the base
rate is not zero, and the hypothesis should carry that denominator. This depends on the sphere
packing reclassification holding (debt **D6**).

**7. Disagreement with E5(b).** Banaszczyk's move is itself an existence lemma; case 4 is pure
existence; case 5 gets existence from dimension counting. All three succeed. The better
discriminator is probably whether **the existence guarantee is strictly cheaper than the target**,
rather than formula versus existence.

*This has the same flaw as the criterion it replaces:* n = 3, derived from the cases that motivated
it (debt **D9**).

## Scoring it again, properly

*(Superseded: step D ran this and got κ = 0.048. Kept because it is how the NEXT vocabulary gets
tested — specifically the two-field assignment `DIAGNOSTIC.md` calls for.)*

~~~sh
cd ../p1-retrodiction
python3 tools/kappa.py template --kind labels > labels_B.json   # second labeller fills this blind
python3 tools/kappa.py labels labels_A.json labels_B.json
~~~

The tool prints the κ < 0.6 verdict itself, so the stop condition is mechanical rather than a
judgement call made after seeing the number.

## P4

Deliberately unwritten. A v3 written now would be one more prescription. The v3 hypotheses are
already encoded as P2 arms: **if predictions (c) and (d) hold, v3 is a return form with about six
computed-content fields, and the named-failure-principles block shrinks to a footnote.** Wait for
the data.
