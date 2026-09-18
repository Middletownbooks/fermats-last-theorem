#!/usr/bin/env python3
"""Command line for the P2 ablation study.

    python3 cli.py arms                     list the arms and their prompt lengths
    python3 cli.py prompt --arm X16         print one assembled prompt
    python3 cli.py pilot --batch 45         run the bare arm only, to find usable problems
    python3 cli.py select                   keep the problems whose bare failure rate is 20-80%
    python3 cli.py freeze                   hash and lock the pre-registration
    python3 cli.py run --batch 60           run the main study in batches
    python3 cli.py score                    score the six predictions, as written
    python3 cli.py export --csv runs.csv    export for analysis/analyze.py

Every run costs money against your own key. Nothing runs until you ask for it.
"""
from __future__ import annotations
import argparse, asyncio, csv, dataclasses, hashlib, json, pathlib, sys

import battery as battery_mod
import blocks, harness, outcomes, prompts
from arms import ARMS, BLOCK_IDS, arm_by_id
from config import Config, JUDGE_BIAS_NOTE
from store import Store

HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "study-state.json"
JUDGE_KEYS = ["return_class", "valid", "small_instance_shown", "scope_executed",
              "scope_discriminating", "validity_executed", "verdict_without_content",
              "stale_verdict", "tags_used", "unenforced_labelled"]


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"cfg": Config().to_dict(), "use": None, "prereg": None, "voided": [],
            "extra_battery": None}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")


def resolve(st: dict) -> tuple[Config, list[dict], list[dict]]:
    cfg = Config(**st["cfg"])
    retire = set(st.get("retired") or ())
    all_items = battery_mod.load(st.get("extra_battery"), retire=retire)
    use = st.get("use")
    items = [p for p in all_items if use is None or p["id"] in use]
    return cfg, all_items, items


def snapshot(cfg: Config, items: list[dict]) -> str:
    return json.dumps({
        "battery": items,
        "prompts": [[a.id, prompts.proto_text(a)] for a in ARMS],
        "core": blocks.core(cfg.words),
        "cfg": cfg.to_dict(),
        "preds": blocks.PRED_TEXT,
        "judge": prompts.judge_prompt({"statement": "", "truth": ""}, "", cfg.with_witness_field),
        "judge_schema": prompts.JUDGE_SCHEMA,
    }, sort_keys=True)


# --- commands --------------------------------------------------------------
def cmd_arms(a, st):
    cfg, _, items = resolve(st)
    print(f"{'arm':6} {'kind':7} {'chars':>7}  {'A B C D E F'}  label")
    for arm in ARMS:
        grid = " ".join("#" if arm.present(b) else "." for b in BLOCK_IDS)
        print(f"{arm.id:6} {arm.kind:7} {len(prompts.proto_text(arm)):>7}  {grid}  {arm.label}")
    print(f"\nfull template is {blocks.FULL_LEN} chars; both placebos are length-matched to it "
          f"with non-repeating text.")
    print(f"planned main study: {len(ARMS) * len(items) * cfg.reps} runs, "
          f"{len(ARMS) * len(items) * cfg.reps * 3} API calls before continuations.")


def cmd_prompt(a, st):
    cfg, all_items, _ = resolve(st)
    p = battery_mod.by_id(all_items, a.pid)
    print(prompts.build_prompt(arm_by_id(a.arm), p, cfg.words, cfg.framing))


def cmd_pilot(a, st):
    cfg, _, items = resolve(st)
    store = Store(HERE / "runs")
    res = asyncio.run(harness.run_queue("pilot", items, cfg, store, a.batch, seed=a.seed))
    print(res["message"])
    cmd_pilot_table(a, st)


def cmd_pilot_table(a, st):
    cfg, _, items = resolve(st)
    store = Store(HERE / "runs")
    types = battery_mod.types(items)
    R = store.judged("pilot", types)
    print(f"\n{'id':4} {'type':6} {'n':>3} {'wrong definitive':>17} {'not solved':>11}  verdict")
    for p in items:
        G = [r for r in R if r["pid"] == p["id"]]
        f = outcomes.rate(G, "fail", types)
        s = outcomes.rate(G, "solved", types)
        verdict = "" if not G else (
            "in range" if 0.2 <= f <= 0.8 else
            "in range on unsolved only" if 0.2 <= 1 - s <= 0.8 else "at floor or ceiling")
        print(f"{p['id']:4} {p['type']:6} {len(G):>3} {outcomes.pct(f):>17} "
              f"{outcomes.pct(1 - s):>11}  {verdict}")


def cmd_select(a, st):
    cfg, all_items, items = resolve(st)
    store = Store(HERE / "runs")
    types = battery_mod.types(all_items)
    R = store.judged("pilot", types)
    keep = []
    for p in all_items:
        G = [r for r in R if r["pid"] == p["id"]]
        if G and 0.2 <= outcomes.rate(G, "fail", types) <= 0.8:
            keep.append(p["id"])
    if not keep:
        print("no problem has a bare failure rate in [20%, 80%]. Run the pilot first, or accept "
              "that this battery cannot separate the arms and replace it (see battery.py).")
        return
    st["use"] = keep
    save_state(st)
    print(f"keeping {len(keep)} of {len(all_items)} problems: {', '.join(keep)}")


