"""The frozen scoring rules, ported from the artifact.

These are the pre-registered rules. They are ported to behave identically, NaN semantics included,
and tests/test_fidelity.py checks that by running the artifact's own JavaScript on the same random
inputs and comparing every verdict. Do not "clean up" anything in this file: a change here is a
re-freeze, and must be declared as one.

Two JavaScript behaviours that a naive port gets wrong, and which are reproduced deliberately:
  * a rate over an empty group is NaN, not 0, and every comparison against NaN is false, so an
    empty group yields UNDETERMINED rather than a spurious verdict;
  * Math.round is floor(x + 0.5), not Python's round-half-to-even.
"""
from __future__ import annotations
import math
from typing import Callable, Iterable, Sequence

from arms import arm_by_id, BARE, FULL, BLOCK_IDS

NAN = float("nan")


def js_round(x: float) -> int:
    return math.floor(x + 0.5)


def pct(x: float) -> str:
    return "–" if math.isnan(x) else f"{js_round(x * 100)}%"


def _jsnum(x: float) -> str:
    """JavaScript renders Math.round(NaN) as the string "NaN"; reproduce that, not an em dash."""
    return "NaN" if math.isnan(x) else str(js_round(x))


def pp(x: float) -> str:
    if math.isnan(x):
        return "–"
    return ("+" if x > 0 else "") + str(js_round(x * 100))


# --- per-run outcome -------------------------------------------------------
def outcome(run: dict, problem_type: str, judgement: dict | None = None) -> dict | None:
    """The artifact's outcome(). `problem_type` is the battery item's true/false/open."""
    j = judgement or run.get("j1")
    if not j:
        return None
    c, v = j.get("return_class"), bool(j.get("valid"))
    definitive = c in ("a", "b", "between")
    correct = (problem_type == "true" and c == "a" and v) or \
              (problem_type == "false" and c == "b" and v)
    return {"fail": definitive and not correct,
            "solved": correct or (problem_type == "open" and c == "c"),
            "cls": c}


def val(run: dict, key: str, types: dict[str, str]) -> bool:
    if key in ("fail", "solved"):
        return outcome(run, types[run["pid"]])[key]
    return bool(run["j1"].get(key))


def rate(runs: Sequence[dict], key: str, types: dict[str, str]) -> float:
    if not runs:
        return NAN
    return sum(1 for r in runs if val(r, key, types)) / len(runs)


def mean(runs: Sequence[dict], f: Callable[[dict], float]) -> float:
    if not runs:
        return NAN
    return sum(f(r) for r in runs) / len(runs)


def _term(p: float, n: int) -> float:
    return NAN if n == 0 else p * (1 - p) / n


def diff(g1: Sequence[dict], g0: Sequence[dict], key: str, types: dict[str, str]) -> dict:
    p1, p0 = rate(g1, key, types), rate(g0, key, types)
    n1, n0 = len(g1), len(g0)
    se = math.sqrt(_term(p1, n1) + _term(p0, n0))
    d = p1 - p0
    return {"p1": p1, "p0": p0, "n1": n1, "n0": n0, "d": d,
            "lo": d - 1.96 * se, "hi": d + 1.96 * se}


def kappa(runs: Sequence[dict], f: Callable[[dict, dict], bool]) -> dict:
    pairs = [(f(r, r["j1"]), f(r, r["j2"])) for r in runs if r.get("j1") and r.get("j2")]
    n = len(pairs)
    if not n:
        return {"n": 0, "k": NAN, "agree": NAN}
    a = sum(1 for x, y in pairs if x == y) / n
    p1 = sum(1 for x, _ in pairs if x) / n
    p2 = sum(1 for _, y in pairs if y) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    return {"n": n, "agree": a, "k": NAN if pe == 1 else (a - pe) / (1 - pe)}


