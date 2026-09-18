#!/usr/bin/env python3
"""Differential test: does this port score identically to the original artifact?

The artifact's JavaScript is not re-typed here; it is executed. Random mock runs go through both
implementations and every prediction verdict, every interval endpoint, every arm rate and both
judge kappas must agree. A divergence means the port has silently re-frozen the pre-registered
rules, which is exactly what the handoff forbids doing quietly.
"""
from __future__ import annotations
import json, math, pathlib, random, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import blocks, outcomes, arms  # noqa: E402

TOL = 1e-9
JUDGE_FLAGS = ["small_instance_shown", "scope_executed", "scope_discriminating",
               "validity_executed", "verdict_without_content", "stale_verdict",
               "tags_used", "unenforced_labelled"]


def mock_runs(seed: int, n: int) -> list[dict]:
    rng = random.Random(seed)
    battery = blocks.BATTERY0
    out = []
    for i in range(n):
        p = rng.choice(battery)
        a = rng.choice(arms.ARMS)

        def judgement() -> dict:
            j = {"return_class": rng.choice(["a", "b", "c", "between", "none"]),
                 "valid": rng.random() < 0.4, "note": ""}
            for k in JUDGE_FLAGS:
                j[k] = rng.random() < 0.5
            return j

        out.append({"id": f"main_{p['id']}_{a.id}_{i}", "phase": "main", "pid": p["id"],
                    "arm": a.id, "rep": 1, "text": "x" * 10,
                    "chars": rng.randint(200, 9000), "promptChars": rng.randint(100, 12000),
                    "truncated": False, "j1": judgement(), "j2": judgement()})
    return out


def score_python(runs: list[dict]) -> dict:
    types = {p["id"]: p["type"] for p in blocks.BATTERY0}
    R = [r for r in runs if r["phase"] == "main" and r.get("j1") and r["pid"] in types]
    eff = outcomes.block_effects(R, types)
    arm_rates = {}
    for a in arms.ARMS:
        G = [r for r in R if r["arm"] == a.id]
        arm_rates[a.id] = {"n": len(G),
                           "fail": outcomes.rate(G, "fail", types),
                           "solved": outcomes.rate(G, "solved", types),
                           "scope": outcomes.rate(G, "scope_executed", types),
                           "chars": outcomes.mean(G, lambda r: r["chars"])}
    return {"n": len(R),
            "predictions": outcomes.predictions(R, types),
            "effects": eff,
            "armRates": arm_rates,
            "kappaFail": outcomes.kappa(
                R, lambda r, j: outcomes.outcome(r, types[r["pid"]], j)["fail"]),
            "kappaScope": outcomes.kappa(R, lambda r, j: bool(j.get("scope_executed")))}


def score_js(runs: list[dict]) -> dict:
    proc = subprocess.run(
        ["node", str(ROOT / "tools" / "score_with_artifact.mjs")],
        input=json.dumps({"runs": runs}), capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def num_eq(py, js, path: str, errs: list[str]) -> None:
    """JS emits null where Python has NaN; both mean 'undefined'."""
    if py is None or (isinstance(py, float) and math.isnan(py)):
        if js is not None:
            errs.append(f"{path}: python NaN, js {js}")
        return
    if js is None:
        errs.append(f"{path}: python {py}, js null/NaN")
        return
    if abs(float(py) - float(js)) > TOL:
        errs.append(f"{path}: python {py!r} != js {js!r}")


def compare(py: dict, js: dict) -> list[str]:
    errs: list[str] = []
    if py["n"] != js["n"]:
        errs.append(f"n: {py['n']} != {js['n']}")
    for k in sorted(py["predictions"]):
        a, b = py["predictions"][k], js["predictions"][k]
        if a["v"] != b["v"]:
            errs.append(f"prediction ({k}) verdict: {a['v']} != {b['v']}")
        if a["d"] != b["d"]:
            errs.append(f"prediction ({k}) detail:\n    py: {a['d']}\n    js: {b['d']}")
    for blk in sorted(py["effects"]):
        for f in ("p1", "p0", "d", "lo", "hi"):
            num_eq(py["effects"][blk][f], js["effects"][blk][f], f"effect {blk}.{f}", errs)
        if py["effects"][blk]["n1"] != js["effects"][blk]["n1"]:
            errs.append(f"effect {blk}.n1 differs")
    for aid in sorted(py["armRates"]):
        for f in ("fail", "solved", "scope", "chars"):
            num_eq(py["armRates"][aid][f], js["armRates"][aid][f], f"arm {aid}.{f}", errs)
    for kk in ("kappaFail", "kappaScope"):
        for f in ("k", "agree"):
            num_eq(py[kk][f], js[kk][f], f"{kk}.{f}", errs)
    return errs


def test_constants_match_artifact() -> list[str]:
    fresh = json.loads(subprocess.run(
        ["node", str(ROOT / "tools" / "extract_from_artifact.mjs")],
        capture_output=True, text=True, check=True).stdout)
    committed = json.loads((ROOT / "blocks.json").read_text())
    return [] if fresh == committed else ["blocks.json is stale: regenerate it from the artifact"]


def test_prompts_match_artifact() -> list[str]:
    """Factorial and E+F arms must be byte-identical. Placebos intentionally differ."""
    import prompts
    committed = json.loads((ROOT / "blocks.json").read_text())
    errs = []
    for a in arms.ARMS:
        mine = prompts.build_prompt(a, blocks.BATTERY0[0], words=1200, framing="prove")
        theirs = committed["PROMPT_F1"][a.id]
        if a.kind in ("pfmt", "prig"):
            if mine == theirs:
                errs.append(f"{a.id}: placebo should differ (non-repeating filler) but matches")
            continue
        if mine != theirs:
            errs.append(f"{a.id}: prompt differs from the artifact's")
    return errs


def main() -> int:
    all_errs: list[str] = []
    for name, fn in (("constants", test_constants_match_artifact),
                     ("prompts", test_prompts_match_artifact)):
        errs = fn()
        print(f"{'ok  ' if not errs else 'FAIL'} {name}")
        all_errs += errs

    for seed, n in ((1, 40), (2, 200), (3, 600), (4, 5), (5, 0)):
        runs = mock_runs(seed, n)
        errs = compare(score_python(runs), score_js(runs))
        print(f"{'ok  ' if not errs else 'FAIL'} differential seed={seed} n={n}")
        all_errs += [f"[seed {seed}] {e}" for e in errs]

    if all_errs:
        print("\n" + "\n".join(f"  {e}" for e in all_errs[:40]))
        print(f"\n{len(all_errs)} failure(s).")
        return 1
    print("\nAll fidelity checks passed: this port scores identically to the artifact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
