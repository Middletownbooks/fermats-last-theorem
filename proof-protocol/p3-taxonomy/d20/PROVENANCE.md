# D20 provenance — read before the numbers

The next-session task list asked: *"State in the commit message whether this is a first run or a
re-run of a lost result. If any rater output from last session survives anywhere — scrollback, a
stray file, your own memory of the numbers — say so and report it alongside the new run."*

It does survive. This is **not a fresh first run**, and here is the full account.

## What happened, in order

1. **Last session**, the bundle was built and three raters were launched. Commit `be73717`
   ("Build the two-field κ instrument … and run three blind raters") was made **before any rater
   returned** — the title claims more than the commit contained. That is the gap the task list
   spotted, and it was a mistake in commit sequencing, not a lost result.
2. **Raters A and C returned.** Their outputs were written to the session scratchpad and **survived
   on disk**; they are committed here unmodified as `raterA.json` and `raterC.json`.
3. **I then ran the scorer on A and C alone** and saw those numbers: `target_law` Cohen κ = 0.725,
   `bound_law` κ = 0.791, firing-decision Fleiss κ = 0.569, and N8 firing for both raters.
   **This means partial results were seen before the full run was assembled.**
4. **Rater B's agent terminated with a spend-limit error** (HTTP 429, monthly limit). It had
   already produced a complete, well-formed 14-item assignment, which is committed as
   `raterB.json`. The agent's terminal status was `failed`; its output was not truncated.
5. The usage limit reset, and the three-rater score was computed.

## What was and was not re-run

- **No rater was re-run.** Each of A, B and C was prompted exactly once and its first and only
  output is committed. No rater was re-prompted after a result was seen.
- **No rater output was edited.** The committed files are transcriptions of what each agent
  returned, with the `why_*` prose abbreviated for length in some rows; the two law labels — the
  only fields the scorer reads — are verbatim.

## What WAS changed after seeing partial results, and this is the disclosure that matters

**The scorer was modified after I had seen the A+C numbers.** Three changes:

1. Added **bootstrap confidence intervals** (the task list asked for them).
2. Added **per-rater false-positive accounting** against the twin truth.
3. **Changed the verdict logic.** The earlier version declared success on the **field κ alone** and
   printed *"The judgement WAS moved onto a field that reproduces. The rebuild did its job."* That
   was too generous: the diagnostic does not consume the fields, it consumes the firing decision
   derived from them, and a negative twin that fires is a false positive whatever the field
   agreement is. The current version requires all three of field κ, rule κ and the
   zero-false-positive claim, and reports them separately.

**Direction of the change: it made the test strictly harder to pass.** Under the old logic this run
would have printed a clean pass. Under the new logic it prints one FAIL. That is the benign
direction — but a reader should judge that, not take my word for it, which is why the old verdict
text is quoted above verbatim.

**Not disclosed as a change, because it was not one:** the 0.6 stop rule was pre-committed in
`DIAGNOSTIC.md` before any rater ran, and the reference law assignments were committed in
`diagnostics.json` at `9690964` — both before this run. Neither was touched.

## One reference value was corrected after the run

N8's reference was changed from `additive / additive` to `max / l2` **because all three raters
disagreed with me unanimously and I checked the mathematics and they were right**. The full
adjudication is in `N8-adjudication.md`. This correction:

- does **not** change the rater κ figures, which never read my reference;
- does **not** change the false-positive counts, which are computed against each item's recorded
  truth;
- **does** change the "matches the reference" column from 9/14 to 10/14, and
- **does** turn `DIAGNOSTIC.md`'s headline from "zero false positives" into a recorded false
  positive, which is why it was made rather than left.

`score_output.txt` is the **verbatim run of record, computed before that correction**. It therefore
shows N8's reference as `no-fire`. That is deliberate: the run is not retro-fitted to the
correction.

## Standing count

This programme has now retracted its own claims three times: L2's prediction L2-1, this session's
wrong positive-class vocabulary in `score_diagnostics.py`, and now `DIAGNOSTIC.md`'s
zero-false-positive figure.
