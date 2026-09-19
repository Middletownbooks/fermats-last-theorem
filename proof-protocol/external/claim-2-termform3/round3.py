#!/usr/bin/env python3
"""
Round 3. One condition per invocation: `python3 round3.py A3|B3|C3|D3|B3all|A5|A3plus|A3u|B3u`.

Follows PREREG.md (sha256 in PREREG.sha256), committed before this file was
written. Deviations are recorded in each output under "deviations", with the
reason, and were all made before any Round-3 result was seen.
"""
import ast
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
T2 = HERE.parent / "termform2"
sys.path.insert(0, str(HERE.parent / "termform"))
sys.path.insert(0, str(T2))
sys.path.insert(0, str(HERE.parent))

import invariants as INV                                     # noqa: E402
import synth3 as S                                           # noqa: E402
from outer import Outer, digest, verify_operators            # noqa: E402
from round2 import EVALQ, HOLDOUT, RESERVE, TRAIN            # noqa: E402
from stages import abstention, disagreement                  # noqa: E402

import numpy as np                                           # noqa: E402

SEED = 20260919
PREREG_SHA = (HERE / "PREREG.sha256").read_text().strip()

# condition -> body budget, carried set, outer cost, beam, unit cap
CONDITIONS = {
    "A3":     dict(body=3, carry="none",         cost=5, beam=1200,    units=500),
    "B3":     dict(body=3, carry="out_of_reach", cost=5, beam=1200,    units=500),
    "C3":     dict(body=3, carry="random",       cost=5, beam=1200,    units=500),
    "D3":     dict(body=3, carry="oor_expanded", cost=5, beam=1200,    units=500),
    "B3all":  dict(body=3, carry="all_promoted", cost=5, beam=1200,    units=500),
    "A5":     dict(body=5, carry="none",         cost=5, beam=1200,    units=500),
    "A3plus": dict(body=3, carry="none",         cost=7, beam=2400,    units=500),
    # the beam-free pair: small enough to exhaust the cost-5 space
    "A3u":    dict(body=3, carry="none",         cost=5, beam=10 ** 9, units=40),
    "B3u":    dict(body=3, carry="out_of_reach", cost=5, beam=10 ** 9, units=40),
    # controls for the two ways B3u could be right for the wrong reason
    "B3uo":   dict(body=3, carry="outer_only",   cost=5, beam=10 ** 9, units=40),
    "C3u":    dict(body=3, carry="random",       cost=5, beam=10 ** 9, units=40),
    "A3u52":  dict(body=3, carry="none",         cost=5, beam=10 ** 9, units=47),
}

DEVIATIONS = [
    {"what": "the outer search is beamed in every condition except A3u and B3u",
     "why": ("PREREG section 4 promised an unbeamed cost-5 search in every "
             "pre-registered condition, on the expectation that the body cut would "
             "shrink the atom set enough to exhaust the space. It does not: "
             "formation at body budget 3 yields 599 formed terms, and at ~500 atoms "
             "the cost-5 space is of order 10^9 expansions. The beam-free comparison "
             "is therefore run as a separate pair, A3u and B3u, at a unit cap of 40 "
             "(45 and 52 atoms), which IS exhaustible; the main conditions keep "
             "Report P's unit cap 500 and beam 1200 so the numbers stay comparable "
             "with Report P's. Both are reported. Made before any result was seen."),
     "affects": "all conditions equally"},
    {"what": "targets semantically equal on TRAIN to a carried term are STRUCK",
     "why": ("The frozen promotion rule promotes certified terms, and two of Round "
             "2 condition A's certified terms ARE pre-registered targets. Handing a "
             "condition a target as a cost-1 atom makes that target non-discriminating "
             "-- the T3 lesson of Report P section 8. The strike list is computed "
             "mechanically in this file, applies to every condition, and both the "
             "struck and unstruck counts are reported."),
     "affects": "the target comparison only"},
    {"what": "three further unbeamed controls added: B3uo, C3u, A3u52",
     "why": ("B3u differs from A3u in two ways at once, not one: it has 7 more atoms, "
             "AND its 40 self-formed units are selected from a 6 970-term formation pool "
             "instead of A3u's 599, because the carried atoms enter formation. B3uo "
             "withholds the carried terms from formation (Report P's Bo), C3u carries 7 "
             "random out-of-reach terms instead, and A3u52 gives A3u 7 extra self-formed "
             "units so the atom count matches. Added after seeing B3u's headline numbers "
             "and before drawing any conclusion from them; they can only weaken the "
             "positive result, never strengthen it."),
     "affects": "the interpretation of B3u vs A3u"},
]


