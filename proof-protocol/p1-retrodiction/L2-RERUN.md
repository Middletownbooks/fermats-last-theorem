# Re-running L2 properly (task 8)

L2's **pre-registered κ was never measured**. Re-running is worth doing only with all four fixes
below. Three are built here; the fourth is a rule, and it is already enforced by `tools/validate.py`.

> **Do not reuse the original five blind encodings.** They would contaminate new raters with the old
> ones. The design fixes below are safe to inherit; the encodings are not. Use fresh cases and your
> own encoders.

## Fix 1 — a genuine third rater, provenance hidden, X/Y randomised

**Built: `tools/make_rating_sheet.py`.**

L2's defect was not a small one. The third rater was never run, and *every* slot mark was made by a
single **non-blind** rater who knew which encoding was the reference. A rater who knows which column
is whose cannot produce an inter-rater statistic about it. The substitute figure — κ = 0.286, 95% CI
[0.000, 0.667] at n = 5 — is to be read as **unmeasured, not as a bound.**

~~~sh
python3 tools/make_rating_sheet.py build --a enc_first/ --b enc_blind/ --seed 7 \
        --out sheet.json --key key.json
# give the rater sheet.json only
python3 tools/make_rating_sheet.py score --sheet filled.json --key key.json
~~~

- Provenance is **stripped**, not merely omitted: encoder names, passes, timestamps and
  self-describing fields are removed, and the tool was tested against sentinel strings to confirm
  none survives into the sheet.
- X/Y assignment is randomised **per case**, so a rater who works out the pattern on one case learns
  nothing about the next.
- The key is written to a separate file. `score` refuses to report a κ from one rater: it prints the
  agreement rate and says plainly that one rater cannot produce an inter-rater statistic, which is
  exactly the error being fixed.

## Fix 2 — a worked example per slot

**Built: `schema/encoder-schema-v2.json`.**

This is the fix that matters most for any κ that comes out. `state` agreed on **1 of 5** in L2, and
**four of those five divergences were the two encoders reading the SLOT differently**, not disagreeing
about mathematics:

- the first encoder's `state` was **the problem's object** — "Kakeya set K ⊆ F_q^n", "the mean value
  J_{s,k}";
- the blind encoders' `state` was **what a partial attempt carries**, which is what the schema
  actually asks for.

Without worked examples, that variance dominates everything else. Every slot in v2 now carries a
worked example, a **not-this**, and where useful a one-line test. For `state`: *if I paused the proof
mid-argument, what would be written on the page?*

`move` also gains the formula-versus-existence-theorem distinction as **its own field**. v1 asked for
it in prose and it came back non-comparable, so the slot could not be scored on its defining feature.

Every slot may be explicitly `null` **with a reason**, so an empty slot is distinguishable from an
unconsidered one. L2 had 6 of 25 slot-pairs with nothing on one side and no way to tell which kind of
nothing it was.

## Fix 3 — `bound` holds multiple regimes; `leaks` are indexed by regime

**Built: in `encoder-schema-v2.json`, and already applied to the case data.**

Case 5 is why. At a 2008 cutoff, finite-field Kakeya had two regimes and **neither dominated**:

~~~
(n+2)/2 > 4n/7   ⟺   n < 14
~~~

verified in `tools/check_corrections.py`. The two regimes leak differently — a union bound for the
low-dimensional geometric argument, a feasibility theorem for the high-dimensional arithmetic one.
**A single-regime `bound` field forces a single leak where there are two.**

Case 5's `before.json` now carries `bound_regimes` and `leaks` indexed by regime. Note that the
high-dimensional exponent itself is **disputed** — see `../CITATIONS.md` row `C5-4n7`: 4n/7 + 3/7 is
Katz–Tao's *Euclidean Minkowski-dimension* bound, and no source reached this session states it for
|K| in F_q^n. The two-regime structure survives that; the crossover point may not.

## Fix 4 — cutoffs dated from the arXiv posting

**Enforced: `tools/validate.py` fails the tree on a source dated at or after its superseding paper.**

L2's case 9 was **voided by this exact error**. The cutoff was set at 2011-12-31 intending "before
Wooley", but Wooley's efficient-congruencing paper is **arXiv:1101.0574, posted 2011-01-03** — eleven
months *inside* the cutoff. The two encoders were answering different questions.

The rule: **date every work from its arXiv posting (v1 of the preprint), never the journal year**,
which can lag by one to two years. Applying it found a second instance immediately: Bateman–Katz is
conventionally cited as 2012 but was posted 2011-01 (`../CITATIONS.md` row `C2-batemankatz`). When
case 9's cutoff was corrected, `validate.py` immediately flagged a source that had been keyed to the
old date — the check working as intended.

## What a re-run would and would not settle

It would give the inter-encoder κ that L2 pre-registered and never measured. It would **not** address
contamination: L2 measured 5 of 5 recognition of the superseding work, and step D measured 100%, on
encoders that were *trying* to comply. Only `prospective/` addresses that.

So the honest ordering is: a re-run improves the *measurement* of encoder agreement, and the
prospective arm is the only thing that improves the *validity* of the whole benchmark. If there is
time for one, it is the prospective arm.

There is also a cheaper, more targeted κ now available, and it is the one
`../p3-taxonomy/DIAGNOSTIC.md` asks for: have raters assign only `target_law` and `bound_law` blind,
from the bound and the extremal construction. Two closed-vocabulary fields, against a measured
baseline of κ = 0.048 for the transformation label. That is a smaller experiment than a full
re-encoding and it tests the thing the rebuilt diagnostic actually depends on.
