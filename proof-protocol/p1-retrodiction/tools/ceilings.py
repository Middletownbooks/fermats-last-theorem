#!/usr/bin/env python3
"""The ceiling register: boards whose practitioners said, IN PRINT AND BEFORE THE FACT, that the
board could not reach the known or conjectured truth.

Why this exists. D25 measured that the retrospective arm is saturated by recall: a rule-less rater
separates positives from twins perfectly, because it only has to name the problem. Underneath that
is a subtler problem -- every leak in the retrospective corpus is one WE identified after the board
was left, so the item's ground truth is our own hindsight. A ceiling statement is the opposite: the
cap is named by the people on the board, with a number, while the outcome is still open. That is the
one retrospective structure whose LABEL does not come from hindsight, and for an unresolved ceiling
it is a prospective item with a published resolution criterion.

This is NOT part of the prospective arm and must never be pooled with it. The arm watches new
arXiv postings and resolves in weeks; a ceiling may stand for a decade. Keeping one number for both
would let a slow item dilute a fast one.

Records are sealed with the SAME function as the prospective arm (imported, not copied) and the log
is append-only. `add` takes a JSON file so a record can be reviewed before it is sealed.

    ceilings.py add --file ceilings/roth-density-increment-bohr.json
    ceilings.py amend --id <id> --field <path> --was "..." --now "..." --why "..."
    ceilings.py verify
    ceilings.py report
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prospective import seal                             # one definition of a seal, not two

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "ceilings" / "register.jsonl"

# How good the evidence for the CEILING is. The first two are what the register is for.
TIERS = {
    "STATED-BY-AUTHORS": "the people who built or pushed the board say in print that the board is "
                         "capped, with a number attached",
    "STATED-BY-EXPOSITOR": "a survey or exposition says it, not the authors",
    "DERIVED-FROM-PRIMARY": "we computed the cap from a primary statement; the derivation must say "
                            "where it is checked",
    "CLAIMED-POST-HOC": "stated only after the board was left -- DISQUALIFIED, this is hindsight, "
                        "which is the contamination the register exists to avoid",
}
# What the cap is being compared against, which is not always a theorem.
TRUTH = {"THEOREM": "a construction or proof puts the truth beyond the cap",
         "CONJECTURE": "the truth is believed, not proved; the cap is then a cap relative to a "
                       "conjecture and must be read as one"}
STATUS = {"open": "the board has not been left and the cap has not been beaten",
          "held-and-board-left": "the cap held; the advance came from leaving the board",
          "broken-on-the-same-board": "the cap was beaten without leaving the board -- the ceiling "
                                      "statement was wrong, which is the most informative outcome",
          "withdrawn": "the register entry was wrong about what the source says"}
REQUIRED = ("id", "problem", "board", "ceiling", "truth", "evidence_tier", "quote", "source",
            "source_as_of", "resolution_status", "resolution_criterion")


def cap_short_of_truth(rec: dict) -> tuple[bool, str]:
    """A ceiling must fall short of the truth, with one exception that the second registered
    instance forced: a cap can be a SUPREMUM THAT IS NEVER ATTAINED. GPY's board needs
    rho_k(F) > 4 and rho_k(F) < 4 for every k and every one-variable F, so the cap and the
    requirement are the same number and the board misses by an epsilon no k can close. Encoding
    that as 3.999 to satisfy a strict inequality would be fitting the data to the instrument, so
    `cap_attained: false` is declared instead and equality is then allowed, with a note saying
    which side of the boundary is reachable."""
    cap = rec["ceiling"].get("cap_value")
    truth = rec["truth"].get("value_num")
    if not (isinstance(cap, (int, float)) and isinstance(truth, (int, float))):
        return True, ""
    if cap < truth:
        return True, ""
    if cap == truth and rec["ceiling"].get("cap_attained") is False:
        if not rec["ceiling"].get("boundary_note"):
            return False, ("a cap equal to the truth needs `boundary_note` saying which side of the "
                           "boundary the board can reach")
        return True, ""
    return False, (f"the cap ({cap}) must fall SHORT of the truth ({truth}); a cap at or past the "
                   f"truth is not a ceiling, unless it is an unattained supremum declared with "
                   f"`cap_attained: false` and a `boundary_note`")


def read_log() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_add(a) -> int:
    rec = json.loads(pathlib.Path(a.file).read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in rec]
    if missing:
        print(f"REFUSING: record is missing {', '.join(missing)}")
        return 1
    if rec["evidence_tier"] not in TIERS:
        print(f"REFUSING: evidence_tier must be one of {', '.join(TIERS)}")
        return 1
    if rec["evidence_tier"] == "CLAIMED-POST-HOC":
        print("REFUSING: a post-hoc claim is hindsight, which is exactly what this register excludes")
        return 1
    if rec["truth"].get("status") not in TRUTH:
        print(f"REFUSING: truth.status must be one of {', '.join(TRUTH)}")
        return 1
    if rec["resolution_status"] not in STATUS:
        print(f"REFUSING: resolution_status must be one of {', '.join(STATUS)}")
        return 1
    ok, why = cap_short_of_truth(rec)
    if not ok:
        print(f"REFUSING: {why}")
        return 1
    if any(r["id"] == rec["id"] for r in read_log()):
        print(f"{rec['id']} is already registered; the log is append-only")
        return 1
    rec["phase"] = "register"
    rec["logged_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["seal"] = seal(rec)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"registered {rec['id']} ({rec['evidence_tier']}, {rec['resolution_status']})")
    return 0


def cmd_amend(a) -> int:
    """Correct a registered record WITHOUT touching its seal.

    The first thing that happened to this register was that one of my own figures in it was wrong
    (0.55 for a quantity that is 0.5785), and the record was already sealed. Editing the line would
    have made the seal meaningless, so a correction is a new sealed record that names the field, the
    old text and the new one. The original stays readable, which is the point: this programme has
    retracted its own claims before and the standard is to record, not to erase.
    """
    log = read_log()
    if not [r for r in log if r["id"] == a.id and r["phase"] == "register"]:
        print(f"no registered ceiling with id {a.id}")
        return 1
    broken = [r["id"] for r in log if r.get("seal") != seal(r)]
    if broken:
        print("REFUSING to amend while seals are broken on " + ", ".join(broken))
        return 1
    rec = {"phase": "amend", "id": a.id, "field": a.field, "was": a.was, "now": a.now,
           "why": a.why, "amends_seal": next(r["seal"] for r in log
                                             if r["id"] == a.id and r["phase"] == "register")}
    rec["logged_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rec["seal"] = seal(rec)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"amended {a.id}.{a.field}: {a.was!r} -> {a.now!r} (original record untouched)")
    return 0


def cmd_verify(a) -> int:
    log = read_log()
    bad = [f"{r.get('id')}: SEAL BROKEN -- the record was edited in place" for r in log
           if r.get("seal") != seal(r)]
    amendments = [r for r in log if r["phase"] == "amend"]
    for r in [x for x in log if x["phase"] == "register"]:
        ok, why = cap_short_of_truth(r)
        if not ok:
            bad.append(f"{r['id']}: {why}")
    print(f"{len([r for r in log if r['phase'] == 'register'])} registered ceiling(s), "
          f"{len(amendments)} amendment(s)")
    for r in amendments:
        if r["amends_seal"] not in {x.get("seal") for x in log if x["phase"] == "register"}:
            bad.append(f"{r['id']}: amendment points at a record that is not in the log")
    for b in bad:
        print(f"  ERROR: {b}")
    if bad:
        return 1
    print("all seals intact; every cap falls short of its truth")
    return 0


def cmd_report(a) -> int:
    log = read_log()
    by = {}
    for r in log:
        if r["phase"] == "register":
            by.setdefault(r["resolution_status"], []).append(r)
    amendments = [r for r in log if r["phase"] == "amend"]
    print(f"{sum(len(v) for v in by.values())} registered ceiling(s), "
          f"{len(amendments)} amendment(s)\n")
    for st in STATUS:
        for r in by.get(st, []):
            print(f"  {r['id']}")
            print(f"    board      {r['board']}")
            print(f"    cap        {r['ceiling'].get('cap')} of {r['ceiling'].get('quantity')}")
            print(f"    truth      {r['truth'].get('value')} ({r['truth'].get('status')})")
            print(f"    evidence   {r['evidence_tier']}  [{r['source']}, {r['source_as_of']}]")
            print(f"    status     {st} -- {STATUS[st]}")
            if r.get("prediction"):
                print(f"    prediction {r['prediction'].get('claim')}")
            for am in [x for x in amendments if x["id"] == r["id"]]:
                print(f"    AMENDED    {am['field']}: {am['was']} -> {am['now']} ({am['why']})")
            print()
    n_reg = sum(len(v) for v in by.values())
    n_open = len(by.get("open", []))
    print(f"  {n_open} open, {n_reg - n_open} resolved.")
    print("  An open ceiling is an uncontaminated item: the answer does not exist yet, so no rater")
    print("  can recall it. A resolved one cannot be uncontaminated -- what it supplies instead is a")
    print("  label written down BEFORE the resolution, so the item's ground truth is not our own")
    print("  hindsight. Neither is a substitute for the prospective arm, and the counts stay separate.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add"); p.add_argument("--file", required=True); p.set_defaults(fn=cmd_add)
    p = sub.add_parser("amend")
    p.add_argument("--id", required=True); p.add_argument("--field", required=True)
    p.add_argument("--was", required=True); p.add_argument("--now", required=True)
    p.add_argument("--why", required=True); p.set_defaults(fn=cmd_amend)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