def promoted(kind):
    d = json.loads((HERE / "promoted3.json").read_text())
    cert = json.loads((HERE / "certificate.json").read_text())
    oor = set(cert["certified_out_of_reach"])
    rows = d["terms"]
    if kind == "all_promoted":
        pick = [r for r in rows if r["term"] != "n"]
    else:
        pick = [r for r in rows if r["term"] in oor]
    return [ast.literal_eval(repr(_parse(r["printed_with_units"]))) for r in pick], pick


def _parse(printed):
    from promote import parse
    return parse(printed)


def random_out_of_reach(k, exclude_vectors, body=3):
    """Condition C3: the same NUMBER of formed terms that are also out of reach at
    body budget 3, drawn with a fixed seed from the body-budget-5 formation pool,
    excluding anything semantically equal on TRAIN to a carried B3 term."""
    S.reset()
    formed = S.form_leaves(TRAIN, size1=3, size2=5, verbose=False, tag="poolC")
    pool = []
    for v, t in formed.items():
        # out of reach iff the receiving round's own formation cannot produce it
        pool.append((v, t))
    reach = set(json.loads((HERE / "reach_vectors.json").read_text())["vectors"])
    out = []
    rng = random.Random(SEED)
    cand = [(v, t) for v, t in pool
            if S.vkey(v).hex() not in reach and v not in exclude_vectors]
    rng.shuffle(cand)
    # NO reset here: the chosen terms may contain stage-1 units, whose definitions
    # live in the registry. Resetting it before the caller turns them into leaves
    # loses those definitions and raises KeyError -- which is exactly what the first
    # run of C3u did, and why this comment exists.
    return [t for _, t in cand[:k]], len(cand)


def reach_vectors():
    """Value-vector digests of every term formable at body budget 3. Cached."""
    p = HERE / "reach_vectors.json"
    if p.exists():
        return
    S.reset()
    formed = S.form_leaves(TRAIN, size1=3, size2=3, verbose=False, tag="reach")
    p.write_text(json.dumps({"count": len(formed),
                             "vectors": [S.vkey(v).hex() for v in formed]}, indent=0))
    S.reset()


def build(cond):
    c = CONDITIONS[cond]
    S.reset()
    info = {"condition": cond, **{k: v for k, v in c.items()}}
    forced, prov = [], []
    if c["carry"] in ("out_of_reach", "all_promoted", "oor_expanded", "outer_only"):
        terms, prov = promoted("all_promoted" if c["carry"] == "all_promoted"
                               else "out_of_reach")
        cost = (lambda t: 1) if c["carry"] != "oor_expanded" else S.expanded_size
        forced = [S.leaf(t, TRAIN, cost=cost(t)) for t in terms]
        info["carried_costs"] = sorted(S.size(u) for u in forced)
    elif c["carry"] == "random":
        oor_terms, _ = promoted("out_of_reach")
        exclude = set()
        for t in oor_terms:
            try:
                exclude.add(tuple(S.ev(t, {"n": o}) for o in TRAIN))
            except Exception:
                pass
        S.reset()
        terms, pool_size = random_out_of_reach(len(oor_terms), exclude)
        forced = [S.leaf(t, TRAIN, cost=1) for t in terms]
        info["random_pool_size"] = pool_size
    info["carried_over"] = len(forced)
    info["carried_terms"] = [S.show(u) for u in forced]
    t0 = time.time()
    # `outer_only` withholds the carried terms from FORMATION and gives them to the
    # outer search alone -- Report P's condition Bo, which localises the effect.
    formed = S.form_leaves(TRAIN, size1=c["body"], size2=c["body"],
                           extra_leaves=() if c["carry"] == "outer_only" else forced,
                           verbose=False, tag=cond)
    info["formed_terms"] = len(formed)
    info["formation_seconds"] = round(time.time() - t0, 1)
    units = S.select_units(formed, TRAIN, c["units"] + len(forced), forced_leaves=forced)
    info["units"] = len(units)
    atoms = [("var", "n")] + [("const", x) for x in S.CONSTS] + units
    info["outer_atoms"] = len(atoms)
    return atoms, info, {u[1] for u in forced}, prov


