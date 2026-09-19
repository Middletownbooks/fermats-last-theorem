#!/usr/bin/env python3
"""Build Report Q's tables from the round3_*.json artifacts. Read-only."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ["A3u", "A3u52", "C3u", "B3uo", "B3u", "A3", "C3", "D3", "B3", "B3all", "A3plus", "A5"]
LABEL = {
    "A3u": "unbeamed, carry nothing",
    "A3u52": "unbeamed, 7 extra self-formed atoms",
    "C3u": "unbeamed, 7 RANDOM out-of-reach carried",
    "B3uo": "unbeamed, 7 promoted carried, OUTER ONLY",
    "B3u": "unbeamed, 7 promoted carried, formation + outer",
    "A3": "beamed, carry nothing",
    "C3": "beamed, random carry",
    "D3": "beamed, carried at expanded cost",
    "B3": "beamed, carried at cost 1",
    "B3all": "beamed, every promoted term carried",
    "A3plus": "beamed, carry nothing, cost 7",
    "A5": "beamed, body budget 5, carry nothing",
}


def load():
    out = {}
    for c in ORDER:
        p = HERE / ("round3_%s.json" % c)
        if p.exists():
            out[c] = json.loads(p.read_text())
    return out


def main():
    R = load()
    print("| cond | what | atoms | carried | expansions | exhausted | classes | certified | net new | live targets |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for c, d in R.items():
        i = d["info"]
        print("| %s | %s | %d | %d | %s | %s | %s | %d | %d | %d/%d |" % (
            c, LABEL[c], i["outer_atoms"], i["carried_over"], f"{d['expansions']:,}",
            "yes" if not d["truncated_at_cap"] else "NO",
            f"{d['classes_TRAIN']:,}", d["certified_count"], d["certified_net_new_count"],
            d["targets_reached_count"], len(d["targets_live"])))

    base = R.get("A3u")
    if base:
        print("\nAgainst the exhaustive A3u:")
        for c, d in R.items():
            if c == "A3u":
                continue
            extra = sorted(set(d["certified"]) - set(base["certified"]))
            lost = sorted(set(base["certified"]) - set(d["certified"]))
            print("  %-7s +%-2d %-70s  lost %s" % (c, len(extra), ",".join(extra)[:70], lost or "none"))

    print("\nEnablement: certified terms that are NOT a carried atom and are unreachable without one")
    for c, d in R.items():
        rows = [(k, v) for k, v in sorted(d["certified"].items())
                if v.get("uses_carried") and not v.get("reachable_without_carried")
                and k in d["certified_net_new"]]
        if rows:
            print("  %s:" % c)
            for k, v in rows:
                print("     %-16s cost %d  %s" % (k, v["cost"], v["term"]))

    print("\nReachable space |R(s)| on TRAIN")
    lv = sorted({l["cost"] for d in R.values() for l in d["level_log"]})
    print("| cost | " + " | ".join(R) + " |")
    print("|---" * (len(R) + 1) + "|")
    for s in lv:
        row = []
        for d in R.values():
            hit = [l for l in d["level_log"] if l["cost"] == s]
            row.append(f"{hit[0]['classes_cumulative']:,}" if hit else "")
        print("| %d | %s |" % (s, " | ".join(row)))


if __name__ == "__main__":
    main()
