# Pre-registration — Report Q: does carry-over transmit anything when the
# receiving round provably cannot re-derive it?

Committed before any Round-3 search is run. Every falsifiable prediction is in
section 6 and will be scored as written, including the ones that fail.

## 1. What Report P left open

Report P's verdict was RESULT C: carried Round-1 vocabulary does not outperform
carrying nothing, at matched budget and matched symbol count, and its section 4
gave the mechanism — Round 2's own formation stage re-derives every
non-degenerate Round-1 term at the same price, because **both rounds run the
same procedure at the same limits**. Its section 12 states the condition the
loop needs:

> `V_{k+1} ⊄ reachable(V_k under one round's own formation budget)`

and names the first fix: *"Make each round's formation budget strictly smaller
than the depth of the structures being sought … the budget must be cut in the
body size, not the number of stages."*

That is the only intervention tested here. Nothing in `termform/` or
`termform2/` is modified; Reports M and P and their artifacts stay
byte-identical.

## 2. The intervention

Quantifier bodies in this language have odd sizes: an atom costs 1 and a binary
operation costs `1 + a + b`, so bodies come at sizes 1, 3, 5, 7. Round 1 and
every Round-2 condition run `form_leaves(size1=3, size2=5)`. **Round 3 runs
`size1=3, size2=3` in both stages**, which removes exactly the size-5 bodies
and leaves the two-stage structure and everything else untouched.

Six terms that Round 2's condition A formed for itself at body budget 5 require
a size-5 body, and are therefore candidates for a vocabulary that is outside the
receiving round's reach:

| term | printed form | body size |
|---|---|---|
| `bit_length` | `least(k: (n // (2 ^ k)))` | 5 |
| `even_divisors` | `count(k: (n % (k + k)))` | 5 |
| `isqrt` | `count(k: (k - (n // k)))` | 5 |
| `n_minus_n_div_spf` | `count(k: (n // (k * <spf>)))` | 5 |
| `v_2` | `count(k: (n % (2 ^ k)))` | 5 |
| `sqdiv` | `count(k: (n % (k * k)))` | 5 |

## 3. Provenance of the carried set, and the certificate

**Prior round.** Round 2 condition A at the honoured budget, committed as
`termform2/round2b_A.json`. Its certified set is the 13 untargeted library
matches plus the 5 reached targets recorded there.

**Promotion rule.** The frozen rule from `round1_manifest.json`, quoted and
applied mechanically, with no hand selection:

> promote every certified term, plus every formed term appearing as a NAMED UNIT
> inside a certified term.

**Filter.** The carried set for condition B3 is the promoted set restricted to
terms **certified unreachable at body budget 3**. The filter is the
intervention; condition B3all carries the unfiltered set so its contribution is
measured rather than assumed.

**Certificate, run before any condition is scored.** The complete body space at
budget 3 is enumerated with the beam switched off, and each carried term's value
vector on TRAIN is checked absent from it. A carried term that turns out to be
formable at budget 3 is **struck from the carried set**, and the strike is
recorded in the report. This is the check Report P's leakage audit performed too
late to protect target T3.

## 4. Conditions

Objects, splits and the invariant library are exactly Report P's, unchanged:
TRAIN 2–40, RESERVE 41–55, HOLDOUT 56–90, EVALQ 121–160, pairwise disjoint and
asserted in code. Targets are the 13 in `termform2/invariants.py` `TARGETS`,
unchanged and not re-chosen: `is_prime, is_square, n_div_spf, gpf, omega, Omega,
is_squarefree, rad, v_2, sigma, is_prime_power, phi, v_spf`.

| condition | body budget | carried vocabulary | carried cost |
|---|---|---|---|
| **A3** | 3 | none | — |
| **B3** | 3 | the certified-out-of-reach promoted terms | 1 |
| **C3** | 3 | the same NUMBER of random out-of-reach formed terms, seed 20260919, excluding anything semantically equal on TRAIN to a B3 term | 1 |
| **D3** | 3 | the B3 set | its expanded size |
| *B3all* | 3 | every promoted term, filter off | 1 |
| *A3+* | 3 | none, outer budget raised to cost 7 with beam 2400 | — |
| **A5** | 5 | none | — |

Italic rows are exploratory and are declared so here, before any result.

**The outer search is UNBEAMED at cost ≤ 5 in every non-italic condition.** The
body cut shrinks the atom set enough to enumerate the whole space, so the
comparisons carry no beam artefact. This matters because Report P's one positive
result for carry-over dissolved when an unbeamed control was run.

**Symbol count is not matched** and cannot be: A3's atom set is whatever its own
formation produces, and B3 adds the carried terms to it. C3 is the control for
that — same count, same provenance, different mathematical content — exactly the
role Report P's condition C played.

## 5. What counts as a result

* *certified invariant*: a term whose value vector matches a library invariant on
  TRAIN, then RESERVE, then the frozen HOLDOUT. HOLDOUT is touched once per
  condition, after selection.
* *target reached*: a certified match to one of the 13 targets.
* every reached target goes through `stages/disagreement.resolve` with RESERVE as
  the probe reserve and `assert_disjoint(RESERVE, HOLDOUT)` called first, and
  through `stages/abstention` licensing before HOLDOUT is read.
* `R(s)` is the set of distinct value vectors on TRAIN reachable at outer cost
  ≤ s, reported per level as in Report P.

## 6. Falsifiable predictions

| | prediction |
|---|---|
| **Q-1** | A3 certifies strictly fewer invariants than A5 — the body cut must bite, or nothing else here means anything |
| **Q-2** | B3 reaches at least **two** targets that A3 does not |
| **Q-3** | B3 certifies at least as many invariants as A3 |
| **Q-4** | B3 reaches more targets than C3 |
| **Q-5** | D3 reaches the same targets as A3, not as B3 |
| **Q-6** | A3+ does **not** close the gap: it reaches fewer of B3's extra targets than B3 does |
| **Q-7** | `is_squarefree` is reached by B3 and not by A3 |
| **Q-8** | `|R_B3(5)| > |R_A3(5)|` — the inclusion that failed as Report P's P-1 |

I expect Q-2, Q-3, Q-4, Q-7 and Q-8 to hold and Q-6 to hold weakly. If Q-2 and
Q-7 fail, carry-over fails even when the receiving round provably cannot
re-derive the vocabulary, and the negative result of Report P is not a
budget-matching artefact but a fact about the outer search.

## 7. What this experiment cannot show

* It does not test the loop as originally posed — equal budgets each round. It
  tests the **precondition** Report P identified, which is a weaker and prior
  question.
* A positive result here would show that carry-over can matter, **not** that it
  matters in a system whose rounds are equally deep. Report P's negative stands
  for that case.
* The body cut is a deliberate handicap on the receiving round. Any claim of the
  form "carrying helps" must be read as "carrying helps a round that cannot
  reach the carried structure", which is a statement about the *relation* between
  a round's reach and its inheritance, not about vocabulary in general.
* Nothing here is formally verified, and no discovered mathematics is new: every
  invariant in the library is standard.
