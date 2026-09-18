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

**Product-law matching**, 10 in-domain items:

| | board changed | tight / no change |
|---|---|---|
| **fires** | 4 | **0** |
| does not fire | 1 | 5 |

Fires on 1 (sensitivity), 2 (cap set), 4 (Kadison–Singer), 10 (parallel repetition). **Zero false
positives on five negative twins.**

**Collectivize a union bound**, 5 in-domain items: 2/2 sensitivity, 3/3 specificity. The refinement
survives exactly the cases that killed the original — it fires on 4 and 8, and correctly declines on
N1, N2 and N8, which is the specificity the seed said was missing.

### The two findings that matter more than the counts

**1. The false negative on case 3 is principled, and it splits the catalogue.** Shannon's fractional
clique cover α\* is *already multiplicative* under the strong product — Shannon chose it for that
reason. Its product law was never wrong; it was merely **not tight**. So case 3's board change is a
different phenomenon from cases 1, 2, 4 and 10, and forcing it into the same entry is what made the
original "de-tensorize" look incoherent. N4 (Θ(C7)) behaves identically and is still open, which is
consistent: a tightness failure is not repaired by changing the law.

**2. N3 is the discriminator, and it is the case the leak-based version could not do.** N3 (3AP-free
sets in [N]) is case 2's twin and carries the *same surface leak*. But `[N₁] × [N₂]` is not
`[N₁N₂]` for arithmetic-progression structure, so 3AP-free sets do not multiply as they do in
F₃ⁿ — the product operation that makes case 2 fire is **absent**. The rebuilt diagnostic separates
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

## The one test that settles it

Have raters who have **not seen these rules** assign `target_law` and `bound_law` blind, from the
bound and the extremal construction alone, and compute κ on those two fields.

- **κ ≥ 0.6** where the transformation label scored **0.048** ⟹ the rebuild did its job: the
  judgement was moved onto a field that reproduces.
- **κ < 0.6** ⟹ this is one more unreproducible ranking, and it should be reported as such rather
  than defended.

`../p1-retrodiction/tools/kappa.py` already implements the stop rule. It needs the two-field
template, which is the next concrete piece of work here.