# --- the six pre-registered predictions ------------------------------------
def predictions(runs: Sequence[dict], types: dict[str, str]) -> dict[str, dict]:
    fact = [r for r in runs if arm_by_id(r["arm"]).kind == "fact"]

    def eff(block: str, key: str) -> dict:
        hi = [r for r in fact if arm_by_id(r["arm"]).lv[block] > 0]
        lo = [r for r in fact if arm_by_id(r["arm"]).lv[block] < 0]
        return diff(hi, lo, key, types)

    def by(arm_id: str) -> list[dict]:
        return [r for r in runs if r["arm"] == arm_id]

    def ok(e: dict) -> bool:
        return not math.isnan(e["lo"])

    out: dict[str, dict] = {}

    e = eff("D", "fail")
    out["a"] = {"v": "UNDETERMINED" if not ok(e) else ("REFUTED" if e["hi"] < 0 else "NOTREFUTED"),
                "d": f"D effect on failure {pp(e['d'])} pts [{pp(e['lo'])}, {pp(e['hi'])}]"}

    e1, e2 = eff("E", "verdict_without_content"), eff("E", "fail")
    if not ok(e1) or not ok(e2):
        v = "UNDETERMINED"
    elif e1["hi"] < 0 and e2["hi"] < 0:
        v = "SUPPORTED"
    elif e1["d"] >= 0 and e2["d"] >= 0:
        v = "REFUTED"
    else:
        v = "UNDETERMINED"
    out["b"] = {"v": v,
                "d": (f"E on verdict-without-content {pp(e1['d'])} [{pp(e1['lo'])}, {pp(e1['hi'])}]; "
                      f"on failure {pp(e2['d'])} [{pp(e2['lo'])}, {pp(e2['hi'])}]")}

    F = [r for r in fact if arm_by_id(r["arm"]).lv["F"] > 0]
    sc = by("EFSC")
    pF, pS = rate(F, "scope_executed", types), rate(sc, "scope_executed", types)
    out["c"] = {"v": "UNDETERMINED" if len(F) < 10 or len(sc) < 10
                else ("SUPPORTED" if pF < .5 and pS > .8 else "REFUTED"),
                "d": f"prose {pct(pF)} (n={len(F)}); return fields {pct(pS)} (n={len(sc)})"}

    A, B = by("EFON"), by(FULL.id)
    fa, fb = rate(A, "fail", types), rate(B, "fail", types)
    ca, cb = mean(A, lambda r: r["chars"]), mean(B, lambda r: r["chars"])
    out["d"] = {"v": "UNDETERMINED" if len(A) < 10 or len(B) < 10
                else ("SUPPORTED" if fa <= fb + .05 and ca <= .5 * cb else "REFUTED"),
                "d": (f"failure {pct(fa)} vs {pct(fb)}; mean length "
                      f"{_jsnum(ca)} vs {_jsnum(cb)} chars")}

    b_ = rate(by(BARE.id), "fail", types)
    f_ = rate(by(FULL.id), "fail", types)
    g_ = rate(by("PRIG"), "fail", types)
    gap = b_ - f_
    out["e"] = {"v": "UNDETERMINED" if math.isnan(gap) or math.isnan(g_) or gap <= 0
                else ("SUPPORTED" if b_ - g_ >= .5 * gap else "REFUTED"),
                "d": f"bare {pct(b_)}, rigour placebo {pct(g_)}, full {pct(f_)}"}

    e1, e2 = eff("A", "unenforced_labelled"), eff("A", "fail")
    if not ok(e1) or not ok(e2):
        v = "UNDETERMINED"
    elif e2["hi"] < 0:
        v = "REFUTED"
    elif e1["lo"] > 0 and e2["lo"] <= 0 and e2["hi"] >= 0:
        v = "SUPPORTED"
    else:
        v = "UNDETERMINED"
    out["f"] = {"v": v,
                "d": (f"A on labelling {pp(e1['d'])} [{pp(e1['lo'])}, {pp(e1['hi'])}]; "
                      f"on failure {pp(e2['d'])} [{pp(e2['lo'])}, {pp(e2['hi'])}]")}
    return out


def block_effects(runs: Sequence[dict], types: dict[str, str]) -> dict[str, dict]:
    fact = [r for r in runs if arm_by_id(r["arm"]).kind == "fact"]
    out = {}
    for b in BLOCK_IDS:
        hi = [r for r in fact if arm_by_id(r["arm"]).lv[b] > 0]
        lo = [r for r in fact if arm_by_id(r["arm"]).lv[b] < 0]
        out[b] = diff(hi, lo, "fail", types)
    return out
