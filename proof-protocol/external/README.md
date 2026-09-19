# Work for the parent project lives upstream

`Middletownbooks/Claim-2`, branch **`claude/theorem-discovery-lab-jpbph1`**,
`theorem-lab/termform3/`.

**Report Q** — carry-over across a *certified* reach gap. The receiving round's
formation is exhausted by enumeration and provably cannot produce the carried
terms; carrying them adds two invariants that are certified unreachable without
them. Four cheaper explanations eliminated, including 3.7× the compute.

**Report R** — it compounds twice, then stops. `sqdiv → is_prime_power → is_cube`,
then a fixpoint, with an ablation showing the second step depends on the first
specifically. The mechanism splits into *reach extension* and *cost compression*,
and compression pays only on structure a reach extension produced — a round cannot
manufacture reach for itself.

These were mirrored here while this session had read-only access to that
repository. They were pushed upstream (`7dd6935..1d97b8f`), so the copy has been
removed rather than left to drift. Nothing in this protocol tree depends on them.

## And, from the same session, `board-finder/`

Two priorities the project's owner named: how to find more transformable boards, and
what orchestrated agents should be pointed at.

**The board is not the scarce thing.** `leanboard/ab/REPORT_AB_metagame_corpus.md`
had already measured it — four independent models converged on the same Komlós
board, as did the paper that closed it. What is scarce is a functional the move
*conserves*: the trio's own K1 and K3 encodings share a state and a move and differ
only in whether the invariant degrades, O(√log n) against O(1).

**So the screen reads leaks, not transformations** — a leak is on the before-board,
which is all a finder has. `ACCUMULATION` (5 cases), `SATURATION` (2), and a residual
`WRONG_STATISTIC` bucket (6) whose prescription predicts nothing. Usable yield 7 of
13, and the 13/13 fit is called what it is: a post-hoc classification awaiting the
blind κ test.

**For the agents, three checks from three observed failures** — enumeration
completeness (the Horn 1 impossibility claim, contradicted by a paper five days
older), ranking steps by load-bearing weight before checking any (a Monte Carlo that
verified a statement the CLT already gave, while the crux went untested), and asking
an agent whether its own candidate relocates the obstruction, which three of four did
honestly unprompted. Plus a six-item benchmark, because the rule here is to build the
benchmark before the pipeline.

Debts **D34** and **D35** in this tree track what remains untested.

## The audit's anatomy closed the loop back onto this tree

The full Banaszczyk → Guo–Fang–Lu audit supplied the mechanism: the move, the state and
the geometry are unchanged and the terminal check got *easier* — only the invariant
changed, from a **multiplicative** certificate (Gaussian measure, threshold ≍ √(2 ln d))
to an **averaging** one (directional total variation, bound uniform in d). Verified
here from the composition laws alone in `board-finder/verify_mechanism.py`, which also
caught two errors in my own statement of it.

Three consequences for this tree:

* **D25 is no longer standing.** Its negatives are all famous problems, which is what
  made recall sufficient. An invariant *provably equivalent to the theorem* — the
  convolution-compiler board four models converged on, one of them proving the
  equivalence and reporting it as a find — is a negative that recall cannot crack, and
  it is constructible rather than found.
* **D36: `move_kind` has two independent derivations.** This tree got it from
  adjudicating D9; the audit got it from reading two papers. Nothing else here has that.
* **D35 is therefore the cheapest high-value test left** — one field, two categories,
  17 items, on the most-corroborated field in the tree.