def certify(O, carried_ids):
    """Every library invariant reached, confirmed on RESERVE then HOLDOUT."""
    out = {}
    for name, f in sorted(INV.LIBRARY.items()):
        try:
            vec = tuple(f(m) for m in TRAIN)
        except Exception:
            continue
        d = digest(np.array(vec, dtype=np.int64))
        hits = O.watch_hits.get(d) or []
        if not hits:
            continue
        best = min(c for c, _ in hits)
        terms, seen = [], set()
        for c, i in hits:
            if c != best:
                continue
            t = O.term_of(i)
            k = S.show(t)
            if k not in seen:
                seen.add(k)
                terms.append(t)
        ok_r = ok_h = None
        try:
            ok_r = all(S.ev(terms[0], {"n": m}) == f(m) for m in RESERVE)
            ok_h = all(S.ev(terms[0], {"n": m}) == f(m) for m in HOLDOUT)
        except Exception:
            pass
        out[name] = {"cost": best, "distinct_minimal_terms": len(terms),
                     "term": S.show(terms[0]),
                     "matches_RESERVE": ok_r, "matches_HOLDOUT": ok_h,
                     "uses_carried": bool(S.uses_ids(terms[0], carried_ids)),
                     "reachable_without_carried":
                         any(not S.uses_ids(t, carried_ids) for t in terms)}
    return {k: v for k, v in out.items() if v["matches_RESERVE"] and v["matches_HOLDOUT"]}


def main():
    cond = sys.argv[1]
    c = CONDITIONS[cond]
    t0 = time.time()
    reach_vectors()
    disagreement.assert_disjoint(RESERVE, HOLDOUT)
    for a, b in ((TRAIN, RESERVE), (TRAIN, HOLDOUT), (RESERVE, HOLDOUT), (TRAIN, EVALQ)):
        assert not set(a) & set(b)
    opbad = verify_operators(trials=4000)
    atoms, info, carried_ids, prov = build(cond)
    print("%s: %d atoms (%d carried), %d formed" %
          (cond, info["outer_atoms"], info["carried_over"], info["formed_terms"]), flush=True)

    watch = []
    for name, f in INV.LIBRARY.items():
        try:
            watch.append(tuple(f(m) for m in TRAIN))
        except Exception:
            pass
    O = Outer(atoms, TRAIN, cap=20000000, beam=c["beam"], seed=SEED,
              max_atom_cost=c["cost"]).run(c["cost"], watch=watch)
    print("  %d classes, %d expansions, truncated=%s (%.0fs)" %
          (len(O.seen), O.expansions, O.truncated, time.time() - t0), flush=True)

    cert = certify(O, carried_ids)
    # A target is struck only if a carried atom that the condition can actually USE
    # has its value vector. Condition D3 charges the carried terms their expanded
    # sizes, 6-9, all above its cost-5 budget, so `Outer` drops them: striking a
    # target there would shrink D3's denominator for atoms it cannot reach.
    carried_vectors, over_budget = {}, []
    for u in atoms:
        if u[0] == "leaf" and u[1] in carried_ids:
            if S.size(u) > c["cost"]:
                over_budget.append(S.show(u))
                continue
            try:
                carried_vectors[tuple(S.ev(u, {"n": m}) for m in TRAIN)] = S.show(u)
            except Exception:
                pass
    info["carried_atoms_over_budget"] = over_budget
    struck = []
    for name in INV.TARGETS:
        try:
            v = tuple(INV.LIBRARY[name](m) for m in TRAIN)
        except Exception:
            continue
        if v in carried_vectors:
            struck.append(name)
    targets_live = [t for t in INV.TARGETS if t not in struck]
    reached = [t for t in targets_live if t in cert]
    reached_all = [t for t in INV.TARGETS if t in cert]

    net_new = {k: v for k, v in cert.items()
               if tuple(INV.LIBRARY[k](m) for m in TRAIN) not in carried_vectors}

    out = {"label": "ROUND3", "condition": cond, "prereg_sha256": PREREG_SHA,
           "deviations": DEVIATIONS, "info": info,
           "splits": {"TRAIN": [TRAIN[0], TRAIN[-1]], "RESERVE": [RESERVE[0], RESERVE[-1]],
                      "HOLDOUT": [HOLDOUT[0], HOLDOUT[-1]], "EVALQ": [EVALQ[0], EVALQ[-1]]},
           "operator_check_mismatches": len(opbad),
           "vectorisation_check": O.verify(300),
           "classes_TRAIN": len(O.seen), "expansions": O.expansions,
           "truncated_at_cap": O.truncated, "level_log": O.level_log,
           "certified": cert, "certified_count": len(cert),
           "certified_net_new": sorted(net_new), "certified_net_new_count": len(net_new),
           "targets_struck_as_carried": struck,
           "targets_live": targets_live,
           "targets_reached": reached, "targets_reached_count": len(reached),
           "targets_reached_including_struck": reached_all,
           "carried_terms": info["carried_terms"],
           "wall_seconds": round(time.time() - t0, 1)}
    (HERE / ("round3_%s.json" % cond)).write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("  certified %d (net new %d); targets %d/%d live (%s); struck %s (%.0fs)" %
          (len(cert), len(net_new), len(reached), len(targets_live), ",".join(reached),
           struck, out["wall_seconds"]), flush=True)


if __name__ == "__main__":
    main()
