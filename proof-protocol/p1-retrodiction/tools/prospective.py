#!/usr/bin/env python3
"""The prospective arm: log a diagnostic's prediction BEFORE the method section is read.

Every retrospective case in this programme is contaminated. Step D measured 100% recognition of
the source problem; L2 measured 5 of 5, on encoders that were TRYING to comply and that
self-reported the contamination in the leak field every time. No amount of cutoff discipline fixes
that. This is the only instrument here that can produce an uncontaminated estimate, and it only
works if predictions are sealed before the answer is visible.

Two phases, and the seal is what makes the first one binding:

  open     record the before-board, the diagnostic's prediction and a timestamp, then SHA-256 the
           whole prediction record. The hash goes in the log beside it.
  resolve  add what the paper actually did. resolve CANNOT alter a sealed prediction: it appends a
           second record, and `verify` recomputes every seal and fails if any prediction changed.

The log is append-only JSONL. Never edit it by hand; that is what `verify` is for.

    prospective.py open --id 2609.xxxxx --problem "..." --bound "..." \
                        --target-law multiplicative --bound-law additive \
                        --predict fire --read title-and-abstract-only
    prospective.py resolve --id 2609.xxxxx --outcome board-changed --what-they-did "..."
    prospective.py verify
    prospective.py report
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "prospective" / "log.jsonl"
LAWS = ["multiplicative", "additive", "l2", "max", "none", "unknown"]
PREDICTIONS = ["fire", "no-fire", "not-applicable"]
OUTCOMES = ["board-changed", "same-board-better-play", "tight-no-change", "withdrawn", "unresolved"]
READ = ["title-and-abstract-only", "title-abstract-and-introduction", "full-text"]


def seal(rec: dict) -> str:
    body = {k: v for k, v in rec.items() if k not in ("seal", "logged_at")}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def read_log() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def append(rec: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rec["logged_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["seal"] = seal(rec)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_open(a) -> int:
    existing = [r for r in read_log() if r["id"] == a.id and r["phase"] == "open"]
    if existing:
        print(f"{a.id} already has a sealed prediction; a second one would defeat the point")
        return 1
    fired = "fire" if (a.target_law != a.bound_law and a.target_law != "unknown"
                       and a.bound_law != "unknown") else "no-fire"
    if a.predict != fired:
        print(f"WARNING: you predicted {a.predict} but the product-law rule computes {fired} from "
              f"target_law={a.target_law}, bound_law={a.bound_law}. Logging your prediction and "
              f"the computed one separately.")
    append({"phase": "open", "id": a.id, "problem": a.problem, "bound_before": a.bound,
            "product_operation": a.operation, "target_law": a.target_law,
            "bound_law": a.bound_law, "prediction": a.predict, "rule_computes": fired,
            "how_much_was_read": a.read, "diagnostic": a.diagnostic, "notes": a.notes or ""})
    print(f"sealed prediction for {a.id}: {a.predict} (rule computes {fired})")
    return 0


def cmd_resolve(a) -> int:
    log = read_log()
    if not [r for r in log if r["id"] == a.id and r["phase"] == "open"]:
        print(f"no sealed prediction for {a.id}; open one first")
        return 1
    if [r for r in log if r["id"] == a.id and r["phase"] == "resolve"]:
        print(f"{a.id} is already resolved")
        return 1
    append({"phase": "resolve", "id": a.id, "outcome": a.outcome,
            "what_they_did": a.what_they_did, "notes": a.notes or ""})
    print(f"resolved {a.id}: {a.outcome}")
    return 0


def cmd_verify(a) -> int:
    log = read_log()
    bad = []
    for r in log:
        if r.get("seal") != seal(r):
            bad.append(f"{r.get('id')} / {r.get('phase')}: SEAL BROKEN — the record was edited")
    ids = {}
    for r in log:
        ids.setdefault(r["id"], []).append(r["phase"])
    for i, phases in ids.items():
        if phases.count("open") > 1:
            bad.append(f"{i}: more than one sealed prediction")
        if phases.count("resolve") > 1:
            bad.append(f"{i}: resolved more than once")
    print(f"{len(log)} records, {len(ids)} items")
    for b in bad:
        print(f"  ERROR: {b}")
    if bad:
        return 1
    print("all seals intact; no prediction was altered after sealing")
    return 0


def cmd_report(a) -> int:
    log = read_log()
    opens = {r["id"]: r for r in log if r["phase"] == "open"}
    res = {r["id"]: r for r in log if r["phase"] == "resolve"}
    print(f"{len(opens)} sealed predictions, {len(res)} resolved, "
          f"{len(opens) - len(res)} awaiting resolution\n")
    print(f"  {'id':16} {'pred':14} {'outcome':26} {'read':32} verdict")
    tp = fp = tn = fn = 0
    for i, o in sorted(opens.items()):
        r = res.get(i)
        if not r:
            print(f"  {i:16} {o['prediction']:14} {'(awaiting)':26} {o['how_much_was_read']:32} —")
            continue
        pos = r["outcome"] == "board-changed"
        f_ = o["prediction"] == "fire"
        v = ("TP" if f_ and pos else "FALSE POSITIVE" if f_ else
             "FALSE NEGATIVE" if pos else "TN")
        tp += f_ and pos; fp += f_ and not pos; fn += (not f_) and pos; tn += (not f_) and not pos
        print(f"  {i:16} {o['prediction']:14} {r['outcome']:26} {o['how_much_was_read']:32} {v}")
    n = tp + fp + tn + fn
    if n:
        print(f"\n  uncontaminated 2x2 on {n} resolved item(s): "
              f"TP {tp}  FP {fp}  FN {fn}  TN {tn}")
    print("\n  This is the ONLY table in the programme not built on cases whose answers were "
          "already known to the encoder.\n  It will take a long time to say anything. That is the "
          "cost of it meaning something.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("open")
    p.add_argument("--id", required=True); p.add_argument("--problem", required=True)
    p.add_argument("--bound", required=True); p.add_argument("--operation", default="unknown")
    p.add_argument("--target-law", choices=LAWS, default="unknown")
    p.add_argument("--bound-law", choices=LAWS, default="unknown")
    p.add_argument("--predict", choices=PREDICTIONS, required=True)
    p.add_argument("--diagnostic", default="product-law-matching")
    p.add_argument("--read", choices=READ, required=True)
    p.add_argument("--notes"); p.set_defaults(fn=cmd_open)
    p = sub.add_parser("resolve")
    p.add_argument("--id", required=True); p.add_argument("--outcome", choices=OUTCOMES, required=True)
    p.add_argument("--what-they-did", required=True); p.add_argument("--notes")
    p.set_defaults(fn=cmd_resolve)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