def cmd_battery(a, st):
    if a.swap_in_corpus:
        if st.get("prereg"):
            print("battery is locked by the pre-registration; unfreeze first")
            return 1
        st["extra_battery"] = str(HERE / battery_mod.CORPUS_PATH)
        st["retired"] = sorted(battery_mod.RETIRE_FOR_CORPUS)
        st["use"] = None
        save_state(st)
        print("repo corpus swapped in. Retired, with the reason each was expected to ceiling:")
        for k, why in sorted(battery_mod.RETIRE_FOR_CORPUS.items()):
            print(f"  {k}: {why}")
        print("\nThis retirement list is a PREDICTION. Run the pilot and re-choose from the "
              "measured per-item failure rates.")
    _, all_items, items = resolve(st)
    print(f"\n{'id':4} {'type':6} {'source':34} statement")
    for p in items:
        src = p.get("provenance", "")[:33]
        print(f"{p['id']:4} {p['type']:6} {src:34} {p['statement'][:64]}")
    n = {t: sum(1 for p in items if p["type"] == t) for t in ("true", "false", "open")}
    repo = sum(1 for p in items if p["id"].startswith("R"))
    print(f"\n{len(items)} items: {n['false']} false, {n['true']} true, {n['open']} open; "
          f"{repo} from the repo corpus, {len(items) - repo} textbook.")
    if repo:
        print("Corpus ground truths are machine-verified: tools/verify_corpus.py")


def cmd_freeze(a, st):
    cfg, _, items = resolve(st)
    if st.get("prereg"):
        print(f"already frozen: {st['prereg']['hash']}")
        return
    h = hashlib.sha256(snapshot(cfg, items).encode()).hexdigest()
    st["prereg"] = {"hash": h, "ts": __import__("time").time(), "n_items": len(items)}
    save_state(st)
    print(f"pre-registration frozen\n  hash  {h}\n  items {len(items)}\n"
          f"  runs  {len(ARMS) * len(items) * cfg.reps}\n\n"
          f"Commit this hash, and analysis/preregistration.md, before running the main study.")


def cmd_unfreeze(a, st):
    if not st.get("prereg"):
        print("not frozen")
        return
    st["voided"] = st.get("voided", []) + [st["prereg"]["hash"][:12]]
    st["prereg"] = None
    save_state(st)
    print("pre-registration voided. Runs already made were made under it; export before changing "
          "anything.")


def cmd_run(a, st):
    cfg, _, items = resolve(st)
    if not st.get("prereg"):
        print("freeze the pre-registration first (python3 cli.py freeze)")
        return 1
    store = Store(HERE / "runs")
    res = asyncio.run(harness.run_queue("main", items, cfg, store, a.batch, seed=a.seed))
    print(res["message"])


def cmd_status(a, st):
    cfg, _, items = resolve(st)
    store = Store(HERE / "runs")
    for phase in ("pilot", "main"):
        pl = harness.plan(phase, items, cfg, Store(HERE / "runs"))
        done = sum(1 for r in pl if harness.is_done(r))
        errs = sum(1 for r in store.phase(phase) if r.get("err"))
        print(f"{phase:6} {done}/{len(pl)} complete, {errs} with errors")
    print(f"prereg: {st['prereg']['hash'][:16] if st.get('prereg') else 'NOT FROZEN'}")


def cmd_score(a, st):
    cfg, _, items = resolve(st)
    store = Store(HERE / "runs")
    types = battery_mod.types(items)
    R = store.judged("main", types)
    if not R:
        print("no judged main-study runs yet")
        return
    print(f"n = {len(R)} judged runs\n")
    print("PREDICTIONS, scored as written")
    for k, o in outcomes.predictions(R, types).items():
        print(f"  ({k}) {o['v']:14} {o['d']}")
    print("\nMAIN EFFECT ON FAILURE (factorial arms only)")
    print(f"  {'blk':4} {'n+/n-':>9} {'present vs absent':>20} {'difference [95%]':>24}")
    for b, e in outcomes.block_effects(R, types).items():
        print(f"  {b:4} {str(e['n1']) + '/' + str(e['n0']):>9} "
              f"{outcomes.pct(e['p1']) + ' vs ' + outcomes.pct(e['p0']):>20} "
              f"{outcomes.pp(e['d']) + ' [' + outcomes.pp(e['lo']) + ', ' + outcomes.pp(e['hi']) + ']':>24}")
    k1 = outcomes.kappa(R, lambda r, j: outcomes.outcome(r, types[r["pid"]], j)["fail"])
    k2 = outcomes.kappa(R, lambda r, j: bool(j.get("scope_executed")))
    print(f"\nJUDGE AGREEMENT  failure: {outcomes.pct(k1['agree'])} agreement, "
          f"kappa {k1['k']:.2f} (n={k1['n']})")
    print(f"                 scope:   {outcomes.pct(k2['agree'])} agreement, kappa {k2['k']:.2f}")
    if (k1["k"] == k1["k"] and k1["k"] < 0.6) or (k2["k"] == k2["k"] and k2["k"] < 0.6):
        print("\n  Judge kappa is below 0.6. Do not report these tables without reading "
              "transcripts first.")
    over = sum(1 for r in R for s in ("j1", "j2") if r.get(s, {}).get("checker_overrode"))
    print(f"\nARITHMETIC CHECKERS overrode a judge {over} time(s).")
    print(f"\nNOTE: {JUDGE_BIAS_NOTE}")
    print("\nThese intervals treat runs as independent. Runs share problems, so they are too "
          "narrow. The pre-registered analysis is the mixed-effects model in analysis/.")


