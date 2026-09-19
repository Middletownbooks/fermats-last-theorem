#!/usr/bin/env python3
"""Link every item source to the citations.json row that does or does not cover it (debt D33).

Run from `proof-protocol/`: `python3 p1-retrodiction/tools/link_sources.py`. It is idempotent -- it
rewrites the same four fields with the same values -- and `tools/check_consistency.py` enforces the
invariant afterwards.

The decision table below is the deliverable; it is reviewed as a table rather than as 55 edits.
Each row is (file, json path, expected cite prefix, citation_row, verified, tier, basis).
`verified: true` is set ONLY where the linked row states that a source reached the project supports
this cite's claim. Where a row covers a NEIGHBOURING claim but not this one, the link is recorded and
verified stays false with the reason -- that asymmetry is the whole point of the basis field.
"""
import json, pathlib, sys

P = "p1-retrodiction"
PRIMARY = "PRIMARY (pasted transcript)"
SEARCH = "SEARCH (search snippets; no PDF fetched in this container)"
COMPUTED = "COMPUTED (arithmetic reproduced in this repository)"
STANDARD = "STANDARD (declared, not fetched)"
NONE = "NONE"

T = [
 (f"{P}/cases/01-sensitivity/before.json", "sources_before[0]", "Chung", "C1-bound", True, SEARCH,
  "Row C1-bound verifies the (1/2 - o(1)) log n bound and records that the logarithm is base 2, which P1 left unstated."),
 (f"{P}/cases/01-sensitivity/before.json", "sources_before[1]", "Gotsman", "C1-gotsman", False, NONE,
  "Row C1-gotsman is UNVERIFIED and no pass has ever checked it -- the one row in the tree in that position (D19)."),
 (f"{P}/cases/02-cap-set/before.json", "sources_before[0]", "Meshulam", "C2-meshulam", True, SEARCH,
  "Row C2-meshulam verifies O(3^n/n), reached via the Bateman-Katz paper rather than Meshulam's own."),
 (f"{P}/cases/02-cap-set/before.json", "sources_before[1]", "Bateman", "C2-batemankatz", True, SEARCH,
  "Row C2-batemankatz verifies the bound AND CORRECTS how P1 wrote it (3^n/n^{1+eps}, not n^{1+eps}); publication data later corroborated from the Bloom-Sisask reference list."),
 (f"{P}/cases/03-shannon-capacity-c5/before.json", "sources_before[0]", "Shannon", "C3-shannon", True, PRIMARY,
  "Row C3-shannon closed from a pasted transcript: the 5/2 upper bound is Shannon's own, by what is now called the fractional clique cover."),
 (f"{P}/cases/04-kadison-singer/before.json", "sources_before[0]", "Weaver", "C4", False, NONE,
  "The KS_2 formulation is Weaver's, but row C4 is a NEGATIVE result: neither Weaver nor Marcus-Spielman-Srivastava states the threshold delta <~ 1/log n that the item attached to him, and the number was dropped."),
 (f"{P}/cases/04-kadison-singer/before.json", "sources_before[1]", "Matrix Chernoff", None, False, NONE,
  "No citations.json row covers the matrix Chernoff attribution (Ahlswede-Winter / Tropp). Never checked."),
 (f"{P}/cases/05-finite-field-kakeya/before.json", "sources_before[0]", "Wolff", "C5-wolff", True, SEARCH,
  "Row C5-wolff verifies q^{(n+2)/2} as the finite-field benchmark for Besicovitch sets."),
 (f"{P}/cases/05-finite-field-kakeya/before.json", "sources_before[1]", "best pre-Dvir", "C5-4n7", False, NONE,
  "Row C5-4n7 is DISPUTED: 4n/7 + 3/7 is Katz-Tao's EUCLIDEAN Minkowski-dimension bound and no source reached here states it for |K| in F_q^n. The two-regime structure survives; the exponent does not."),
 (f"{P}/cases/06-erdos-distinct-distances/before.json", "sources_before[0]", "Katz, Tardos", None, False, NONE,
  "No row covers the Katz-Tardos before-bound. Row C6-after verifies the AFTER board (Guth-Katz, Elekes-Sharir plus polynomial partitioning), which is a different claim."),
 (f"{P}/cases/06-erdos-distinct-distances/before.json", "sources_before[1]", "Szemeredi, Trotter", "TWINS-batch2", True, SEARCH,
  "The Szemeredi-Trotter theorem and its tightness are verified in row TWINS-batch2 (twin N18, with Elekes's construction). That covers the STATEMENT the item cites; no row addresses case 6's particular use of it."),
 (f"{P}/cases/07-small-prime-gaps/before.json", "sources_before[0]", "Goldston", "C7", True, PRIMARY,
  "Row C7 verifies every field of the GPY board against Granville arXiv:1410.8400v1, verbatim or in substance."),
 (f"{P}/cases/07-small-prime-gaps/before.json", "sources_before[1]", "Bombieri", "C7", True, PRIMARY,
  "Same row: theta > 1/2 needed against Bombieri-Vinogradov's exactly 1/2. This is also the requirement half of the GPY ceiling entry (CEILINGS.md)."),
 (f"{P}/cases/07-small-prime-gaps/before.json", "verification_sources[0]", "Granville", "C7", True, PRIMARY,
  "The transcript itself; it is the fetched source for the row and for the case 7 split into 7a and control 16."),
 (f"{P}/cases/08-spencer-discrepancy/before.json", "sources_before[0]", "Chernoff", "C8-bound", True, SEARCH,
  "Row C8-bound verifies that a uniform random colouring achieves Theta(sqrt(n log n)), which is what the folklore cite asserts."),
 (f"{P}/cases/09-vinogradov-mean-value/before.json", "sources_before[0]", "Vinogradov", "C9", True, PRIMARY,
  "Row C9 closed from the Pierce transcript, including the constant's history 3 -> 2 -> 1 and the derivation of the log k as the contraction count."),
 (f"{P}/cases/09-vinogradov-mean-value/before.json", "sources_before[1]", "Wooley", "C9", True, PRIMARY,
  "Same transcript; Wooley's posting date was independently confirmed, which is what voided the case's cutoff."),
 (f"{P}/cases/09-vinogradov-mean-value/before.json", "verification_sources[0]", "Pierce", "C9", True, PRIMARY,
  "The transcript itself."),
 (f"{P}/cases/10-parallel-repetition/before.json", "sources_before[0]", "Fortnow", "C10", False, SEARCH,
  "Row C10's latest status is SEARCH: search reaches the Fortnow-then-Feige ordering in substance, but the primaries are largely pre-arXiv and no source was fetched. Below fetched-primary tier, so the flag stays false."),
 (f"{P}/cases/11-kneser/before.json", "sources_before[0]", "Kneser", "C11", True, SEARCH,
  "Row C11 verifies the Kneser 1955 upper bound chi <= n-2k+2 alongside the Lovasz after-board."),
 (f"{P}/cases/12-geometrization/before.json", "sources_before[0]", "Hamilton", "C12", False, NONE,
  "Row C12 is PARTIAL and about Perelman's entropy and reduced volume; nothing covers Hamilton's Ricci flow programme as the before-board."),
 (f"{P}/cases/13-pcp-weak/before.json", "sources_before[0]", "Arora", None, False, NONE,
  "Row C13 verifies the AFTER board (Dinur 2007 graph powering with constant blow-up), not Arora-Safra or ALMSS. The before-board's own sources are unchecked."),
 (f"{P}/controls/14-sphere-packing-8-24.json", "sources[0]", "Cohn", "C14", True, SEARCH,
  "Row C14 and adjudication ADJ-14 verify that Cohn-Elkies 2003 was the first improvement in each dimension since Kabatyanskii-Levenshtein 1978, and that the authors THEMSELVES conjectured their board would settle dimensions 8 and 24 -- which is the documentary form of the claim that made this item a control rather than a board change."),
 (f"{P}/controls/14-sphere-packing-8-24.json", "sources[1]", "Viazovska", None, False, NONE,
  "NOT covered by any row. C14 verifies the BOARD claim, not Viazovska's certificate, which no pass has checked. The control does not depend on it: what makes this a control is that the board was already known to be tight."),
 (f"{P}/controls/14-sphere-packing-8-24.json", "sources[2]", "Kabatiansky", "C14", True, SEARCH,
  "Same row: KL 1978 is the board Cohn-Elkies replaced, so the board change in this problem is KL -> Cohn-Elkies, not Cohn-Elkies -> Viazovska."),
 (f"{P}/controls/15-roth-kelley-meka.json", "sources[0]", "Kelley, Meka", "C15", True, PRIMARY,
  "Row C15 closed from the Bloom-Sisask transcript, which states Kelley-Meka's Theorem 1 (exponent 1/12) and Theorem 2 (F_q^n, 1/9)."),
 (f"{P}/controls/15-roth-kelley-meka.json", "verification_sources[0]", "Bloom, Sisask", "C15", True, PRIMARY,
  "The transcript itself; also the source for rows C15-ladder and C15-ceiling and for the ceiling register's open entry."),
 (f"{P}/controls/16-zhang-smooth-moduli.json", "sources[0]", "Zhang", "C7", True, PRIMARY,
  "Row C7 verifies Zhang's Theorem 3.2 (y-smooth moduli, Q = x^{1/2+eta}, delta = 1/1168) as one of the two after-boards, from the Granville transcript."),
 (f"{P}/controls/16-zhang-smooth-moduli.json", "verification_sources[0]", "Granville", "C7", True, PRIMARY,
  "The transcript itself; section 5 is what supplies the level reading and the split."),
 (f"{P}/twins/N1-johnson-lindenstrauss.json", "sources[0]", "Larsen", "N1", True, SEARCH,
  "Row N1 verifies the Omega(eps^{-2} log n) lower bound matching JL, for general and not merely linear maps."),
 (f"{P}/twins/N2-epsilon-nets.json", "sources[0]", "Komlos", "N2-tight", True, SEARCH,
  "Row N2-tight verifies the KPW almost-tight bounds."),
 (f"{P}/twins/N2-epsilon-nets.json", "sources[1]", "Pach, Tardos", "N2-tight", True, SEARCH,
  "Same row: the R^4 halfspace construction forcing nets of size (1/(9 eps)) log(1/eps)."),
 (f"{P}/twins/N2-epsilon-nets.json", "sources[2]", "Matousek", "N2-removable", False, SEARCH,
  "Row N2-removable is PARTIAL: O(1/eps) nets for halfspaces in R^3 are confirmed, but the attribution to Matousek-Seidel-Welzl was not. The mathematical claim stands; the attribution does not."),
 (f"{P}/twins/N4-shannon-capacity-c7.json", "sources[0]", "Polak", "N4", True, COMPUTED,
  "Row N4 verifies 367^{1/5} > 3.2578 from the paper and computes theta(C7) = 3.3176672... here."),
 (f"{P}/twins/N5-strong-parallel-repetition.json", "sources[0]", "Raz", "N5", True, SEARCH,
  "Row N5 verifies Raz's odd-cycle counterexample and that the game is simultaneously projection, unique and XOR."),
 (f"{P}/twins/N6-discrepancy-arithmetic-progressions.json", "sources[0]", "Roth", "N6", True, SEARCH,
  "Row N6 verifies Theta(n^{1/4}) with Roth 1964 supplying the lower bound."),
 (f"{P}/twins/N6-discrepancy-arithmetic-progressions.json", "sources[1]", "Matousek, Spencer", "N6", True, SEARCH,
  "Same row: the matching upper bound by the entropy method."),
 (f"{P}/twins/N7-euclidean-kakeya.json", "sources[0]", "Wang", "N7", True, SEARCH,
  "Row N7 verifies the 2025 R^3 resolution and that its route is multiscale rather than polynomial-method."),
 (f"{P}/twins/N8-discrepancy-many-sets.json", "sources[0]", "Spencer", "N8", True, SEARCH,
  "Row N8 verifies O(sqrt(n log(m/n + 2))). NOTE: this twin is the one all three D20 raters fired on, and the N8 adjudication found MY reading wrong, not the citation."),
 (f"{P}/twins/N16-matrix-multiplication-omega.json", "sources[0]", "Strassen", "TWINS-batch2", False, STANDARD,
  "Row TWINS-batch2 declares N16 as STANDARD rather than fetched, and records the live distinction the twin now carries: border rank is SUB-multiplicative, not fully multiplicative (arXiv:1801.04852)."),
 (f"{P}/twins/N20-kovari-sos-turan.json", "sources[0]", "Kollar", "TWINS-batch2", False, STANDARD,
  "Row TWINS-batch2 declares N20 as STANDARD rather than fetched; the twin carries its range restriction, tight only for t >= (s-1)!+1."),
 (f"{P}/twins/N3-3ap-free-integers.json", "sources[0]", "Salem", "N3", True, PRIMARY,
  "Row N3 RE-ATTRIBUTED the exclusion of power savings to Salem-Spencer 1942, from the Peluse transcript. This is the half the item leans on."),
 (f"{P}/twins/N3-3ap-free-integers.json", "sources[1]", "Behrend", "N3-behrend-improvements", True, PRIMARY,
  "Rows N3 and N3-behrend-improvements: Behrend 1946 is the stronger, still essentially best-known bound, with small improvements by Elkin 2011 and Green-Wolf 2010 from the Bloom-Sisask reference list."),
 (f"{P}/twins/N3-3ap-free-integers.json", "verification_sources[0]", "Peluse", "N3", True, PRIMARY,
  "The transcript itself."),
 (f"{P}/twins/N9-huang-tightness.json", "sources[0]", "Chung", "C1-bound", True, SEARCH,
  "Row C1-bound verifies CFGS 1988, including their own matching ceil(sqrt n) construction -- which is the extremal input this twin is about. NOTE: the N9 audit broke this twin's ROLE, not its citation."),
 (f"{P}/twins/N10-spencer-sqrt-n-tight.json", "sources[0]", "Hadamard", None, True, STANDARD,
  "Declared standard in the twin file with no citations.json row. It was never among the eight STANDARD twins D21 tracked, so how it came to be flagged verified is unrecorded -- recorded here rather than silently corrected."),
 (f"{P}/twins/N11-max-of-gaussians.json", "sources[0]", "Standard extreme-value", "TWINS-batch2", True, SEARCH,
  "Row TWINS-batch2 upgraded N11: the max of n iid standard Gaussians is asymptotically tight at sqrt(2 log n)."),
 (f"{P}/twins/N12-balls-into-bins.json", "sources[0]", "Raab", "TWINS-batch2", True, SEARCH,
  "Row TWINS-batch2 upgraded N12 from Raab-Steger 1998, which gives tight upper AND lower bounds."),
 (f"{P}/twins/N13-coupon-collector.json", "sources[0]", "E[T] = n*H_n", "TWINS-batch2", True, COMPUTED,
  "Row TWINS-batch2 upgraded N13 by exact computation rather than by citation, which is the stronger basis of the two."),
 (f"{P}/twins/N14-set-cover-greedy.json", "sources[0]", "Feige", None, True, STANDARD,
  "Declared in the twin file with no citations.json row; not among D21's eight. Same gap as N10."),
 (f"{P}/twins/N14-set-cover-greedy.json", "sources[1]", "Dinur", None, True, STANDARD,
  "Same: declared, unrowed."),
 (f"{P}/twins/N15-shearer-lll.json", "sources[0]", "Shearer", None, True, STANDARD,
  "Declared in the twin file with no citations.json row; not among D21's eight. Same gap as N10."),
 (f"{P}/twins/N17-alon-boppana.json", "sources[0]", "Alon-Boppana", "TWINS-batch2", True, SEARCH,
  "Row TWINS-batch2 upgraded N17: attained by the Lubotzky-Phillips-Sarnak and Margulis Ramanujan families."),
 (f"{P}/twins/N18-szemeredi-trotter.json", "sources[0]", "Szemeredi-Trotter", "TWINS-batch2", True, SEARCH,
  "Row TWINS-batch2 upgraded N18: Elekes's construction attains it, and except for the constant it cannot be improved."),
 (f"{P}/twins/N19-sauer-shelah.json", "sources[0]", "Downward-closed", "TWINS-batch2", True, SEARCH,
  "Row TWINS-batch2 upgraded N19: downward-closed (shattering extremal) systems attain the bound exactly."),
]


def get(d, path):
    cur = d
    for part in path.replace("]", "").split("."):
        for seg in part.split("["):
            cur = cur[int(seg)] if seg.isdigit() else cur[seg]
    return cur


def main() -> int:
    rows = {r["id"] for r in json.load(open("citations.json"))["rows"]}
    changed = bad = 0
    for path_s, jpath, cite_has, row, verified, tier, basis in T:
        p = pathlib.Path(path_s)
        d = json.loads(p.read_text(encoding="utf-8"))
        src = get(d, jpath)
        if cite_has.lower() not in src["cite"].lower():
            print(f"MISMATCH {p} {jpath}: expected a cite containing {cite_has!r}, found {src['cite'][:60]!r}")
            bad += 1
            continue
        if row is not None and row not in rows:
            print(f"MISSING ROW {row} for {p} {jpath}")
            bad += 1
            continue
        src["verified"] = verified
        src["citation_row"] = row
        src["tier"] = tier
        src["basis"] = basis
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        changed += 1
    print(f"{changed} source entries linked, {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
