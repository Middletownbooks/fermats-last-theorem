# Pre-registration — D35, a second reading of `move_kind`

Written and committed **before** the rater is asked. The sheet (`SHEET.md`) and the key
(`key.json`) are generated from the case files by `build_sheet.py`, so no move text here
is authored by me.

## Why this run exists

`move_kind` is the **binding conjunct** of the transformable-board screen: extending the
tightness field cannot make the screen fire without it. It was assigned by one instance,
for D9, with no second reading. If it does not reproduce, `FINDER.md`'s precision figure
is noise.

## What the rater gets

The 17 items in a fixed scramble (seed 35, order recorded in `key.json`), each showing the
move **as the record states it**, with one question and three permitted answers: `FORMULA`,
`EXISTENCE-THEOREM`, `NO MOVE RECORDED`. Tools forbidden. Reasons required, and — per this
tree's own lesson — the reasons are read before the codes are scored.

My codes, the reasons for them, and the after-boards are withheld. So is the fact that
one class holds 12 of the 17.

## Two confounds I can see in advance, and what is done about them

**Self-answering text.** Two items' recorded move text contains its own answer:

| item | shown text |
|---|---|
| 07-small-prime-gaps | *"…an EXPLICIT FORMULA, not an existence theorem."* |
| 16-zhang-smooth-moduli | *"Selberg's explicit formula, unchanged"* |

Agreement on those two is not evidence of anything. The headline κ is computed **with them
excluded**, and the full-set κ is reported beside it. This is a defect in the record, not
in the rater: a field that states its own classification cannot be independently rated.

**Class imbalance.** My column is 12 formula / 2 existence-theorem / 3 n-a. Raw agreement
is therefore cheap, which is exactly why κ and not agreement is the headline, and why the
two-class subset (dropping the `n/a` items) is reported separately.

## Predictions

| # | prediction |
|---|---|
| **E-1** | κ ≥ 0.6 on the 15 non-self-answering items |
| **E-2** | **the risky one, and it is against me.** Items 2 and 5 of the sheet — *"Random partition."* (Kadison–Singer) and *"Uniform random colouring."* (Spencer) — are near-identical in form, and my column splits them: existence-theorem and formula respectively. I predict the rater codes them **the same**, either way. If it does, my own column is inconsistent on the screen's binding conjunct, which is D35's fear realised and not a rater error |
| **E-3** | the two self-answering items are coded FORMULA, and that tells us nothing |
| **E-4** | of the five items with **no move slot** in the record, the rater answers `NO MOVE RECORDED` on all five — including 12-geometrization and 15-roth-kelley-meka, where my column says *formula*. Those two disagreements would be a **coverage** failure of the record (I filled a slot the source does not have), not a disagreement about mathematics |
| **E-5** | the rater's reasons on any disagreement name the *shape of the move* rather than unfamiliarity with the problem |

## Failure conditions, stated in advance

- **κ < 0.6 on the 15** → `move_kind` does not reproduce; the screen has no measured
  selectivity and `FINDER.md`'s precision figure must be reported as noise until re-run.
- **E-2 fires** → the column is internally inconsistent on two items of the same form.
  That is not fixed by re-coding one of them afterwards to match the rater; it is fixed by
  stating the criterion that separates *"random partition"* from *"uniform random
  colouring"* **in advance of** looking at the rater's reason, or by conceding that both
  are the same kind and the screen loses one of its two existence-theorem items.
- **κ ≥ 0.6 with E-2 firing** is the likeliest outcome and the most misleading: high
  overall agreement can coexist with the binding conjunct being unreliable exactly where
  the screen depends on it. The 2-item existence-theorem class is where all the
  selectivity lives, so agreement there dominates the interpretation regardless of κ.

## What this run cannot show

It cannot show the screen *works*. It can only show whether the field it turns on is
reproducible. A perfectly reproducible field can still be the wrong field.
