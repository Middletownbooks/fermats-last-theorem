# Contemporaneous within-problem pairs

*Candidates: `pairs/candidates.json`. Power: `tools/pair_power.py`. Debt **D31**.*

## The problem this is trying to solve

`D25` measured the ceiling: a rule-less rater given the same items scored **J = 1.000** against the
diagnostic's 0.607, with **13/13 recognition**. The rater does not need a rule because it does not
need the mathematics — it needs the problem's name. Every fix that keeps one item per problem fails
for the same reason.

A **contemporaneous within-problem pair** removes the shortcut by construction: one problem, one
period, two teams, one of which changed the board and one of which did not. Both halves *are* the
problem, so naming it buys nothing. The case 7 split produced the first one (Maynard–Tao against
Zhang, 2013), and `D31` records why it was deliberately **not** run at n = 1: a rater scoring 1/1
or 0/1 produces a number that cannot be interpreted.

## How many pairs would be enough

Each pair is one binary decision at chance 1/2, so the test is an exact one-sided sign test
(`tools/pair_power.py`):

| pairs | all correct | one miss |
|---|---|---|
| 4 | 0.0625 | 0.3125 |
| **5** | **0.0312** | 0.1875 |
| 7 | 0.0078 | 0.0625 |
| **8** | **0.0039** | **0.0352** |

**Five pairs scored perfectly clear α = 0.05; eight are needed to survive a single miss.** At n = 7
one miss gives p = 0.0625 and fails, so 8 is the honest collecting target and 5 is the floor.

**What this does not buy.** The sign test asks whether a rater can separate the halves. It does not
ask whether the *diagnostic* adds anything — for that, the D25 baseline rater must be run on the same
pairs and **beaten**. A pair set that a rule-less rater also separates 8/8 is another D25, not an
answer to it.

## What is in hand

| | kind | status |
|---|---|---|
| **bounded gaps 2013** — case 07a (Maynard–Tao, board changed) vs control 16 (Zhang, level-*n* board unchanged) | discrimination | **encoded**, sourced at primary tier, not run |
| **Roth 2023** — control 15 (Kelley–Meka) vs control 17 (Bloom–Sisask), days apart, both on the density-increment board | **control pair** | **encoded**, sourced at primary tier |

The Roth 2023 pair **does not count toward the five**: both halves are must-not-fire, so there is no
"which is which" to score. What it measures is *specificity inside one problem-period* — a diagnostic
that fires on either half is firing on better play — and the authors' own words make the encoding
unusually clean: *"our sole contribution is at the technical level … all of the main ideas are the
same as in [14]."* Different number, worth having, one pair short of nothing. It is now encoded as controls 15 and 17, and control 17 declares the asymmetry that would matter if it were ever reused inside a discrimination pair: its half is a low-stakes advance, while every other item in P1 is a headline result, so a rater could separate the halves by prominence rather than by mechanism.

## The candidate list, ranked

Every claim below is **recalled, not sourced**. Egress is blocked and this project's standard is a
source reached in-session, so each entry names the document that would settle it and the way it might
fail. Full text in `pairs/candidates.json`.

1. **Sunflower lemma, 2019 — the best candidate.** Alweiss–Lovett–Wu–Zhang break Erdős–Rado with the
   spread/random-restriction route; Rao publishes a shorter proof with a better constant *on that new
   board* weeks later. Two teams, one season, one bound, and **neither half is a failure** — both
   improved the record, so the rater cannot separate them by who won. *Needs* arXiv:1908.08483 and
   arXiv:1909.04774. *Risk:* if Rao's argument is better read as a different board, the pair becomes
   two board changes and dies exactly as the cap-set candidate did.
2. **Bounded gaps 2013, extended to a triple.** Adding Polymath8a (Zhang's equidistribution constant
   improved to δ = 7/300) and Polymath8b (Maynard's sieve optimised) would make **one problem carry
   all three categories the tree distinguishes**: board change, level-(n−1) board change, and better
   play — the sharpest available test of D30's level axis. *Risk:* overlapping community, so the
   two-teams condition is weak; tolerable as a third member, not as a standalone pair.
3. **Matrix multiplication, 2021–2023.** Refined laser method versus asymmetric hashing: the case
   where "refinement" versus "new mechanism" is genuinely contested rather than obvious in hindsight,
   which is where a diagnostic would have to earn its keep. It also pairs with the ceiling register —
   the laser method's limit on the Coppersmith–Winograd tensor is a *proved* barrier, which would be
   that register's first `PROVED`-tier entry. *Risk:* if practitioners disagree about the
   adjudication, the pair has no ground truth. That would be worth recording as a finding, but it is
   not a pair.
4. **Spencer constructive, 2010–2014 — recorded so it is not mistaken for a pair.** Bansal's SDP,
   Lovett–Meka's random walk and Rothvoß's convex geometry are three *parallel* boards for one
   theorem, none of them better play on another. That is a structure the catalogue has no entry for
   and must not acquire one reflexively.
5. **Strong parallel repetition, 2008 — not a pair.** Rao's projection-game theorem and Raz's
   odd-cycle counterexample are both correct, about different regimes. It is a twin, and it already
   is one (N5).

**Rejected, so they are not proposed again.** Cap set 2016 (Croot–Lev–Pach vs Ellenberg–Gijswijt:
*both* changed the board — a method and its application, per row `C2-after-split`); sphere packing
2016 (Viazovska vs CKMRV: *neither* changed the board, per `ADJ-14`, and they share an author).

## The honest arithmetic of this plan

One discrimination pair in hand, four ranked candidates, of which **at most three could survive
their stated risks**. That is 4 against a floor of 5 and a target of 8. So this route does not get
there on current material: it needs either candidates nobody in this session thought of, or the
prospective arm, which needs no pairs at all because nothing has happened yet. **Both routes stay
open, and the pair route is the cheaper one to be wrong about** — a candidate that fails costs one
transcript, while a prospective prediction that resolves badly costs months of waiting.
