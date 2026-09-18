#!/usr/bin/env python3
"""Structural validation of the P1 tree.

Fails (exit 1) on anything that would corrupt a scoring round:
  * a case with no held-out answer, or a held-out answer with no case;
  * after-board text that has leaked into a before-board;
  * a before-board citing a source dated at or after its superseding paper (L2);
  * a transformation label outside the taxonomy vocabulary;
  * a calibration id appearing among the scoreable items.

Warnings do not fail the run but are printed.
"""
from __future__ import annotations
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAXONOMY = ROOT.parent / "p3-taxonomy" / "taxonomy.json"
SHINGLE = 8                      # words; long enough that overlap is copying, not coincidence
FORBIDDEN_IN_BEFORE = {"after_board", "transformation", "source", "label_kappa"}

errors: list[str] = []
warnings: list[str] = []


def load(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def shingles(text: str, n: int = SHINGLE) -> set[tuple[str, ...]]:
    ws = words(text)
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def all_strings(obj) -> str:
    """Every string anywhere in a JSON document, concatenated."""
    out: list[str] = []
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, str):
            out.append(cur)
        elif isinstance(cur, dict):
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return " ".join(out)


def years(s: str) -> list[int]:
    return [int(y) for y in re.findall(r"\b(1[89]\d{2}|20\d{2})\b", s or "")]


def main() -> int:
    vocab = load(TAXONOMY)["label_vocabulary"]
    allowed = set(vocab["atoms"]) | set(vocab["special"])
    sep = vocab["combination_separator"]

    case_dirs = sorted(p for p in (ROOT / "cases").iterdir() if p.is_dir())
    held_files = sorted((ROOT / "heldout").glob("*.json"))
    case_ids = {p.name for p in case_dirs}
    held_ids = {p.stem for p in held_files}

    for missing in sorted(case_ids - held_ids):
        errors.append(f"case {missing} has no held-out answer")
    for orphan in sorted(held_ids - case_ids):
        errors.append(f"held-out answer {orphan} has no case")

    # --- per case -------------------------------------------------------
    for d in case_dirs:
        before = load(d / "before.json")
        if before.get("id") != d.name:
            errors.append(f"{d.name}: id field is {before.get('id')!r}")
        for key in FORBIDDEN_IN_BEFORE:
            if key in before:
                errors.append(f"{d.name}: before.json carries forbidden key {key!r}")

        hp = ROOT / "heldout" / f"{d.name}.json"
        if not hp.exists():
            continue
        held = load(hp)

        # L1/L3 leak check: no long shingle of the after-board may appear in the before-board.
        before_sh = shingles(all_strings(before))
        after_sh = shingles(held.get("after_board", ""))
        overlap = before_sh & after_sh
        if overlap:
            sample = " ".join(sorted(overlap)[0])
            errors.append(f"{d.name}: after-board text leaked into before.json: ...{sample}...")

        # `verification_sources` may post-date the cutoff: they are what a later reader checked
        # the row against, not what the encoder was allowed to use. Conflating the two produced a
        # false positive here, which is how the distinction was found.
        for vs in before.get("verification_sources", []):
            if not vs.get("role"):
                warnings.append(f"{d.name}: verification source {vs.get('cite')!r} has no role note")

        # L2: sources_before must pre-date the superseding paper.
        sup = years(before.get("supersede", {}).get("date", ""))
        sup_year = min(sup) if sup else None
        if sup_year is None:
            warnings.append(f"{d.name}: superseding paper has no parseable date")
        else:
            for src in before.get("sources_before", []):
                ys = years(str(src.get("date", "")))
                if not ys:
                    warnings.append(f"{d.name}: source {src.get('cite')!r} has no parseable date")
                    continue
                latest = max(ys)
                if latest > sup_year:
                    errors.append(
                        f"{d.name}: source {src.get('cite')!r} dated {latest} is not before the "
                        f"superseding paper ({sup_year})")
                elif latest == sup_year:
                    warnings.append(
                        f"{d.name}: source {src.get('cite')!r} shares its year ({latest}) with the "
                        f"superseding paper; check it pre-dates it")

        label = held.get("transformation", "")
        atoms = label.split(sep) if label else []
        for a in atoms:
            if a not in allowed:
                errors.append(f"{d.name}: transformation atom {a!r} is not in the vocabulary")
        if held.get("second_blind_label") is None:
            warnings.append(f"{d.name}: no second blind label, so label kappa is not computable")

    # --- twins and controls --------------------------------------------
    # REJECTED.json is a ledger of candidates that failed vetting, not a twin.
    twins = sorted(p for p in (ROOT / "twins").glob("*.json")
                   if p.stem != "REJECTED")
    controls = sorted((ROOT / "controls").glob("*.json"))
    for p in twins:
        t = load(p)
        if t.get("twin_of") and t["twin_of"] not in case_ids:
            errors.append(f"{p.stem}: twin_of {t['twin_of']!r} is not a case")
        if t.get("expected_diagnostic_behaviour") != "fires":
            warnings.append(f"{p.stem}: unexpected expected_diagnostic_behaviour")
    for p in controls:
        c = load(p)
        if c.get("expected_diagnostic_behaviour") != "must-not-fire":
            errors.append(f"{p.stem}: a control must be marked must-not-fire")

    # --- calibration exclusions ----------------------------------------
    calib = load(ROOT / "calibration" / "excluded.json")
    scoreable = case_ids | {p.stem for p in twins} | {p.stem for p in controls}
    for item in calib["items"]:
        if item["id"] in scoreable:
            errors.append(f"calibration item {item['id']!r} appears among scoreable items")

    # --- report ---------------------------------------------------------
    print(f"cases {len(case_dirs)}  twins {len(twins)}  controls {len(controls)}  "
          f"calibration-excluded {len(calib['items'])}")
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR:   {e}")
    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1
    print(f"\nOK ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
