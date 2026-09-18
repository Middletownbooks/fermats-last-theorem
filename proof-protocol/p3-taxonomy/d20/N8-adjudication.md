# N8: three raters against one reference

All three independent raters assigned `target_law = max`, `bound_law = l2` to N8 (discrepancy of
m sets on n points). My reference said `additive / additive`. The scorer's own limits note says:
*"where all three raters agree against me, I am the outlier."* So this is adjudicated, not defended.

## The mathematics

**Product operation: disjoint union of set systems.** Ground sets disjoint, so `n = n₁ + n₂` and
`m = m₁ + m₂`.

**Target.** Every set of S₁ lies entirely inside ground set 1. A colouring may therefore be chosen
independently on each ground set, and each system attains its own optimum. So

~~~
disc(S₁ ⊔ S₂) = max( disc(S₁), disc(S₂) )
~~~

That is the **max** law. The raters are right and my `additive` was wrong.

**Bound.** With `m/n` preserved, `√(n log(m/n))` gives

~~~
B(S₁ ⊔ S₂)² = (n₁ + n₂) log(m/n) = B(S₁)² + B(S₂)²
~~~

That is the **l2** law. The raters are right again; my `additive` was wrong here too.

**So the reference is corrected to `max / l2`.** The two laws differ, so product-law matching
**fires** — on an item whose truth is *tight* (`√(n log(m/n))` is the answer). That is a
**genuine false positive**, not a rater error.

## What this costs, and what it exposes

`DIAGNOSTIC.md` claimed **zero false positives over eight negatives**. That claim is **withdrawn**.
It was computed from my own assignments, and one of them was wrong in the direction that flattered
the diagnostic.

The interesting part is *why* the diagnostic fires here, because it is not a slip in the rule. It is
a defect in the rule's **domain condition**.

The stated condition is: *a product operation exists and the size parameter is additive under it.*
Disjoint union satisfies that literally — `n` adds. But it does not preserve the problem's
**parameterisation**: the tight bound `√(n log(m/n))` is tight as a function of the *pair* `(n, m)`,
and disjoint union moves both coordinates at once. Under such an operation the target and the bound
can legitimately obey different laws with **no board change available**, because the mismatch is an
artefact of the operation rather than of the invariant.

Compare the cases where the diagnostic works. Cap sets: `A₁ × A₂` is a cap in `F₃^{n₁+n₂}` and the
family is parameterised by `n` alone. Hypercubes: `Q_{n₁} × Q_{n₂} = Q_{n₁+n₂}`, again one
parameter. Direct sums for Kadison–Singer: one parameter, the block count. **The diagnostic's
successes are all single-parameter families. Its false positive is the two-parameter one.**

## The repair, stated as a hypothesis and not adopted

> Strengthen the domain condition: the product operation must act on the family's **full parameter
> vector** in a way that keeps the target's defining problem the same problem — not merely be
> additive in one coordinate.

This is **not** applied to the data. It was derived from the item it would exclude, which is the
exact circularity the seed flagged for product-law matching in the first place and which L2 then
caught. Adopting it here would repeat that mistake at one remove.

What it needs: items chosen by someone who has not seen this adjudication, including two-parameter
families where the board *did* change. If the strengthened condition survives that, it is a finding.
Until then N8 stands as a **recorded false positive** and the diagnostic's specificity is
7/8, not 8/8.

## Also recorded

- **Rater C** additionally fired on N4 (Θ(C7)), by assigning `target_law = none` on the ground that
  367 in the fifth power strictly beats α(C7)⁵ = 243, so the quantity is supermultiplicative rather
  than multiplicative. That is a defensible reading, and it is the same reading C gave to case 3
  (C5). It is a **single-rater** divergence, not unanimous, so it is recorded but does not move the
  reference.
- **Rater A** additionally fired on N2 (ε-nets), assigning `target_law = max`. Single-rater.
- **Rater B** declined to fire on case 4 (Kadison–Singer), reading the matrix-Chernoff `log`
  penalty as "the max law with a logarithmic loss" rather than as an additive law. That is a **false
  negative on a positive** and it is the most interesting of the three single-rater divergences,
  because it shows the five-category vocabulary has no way to express "the right law, degraded by a
  log" — which is arguably exactly what case 4's board did.
