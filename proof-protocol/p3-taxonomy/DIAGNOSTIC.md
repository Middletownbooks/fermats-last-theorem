# The diagnostic, rebuilt on the fields that reproduce

**Task 4.** L2 measured which fields survive an independent re-encoding:

| field | agreement |
|---|---|
| `bound` | **3 of 4** comparable |
| leading leak mechanism | **2 of 5** |
| `state` | 1 of 5 |

and the load-bearing detail: **6 of 7** P1 mechanisms were named *somewhere* in the blind table.
The two encoders draw from the same pool and **rank it differently**. A diagnostic that reads "the
leak" reads that ranking, and the ranking does not reproduce.

So the leak table cannot validate a diagnostic — not because the underlying mathematics is wrong,
but because the field carrying it is unreliable. The Huang signing really does change the product
law of the cube spectrum, and that really is why interlacing becomes available. The rebuild keeps
the mathematics and throws away the field.

## What the rebuilt diagnostics read

Three inputs, all objective and all pre-existing:

1. **The product operation** ⊗ on instances of the problem, and whether the size parameter is
   additive under it.
2. **The target's law under ⊗**, read off *the extremal construction* — you take the product of the
   extremal family and measure.
3. **The bound's law under ⊗**, read off *the formula*.

No leak table. Nothing that requires ranking mechanisms by importance.

### Product-law matching

> **FIRE iff the product operation exists and `target_law ≠ bound_law`.**

Where no product operation exists, the diagnostic is **NOT APPLICABLE**, which is not a prediction
and is not scored against it. Laws come from a closed vocabulary:
`multiplicative | additive | l2 | max | none`.

### Collectivize a union bound, refined

> **FIRE iff a union bound over m events produces the factor, and NOT
> (`independence_realisable` AND `target_requires_simultaneous_control`).**

The seed's proposed refinement asked only whether some instance makes the m events near-independent.
That is **not sufficient**, and case 4 is why: direct sums realise independence exactly, yet the log
is removable. The missing conjunct is whether the target must control all m events *at once*. Where
the target decomposes — where a partition may be chosen separately per block — independence is not
an obstruction and the log comes off.

### Auxiliary-witness lift

**Dropped.** The task allowed a diagnostic computable from the before-board alone, or removal. There
is no such diagnostic: "introduce an auxiliary object whose existence certifies the bound" has no
before-board trigger, because essentially every proof introduces one. The seed already conceded
near-zero discriminating power; step D measured κ = 0.048 across the catalogue; the standing
instruction is that the catalogue shrinks before it grows. Dropped rather than rescued.

## Results

Run `python3 score_diagnostics.py`. The rules are applied mechanically from the structural fields;
the recorded expectation is only a cross-check, and a disagreement is reported as an error.

> ## FIRST, READ `BASELINE.md`: the diagnostic loses to no diagnostic
>
> A rule-less rater, given the same item text and asked only whether the bound was superseded,
> scored **perfectly** — 5/5 positives, 8/8 negatives, Youden's **J = 1.000** against this
> diagnostic's **0.675**. The lift is **−0.325**. Its recognition probe came back **13 of 13**: it
> named every problem and was recalling answers, not inferring from product structure.
>
> So every table below is a *weaker version of recall*, measured against a ceiling recall already
> reaches. They are evidence that the diagnostic is self-consistent, not that it works. The
> retrospective arm cannot settle that question; only `../p1-retrodiction/prospective/` can.
>
> ## The zero-false-positive claim is WITHDRAWN
>
> An earlier version of this file reported **4 fires, 0 false positives over 8 negatives**. That
> was computed from my own law assignments, and **D20 found one of them wrong in the direction that
> flattered the diagnostic**. Three independent blind raters unanimously assigned N8
> `target_law = max, bound_law = l2` where I had `additive / additive`; I checked the mathematics
> and they are right. The corrected table is below. See `d20/N8-adjudication.md`.
>
> The figures below are also **raw accuracies**, and this programme's own rule is that scores are
> lift over a baseline, never raw accuracy. That baseline has not been run. Do not quote these
> numbers as results until it has.

