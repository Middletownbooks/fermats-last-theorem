# My own answer to the N9 attack, written before the auditor reported

Recorded first so that the comparison afterwards is between two independent answers, rather than me
agreeing with whichever one arrives. Timestamped by its commit.

## On attack point 1: is `bound_law` a real law, or just substitution?

**The objection is largely right, and it is sharper than the task list puts it.**

Board B's bound is √n. Substituting an additive parameter gives

~~~
√(n₁ + n₂) = √( (√n₁)² + (√n₂)² )
~~~

which is the l2 law **exactly**. Board A's bound is (1/2)log₂ n, and log(n₁+n₂) is not log n₁ + log
n₂, not a product, and only max + O(1). So there *is* an asymmetry: √ is (up to scaling) the unique
functional form for which substituting an additive parameter yields an exact l2 law, while log yields
no exact law at all. That is why the raters split between "none" and "max" on Board A and were
unanimous on Board B.

**But the objection survives in a stronger form that I did not previously state.** If `bound_law` is
computed by substituting an additive `n` into the bound's formula, then it is a property of *the
bound's growth rate in n*, not of the invariant's compositional behaviour. And `target_law` read the
same way would be a property of the target's growth rate. Under that reading,

> "the laws differ" ⟺ "the bound's growth rate differs from the target's" ⟺ "the bound is not tight"

and the diagnostic reduces to **"is the bound the wrong order of magnitude?"** — which is very close
to a restatement of the thing it is supposed to predict, and would make the whole rule near-vacuous.

**What stops that reduction being exact is N8**, and this is the part I had not connected. In N8
`target_law` was read off the extremal construction **under the product operation** (disjoint union:
colour each side independently, so max), *not* off the target's growth rate in n. Those are different
quantities, and there the bound is tight while the laws still differ. So:

- where the product operation is the family's own parameterisation (cap sets, hypercubes, direct
  sums), `target_law` and "growth rate in n" coincide, and the diagnostic is close to the vacuous
  reading;
- where it is not (disjoint union of two-parameter systems), they come apart — and that is exactly
  where the diagnostic takes its false positive.

**So the N8 defect (D23) and the vacuity objection are the same defect seen from two sides.** When the
product operation matches the parameterisation, the rule is nearly a tautology; when it does not, the
rule is wrong. Neither regime is one where it does independent work. That is a substantially worse
finding than D23 alone, and I did not see it until the attack was framed.

**My verdict on point 1: the claim MOVES.** `bound_law` should not be described as the invariant's
product law when it is computed by substitution. Either it must be computed from how the *invariant*
composes (for Huang: how the signing of Q_{n₁+n₂} relates to signings of the factors — a real
question with a possibly different answer), or the rule must be restated as what it actually is.

## On point 2, tightness

I expect this to survive with a caveat about rounding: Huang gives Δ ≥ √n and CFGS give ⌈√n⌉, so for
non-square n there is a gap of less than 1 between the bound and the construction, closed only
because Δ is an integer and ⌈√n⌉ is the least integer ≥ √n. That is a genuine match for integer Δ.
I am not confident the CFGS construction attains ⌈√n⌉ for **every** n rather than for a special form,
and if it does not, "nothing further comes off" is overstated for the remaining n.

## On point 3, what the sensitivity conjecture needs

I expect this to move. The degree bound gives s(f) ≥ √(deg f) (via Gotsman–Linial), and the
sensitivity conjecture is a polynomial relation between sensitivity and block sensitivity or degree.
Huang's result closes the relation with a *specific* exponent; the question of the **optimal**
exponent is a different statement and, as far as I know, was not closed by it. If so, calling the
problem "tight, nothing further comes off" conflates the degree bound with the conjecture, and the
twin's description should say which one it means.
