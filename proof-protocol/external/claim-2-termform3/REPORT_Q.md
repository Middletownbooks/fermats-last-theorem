# Report Q — Carry-over across a certified reach gap: the loop transmits, and how much

**Verdict: RESULT A, bounded and located.** When the carried vocabulary is
*certified* to lie outside the receiving round's own formation reach, carry-over
stops being redundant and starts working: it adds two invariants that are
**provably unreachable without it**, in a search whose space is exhausted rather
than beamed. The effect is real, content-dependent, and **small** — seven carried
terms bought two enabled discoveries — and every cheaper explanation for it was
run and eliminated. Report P's negative result is therefore a budget-matching
artefact in the exact sense Report P suspected, and the loop it could not observe
is a weak one rather than a compounding one.

Pre-registration: `PREREG.md`, sha256
`c77b91128f1f58ee2d1e48b05c8ae079475ec85926e16ba345c14ee5f11b13d3`, committed
before any Round-3 code was written. Five of its eight predictions held, two
failed and one was struck by the instrument. They are scored as written in
section 8.

Nothing in `termform/` or `termform2/` is modified. Reports M and P and their
artifacts are byte-identical.

---

## 1. What this changes about Report P

Report P's mechanism was explicit: Round 2's formation stage re-derives every
non-degenerate Round-1 term at the same price, because both rounds run the same
procedure at the same limits, so *promotion is redundant by construction* and the
loop has nothing to transmit. Its section 12 stated the condition the loop needs,

> `V_{k+1} ⊄ reachable(V_k under one round's own formation budget)`,

and named the first fix: cut the budget in the **body** size. That is the only
intervention here. Round 3 runs `form_leaves(size1=3, size2=3)` instead of
`(3, 5)`, which removes exactly the size-5 quantifier bodies and leaves the
two-stage structure, the objects, the splits, the cost model and the library
untouched.

## 2. The certificate — the claim Report P could not make

`certificate.py` runs the receiving round's **own** formation at body budget 3
with the caps raised to 10⁹ and the beam off, so the body space is *exhausted*:
78 stage-1 body classes, 2 520 stage-2 body classes, no truncation, **599 formed
terms**. None of the seven carried terms is among them.

| carried term | why the round cannot form it |
|---|---|
| `least(k: (n // (2 ^ k)))` | body size 5 |
| `count(k: (n % (k + k)))` | body size 5 |
| `count(k: (k - (n // k)))` | body size 5 |
| `count(k: (n // (k * <spf>)))` | body size 5 with the unit as a leaf |
| `count(k: (n % (2 ^ k)))` | body size 5 |
| `count(k: (n % (k * k)))` | body size 5 |
| `(1 // <count(k: (n % (k * k)))>)` | its unit has body size 5 |

**7 of 7 certified out of reach, 0 struck.** This is the first time in the
programme that `V_1 ⊄ reachable(V_0)` is established by enumeration instead of
assumed.

Provenance is the frozen rule, applied mechanically by `promote3.py` with no hand
selection: *promote every certified term, plus every formed term appearing as a
named unit inside a certified term*, applied to the prior round — Round 2
condition A at the honoured budget, `termform2/round2b_A.json`. That yields 19
promoted terms, of which 7 are out of reach at body budget 3 and 12 are not.

## 3. The headline table

Every row ran to completion without hitting the class cap except `A3plus`, which
is marked. The five unbeamed rows **exhaust** their cost-≤5 space, so for them
"did not reach X" is a proof rather than a beam draw.

