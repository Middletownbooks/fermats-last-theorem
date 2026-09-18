# The prospective arm

**The only instrument in this programme that can produce an uncontaminated estimate.**

Every retrospective case here is contaminated, and not for want of trying:

- **Step D** measured **100% recognition** of the source problem.
- **L2** measured **5 of 5** recognition of the superseding work — on encoders that were *trying* to
  comply with a date cutoff, and that self-reported the contamination in the leak field every time.

No amount of cutoff discipline fixes that. It was measured, not assumed. So the seed's L4 is right:
the only clean estimate is prospective — log the diagnostic's prediction on a new board-change claim
**before** reading the method section.

## How the blinding is enforced

Not by promising. By a seal.

~~~sh
python3 ../tools/prospective.py open --id 2609.xxxxx --problem "..." --bound "..." \
        --target-law multiplicative --bound-law additive --predict fire \
        --read title-and-abstract-only --notes "..."
python3 ../tools/prospective.py resolve --id 2609.xxxxx --outcome board-changed --what-they-did "..."
python3 ../tools/prospective.py verify     # recomputes every seal
python3 ../tools/prospective.py report     # the uncontaminated 2x2
~~~

- `open` writes the prediction and SHA-256 seals the record.
- `resolve` **appends**; it cannot alter a sealed prediction.
- `verify` recomputes every seal and fails if any record was edited, and refuses a second prediction
  on the same item.

This was tested by tampering: flipping one sealed prediction makes `verify` exit 1 and name the
record. The log is append-only JSONL — never edit it by hand.

`open` also records what the rule computes from `target_law` and `bound_law` **separately** from
what the human predicted, and warns when they disagree. That way a prediction cannot quietly be
attributed to the diagnostic when it was actually a hunch.

## The first batch

Five predictions, sealed 2026-09-18, all resolved-pending:

| id | diagnostic | prediction |
|---|---|---|
| 2607.21517 | product-law matching | no-fire — better play on the unchanged ϑ/LP board |
| 2609.15025 | union bound, refined | **fire** — the log comes off, matrix Spencer reaches O(√n) |
| 2608.14454 | product-law matching | not-applicable — no product operation, so no claim |
| 2608.30273 | product-law matching | no-fire — "recursive constructions" is play, not a new board |
| 2606.12181 | union bound, refined | fire — direct-sum structure, target is a max |

**Why these are genuinely blind.** All five ids post-date this model's training cutoff, and
`arxiv.org`, `export.arxiv.org`, Crossref and Semantic Scholar are all **egress-blocked** from this
container. The method sections are not merely unread; they are unreachable. Only titles, plus one
search summary for 2608.14454, were seen — and each entry's `notes` records exactly that.

Two caveats recorded in the log rather than left for a reader to notice:

- **2606.12181 is the weakest entry.** June 2026 is only just past the cutoff, so it should be
  down-weighted if the others disagree with it.
- **2608.14454 is logged as `not-applicable`, which is not a prediction.** It is recorded anyway
  because the domain rate — how often the diagnostic declines to speak — is itself a number the
  prospective arm has to report. A diagnostic that abstains on most new work is not useful even if
  it is never wrong.

## What to expect

Nothing, for a long time. Five items cannot produce a rate; the seed's own warning about ~13
positives applies here with far more force. What this arm produces is the *only* table in the
programme not built on cases whose answers the encoder already knew, and the cost of that is that
it accumulates slowly.

The thing to protect is the seal. One unsealed prediction, or one prediction logged after a glance
at the method, and the arm is worth exactly as much as the retrospective cases.

---

## Resolution procedure

**Written before any prediction is resolvable, not after.** The tool enforces the parts it can.

1. **Verify the seals first.** `prospective.py verify` must pass *before* the method section is
   opened. `resolve` refuses to run while any seal is broken, and a prediction whose seal does not
   verify is **void, not resolvable** — record it as void and say so. A seal checked *after* reading
   proves nothing about what was predicted.
2. **Then read the method section.** Not before. The whole value of the arm is that this order held.
3. **Record who read it.** `--method-read-by` is required. In a single-instance programme the
   resolver will often be the predictor; that is permitted and **must be recorded**, because it is a
   weaker resolution than an independent one.
4. **Resolve against the published method, not an abstract.** An abstract can say "new approach"
   about better play, and "improved bound" about a board change. If only the abstract is available,
   leave it pending.
5. **Re-run `verify` afterwards** and keep its output with the resolution.
6. **One prediction per item, ever.** `open` refuses a second. If the first was wrong, that is the
   result.

### What counts as which outcome

| outcome | means |
|---|---|
| `board-changed` | a genuinely new invariant, certificate or object; the argument tracks something different |
| `same-board-better-play` | the bound improved within the existing framework |
| `tight-no-change` | the bound was essentially the best available, or shown tight |
| `withdrawn` | the claim was retracted or the paper withdrawn |
| `unresolved` | still open after the method was read |

Only `board-changed` counts as a positive. `same-board-better-play` is a **negative** — that
distinction is the whole point of the controls (sphere packing, Kelley–Meka), and collapsing it
would make every improvement a board change.

### The not-applicable rate is a result

`report` prints it as a first-class number. Of the five sealed predictions, **one (20%) is
`not-applicable`**. A diagnostic that declines to speak on most new work is not useful even when it
is never wrong, and this rate is the only honest measure of that. It should be quoted alongside any
accuracy figure this arm ever produces.

### Maintenance

Log more, every session, however few. Five is not a sample. The arm's value is entirely in its
length, and it is the only instrument here that recall cannot inflate — which, after the baseline
result, makes it the only one that can answer the programme's actual question.
