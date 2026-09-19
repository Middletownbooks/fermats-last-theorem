# The ceiling register

*Data: `ceilings/register.jsonl` (append-only, sealed). Inputs: `ceilings/*.json`, kept as the
exact text that was sealed. Tool: `tools/ceilings.py` (`add` / `amend` / `verify` / `report`).
Debt **D32**.*

## Why this exists

`D25` measured that the retrospective arm is **saturated by recall**: a rater with no rule separates
positives from negative twins perfectly, and names every problem while doing it. Underneath that
result is a quieter problem which no amount of rater blinding fixes:

> **Every leak in the retrospective corpus is one *we* identified after the board was left.** The
> item's ground truth is our own hindsight about a famous result.

A **ceiling statement** inverts that. It is a claim, *in print and before the outcome exists*, by the
people working on a board, that the board **cannot reach the known or conjectured truth** — with a
number on both sides. The cap is theirs, not ours; the label is contemporaneous, not reconstructed.
One of those was found by accident while sourcing control 15, and looking for the same shape now
outranks adding more twins.

Two uses, and only the first is uncontaminated:

1. **An open ceiling is a prospective item with a published resolution criterion.** No rater can
   recall the answer, because the answer does not exist. The seal is what makes it binding.
2. **A resolved ceiling supplies a label written down before the resolution.** That does not blind a
   rater who remembers the outcome — it fixes the *encoding*, so the item does not consist of us
   explaining after the fact why the board had to be left.

**This register is not part of the prospective arm and its counts must never be pooled with it.**
The arm watches new arXiv postings and resolves in weeks. A ceiling can stand for a decade. One
number over both would let a slow item dilute a fast one.

## What counts as evidence

| tier | meaning | in the register |
|---|---|---|
| `STATED-BY-AUTHORS` | the people who built or pushed the board say the board is capped, with a number | 1 |
| `STATED-BY-EXPOSITOR` | a survey or exposition says it, not the authors | 0 |
| `DERIVED-FROM-PRIMARY` | we computed the cap from a primary statement; the derivation must say where it is checked in code | 1 |
| `CLAIMED-POST-HOC` | stated only *after* the board was left | **refused by the tool** — this is hindsight, which is the thing the register exists to avoid |

A second axis is recorded separately, because the two instances differ on it: whether the **truth**
the cap falls short of is a `THEOREM` (a construction proves the target is reachable) or a
`CONJECTURE` (it is believed). A cap relative to a conjecture is a weaker object and says so in the
record.

**Disqualifiers**, so the register does not fill up with barrier talk:

- No number on one of the two sides. "This method seems to be nearing its limits" is not a ceiling.
- A cap on *this argument's parameters* rather than on the board ("our constant is not optimal").
- Retrospective attribution of a barrier after the board was left — the tool refuses this tier.
- A cap whose value does not fall short of the truth. The one exception is an **unattained
  supremum**, which the second instance forced: GPY's board needs ρ > 4 and reaches every value
  *below* 4 for every *k*, so the cap and the requirement are the same number and the board misses
  by an ε no *k* closes. That is declared with `cap_attained: false` plus a `boundary_note`, rather
  than encoded as 3.999 to satisfy a strict inequality.

## The two registered instances

### 1. Roth in [N], density increment with Bohr sets — **open**

> *"Of course, the Behrend exponent of 1/2 would be the final target, but this seems quite far out of
> reach still; indeed, an exponent of 1/3 (or perhaps even 1/4) seems to be the limit of any argument
> that uses any sort of 'density increment' argument with Bohr sets (whether using Kelley–Meka ideas
> or a more traditional Fourier analytic approach)."*
> — Bloom–Sisask, arXiv:2302.07211v3