| cond | what | atoms | carried | expansions | classes | certified | net new | live targets |
|---|---|---|---|---|---|---|---|---|
| **A3u** | unbeamed, carry nothing | 45 | 0 | 2 623 185 | 383 641 | **14** | 14 | 3/13 |
| A3u52 | unbeamed, 7 extra *self-formed* atoms | 52 | 0 | 4 323 384 | 651 547 | 14 | 14 | 3/13 |
| C3u | unbeamed, 7 **random** out-of-reach carried | 52 | 7 | 5 104 944 | 914 142 | 14 | 14 | 3/13 |
| B3uo | unbeamed, 7 promoted, **outer search only** | 52 | 7 | 4 875 624 | 863 836 | **21** | 15 | 4/11 |
| **B3u** | unbeamed, 7 promoted, formation + outer | 52 | 7 | 5 864 976 | 1 173 171 | **21** | 15 | 4/11 |
| A3 | beamed, carry nothing | 505 | 0 | 13 203 225 | 3 980 473 | 14 | 14 | 3/13 |
| C3 | beamed, random carry | 512 | 7 | 13 418 496 | 4 177 997 | 14 | 14 | 3/13 |
| D3 | beamed, carried at **expanded** cost | 512 | 7 | 13 203 225 | 3 980 473 | 14 | 14 | 3/13 |
| B3 | beamed, carried at cost 1 | 512 | 7 | 13 418 496 | 4 488 225 | 19 | 13 | 3/11 |
| B3all | beamed, **every** promoted term carried | 523 | 18 | 13 758 561 | 4 706 864 | 20 | 5 | 1/8 |
| A3plus | beamed, carry nothing, **cost 7** | 505 | 0 | 48 559 533 (cap hit) | 20 000 000 | 14 | 14 | 3/13 |
| A5 | beamed, **body budget 5**, carry nothing | 505 | 0 | 13 203 225 | 4 933 532 | **25** | 25 | 8/13 |

*net new* excludes any invariant whose value vector on TRAIN equals a carried
atom's: a condition handed an answer has not discovered it. *live targets*
excludes targets struck for the same reason (section 7).

## 4. What carrying actually bought

`B3u` certifies a **strict superset** of `A3u` — nothing is lost — and adds seven:
`bit_length`, `even_divisors`, `isqrt`, `is_squarefree`, `v_2` are the carried
terms themselves, which is bookkeeping. Two are not:

| enabled invariant | cost | term | reachable without the carried atoms |
|---|---|---|---|
| `is_prime_power` | 5 | `((2 * ⟨count(k: n % (k*k))⟩) // ⟨count(k: n % k)⟩)` | **no** |
| `odd_divisors` | 3 | `gcd(⟨count(k: n % (k+k))⟩, ⟨count(k: n % k)⟩)` | **no** |

Both are compositions of a **carried** term with a term the round **formed for
itself** (`tau`), and `A3u` exhausts its space without reaching either. That is
the programme's stated loop, operating: discovered structure carried across a
round boundary changed what the next search could reach.

Two enabled discoveries from seven carried terms is the honest magnitude.

## 5. Four ways this could have been right for the wrong reason, all eliminated

| control | what it holds fixed | result |
|---|---|---|
| **A3u52** | atom count matched at 52 with 7 extra *self-formed* units | 14 certified, 3 targets — **identical to A3u.** Not a symbol-count effect. |
| **C3u** | 7 *random* terms, also certified out of reach, same count and provenance | 14 certified, 3 targets — **identical to A3u.** The effect responds to mathematical content, not to extra atoms. |
| **B3uo** | carried terms withheld from formation, given to the outer search only | 21 certified, 4 targets — **identical to B3u.** The effect is in the outer search's use of the atoms, not in how they perturb formation. |
| **D3** | same terms, charged their expanded sizes 6–9 | identical expansions and classes to A3 — every carried atom is over budget, so the condition collapses to the control. The cost model is causal, as Report P found. |
| **A3plus** | no carry, 3.7× the expansions and two extra cost levels | 14 certified, 3 targets — **identical to A3.** Compute does not substitute for formation depth. |

`A3plus` is the sharpest of these, and it is where this experiment and Report P
diverge most. In Report P, condition E at 3.4× the budget *dissolved* the single
result that pointed B's way. Here the same move buys **nothing at all**: the
carried vocabulary supplies something 48.6 million expansions cannot.

`C3u` also reaches **more** semantic classes than `B3uo` (914 142 against
863 836) while certifying seven fewer invariants — Report P's observation that
class count and useful reach are different quantities, reproduced.

## 6. The beam hides half the effect