**Product-law matching**, **11** in-domain items, after the D20 correction *and* the N9 audit
removed the two hypercube items from the domain:

| | board changed | tight / no change |
|---|---|---|
| **fires** | 3 | **1** |
| does not fire | 1 | 6 |

Fires on 2 (cap set), 4 (Kadison–Singer), 10 (parallel repetition), and — wrongly — on N8.
Sensitivity 3/4, specificity 6/7. Youden's **J = 0.607**, against the rule-less baseline's **1.000**:
lift **−0.393**.

**The domain condition has been patched twice, post hoc, each time by the item that broke it** — for
two-parameter families (D23, from N8) and for closure under the product (D27, from N9). Neither patch
is adopted. Two patches from two items is the signature of a rule being *fitted*, not tested; a third
should be read as a refutation rather than a repair.

**Collectivize a union bound**, 8 in-domain items: **2/2 sensitivity, 6/6 specificity**. The
refinement survives exactly the cases that killed the original — it fires on 4 and 8, and declines
on N1, N2, N8 and the three new independence twins.

The three new union-bound negatives (N11 maximum of n Gaussians, N12 balls into bins, N13 coupon
collector) are the cleanest possible true negatives: independence is exact, the target is a maximum,
so the union bound is not lossy at all and the refined rule has no excuse to fire. It doesn't.

### WITHDRAWN: the "strongest single test" was a confounded example

*Everything in this subsection is withdrawn. See `d20/N9-audit-result.md`.* An adversarial audit,
every computation of which was then verified independently, found that **the feasible set is not
closed under the Cartesian product**: the constraint is a density threshold, density is
multiplicative, and the product of two extremal examples occupies a *quarter* of Q_{n₁+n₂} rather
than half. So the target label was never read off the examples — there are no examples to read — and
both case 1 and N9 have been removed from the diagnostic's domain. Worse, the verdict flip is fully
reproduced by the simpler test *"does the lower bound match the upper bound to within a constant
factor?"*, which needs no product-law machinery at all. The original text follows, struck.

### ~~The strongest single test: the same problem on both sides of a board change~~

**N9 is case 1 after Huang.** Before the signing, the target's law is ℓ² (CFGS's own ⌈√n⌉
construction) and the bound's law is additive (log n from counting) — the laws differ and the
diagnostic fires. After the signing, `A² = nI` makes the bound's law ℓ² too, the laws agree, and
**the diagnostic stops firing** — correctly, because CFGS's construction attains ⌈√n⌉ and nothing
further comes off.

The same problem, the same diagnostic, opposite verdicts, driven entirely by a change in the
invariant's product law. That is a specificity test no cross-problem pair can give, and it is the
single result here most worth trying to break.

### The two findings that matter more than the counts

**1. The false negative on case 3 is principled, and it splits the catalogue.** Shannon's fractional
clique cover α\* is *already multiplicative* under the strong product — Shannon chose it for that
reason. Its product law was never wrong; it was merely **not tight**. So case 3's board change is a
different phenomenon from cases 1, 2, 4 and 10, and forcing it into the same entry is what made the
original "de-tensorize" look incoherent. N4 (Θ(C7)) behaves identically and is still open, which is
consistent: a tightness failure is not repaired by changing the law.

**2. N3 is the discriminator, and there is now a better-sourced reason for it than the one this file
originally gave.** N3 (3AP-free sets in [N]) is case 2's twin and carries the *same surface leak*.
The original reason given here was that `[N₁] × [N₂]` is not `[N₁N₂]` for AP structure, so the
product operation is absent. **Peluse (arXiv:2206.10037) gives a sharper one:** the density increment
costs **O(1) codimension per step in F₃ⁿ** (N_{i+1} ≍ N_i) but **N_{i+1} ≍ α^{O(1)}√N_i in [N]** —
which is precisely why the same argument yields 3ⁿ/n there and only N/log log N here. That is the
mechanism, stated by a survey author rather than inferred by us, and it should be preferred. The rebuilt diagnostic separates
them on an objective structural fact. The same distinction explains N7 against case 5, and 15
(Kelley–Meka) against case 2.

