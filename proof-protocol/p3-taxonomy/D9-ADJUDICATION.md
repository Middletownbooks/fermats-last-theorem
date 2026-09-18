# D9: the E5(b) criterion and its proposed replacement

The last untouched contested claim. The seed proposed replacing E5(b)'s *"formula versus existence
theorem"* with *"is the existence guarantee strictly cheaper than the target?"*, and flagged the flaw
itself: **n = 3, derived from the cases that motivated it.**

Task 7 asked for both scored side by side, and for the replacement to be dropped if it does not beat
what it replaces. Here is what happened when I tried.

## First, a gap in the source material

**E5(b)'s exact statement is not in the seed material.** It is referred to by number and its content
is only inferable from the seed's objection to it. This is the same situation as transformations #3
and #5, whose names are also absent (debt D12). The direction of E5(b)'s prediction — that formula
moves are preferable, or that existence moves are a liability — has to be *inferred*, and I have not
invented it. Everything below is scored against the inferred reading, and that is a limitation of
the scoring, not of the criterion.

## The original criterion: scoreable, and it cannot discriminate here

`schema/encoder-schema-v2.json` makes formula-versus-existence-theorem its own field, so this is now
mechanical. Assigned from each case's before-board move as P1 records it (added to every
`before.json` as `move_kind`):

| | n |
|---|---|
| existence-theorem moves | **2** — cap set (needs a large Fourier coefficient to exist), Kadison–Singer (needs a good partition to exist) |
| formula moves | **8** |
| no move slot recorded | 2 (cases 3 and 10) |
| excluded | 1 (PCP, fit-testing only) |

**And then the scoring stops, for a structural reason: all 13 P1 cases are successes.** Every one is
a board change. A criterion meant to separate success from failure cannot be scored on a corpus with
no failures, and the negative twins are negatives about *tightness of a bound*, not about *moves that
failed*. There is no 2×2 to build.

What can be said is one-sided, and it is what the seed said with a smaller n:

> **2 of 10 scoreable successes had existence-theorem moves** (plus Banaszczyk and Dvir among the
> calibration items the seed cited, which are never scored). Existence-based moves demonstrably do
> succeed.

That **refutes** any reading of E5(b) under which existence-based moves are disqualifying. It does
**not** establish that the distinction is useless, because the corpus cannot test that.

## The replacement: not computable, so dropped

*"Is the existence guarantee strictly cheaper than the target?"* has **no stated metric for
cheapness.** Cheaper in what — the strength of the statement, the size of the object, the
quantifier depth, the proof length? Nothing in the seed material says, and each reading gives
different answers on case 4, where MSS's interlacing argument delivers an existence guarantee of
*exactly* the strength of the target.

`DIAGNOSTIC.md` already applied a standard to this situation, for auxiliary-witness lift:

> *Either give it a diagnostic computable from the before-board alone, or drop it. Do not leave it in
> the catalogue undefined.*

The same standard applies here, and gives the same answer. **The replacement is DROPPED**, not
rescued — consistent with how auxiliary-witness lift was handled and with the standing rule that
catalogues shrink before they grow. If someone supplies a metric for "cheaper", it becomes testable
and can be reconsidered; until then it is a phrase, not a criterion.

## And even if it had been computable

Per debt **D25**, measured this session: a rule-less rater scores **J = 1.000** on the retrospective
items against the best diagnostic's 0.675, with **13/13 recognition**. Any retrospective 2×2 built
here measures a weaker version of recall.

So a D9 scoring would have been **doubly** limited — by the missing failures *and* by the recall
ceiling. The one thing a retrospective comparison retains is **relative** standing: two criteria
scored on the same items face the same ceiling, so "does the replacement beat the original?" is
partially insulated even when "is either any good?" is not. That relative question is exactly the one
that could not be asked here, because only one of the two criteria turned out to be computable.

## Verdict

| | |
|---|---|
| **E5(b) as stated** | refuted as a disqualifying condition — existence-based moves succeed, 2 of 10 here. Untestable as a discriminator on this corpus, which contains no failures. |
| **the proposed replacement** | **DROPPED.** No metric for "cheaper" is stated, so it is not computable from the before-board, which is the standard already applied to auxiliary-witness lift. |
| **what would make it testable** | a corpus containing *failed* board changes — attempts that changed the board and did not work. P1 has none, and its survivorship selection is the reason (the seed flagged this too: *"cases are survivorship-selected famous successes"*). |

That last row is the useful output of this adjudication. **The benchmark cannot evaluate any
criterion about success versus failure, because it contains only successes.** That limitation was
stated by the seed about PPV; this is the second distinct thing it blocks.
