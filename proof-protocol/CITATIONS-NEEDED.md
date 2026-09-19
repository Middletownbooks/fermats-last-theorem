# What is still unreachable from here

**Control 15 is closed, and it was the row worth asking for.** One pasted transcript of
arXiv:2302.07211v3 (Bloom–Sisask, the Kelley–Meka exposition) closed the only unsourced *control* in
the benchmark and delivered four more rows on the way: the exponent ladder, the stated ceiling on the
density-increment board (debt D32), a primary statement of the half of twin N3 the diagnostic leans
on, and publication data for Bateman–Katz and Ellenberg–Gijswijt. Five rows from one document. The
prediction that named it in advance is ledger P-25.

Every egress route remains blocked — not only arxiv, export.arxiv, crossref and doi, but archive.org,
mathworld, ar5iv, semanticscholar, zbmath, dblp, numdam, annals.math.princeton.edu and wikipedia.
Search is the only live channel, and **every PRIMARY-tier closure in this tree came from a transcript
pasted in by the user**: C3, C7, C9, N3, C15.

## What is left, derived from `citations.json` rather than typed

`tools/citation_status.py` computes this; `tools/check_consistency.py` fails the tree if the prose
below drifts from it. One row is UNVERIFIED and three sit below fetched-primary tier.

| row | tier now | what would close it | stakes |
|---|---|---|---|
| **C1-gotsman** Gotsman–Linial 1992 reduction | **UNVERIFIED** — never checked in any pass | **arXiv:1907.00847, first two pages** (see below) | Low as scoring goes: it sits in case 1's *state* slot, not in a bound, and case 1 has already left the diagnostic's domain. But it is the one row no pass has ever looked at, and the prose missed it twice (D19). |
| **C10** parallel repetition | SEARCH | probably unimprovable by transcript — the primaries are largely pre-arXiv | Search reaches it in substance, including the Fortnow-then-Feige ordering. Case 10's `target_law = "none"` rests on these counterexamples. |
| **C12** Perelman | PARTIAL — bibliographic record only | math/0211159 — one transcript | Low. Case 12 fits none of the five transformations, so it does the least work of any row. |
| **N2-removable** ε-nets for halfspaces | PARTIAL | the half about removability, as opposed to the O(1/ε) net size that is confirmed | Low; the twin carries the qualifier. |

Two rows are VERIFIED but rest on **STANDARD-tier** claims and say so: **N16** (border rank — the
sub- versus fully multiplicative distinction is live, arXiv:1801.04852) and **N20** (Kővári–Sós–Turán
— tight only for t ≥ (s−1)!+1).

## What C1-gotsman needs, precisely

**The claim that needs a source:** that the Sensitivity Conjecture *reduces* to the induced-subgraph
maximum-degree problem on Q_n — `deg(f) ≤ poly(s(f))` is equivalent to *every induced subgraph of Q_n
on more than 2^{n−1} vertices has maximum degree n^{Ω(1)}*. That equivalence is the whole reason
Huang's theorem settles the conjecture, and it is what case 1's **state** slot asserts.

**Cheapest document: arXiv:1907.00847 (Huang), first two pages only.** The introduction has to state
the Gotsman–Linial reduction in order to explain why the theorem resolves the conjecture. That paste
closes `C1-gotsman` *and* upgrades `C1-after` from SEARCH to PRIMARY tier — two rows, two pages.

Alternatives, in order: Hatami–Kulkarni–Pankratov, *Variations on the Sensitivity Conjecture* (Theory
of Computing Library, Graduate Surveys 4, 2011), a survey whose subject is exactly this equivalence;
O'Donnell's *Analysis of Boolean Functions*, the sensitivity/degree chapter and its notes; or the
paper itself — Gotsman and Linial, *The equivalence of two problems on the hypercube*, Combinatorica
12(1) (1992), 131–135, which is pre-arXiv and so the hardest to reach from here.

**What would not close it:** a source that merely *cites* Gotsman–Linial, or that states Huang's
theorem without the equivalence. Rows `C1-bound` and `C1-after` already cover the bound and the
theorem; this row is about the reduction.

## If one more document can be pasted

Ranked by what it would change rather than by how open the row looks:

1. **Nothing in this table.** The largest remaining uncertainties in the programme are not citations
   any more. They are D25 (the retrospective arm is saturated by recall), D26 (the corpus has no
   failed board changes), and D18 (the P2 pilot has no API key). A perfect citation layer would move
   none of them.
2. **If a citation must be chosen:** `math/0211159` for C12, because it is the only open row a single
   transcript can close outright.
3. **The one document that would be worth more than any citation** is a *sourced, pre-resolution*
   statement by practitioners that their board is capped short of a known truth, on a problem other
   than Roth's — the shape D32 found in Bloom–Sisask. A handful of those would be the first
   retrospective items in this benchmark whose leak was not identified with hindsight.