`B3` — the same carried set, the same body budget, but beamed at 1 200 with 505
atoms — certifies 19 and reaches `odd_divisors` but **not** `is_prime_power`. The
unbeamed `B3u` reaches both. So a beamed comparison of exactly the kind Report P
ran would have seen half of this effect.

Worse, and worth stating plainly: **`A5` here reaches 8 of 13 targets where Report
P's condition A, at the same body budget, unit cap, beam and cost, reached 5.**
The only difference is the seed — 20260919 against 20260909 — so the beam draw
alone moves the target count by three. That is larger than the entire intervention
Report P was measuring. Both reports' beamed target counts should be read with
that in mind; it is the reason every pre-registered comparison here has an
exhaustive counterpart.

The beamed rows also show that more atoms plus a beam is not a superset of fewer
atoms exhaustively searched: `A3` gains `even_divisors` over `A3u` and **loses**
`divisors_le_sqrt`.

## 7. Target leakage, and the strike the instrument forced

The frozen promotion rule promotes *certified* terms, and two of Round 2 condition
A's certified terms **are** pre-registered targets: `is_squarefree`, carried as
`(1 // ⟨count(k: n % (k*k))⟩)`, and `v_2`, carried as `count(k: n % (2^k))`.
Handing a condition a target as a cost-1 atom makes that target
non-discriminating. Both are therefore **struck** from the target list of any
condition that can use them, mechanically, and `B3all` — which carries the
in-reach promoted terms too — loses five targets that way (`is_prime`,
`is_square`, `n_div_spf` as well).

This is the T3 lesson of Report P section 8, applied in advance rather than caught
afterwards, and it is declared as a deviation because the pre-registration did not
anticipate it (section 9).

For completeness, the unstruck counts, which nobody should quote: `A3u` 3/13,
`B3u` 6/13, `B3` 5/13, `B3all` 6/13.

## 8. Pre-registered predictions, scored as written

| | prediction | outcome |
|---|---|---|
| Q-1 | A3 certifies strictly fewer invariants than A5 | **HELD** — 14 < 25. The body cut bites. |
| Q-2 | B3 reaches at least **two** targets A3 does not | **FAILED** — zero beamed, one (`is_prime_power`) unbeamed. |
| Q-3 | B3 certifies at least as many invariants as A3 | **HELD** — 19 ≥ 14 beamed, 21 ≥ 14 unbeamed. |
| Q-4 | B3 reaches more targets than C3 | **FAILED as written** — 3 = 3 beamed. **HELD** in the unbeamed analogue: B3u 4 > C3u 3. |
| Q-5 | D3 reaches the same targets as A3, not as B3 | **HELD** — identical expansions, classes and targets. |
| Q-6 | A3+ does not close the gap | **HELD** — A3plus is identical to A3 at 3.7× the expansions. |
| Q-7 | `is_squarefree` is reached by B3 and not A3 | **STRUCK** — it *is* a carried term, so the prediction was unscoreable. B3 does certify it; that is bookkeeping, not discovery. |
| Q-8 | `\|R_B3(5)\| > \|R_A3(5)\|` | **HELD** — 4 488 225 > 3 980 473 beamed, 1 173 171 > 383 641 unbeamed. The inclusion that failed as Report P's P-1. |

Five held, two failed, one struck.

**The instructive failure is Q-2, and it is a measurement error, not a hypothesis
error.** The effect appeared exactly where the mechanism predicted — two
compositions of a carried term with a self-formed one — but only one of them is on
the pre-registered target list, because that list was inherited from Report P,
whose Priority 4 chose targets that become simpler under *Round-1* abstractions.
`odd_divisors` is in the library and not in `TARGETS`. Had this experiment scored
targets alone it would have reported a null result while certifying the positive
one in the same artifact. The untargeted library scan is what caught it, and the
lesson is that a target list chosen for one intervention is the wrong instrument
for the next.

## 9. Deviations from the pre-registration

All are recorded in every `round3_*.json` under `deviations`.