This is the first thing in the programme that tells a positive from its matched twin for a stated,
checkable reason.

## What this is not

- **Raw counts on n = 10 and n = 5.** Per the seed's own limit this is a counterexample generator,
  not a rate estimator. Near-perfect separation is what the design can show; a rate is not.
- **The circularity is reduced, not removed.** The rules are mechanical and read only objective
  fields — but *the assignment of the laws* was made by the same instance that restated the rules.
  What changed is that the judgement is now confined to **two closed-vocabulary fields** instead of
  free text, so it can be inter-rater tested the way the leak table was.
- **Product-law matching is not a replacement for the whole catalogue.** It has a stated domain,
  and 11 of 23 items fall outside it. Outside the domain it says nothing, which is the honest
  behaviour and the reason it takes no false positives.

## D20: the test that settles it — RUN, and the result is split

Three independent raters, blinded to the rule and to which items are positives, assigned
`target_law` and `bound_law` from the bound and the extremal construction alone. Inputs, filled
sheets and verbatim output are in `d20/`.

| | κ (Fleiss, 3 raters) | 95% CI | stop rule 0.6 |
|---|---|---|---|
| transformation label (step D baseline) | **0.048** | — | failed |
| `target_law` | **+0.811** | [+0.570, +1.000] | pass |
| `bound_law` | **+0.755** | [+0.494, +1.000] | pass |
| **the firing decision the rule uses** | **+0.618** | **[+0.220, +0.904]** | pass, but barely |

**What passed.** Moving the judgement onto two closed-vocabulary fields was a real improvement —
roughly a sixteenfold increase in κ over the transformation label, on the same kind of task. That
was the rebuild's central bet and the bet paid.

**What did not.** Two things, and both matter more than the headline.

1. **The rule reproduces far worse than its inputs.** κ = 0.618 on the firing decision against
   0.755–0.811 on the fields. That is structural, not noise: the rule consumes the *difference* of
   two labels, and disagreement concentrates on exactly the items where the two labels are close.
   The interval **[+0.220, +0.904]** straddles the stop rule badly. On 14 items the point estimate
   clearing 0.6 is not evidence that the rule clears it.
2. **The zero-false-positive claim did not survive.** Every rater fires on N8; one also fires on
   N2, another on N4. Per-rater false positives were 2, 1 and 2 against my 0.

**The most valuable single finding is not a κ.** It is *why* N8 fires. The domain condition —
"a product operation exists and the size parameter is additive" — is satisfied literally by disjoint
union, which moves **both** coordinates of a two-parameter family. Every case the diagnostic gets
right is a **single-parameter** family; its false positive is the two-parameter one. A candidate
repair is stated in `d20/N8-adjudication.md` and **deliberately not adopted**, because it was derived
from the item it would exclude — the same circularity the seed flagged and L2 caught.

**One rater's divergence is worth more than the counts.** Rater B declined to fire on case 4,
reading the matrix-Chernoff `log` penalty as "the max law with a logarithmic loss" rather than as an
additive law. The five-category vocabulary has **no way to express "the right law, degraded by a
log"** — which is arguably exactly what Kadison–Singer's board did. That is a gap in the vocabulary,
not a mistake by the rater.

### What D20 does not settle

The three raters share **one fixed encoding** of the inputs, written by the instance that wrote the
rules. This measures rater agreement *given* that encoding, not encoder-plus-rater agreement. It is
strictly weaker than L2's design and strictly stronger than no measurement.