def cmd_export(a, st):
    cfg, _, items = resolve(st)
    store = Store(HERE / "runs")
    types = battery_mod.types(items)
    rows = [r for r in store.runs.values() if r.get("text") and r["pid"] in types]
    head = (["id", "phase", "problem", "type", "arm", "arm_kind"] + list(BLOCK_IDS) +
            ["rep", "prompt_chars", "answer_chars", "input_tokens", "output_tokens",
             "answer_model", "effort", "truncated", "refused",
             "fail_j1", "solved_j1", "fail_j2", "solved_j2",
             "checker_status_j1", "checker_overrode_j1", "judge1_model", "judge2_model"] +
            [f"{k}_j1" for k in JUDGE_KEYS] + [f"{k}_j2" for k in JUDGE_KEYS])
    out = pathlib.Path(a.csv)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(head)
        for r in sorted(rows, key=lambda r: r["id"]):
            arm = arm_by_id(r["arm"])
            o1 = outcomes.outcome(r, types[r["pid"]], r["j1"]) if r.get("j1") else None
            # DEFECT-1: outcome() falls back to j1 when handed a missing judgement, so
            # outcome(r, r.get("j2")) scores judge 2's column from judge 1 on every row where the
            # second judge did not run. Guard at the call site; the frozen rule is not touched.
            o2 = outcomes.outcome(r, types[r["pid"]], r["j2"]) if r.get("j2") else None
            j1, j2 = r.get("j1") or {}, r.get("j2") or {}
            w.writerow([r["id"], r["phase"], r["pid"], types[r["pid"]], r["arm"], arm.kind] +
                       [(1 if arm.lv[b] > 0 else 0) if arm.lv else "" for b in BLOCK_IDS] +
                       [r.get("rep"), r.get("prompt_chars"), r.get("chars"),
                        r.get("input_tokens"), r.get("output_tokens"),
                        r.get("answer_model"), r.get("effort"),
                        int(bool(r.get("truncated"))), int(bool(r.get("refused"))),
                        int(o1["fail"]) if o1 else "", int(o1["solved"]) if o1 else "",
                        int(o2["fail"]) if o2 else "", int(o2["solved"]) if o2 else "",
                        j1.get("checker_status", ""), int(bool(j1.get("checker_overrode"))),
                        j1.get("judge_model", ""), j2.get("judge_model", "")] +
                       [j1.get(k, "") for k in JUDGE_KEYS] +
                       [j2.get(k, "") for k in JUDGE_KEYS])
    print(f"{len(rows)} runs -> {out}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"prereg": st.get("prereg"), "cfg": cfg.to_dict(), "battery": items,
             "predictions_text": blocks.PRED_TEXT,
             "scored": outcomes.predictions(store.judged("main", types), types)
             if store.judged("main", types) else None,
             "runs": sorted(rows, key=lambda r: r["id"])}, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"full record -> {a.json}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("arms").set_defaults(fn=cmd_arms)
    p = sub.add_parser("prompt"); p.add_argument("--arm", default="X16")
    p.add_argument("--pid", default="F1"); p.set_defaults(fn=cmd_prompt)
    p = sub.add_parser("pilot"); p.add_argument("--batch", type=int, default=45)
    p.add_argument("--seed", type=int, default=None); p.set_defaults(fn=cmd_pilot)
    sub.add_parser("pilot-table").set_defaults(fn=cmd_pilot_table)
    sub.add_parser("select").set_defaults(fn=cmd_select)
    p = sub.add_parser("battery"); p.add_argument("--swap-in-corpus", action="store_true")
    p.set_defaults(fn=cmd_battery)
    sub.add_parser("freeze").set_defaults(fn=cmd_freeze)
    sub.add_parser("unfreeze").set_defaults(fn=cmd_unfreeze)
    p = sub.add_parser("run"); p.add_argument("--batch", type=int, default=60)
    p.add_argument("--seed", type=int, default=None); p.set_defaults(fn=cmd_run)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("score").set_defaults(fn=cmd_score)
    p = sub.add_parser("export"); p.add_argument("--csv", default="p2-ablation-runs.csv")
    p.add_argument("--json", default=None); p.set_defaults(fn=cmd_export)
    a = ap.parse_args()
    return a.fn(a, load_state()) or 0


if __name__ == "__main__":
    sys.exit(main())
