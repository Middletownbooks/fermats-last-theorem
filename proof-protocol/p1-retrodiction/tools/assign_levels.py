#!/usr/bin/env python3
"""Assign the level axis (debt D30) to every held-out answer and every control.

Run from `proof-protocol/`: `python3 p1-retrodiction/tools/assign_levels.py`. Idempotent.

The decision table below IS the deliverable, reviewable as a table rather than as 17 scattered edits,
in the shape of tools/link_sources.py. Every call is mine alone and the pass is labelled as
single-encoder and unvalidated, exactly like the v0 transformation labels -- see
p3-taxonomy/taxonomy.json -> level_axis.status. Confidence is recorded per item, and the two items at
MEDIUM are the ones a second encoder should be asked about first.
"""
from __future__ import annotations
import json, pathlib, sys

AXES = {"same-level", "input-level", "reduction-level", "substrate", "none", "unclear"}

# id -> (axis, confidence, object_changed, what_stayed_fixed, basis)
T = {
 "01-sensitivity": ("same-level", "high",
   "The board on the reduced object: counting and subcube refinement replaced by a signed adjacency matrix with A^2 = nI, Cauchy interlacing and lambda_1 <= Delta.",
   "The object itself -- an induced subgraph of Q_n on 2^{n-1}+1 vertices -- is what both boards bound.",
   "THE STACK IS WORTH STATING: (sensitivity vs degree) <- (Gotsman-Linial 1992 reduction to induced-subgraph max degree) <- (the spectral tool Huang supplied). Huang changed the BOTTOM of that stack. The level crossing in this problem happened in 1992 and is baked into the item's state slot, which is why the 2019 change reads as same-level."),
 "02-cap-set": ("same-level", "high",
   "Density increment with a hyperplane restriction replaced by a one-shot slice-rank bound on the same subsets of F_3^n.",
   "The object: a progression-free subset of F_3^n.",
   "SUBSTRATE TRANSFER ALONGSIDE IT: Croot-Lev-Pach proved the method in (Z/4Z)^n and Ellenberg-Gijswijt adapted it to F_3^n (row C2-after-split). That is a substrate move BETWEEN TEAMS, not a level move within the board, and it is recorded here because D30 asked for substrate as well as level."),
 "03-shannon-capacity-c5": ("same-level", "high",
   "The upper-bound invariant: fractional clique cover replaced by the theta function via orthonormal representations.",
   "The object: Theta of a fixed graph under the strong product.",
   "Both boards bound the same quantity of the same graph; only the invariant changed."),
 "04-kadison-singer": ("same-level", "high",
   "Random partition plus matrix Chernoff replaced by interlacing families with a barrier argument.",
   "The object: vectors with sum v v^T = I and small norm, partitioned in two.",
   "The dimension-free conclusion comes from the new invariant's behaviour on a direct sum, not from moving the problem."),
 "05-finite-field-kakeya": ("same-level", "high",
   "Incidence counting (bush, hairbrush, Cauchy-Schwarz, sum-product) replaced by the polynomial method.",
   "The object: a Kakeya set K in F_q^n, and the quantity |K|.",
   "The same set is bounded by a different certificate; nothing is reduced to another problem and nothing is supplied from below."),
 "06-erdos-distinct-distances": ("reduction-level", "medium",
   "The OBJECT: the Elekes-Sharir lift sends distances to rigid motions and then to lines in R^3, and polynomial partitioning runs there.",
   "Nothing of the planar counting board is kept; it is retired, not consumed.",
   "MEDIUM CONFIDENCE, and this is one of the two items at the axis's weakest boundary. Read as reduction-level because the bound is proved about a DIFFERENT object (line incidences in R^3) reached by an explicit reduction, rather than by a new invariant on N planar points. A second encoder could defensibly call it same-level with a new move, and should be asked."),
 "07-small-prime-gaps": ("same-level", "high",
   "The sieve board itself: the move space is enlarged from a one-variable F to a k-variable F, so rho grows like log k instead of saturating at 4.",
   "The level of distribution theta, which is consumed unchanged -- Maynard-Tao needs no new input about primes in arithmetic progressions.",
   "THIS IS HALF OF THE PAIR D30 EXISTS FOR. 7a changed the level-n board and kept the level-(n-1) input; control 16 did the exact opposite. Granville's line -- 'one can avoid having to prove any difficult new results about primes in arithmetic progressions' -- is the documentary form of what stayed fixed."),
 "08-spencer-discrepancy": ("same-level", "high",
   "Uniform random colouring with a per-set Chernoff bound and a union bound replaced by entropy and partial colouring.",
   "The object: a colouring of n points with n sets, and the discrepancy.",
   "Same object, new move and new composition."),
 "09-vinogradov-mean-value": ("substrate", "high-that-it-is-CONTESTED",
   "Two after-boards are recorded for one item: efficient congruencing (p-adic) and l^2 decoupling (Archimedean).",
   "The quantity J_{s,k} in the congruencing route; the decoupling route re-expresses the problem analytically.",
   "CONTESTED BY THE PRACTITIONERS, NOT BY US. Pierce sec. 8.5 argues the two share rescaling, multilinear estimates, iteration and transversality, and quotes Wooley that they may be 'p-adic and Archimedean perspectives of one unified method'. If that reading is right the two after-boards are ONE board in two substrates, and this item's multi_answer rubric is scoring a substrate choice rather than a board choice. The axis records the dispute instead of resolving it -- which is the honest state, and is the second sign D30 was opened on."),
 "10-parallel-repetition": ("same-level", "high",
   "The invariant: a conjectured exact multiplicativity replaced by an information-theoretic embedding with per-coordinate relative entropy.",
   "The object: val(G^k) for a two-prover game under the k-fold product.",
   "CROSS-ITEM NOTE: this item's OBJECT is what case 13's before-board consumes as its move. So 10 sits one level below 13 in a stack that the corpus contains but never encoded."),
 "11-kneser": ("reduction-level", "medium",
   "The OBJECT: the neighbourhood complex turns a colouring question about k-subsets of [n] into a topological one, settled by Borsuk-Ulam.",
   "Nothing of the combinatorial and inductive board is kept.",
   "MEDIUM CONFIDENCE, the second item at the weakest boundary, and for the same reason as case 6: the bound is proved about a constructed object in another category. A second encoder could call it same-level with a new invariant."),
 "12-geometrization": ("same-level", "high",
   "The invariants only: W-entropy and reduced volume give kappa-noncollapsing.",
   "The move -- Ricci flow itself -- which the after-board says outright is unchanged.",
   "The clearest same-level item in the corpus: the held-out answer begins 'Same move, new monotone invariants'."),
 "13-pcp-weak": ("same-level", "high",
   "The amplification board: k-fold parallel repetition replaced by graph powering on expanders plus alphabet reduction.",
   "The object: a CSP and its gap.",
   "CROSS-ITEM NOTE, and it cuts the other way from control 16: the OLD board consumed parallel repetition (case 10's object) and paid its blow-up; Dinur's board REMOVES that dependence, with constant-factor size blow-up. So a same-level change here ELIMINATED a level below rather than changing it. Recorded as a note rather than as a sixth axis value, because one instance is not a category."),
 # --- controls -------------------------------------------------------------
 "14-sphere-packing-8-24": ("none", "high",
   "Nothing. Viazovska supplied the terminal certificate on the Cohn-Elkies board.",
   "The whole board: per ADJ-14 the board change in this problem was Kabatyanskii-Levenshtein -> Cohn-Elkies in 2003.",
   "A control: the axis reads none because no board changed at any level."),
 "15-roth-kelley-meka": ("none", "high",
   "Nothing at board level. The play changed -- Hoelder lifting, unbalancing, dependent random choice, almost-periodicity -- on the density-increment board.",
   "The board: the primary source's own fifth step is titled 'Density increment'.",
   "A control, and note the contrast with case 7a: better play that did NOT change the board, against a board change that kept its input."),
 "16-zhang-smooth-moduli": ("input-level", "high",
   "The equidistribution input one level down: y-smooth moduli, factored modulus, Graham-Ringrose, Q = x^{1/2+eta} with delta = 1/1168.",
   "The GPY sieve at level n -- the weights, Selberg's formula and the ratio criterion are untouched.",
   "THE ITEM THIS AXIS EXISTS FOR. Its level_flag already said this in prose; the axis now says it in a field, so a scorer can read it without reading the paragraph."),
 "17-roth-bloom-sisask": ("none", "high",
   "Nothing. The same board re-presented with classical Bohr set machinery, plus announced exponent improvements.",
   "The board and the main ideas, by the authors' own statement: 'our sole contribution is at the technical level ... all of the main ideas are the same as in [14]'.",
   "A control, and the same-period half of the Roth 2023 control pair with 15."),
}

ROOT = pathlib.Path("p1-retrodiction")


def main() -> int:
    n = 0
    for item_id, (axis, conf, changed, fixed, basis) in T.items():
        assert axis in AXES, axis
        held = ROOT / "heldout" / f"{item_id}.json"
        ctrl = ROOT / "controls" / f"{item_id}.json"
        p = held if held.exists() else ctrl
        if not p.exists():
            print(f"MISSING {item_id}")
            return 1
        d = json.loads(p.read_text(encoding="utf-8"))
        d["level"] = {"axis": axis, "confidence": conf, "object_changed": changed,
                      "what_stayed_fixed": fixed, "basis": basis,
                      "assigned_by": "this session, single-encoder and unvalidated",
                      "recorded_for": "debt D30; vocabulary in p3-taxonomy/taxonomy.json -> level_axis"}
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        n += 1
    print(f"{n} items carry a level axis")
    from collections import Counter
    c = Counter(v[0] for v in T.values())
    for k, v in c.most_common():
        print(f"  {k:16} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