1. **The beam.** PREREG section 4 promised an unbeamed cost-5 search in every
   pre-registered condition. Formation at body budget 3 yields 599 formed terms,
   and at ~500 atoms the cost-5 space is of order 10⁹ expansions — not
   exhaustible. The beam-free comparison is run as a separate pair at a unit cap
   of 40 (`A3u`, `B3u`, and the controls `A3u52`, `C3u`, `B3uo`), which *is*
   exhausted; the main conditions keep Report P's unit cap 500 and beam 1 200 so
   the numbers stay comparable with Report P's. Decided before any result was
   seen; both sets are reported throughout.
2. **The target strike** (section 7). A correction to the instrument, applied
   identically to every condition, with both counts reported.
3. **Three controls added after seeing B3u's headline numbers** — `A3u52`, `C3u`,
   `B3uo` — because `B3u` differs from `A3u` in two ways at once, not one. They
   can only weaken the positive result, never strengthen it, and two of the three
   are the ones that make it interpretable.
4. **The strike is budget-aware.** A target is struck only for a carried atom the
   condition can actually use. The first run of `D3` struck two targets for atoms
   its cost model had already put out of budget, which shrank its denominator for
   nothing; fixed and re-run before any conclusion was drawn.

No target, split, seed or cost model was changed after a result was seen, and no
failed prediction was rescued.

## 10. Defects found and fixed, both before any condition was scored

1. **Reach analysis charged a named unit its expanded size.** The first
   `promote3.py` walked the parsed tuple, in which the `<>` markers are already
   gone, so `count(k: (k % ⟨spf⟩))` looked like a size-6 body and therefore out
   of reach. Formation does the opposite: a stage-1 unit enters stage 2 as a
   size-1 leaf, so that body is size 3 and **is** formable. The bug made six
   formable terms look out of reach, which would have inflated the carried set
   with things the round could build for itself — precisely the redundancy this
   experiment exists to remove. Rewritten to analyse the printed form, where the
   markers survive.
2. **`S.reset()` inside the random-carry sampler wiped the registry** that the
   chosen terms' units live in, so `C3u` crashed with `KeyError` in `show`. The
   run had produced no numbers when it failed.

## 11. What this does and does not establish

**Establishes.** Carry-over transmits across a round boundary when the carried
structure is certified outside the receiving round's formation reach. The
transmission is content-dependent (random out-of-reach terms buy nothing), is not
a symbol-count effect, is not substitutable by 3.7× the compute, acts through the
outer search rather than through formation, and is invisible to roughly half of a
beamed measurement.

**Does not establish.** That the loop *compounds*. Two enabled invariants from
seven carried terms is a weak transmission, and both enablements are one
composition deep — a carried term times `tau`. Nothing here shows a third round
reaching something the second could not; that would need this experiment's design
run twice, with the enabled terms promoted again, and the reach gap re-certified.
That is the obvious next experiment and it is now cheap: `certificate.py` makes
the gap a checkable precondition rather than a hope.

**Does not rehabilitate Report P.** For rounds of *equal* depth, Report P's
negative stands exactly as measured: the receiving round re-derives everything and
promotion is redundant. What Report Q adds is that the redundancy, not the loop,
was the binding constraint — and that the loop's payoff, once the redundancy is
removed, is small enough that a programme betting on recursive self-improvement
should size its expectations accordingly.

**Unchanged caveats.** Nothing here is formally verified; no discovered
mathematics is new (every invariant is standard, and the library applied the names
after the fact); the object range is 2–90 with a 121–160 evaluation set; and the
body cut is a deliberate handicap on the receiving round, so "carrying helps" must
always be read as "carrying helps a round that cannot reach the carried
structure".

## 12. Artifacts

`PREREG.md`, `PREREG.sha256`, `promote3.py`, `promoted3.json`, `certificate.py`,
`certificate.json`, `reach_vectors.json`, `round3.py`, `analyze3.py`, and
`round3_{A3u,A3u52,C3u,B3uo,B3u,A3,C3,D3,B3,B3all,A3plus,A5}.json`. Every artifact
records the pre-registration hash, the splits, the deviations, the operator
verification, a 300-term re-evaluation against the reference evaluator, and the
full per-level log.
