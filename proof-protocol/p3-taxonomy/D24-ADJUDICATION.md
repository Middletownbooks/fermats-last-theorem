# D24 — the vocabulary gap, adjudicated

*Verified by `tools/check_d24.py` (all checks pass, and it reproduces the published field κ of
**+0.811** and **+0.755** from `d20/score_output.txt` as a control on the reading).*

## The question, and the rule set in advance

D24 was opened on one observation: the five-value law vocabulary
`{multiplicative, additive, l2, max, none}` cannot express **"the right law, degraded by a log"**.
Rater B declined to fire on case 4 (Kadison–Singer) by reading the matrix-Chernoff penalty that way.

The debt fixed its own decision rule before any analysis: *"Do NOT add a category reflexively. Decide
first whether the gap explains other divergences; if it explains only case 4, it is a property of that
case, not of the vocabulary."*

## The answer: three items, and a second gap nobody named

There are **six** field-level divergences across the three rater sheets. Every one is classified,
with the raters' own words as the evidence:

| item / field | A \| B \| C | what explains it |
|---|---|---|
| `01-sensitivity` / bound | none \| max \| max | **vocabulary — degradation** |
| `02-cap-set` / bound | none \| additive \| none | **vocabulary — degradation** |
| `04-kadison-singer` / bound | none \| max \| additive | **vocabulary — degradation** (A vs B), *plus* a real disagreement (C) |
| `03-shannon-capacity-c5` / target | mult \| mult \| none | **vocabulary — one-directional law** |
| `N4-shannon-capacity-c7` / target | mult \| mult \| none | **vocabulary — one-directional law** |
| `N2-epsilon-nets` / target | max \| additive \| additive | **mechanism** — a genuine disagreement, *not* a vocabulary gap |

**The gap as stated explains three items, not one.** So by D24's own rule it is a property of the
vocabulary. And the striking part is *why*: in cases 1 and 2 **all three raters state the same
mathematics** and differ only on which word to force it into.

- **Case 1.** A: *"log(n₁+n₂) … is none of the shapes."* B: *"log(n₁+n₂) = max(log n₁, log n₂) + O(1),
  so the counting board obeys a max law."* C: *"equals max … up to an additive constant."* Verified:
  the difference is **≤ 1 exactly** (since n₁+n₂ ≤ 2·max), and the *ratio* → 1. Nobody is wrong; the
  vocabulary has no slot for *max + O(1)*.
- **Case 2.** A: *"3ⁿ/n^{1+ε} is not of the form cⁿ."* C: *"3ⁿ times a polynomial saving that does not
  tensor."* B reads the polynomial saving as additive. Verified: the multiplicativity defect is
  exactly `n₁n₂/(n₁+n₂)` — 500 at n₁=n₂=1000, against a main term of 3²⁰⁰⁰ ≈ 10⁹⁵⁴. A multiplicative
  main term times a non-tensoring polynomial factor, which is also not in the vocabulary.
- **Case 4.** A and B agree on the mathematics (*"degrades logarithmically"* / *"the max law with a
  logarithmic loss"*) and differ on the word; C reads a different mechanism. The item D24 was opened
  on carries **both** a vocabulary gap and a real disagreement.

**A second gap, which D24 did not name, explains two more items.** The vocabulary cannot say
**super**multiplicative. C codes `none` on both Shannon-capacity items because the finite quantity
strictly beats multiplicativity — verified: α(C₅⊠C₅) = 5 > 4 = α(C₅)², and 367 > 3⁵ = 243 for C₇ —
while A and B code `multiplicative` for the *limit*, B while explicitly writing *"α itself is only
supermultiplicative."* This is the exact distinction **twin N16 already carries** for border rank
(sub-multiplicative, not fully multiplicative). It was in the tree before this analysis and nobody
connected it to the vocabulary.

## The verdict: do not grow the vocabulary

Two reasons, and the second is decisive.

**1. The recode is worth less than it looks.** Closing both gaps post hoc would lift the field κ from
+0.811 to **+0.941** (target) and from +0.755 to **+0.930** (bound). That number is an *upper bound
obtained by fitting* — it recodes after seeing the disagreements — and `check_d24.py` prints it
labelled as such. It is not a measurement and must never be quoted as one.

**2. A new code does not decide the case it was invented for.** Under the rule as coded, case 4's
firing decision splits: A fires, B does not, C fires. Add `max-degraded` and the same question
survives intact — *is `max-degraded` equal to `max` for the purpose of firing?* If yes, B still
declines; if no, B fires. **The vocabulary cannot contain the decision, because the decision is about
magnitude, not about which law.** A sixth or tenth category relocates the judgement instead of
resolving it, and each new axis is one more forced choice of exactly the kind the raters already
disagree about (5 × {exact, degraded} × {two-sided, one-directional} is 20 cells, not 5).

**What already answers it.** The D28 one-line bound-strength test fires on case 4 for the stated
reason *"the argument needs δ ≲ 1/log n against a dimension-free truth: the gap is an unbounded log
factor."* It reads the **size** of the gap instead of naming a law, agrees with raters A and C, and
needs no category at all. That is the third independent time the machinery has turned out to be
surplus to a test that measures magnitude directly (D28, the ceiling register's two instances, and
now this).

## What this changes, and what it does not

- **D24 closes as answered, not as fixed.** The vocabulary keeps its five values and stays closed.
  The gaps are recorded here so that anyone reviving the product-law rule knows the labels are not
  merely noisy: in three of six divergences the raters agreed on the mathematics and were forced
  apart by the wording.
- **It slightly strengthens D20's split result rather than weakening it.** The fields agree even
  better than measured; the *rule* built on them still fails, and for a reason this analysis makes
  sharper — the rule consumes a *difference of names*, when what matters is a *size*.
- **It does not license the recode.** No κ in this tree may be restated at +0.941/+0.930. The
  published numbers stand at +0.811 and +0.755.
