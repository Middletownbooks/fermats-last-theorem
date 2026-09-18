# N9 audit: the claim does not survive

Task 3 asked for an adversarial attack on N9 by an agent that did not build it, and named three
pressure points. Every load-bearing computation in the auditor's reply was then verified
independently in `../p1-retrodiction/tools/check_n9_audit.py` (26 checks, all passing, standard
library only). **The audit is correct.**

My own answer was recorded *before* the auditor reported, in `N9-my-answer-before-audit.md`, so the
comparison below is between two independent analyses.

## Point 1 — the product law. MOVES, and worse than I had it.

### What I got right
I said the claim moves, and that if `bound_law` is computed by substituting an additive `n` into the
bound's formula then it is a property of the bound's **growth rate**, not of the invariant's
composition — so "the laws differ" collapses towards "the bound is the wrong order". The auditor
reached the same conclusion independently and put it more sharply: *"the rule is measuring bound
strength while wearing a product-law costume."* Two independent analyses converging on that is the
strongest evidence in this file.

### What I missed, and it is decisive
**The feasible set is not closed under the product operation.** The constraint is a *density*
threshold — more than half the cube — and density is **multiplicative**:

~~~
|H₁|·|H₂| ≈ 2^{n₁-1}·2^{n₂-1} = ¼·2^{n₁+n₂}      required: > ½·2^{n₁+n₂}
~~~

Verified: at n₁=n₂=25 the product occupies 0.2500 of Q₅₀ against a required 0.5. **The product of two
extremal examples is not a feasible instance of the problem.** So "take the product of the extremal
family and measure" has *no value here at all*, and the `l2` target label was never read off the
examples — it was read off the closed form `⌈√n⌉` by substitution. The two sides of the rule were
being computed by two different conventions, and I did not notice.

And the honest product law, if one computes it anyway, is **additive**, not l2: Cartesian product
degrees add exactly, so Δ(H₁ □ H₂) = Δ(H₁) + Δ(H₂) = ⌈√n₁⌉ + ⌈√n₂⌉ ≥ ⌈√(n₁+n₂)⌉.

### What I also missed: the label is split-dependent, and the signal is tiny

| split | truth | l2 | max | additive | spread |
|---|---|---|---|---|---|
| 50 : 50 | 10 | 11.31 | 8 | 16 | 80% |
| **99 : 1** | 10 | **10.05** | **10** | 11 | **10%** |
| 75 : 25 | 10 | 10.30 | 9 | 14 | 50% |

At the 99:1 split all three labels agree to within 10%. The "law" is **not an invariant of (problem,
⊗)** — it depends on an arbitrary choice of split. Worse, verified: `√(n₁+n₂) ≤ √2·√max` always, and
`|½log₂(n₁+n₂) − max| ≤ ½` always. So the **most** signal the l2-versus-max distinction can carry is
a factor of **√2**, and it was being used to flag a `log n` versus `√n` gap — a polynomial one. The
rule cannot be doing the work advertised.

### Credit where the auditor gave it
The certificate side *does* have a genuine composition law, and I had not checked it. Given signings
with A² = cI, the **parity-twisted** gluing `A₁⊗I + D⊗A₂`, with `D = diag((−1)^{|x|})`, satisfies
`A² = (c₁+c₂)I` — because `A₁` is supported on edges, which reverse parity, so `A₁D = −DA₁` and the
cross term dies. Verified for five splits up to n=5, together with the fact that the **naive** gluing
`A₁⊗I + I⊗A₂` gives `(c₁+c₂)I + 2A₁⊗A₂` and is *not* a scalar square. That distinction is real.

But it does not save the claim: the certificate's natural parameter `c` is additive and the bound is
`√c`. Board A's parameter is also additive and its bound is `½log₂`. **Same structure, different
function** — which is bound strength, not composition behaviour.

### The confound
The simpler rule *"does the best known lower bound match the upper bound to within a constant
factor?"* reproduces **both** verdicts exactly, needs no product-law machinery, and is immune to the
rater dispute over Board A's label. An over-determined example cannot be evidence for a specific
mechanism.

## Point 2 — tightness. SURVIVES, and my caveat was unnecessary.

I predicted it would survive "with a caveat about rounding", and doubted the construction held for
all `n`. **Both doubts were wrong, in the conservative direction.**

- **Integrality closes it.** Δ is an integer, so `Δ ≥ √n ⟺ Δ ≥ ⌈√n⌉`. Huang's theorem therefore gives
  the integer bound `⌈√n⌉` for **every** n, and CFGS meet it exactly. Zero room, all n. The commonly
  quoted hedge "tight at perfect squares" is an artefact of not invoking integrality — it applies to
  the **eigenvalue** functional (λ₁ ≥ √n, attained only at squares), not to the degree functional.
- **Monotonicity makes the construction at squares sufficient.** `f(n) ≤ f(n+1)`: split Q_{n+1} into
  two copies of Q_n, one holds ≥ 2^{n-1}+1 of the 2^n+1 vertices, and deleting vertices only lowers
  degrees. So CFGS at perfect squares already forces `f(n) = ⌈√n⌉` everywhere. Hand-checked at
  n = 1, 2, 3.

**The auditor's one unverifiable item is closed from work already in this repo.** It flagged that it
could not confirm CFGS's exact upper bound. `../CITATIONS.md` row `C1-bound`, verified last session,
states it: CFGS construct a (2^{n−1}+1)-vertex induced subgraph of maximum degree **⌈√n⌉**. No
softening needed.

## Point 3 — "nothing further comes off". MOVES: two statements were conflated.

I predicted this and identified that the optimal exponent is a separate question. The auditor supplied
the chain:

- **Gotsman–Linial** converts the cube statement into `deg(f) ≤ s(f)²`. This step **is** tight —
  reversing it on the CFGS construction gives functions with `deg = s²`.
- **Nisan–Szegedy**, sharpened by **Tal**, gives `bs(f) ≤ deg(f)²`, hence `bs ≤ s⁴`. This step is
  **not** known tight: the best separation is Kushilevitz's `bs = Ω(deg^{1.63})`.
- Best known separation overall is `bs ≥ (2/3)s² − s/3` (Ambainis–Sun). **The true exponent is open
  in [2, 4]**, conjectured 2.

The chain cannot be tight because steps 1 and 2 are extremal on *different* functions. So: the
**qualitative** sensitivity conjecture is resolved — that is Huang's contribution — and the
**quantitative** version is wide open, with the loss living in the `deg → bs` step, which has nothing
to do with the cube.

## What was changed

1. **Case 1 and N9 both leave the diagnostic's domain**, marked `applicable: false` with the closure
   reason. Not because the mathematics is wrong but because *the diagnostic is not defined there*:
   its target label requires reading a product of extremal examples, and no such product exists.
2. **N9 is demoted.** `DIAGNOSTIC.md` called it "the single result most worth trying to break". It was
   instead a **confounded** example, over-determined by a simpler bound-strength test. That sentence
   is withdrawn.
3. **N9's tightness claim is scoped**: `f(n) = ⌈√n⌉` is determined for all n and nothing further comes
   off *that functional*; the sensitivity question is **not** closed.
4. **The domain condition has now been patched twice, post hoc, each time by the item that broke it** —
   once for two-parameter families (D23, from N8) and once for closure under the product (D27, from
   N9). Two patches from two items is the signature of a rule being **fitted rather than tested**, and
   neither patch is adopted for that reason.
