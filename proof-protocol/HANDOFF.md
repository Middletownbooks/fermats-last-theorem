# Seed document 1 of 2 — the handoff note

*Reproduced as received, 2026-09-18. This is the source for everything under `proof-protocol/`;
where this project's data and code disagree with it, the disagreement is recorded in `DEBTS.md`
rather than silently resolved. The failure-register table at the end arrived as loose lines; it is
reproduced faithfully here and as structured rows in `debts.json`.*

---

Handoff: proof-protocol measurement commission (P1–P4)

Date: 2026-09-18. Author: a chat Claude instance with no repo access and no agent substrate. Attach alongside this note: (1) the chat response containing P1 v0, P3 preliminary, P2 pre-registration; (2) the harness source, p2-ablation-harness.html (published at https://claude.ai/artifact/27fx1ooLK5F6XTaTu4daoZ).

Status in one line: nothing has been measured yet. P1 is a single-encoder draft, P2 is an untested-against-live-Claude instrument, P3 is one contaminated rater's scoring, P4 is deliberately unwritten.

Tasks are in priority order. Stop after any of them and the work is still useful.

## 1. Replace the battery's weakest items with the repo's own corpus  (repo instance only)

The harness battery is 15 textbook-grade items; I expect many to hit ceiling in the pilot. The repo holds something better: real agent failures with known ground truth — the false impossibility theorem whose counterexample was already published (E7), the unsupported "this forces that" steps behind both negative verdicts (E8), the variance-1 Monte Carlo check (E9). Convert each into a battery item: {id, type: true|false|open, statement, truth} where statement is the claim the agent was led to and truth is what the judge needs to grade it. These have a demonstrated non-zero failure rate on a real agent, which is exactly the E10 requirement. Paste into the Battery tab's JSON box, or into the port (task 3).

## 2. Blind re-encoding of P1  (either instance; needs subagents + web)

P1 v0 was encoded by one model that knows every answer. Before any P3 score means anything:

- Split P1 into cases/<n>/before.json (five slots, bound, leak table, pre-dated sources only) and heldout/<n>.json (after-board, transformation label). No scored agent may ever read heldout/.
- For each case, spawn a subagent given only sources dated before the superseding paper; have it fill before.json independently. Diff against mine. Report Cohen's κ on slot contents.
- Separately, have two subagents label each held-out after-board with one of the five transformations or "none". If label κ < 0.6 the vocabulary is not operational — report that as the P3 result.
- Run the telegraph baseline: leak table only, no procedure, guess the after-move. Procedure scores are lift over this, never raw accuracy. Ask each agent afterwards to name the source problem; stratify.
- Banaszczyk, Bansal–Jiang and Guo–Fang–Lu are calibration only. They generated the taxonomy; never score them.

## 3. Port the harness to a script with a real API key  (either instance)

The published artifact is constrained by its runtime: no token counts (cost is chars ÷ 4), no named model (tiers only), no system prompt, no temperature control, a rate limit built for interactive pages. A Python port removes all four. Everything needed is in the HTML: BLOCKS, SCHEMA, PFMT, PRIG, CORE, judgePrompt, the arm generator (E = ABC, F = BCD), outcome(), and predictions() with the six coded rules. Keep those rules byte-identical or re-freeze and say so.

Improve while porting:

- Placebos currently reach template length by cycling ~10 paragraphs. Write non-repeating filler.
- Use a different model family for at least one judge; same-model judging is a known bias.
- Judges cannot be blinded to arm (tags and field numbers leak it). Record this; don't pretend otherwise.
- Do exact arithmetic on any accepted counterexample in code, not in the judge.

## 4. Pre-register the analysis, not just the predictions

The harness reports difference-of-proportions intervals that treat runs as independent. Runs share problems, so those intervals are too narrow. Before unblinding, commit the real analysis: mixed-effects logistic regression, failure ~ A+B+C+D+E+F with a random intercept per problem, on the exported CSV. Resolution IV means main effects are clean of two-way interactions but two-way interactions alias each other — do not interpret any of them. Power: ~40 runs per factor level detects roughly a 30-point shift; smaller effects will read as null. Say so in the write-up rather than calling small effects absent.

## 5. Verification debts in P1  (needs web)

All citations were recalled, not fetched. Specifically shaky:

- Case 9 (Vinogradov): the pre-Wooley bound s ≳ c·k² log k and the "log k rounds" leak. Medium confidence.
- Case 5: the best pre-Dvir exponent (I wrote ≈ q^{4n/7}).
- Case 1: Chung–Füredi–Graham–Seymour constant, (½ − o(1)) log n.
- N4: Polak–Schrijver lower bound for Θ(C7).
- Battery O3: that x³+y³+z³ = 114 is still open. Re-check on the day of freezing.

Reclassifications to adjudicate: sphere packing moved from "board change" to "same-board control" (the board is Cohn–Elkies 2003; Viazovska supplied the certificate). PCP demoted to fit-testing only because its "before" was a successful proof, not a failing bound.

## 6. Claims I made that the originating instance should attack

- Product-law matching (replacement for "de-tensorize"): require the invariant to obey the same product law as the target on the extremal family. I derived it from the cases I then scored it on. It needs cases chosen by someone who has not seen the hypothesis. Until then it is a guess.
- Against E5(b): Banaszczyk's move, Marcus–Spielman–Srivastava, and Dvir all rest on existence statements and all succeed. Proposed replacement: "is the existence guarantee strictly cheaper than the target?" Untested, n = 3, same flaw as the original.
- Against the commission's contamination control: forced-choice discrimination is still solved by recognition. My alternative (score the procedure, negative twins, telegraph baseline, recognition probe, prospective arm) is argued, not validated. The prospective arm is the only clean estimate.
- Base rate: 2 of 15 headline results (Viazovska, Kelley–Meka) were better play on an unchanged board. The programme's core hypothesis should carry that denominator.

## 7. Do not do

- Do not write v3 before P2 data exists. The v3 hypotheses are already encoded as arms: if (c) and (d) hold, v3 is a return form with about six computed-content fields and §4 becomes a footnote.
- Do not add a sixth transformation. Transformations 3 and 5 fit almost nothing in P1 and are probably artefacts of the Komlós trio; the catalogue should shrink before it grows.
- Do not report harness results with judge κ below ~0.6 without reading transcripts first.

## 8. Failure register (what was tried and dropped, and cost)

Tried / Outcome / Cost

- Forced-choice discrimination as contamination control — Rejected on argument; not tested — Reasoning only
- Sphere packing as a board-change case — Reclassified as control — Reasoning only
- PCP as a scoreable case — Demoted — Reasoning only
- Running P2 in chat — Impossible (no agent substrate); built harness instead — One artifact
- Raw-API harness with token counts — Blocked by published-page runtime; fell back to sampling capability — Lost O5 precision
- Live integration test of harness — Not done; logic tested against mocks only (600 simulated runs) — —
