# The baseline (task 2): the diagnostic loses to no diagnostic at all

`DIAGNOSTIC.md` reported its 2×2s as **raw accuracies**. This programme's own rule, inherited from
the seed and written into `p1-retrodiction/README.md`, is: *"scores are lift over the telegraph
baseline, never raw accuracy."* So the headline result was stated in a unit the repo forbids. This is
the baseline it should have been stated against.

## The baselines, chosen and stated before running

The seed's telegraph arm was "the leak table with no procedure". The rebuilt diagnostic reads **no
leak table**, so that exact arm does not apply. Three baselines were fixed in `tools/baseline.py`
before any was run:

| | baseline | what it tests |
|---|---|---|
| **B0** | fire on everything in domain | a floor |
| **B1** | fire on nothing in domain | the other floor |
| **B2** | a rater given the **same item text**, asked only *"was that bound superseded by a fundamentally different approach, or was it essentially the best available?"* — no rule, no vocabulary, no mention that a rule exists | whether the diagnostic **adds** anything |

Scored with **Youden's J = sensitivity + specificity − 1**, because a constant rule cannot game it:
B0 and B1 both score J = 0 by construction, whatever the class balance.

## Results

~~~
13 in-domain items: 5 positive, 8 negative

  B0  fire on everything      TP 5  FN 0  FP 8  TN 0   J = +0.000
  B1  fire on nothing         TP 0  FN 5  FP 0  TN 8   J = +0.000
  B1b coin flip (20k trials)  mean J = -0.001, 95% within [-0.550, +0.550]

  product-law matching        TP 4  FN 1  FP 1  TN 7   J = +0.675
  B2  rule-less rater         TP 5  FN 0  FP 0  TN 8   J = +1.000
~~~

- **Against the floors:** the diagnostic clears them, and only 0.97% of coin flips reach J ≥ 0.675
  on 13 items. Necessary, and not impressive — clearing a constant rule is the minimum.
- **Against B2: the lift is −0.325.** The rule-less rater scored **perfectly**: 5 of 5 positives,
  8 of 8 negatives, no errors. The diagnostic is **worse than no diagnostic**.

## Why B2 was perfect, and what that costs the whole benchmark

**The recognition probe came back 13 of 13.** The rater named every problem: *"the sensitivity
conjecture"*, *"cap set problem"*, *"Kadison–Singer / Weaver KS₂"*, *"Shannon capacity of the
7-cycle"*, *"Sauer–Shelah lemma"*. It was not inferring from the product structure. **It was
recalling the answers.**

That is step D's 100%-recognition finding and L2's 5-of-5, reproduced a third time, and this time
with the consequence made explicit:

> **A contaminated rater ceilings this benchmark perfectly. So the benchmark cannot measure a
> diagnostic's value at all.** Every retrospective number in this programme — the withdrawn 4/0, the
> corrected 4/1, the union-bound 2/2 and 6/6 — is a *weaker* version of recall, measured against a
> ceiling that recall already reaches.

This does **not** show product-law matching is mathematically worthless. The Huang signing really
does change the product law of the cube spectrum. It shows something narrower and worse for the
programme: **retrospective cases cannot tell us whether it helps**, because anything that can compute
the diagnostic can also just remember the answer.

## What survives

- **The seed was right about L4, and it is now measured rather than argued.** *"The only fully clean
  estimate is prospective."* Three independent measurements now say the retrospective arm is
  saturated by recall.
- **`prospective/` is not one instrument among several. It is the only one.** Its five sealed
  predictions are worth more than every 2×2 in this tree.
- **The negative twins still do real work** — just not the work claimed. They cannot validate a
  diagnostic against a recalling rater, but they did catch N8, which exposed the domain defect
  (D23). Falsification survives where measurement does not.
- **D20's field κ still stands.** Whether two raters agree on `target_law` is a question about
  reproducibility of an encoding, not about predictive value, and recall does not inflate it.

## What must change in how this repo is read

1. **Do not quote any retrospective 2×2 as evidence that a diagnostic works.** Quote it, if at all,
   as evidence that a diagnostic is *self-consistent*, against a baseline that beats it.
2. **The headline claim of the rebuild is withdrawn twice over** — once by D20 (the
   zero-false-positive figure), and once here (the remaining figures have negative lift).
3. **n = 1 rater on 13 items.** This is a single observation, not a rate. But the direction is
   stark, the recognition probe explains it, and it agrees with two prior measurements. It would take
   a strong result to overturn it, not a noisy one.
