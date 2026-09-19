# Report — D35, the second reading of `move_kind`

Scored against `PREREG_D35.md` by `score_d35.py`, both committed before the rater was
asked and before its answer existed. Sheet derived by `build_sheet.py` from the case
files; verdicts transcribed in `verdicts.json`; the screen recomputed under both columns
by `screen_under_rater2.py`.

**Both pre-registered failure conditions fired.**

## 1. The numbers

| subset | n | agreement | chance | Cohen's κ |
|---|---|---|---|---|
| all 17 | 17 | 0.647 | 0.343 | **0.463** |
| 15 non-self-answering (headline) | 15 | 0.600 | 0.298 | **0.430** |
| two-class only, `n/a` dropped both sides | 10 | 0.600 | 0.440 | **0.286** |

E-1 predicted κ ≥ 0.6 on the 15. It is 0.430. **`move_kind` does not reproduce.**

E-2 fired: the rater coded *"Random partition."* and *"Uniform random colouring."* the
same — both EXISTENCE-THEOREM — where my column splits them.

E-3, E-4, E-5 passed. The two self-answering items were coded FORMULA, which is worth
nothing, as registered. All five no-move-slot items were declined, which confirms that on
two of them — `12-geometrization` and `15-roth-kelley-meka` — **I filled a slot the source
does not have.** Every disagreement's reason named the shape of the move or the missing
slot, not unfamiliarity.

## 2. The disagreement is systematic, not noise

All six disagreements run the same way:

| item | rater 1 (me) | rater 2 |
|---|---|---|
| 01-sensitivity | formula | existence-theorem |
| 08-spencer-discrepancy | formula | existence-theorem |
| 09-vinogradov-mean-value | formula | existence-theorem |
| 17-roth-bloom-sisask | formula | existence-theorem |
| 12-geometrization | formula | no move recorded |
| 15-roth-kelley-meka | formula | no move recorded |

Six of six are *mine = formula*. That is one criterion difference applied consistently,
not a scatter. The rater stated its criterion up front: FORMULA when the object is written
down or the quantity computed directly; EXISTENCE-THEOREM when the move cannot legally
proceed until a good object — a large coefficient, a good partition or colouring, a good
subcube or congruence class, almost-periods, a Bohr set — **has been shown to exist by
pigeonhole, averaging or the probabilistic method**.

Mine was, in effect, *does the record's text read like a computation?* On terse entries
("Uniform random colouring", "Subcube refinement", "p-adic congruencing iteration") that
surface test says formula while the rater's mechanism test says existence-theorem. The
rater's criterion is the better one: it is about the argument, mine was about the prose.

Per `PREREG_D35.md`, E-2's remedy is **not** to re-code one item to match. I have now read
the rater's reason, so the option of stating a separating criterion in advance is gone, and
the registered alternative is to concede that the two are the same kind. Conceded. The
direction the concession runs is the rater's — both are existence-theorem — and the prereg
guessed that direction wrong, having assumed the concession would make both *formula* and
cost the screen an item. It adds items instead: the existence-theorem class goes from
**2 of 17 to 6 of 17**.

## 3. The failure condition's stated consequence is partly wrong, and here is the computation

`PREREG_D35.md` said κ < 0.6 means "the screen has no measured selectivity and FINDER.md's
precision figure must be reported as noise until re-run." The first half stands. The second
half, as written, does not — and it is better to show why than to leave my own wording
standing unchallenged:

```
rater 1 (committed column)   fires on 2: 02-cap-set, 04-kadison-singer   PRECISION 2/2
rater 2 (blind, D35)         fires on 2: 02-cap-set, 04-kadison-singer   PRECISION 2/2
existence-theorem class: 2 of 17 -> 6 of 17
applicability:           2 of 17 -> 2 of 17
```

The screen's output is **identical** under a column that reclassifies a third of the corpus.
Two reasons, and both matter more than the κ:

1. **The screen is gated on a second, sparser field.** It fires on
   `move_kind == existence-theorem` **and** `tight_to_constant == False`, and only 2 of 17
   items have both inputs. The four items rater 2 moved into the existence class have no
   tightness assignment, so they cannot reach the screen at all. The field's unreliability
   is currently *masked by the coverage bottleneck* — which `FINDER.md` §5 already names as
   the real obstacle, for a different reason than this one.
2. **Precision cannot fall, so it was never a measurement.** All 13 cases are successes
   whose board changed (D26). With no negative in the scored set, every fire is a true
   positive by construction. A number that survives redefining a third of its input is not
   measuring the classifier; 2/2 = 1.000 is arithmetic, not evidence. This run is the
   demonstration of that, which is worth more than the κ it came for.

So the honest report is: **the field does not reproduce, and the screen's published figure
is invariant to that fact** — not because the field doesn't matter, but because the screen
currently reads too few items for it to bite. It will bite the moment coverage improves,
and that is registered as a prediction rather than left as a caveat: fill the tightness
field and the screen's yield becomes column-dependent, 2 against up to 6.

## 4. What actually gets fixed

The tree's own standing lesson from the D20 run applies exactly: the five-transformation
vocabulary scored κ = 0.048 across three raters while the underlying computations were
fine, and the lesson drawn was *the computation needs no agreement on a word*. The same
remedy applies here. **Stop coding the category; demand the object.**

- The instrument's T2 already half-does this — *"if a theorem, name it and say what it
  costs"* — and is now strengthened so both branches name something checkable: the
  theorem, or the formula written down. A label with nothing named is not an answer.
- `move_kind` gains a second reading in the record itself, derived from this run, so the
  field is never again read as single-rater. The disagreement is preserved, not resolved by
  overwrite: overwriting my column with the rater's would destroy the only measurement of
  it that exists.

## 5. What this run cannot show

It cannot show the screen works, and now it cannot show it fails either. It shows that the
field the screen turns on is unreliable between two raters, that the unreliability is a
single systematic criterion difference, and that the screen's headline number is currently
insensitive to all of it.