Cap **1/3** on the exponent *e* in `|A| ≤ exp(−c(log N)^e)N`; truth at **1/2**, a `THEOREM`
(Behrend's construction). The published record is 1/12, with 1/9 and 5/41 announced in the same
paragraph and 1/7 believed to be the method's natural limit — so **even the believed limit of the
method is less than half way to the board's own stated cap, which is itself short of the truth.**

What the two diagnostics say about it is the interesting part:

- **Product-law matching is `NOT-APPLICABLE`.** [N] has no product structure of the kind the rule
  reads — that absence is twin N3's load-bearing claim, and the primary source states it outright.
  The rebuilt diagnostic is *silent* on the one item in this tree whose leak is sourced rather than
  reconstructed.
- **The one-line bound-strength test (D28) fires**, because 1/12 is strictly weaker than 1/2.

The prediction sealed with the record is the **authors'**, adopted rather than formed independently:
the exponent will not pass 1/3 on that board. It is registered to test the register, not to display
judgement. Horizon: unknown, probably long, and stated as a limitation rather than sold as a feature.

### 2. GPY's one-dimensional sieve — **held, and the board was left**

The criterion is `(1/2)·θ·ρ_k(F) > 1`. For the one-variable *F*, `ρ_k(F) → 4` and never reaches it,
**independently of k** (sup **3.9995** at k = 10⁹, tabulated in `tools/check_citations_response.py` §(d)).
Under Bombieri–Vinogradov's θ = 1/2 the criterion therefore caps at exactly the value it must exceed.
The *requirement* θ > 1/2 is stated by the source; the *cap* is derived here, so the tier is
`DERIVED-FROM-PRIMARY`, and the truth — bounded gaps, in 2005 — was a `CONJECTURE`.

The cap held, and the advance came **twice, both times by leaving a board**:

- **Maynard–Tao** left the *sieve* board: a multidimensional sieve makes the ratio grow like log *k*
  (0.5785 at k = 105, **7.564** at k = 10⁶, against the one-variable cap of 4). That is case 7a, the positive.
- **Zhang** did *not* leave the sieve board. He beat the θ > 1/2 requirement by changing the
  *equidistribution* board **one level down** (smooth moduli, Q = x^{1/2+η}, δ = 1/1168). That is
  control 16, and it is why debt **D30** exists.

**The lesson the second instance forces on the first:** a ceiling names *which* board is capped, and
an advance can come from leaving a **different** board than the one the cap is about. So a
resolution must record the **level** at which the board changed, not merely that one did.

Note also that the two instances are read by *different* tests — the Roth cap is a bound against a
construction, which the one-line test can read; the GPY cap is on a *criterion*, which it cannot.
**Neither test covers both instances.** That is the third independent appearance of the D28 finding:
the machinery is not merely surplus, it is silent exactly where the sourced item is.

## Candidates, and what each one needs

Named from memory, so **each is a candidate and none is a register entry**: this project's standard
is a source reached in-session, and egress is blocked. What each needs is one document.

| candidate | the board | what to look for |
|---|---|---|
| Selberg's parity problem | sieve methods | Selberg's own statement that a sieve cannot distinguish an even from an odd number of prime factors, with the factor-2 loss quantified. Left by Friedlander–Iwaniec's asymptotic sieve. |
| the logarithmic barrier in Roth's theorem | Fourier-analytic density increment | a pre-2020 statement of *why* `1/log N` was a barrier rather than just the record. Bloom–Sisask's own "Breaking the logarithmic barrier" is the resolution, not the ceiling. |
| Kakeya in F_q^n below n/2 | bush and hairbrush arguments | a statement that the purely geometric arguments cannot pass n/2 — this would pair with case 5, whose two regimes already leak differently. |
| the laser method's limit for ω | laser method on the Coppersmith–Winograd tensor | **a proved barrier, not a stated one** (Ambainis–Filmus–Le Gall: the method on that tensor cannot give ω < 2.3078). |

That last row would need a **`PROVED` evidence tier**, which is *deliberately not added yet*: the
standing rule in this project is that catalogues shrink before they grow, and a tier with no instance
is exactly the speculative growth that rule is for. Add the tier when the instance arrives, with its
source.

## A rejected candidate, recorded because it sits on the boundary

The Huang transcript supplied one near-miss, and it **fails the test** — which is worth recording,
because a register whose tiers never exclude anything is not a register.

Huang's concluding remarks note that his Theorem 1.5 gives only `bs(f) ≤ s(f)⁴`, while the best known
separation is quadratic (Ambainis–Sun: `bs = (2/3)s² − (1/3)s`), and suggest closing the gap by
applying the spectral method to boolean functions rather than to the hypercubes. Numbers on both sides
— exponent 4 against exponent 2 — and a pre-resolution statement by the author.

But it is a **suggested route, not a stated ceiling**: he does not claim the present board *cannot*
reach the quadratic. Under the disqualifiers above that is "a cap on this argument's parameters rather
than on the board", so it is not an entry.

It did expose one thing about the instrument. This quantity is **smaller-is-stronger** — a smaller
exponent in `bs ≤ s^C` is a better theorem — whereas both registered entries are larger-is-stronger,
so `ceilings.py`'s `cap_value < truth_num` check would have rejected it on the wrong grounds. A
`direction` field would be needed, and it is **deliberately not added**, for the same reason as the
`PROVED` tier: no accepted instance requires it yet, and catalogues shrink before they grow.

## The first amendment, recorded because the log is append-only

The first thing that happened to this register was that one of my own figures inside a sealed record
was wrong: `0.55` for a quantity that is `0.5785`. The record could not be edited without making its
seal meaningless, so the correction is a **second sealed record** naming the field, the old text, the
new one and the reason — `ceilings.py amend`. The original line stays readable. The figure the entry
actually leans on (7.564 at k = 10⁶ against a cap of 4) was unaffected, but the mechanism is the point:
this programme has retracted its own claims twice, and the standard is to record, not to erase.

## Honest limits

1. **One open instance is not a measurement.** Two items, one of which is already resolved and
   famous, cannot estimate anything. The register is an instrument and an argument about item design.
2. **The open instance may not resolve for years.** A benchmark cannot be validated on items that
   slow. The register's claim is that its labels are not hindsight — not that it is fast.
3. **A resolved ceiling is still recall-contaminated for raters.** Everyone knows Maynard–Tao. What
   it fixes is the encoding, not the blinding.
4. **The Roth prediction is not mine.** It is the authors', adopted. A register full of adopted
   predictions measures the literature's calibration, not a diagnostic's — which is worth having, and
   is a different claim.
