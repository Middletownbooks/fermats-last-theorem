#!/usr/bin/env python3
"""What the P2 study costs to run, and whether it can reach its own power threshold (task 6).

The pilot is blocked on ANTHROPIC_API_KEY. This produces the estimate that makes the request
answerable, and then asks the harder question: the pre-registered power target is roughly a 30-point
shift at ~40 runs per factor level — what run count does the realised design actually need, and is
the implied budget realistic? A study that cannot reach its own power threshold should learn that
BEFORE it spends anything.

Token counts here are ESTIMATED from characters, because counting properly needs the API. The
divisor is stated and the whole point of the Python port was to stop estimating — so treat these as
planning figures and replace them with `usage` totals after the first batch.
"""
from __future__ import annotations
import argparse, math, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import battery as battery_mod, blocks, prompts  # noqa: E402
from arms import ARMS  # noqa: E402
from config import Config  # noqa: E402

CHARS_PER_TOKEN = 4.0                      # the artifact's own heuristic, kept for comparability
PRICES = {  # $ per million tokens, from the model table
    "claude-opus-5": (5.0, 25.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-haiku-4-5": (1.0, 5.0),
}
Z_975, Z_80 = 1.959963985, 0.841621234


def n_for(delta: float, base: float, deff: float) -> float:
    p1, p2 = base, max(min(base + delta, .999), .001)
    pbar = (p1 + p2) / 2
    return deff * ((Z_975 * math.sqrt(2 * pbar * (1 - pbar)) +
                    Z_80 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / delta ** 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--answer-out-tokens", type=int, default=4000,
                    help="output tokens per answer INCLUDING adaptive thinking (default 4000)")
    ap.add_argument("--judge-out-tokens", type=int, default=800)
    ap.add_argument("--base-rate", type=float, default=0.40, help="assumed bare failure rate")
    ap.add_argument("--icc", type=float, default=0.10)
    a = ap.parse_args()

    cfg = Config()
    items = battery_mod.load(str(pathlib.Path(__file__).resolve().parent.parent /
                                battery_mod.CORPUS_PATH),
                             retire=set(battery_mod.RETIRE_FOR_CORPUS))
    n_arms, n_items = len(ARMS), len(items)
    runs_main = n_arms * n_items * cfg.reps
    runs_pilot = n_items * cfg.pilot_reps

    proto = [len(prompts.proto_text(x)) for x in ARMS]
    mean_prompt_chars = (sum(proto) / len(proto)
                         + sum(len(p["statement"]) for p in items) / n_items
                         + len(blocks.core(cfg.words)) + 60)
    ans_in = mean_prompt_chars / CHARS_PER_TOKEN
    ans_out = a.answer_out_tokens
    judge_in = (len(prompts.judge_prompt({"statement": "x" * 200, "truth": "y" * 600},
                                         "z" * int(ans_out * CHARS_PER_TOKEN))) / CHARS_PER_TOKEN)

    def cost(runs: int) -> tuple[float, int, int]:
        ai, ao = PRICES[cfg.answer_model]
        tot = runs * (ans_in / 1e6 * ai + ans_out / 1e6 * ao)
        tin = runs * (ans_in + 2 * judge_in)
        tout = runs * (ans_out + 2 * a.judge_out_tokens)
        for m in (cfg.judge1_model, cfg.judge2_model):
            ji, jo = PRICES[m]
            tot += runs * (judge_in / 1e6 * ji + a.judge_out_tokens / 1e6 * jo)
        return tot, int(tin), int(tout)

    print(f"DESIGN AS CONFIGURED\n  {n_arms} arms x {n_items} items x {cfg.reps} reps = "
          f"{runs_main} main runs ({runs_main * 3} API calls)")
    print(f"  pilot: {n_items} items x {cfg.pilot_reps} reps = {runs_pilot} runs "
          f"({runs_pilot * 3} calls)")
    print(f"  models: answer {cfg.answer_model}, judges {cfg.judge1_model} + {cfg.judge2_model}")
    print(f"\nPER-RUN TOKEN ESTIMATE (chars / {CHARS_PER_TOKEN}; replace with usage after batch 1)")
    print(f"  answer in  ~{ans_in:7.0f}   answer out ~{ans_out:7.0f} (incl. adaptive thinking)")
    print(f"  judge in   ~{judge_in:7.0f} x2  judge out  ~{a.judge_out_tokens:7.0f} x2")

    print("\nCOST")
    for label, runs in (("pilot", runs_pilot), ("main study", runs_main),
                        ("pilot + main", runs_pilot + runs_main)):
        c, ti, to = cost(runs)
        print(f"  {label:14} {runs:>5} runs   ~{ti/1e6:6.1f}M in  ~{to/1e6:5.1f}M out   "
              f"~${c:,.0f}")

    print("\nPOWER: can the design reach its own threshold?")
    per_level = runs_main // 2
    m = per_level / n_items
    deff = 1 + (m - 1) * a.icc
    print(f"  runs per factor level: {per_level}  ({m:.1f} per problem per level)")
    print(f"  assumed ICC {a.icc} -> design effect {deff:.2f}; assumed base rate {a.base_rate:.0%}")
    lo, hi = 0.005, 0.60
    for _ in range(80):
        mid = (lo + hi) / 2
        if n_for(mid, a.base_rate, deff) > per_level:
            lo = mid
        else:
            hi = mid
    print(f"  smallest detectable difference at 80% power: {hi*100:.1f} points")
    print(f"\n  The pre-registered target is ~30 points. The configured design "
          f"{'REACHES' if hi * 100 <= 30 else 'DOES NOT REACH'} it.")
    for target in (30, 20, 15, 10):
        need = n_for(target / 100, a.base_rate, deff)
        total = math.ceil(need * 2 / (n_arms * n_items)) * n_arms * n_items
        c, _, _ = cost(total)
        print(f"  to detect {target:>2} points: {need:>6.0f} runs per level -> "
              f"{total:>5} main runs  ~${c:,.0f}")

    print("\n  THE BINDING CONSTRAINT IS THE DESIGN EFFECT, NOT THE BUDGET.")
    print("  Clustering by problem inflates the variance by the factor above, and it is driven by")
    print("  the SMALL NUMBER OF PROBLEMS, not the number of runs. Adding reps on 15 problems buys")
    print("  progressively less; adding problems buys more per dollar. If the pilot leaves fewer")
    print("  than ~12 usable problems, no affordable number of reps reaches 30 points, and the")
    print("  right response is to enlarge the battery rather than to buy more runs.")
    print("\n  Also unbudgeted: continuations when a reply is cut off (up to "
          f"{cfg.max_cont} per run), and re-runs after any failed batch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
