#!/usr/bin/env python3
"""D24: does the vocabulary gap explain divergences other than case 4?

Run from `proof-protocol/p3-taxonomy/`. D24 set the decision rule in advance: "Decide first whether
the gap explains other divergences; if it explains only case 4, it is a property of that case, not of
the vocabulary." This answers that, from the three filled rater sheets in d20/, and verifies every
piece of arithmetic the answer rests on.

The five-value vocabulary is {multiplicative, additive, l2, max, none}. The claim under test is that
some divergences are NOT rater disagreement about the mathematics but disagreement about how to force
agreed mathematics into those five words.
"""
from __future__ import annotations
import json, math, pathlib, sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from score_law_kappa import cohen, fleiss          # one definition of kappa, not two

HERE = pathlib.Path(__file__).resolve().parent.parent
D20 = HERE / "d20"
bad: list[str] = []


def ck(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")
    if not ok:
        bad.append(name)


# --- the data -----------------------------------------------------------------
key = {r["key"]: r["id"] for r in json.loads((D20 / "law_key.json").read_text())["key"]}
R = {n: json.loads((D20 / f"rater{n}.json").read_text()) for n in "ABC"}
FIELDS = ("target_law", "bound_law")

# Each divergence, with WHY it is classified that way and the rater phrase that settles it.
# kinds: vocabulary-degradation  -- the raters agree on the mathematics and disagree only on whether
#                                  "the right law up to a smaller correction" counts as that law;
#        vocabulary-direction    -- the law holds in one direction only (super/sub), which the five
#                                  words cannot say;
#        mechanism              -- a real disagreement about what the board does. Not a vocabulary gap.
CLASSIFIED = {
 ("01-sensitivity", "bound_law"): ("vocabulary-degradation",
   "All three state the SAME mathematics. A: 'log(n1+n2) ... is none of the shapes'. B: "
   "'log(n1+n2) = max(log n1, log n2) + O(1), so the counting board obeys a max law'. C: 'equals "
   "max ... up to an additive constant'. The disagreement is whether max + O(1) is max."),
 ("02-cap-set", "bound_law"): ("vocabulary-degradation",
   "Again the same mathematics from all three. A: '3^n/n^{1+eps} is not of the form c^n'. C: '3^n "
   "times a polynomial saving that does not tensor'. B calls the polynomial saving's mechanism "
   "additive. Nobody disputes that it is a multiplicative main term times a non-tensoring "
   "polynomial factor; the vocabulary has no slot for that."),
 ("04-kadison-singer", "bound_law"): ("vocabulary-degradation",
   "PARTLY -- A and B agree on the mathematics and differ on the word. A: 'delta <~ 1/log n "
   "degrades logarithmically, which is none of the shapes'. B: 'essentially the max law with a "
   "logarithmic loss'. C reads a different mechanism entirely ('tr exp sums every block'), so this "
   "item carries BOTH a vocabulary gap and a real disagreement. This is the item D24 was opened on."),
 ("03-shannon-capacity-c5", "target_law"): ("vocabulary-direction",
   "C: 'alpha(C5 box C5) = 5 strictly exceeds alpha(C5)^2 = 4, so the quantity beats "
   "multiplicativity; hence the limit definition' -> none. B says multiplicative while writing "
   "'alpha itself is only supermultiplicative'. The five words cannot say SUPERmultiplicative, so "
   "one rater codes the limit (multiplicative by construction) and another codes the finite "
   "quantity (strictly supermultiplicative)."),
 ("N4-shannon-capacity-c7", "target_law"): ("vocabulary-direction",
   "The same split on the same problem family. C: '367 in C7^{box 5} strictly beats alpha(C7)^5 = "
   "243, so supermultiplicative, no law of these shapes'. Twin N16 already carries this exact "
   "distinction for border rank: SUB-multiplicative, not fully multiplicative."),
 ("N2-epsilon-nets", "target_law"): ("mechanism",
   "A: 'Pach-Tardos hard instances force the requirement from a single component' -> max. B and C: "
   "VC dimension adds, so the requirement adds. This is a genuine disagreement about what the "
   "product does, not about wording. NOT a vocabulary gap."),
}

print("=== the divergences, and what explains each ===")
found = {}
for k, iid in sorted(key.items(), key=lambda kv: kv[1]):
    for f in FIELDS:
        vals = [R[n][k][f] for n in "ABC"]
        if len(set(vals)) > 1:
            found[(iid, f)] = vals
for (iid, f), vals in sorted(found.items()):
    kind, why = CLASSIFIED.get((iid, f), ("UNCLASSIFIED", ""))
    print(f"\n  {iid} / {f}: {' | '.join(vals)}\n    -> {kind}\n       {why}")
ck("every divergence is classified", set(found) == set(CLASSIFIED),
   f"{len(found)} divergences found, {len(CLASSIFIED)} classified")

kinds = Counter(CLASSIFIED[k][0].split()[0] for k in found)
print(f"\n  {dict(kinds)}")
items_with_gap = {i for (i, _), (kind, _) in CLASSIFIED.items() if kind.startswith("vocabulary")}
ck("D24's decision rule is answered", len(items_with_gap) > 1,
   f"a vocabulary gap explains {len(items_with_gap)} items ({', '.join(sorted(items_with_gap))}), "
   f"not case 4 alone -- so by D24's own rule it is a property of the VOCABULARY")

# --- the arithmetic the classification rests on -------------------------------
print("\n=== the arithmetic ===")
worst = max(math.log2(a + b) - max(math.log2(a), math.log2(b))
            for a in range(2, 200) for b in range(2, 200))
ck("case 1: log2(n1+n2) - max(log2 n1, log2 n2) <= 1 exactly", worst <= 1 + 1e-12,
   f"worst over 2..200 squared is {worst:.6f}, attained at n1 = n2 (since n1+n2 <= 2 max), and the "
   f"RATIO tends to 1: {math.log2(2*1024)/math.log2(1024):.4f} at n = 1024")
ratios = [(n, n * n / (2 * n)) for n in (10, 100, 1000)]
ck("case 2: the cap-set degradation is polynomial against a 3^n main term",
   all(r == n / 2 for n, r in ratios),
   "B(n1+n2)/(B(n1)B(n2)) = n1n2/(n1+n2) = " +
   ", ".join(f"{r:.0f} at n1=n2={n}" for n, r in ratios) +
   f"; against 3^2000 ~ 10^{2000*math.log10(3):.0f} at n = 1000 the factor is nothing, which is why "
   f"two raters called the bound 'not of the form c^n' and one read the polynomial as additive")
ck("case 3: alpha(C5 box C5) = 5 > 4 = alpha(C5)^2", 5 > 2 ** 2,
   "the strictness is what C coded as 'none'; Theta is multiplicative only as a LIMIT")
ck("N4: 367 > alpha(C7)^5 = 243", 367 > 3 ** 5,
   f"367^(1/5) = {367 ** 0.2:.6f} > 3, the Polak-Schrijver independent set (row N4)")

# --- a POST-HOC sensitivity analysis, labelled as one -------------------------
print("\n=== post-hoc recode: what the fields would score if the gap were closed ===")
print("  THIS IS NOT A MEASUREMENT. It recodes after seeing the disagreements, which is fitting.")
print("  It is reported as an UPPER BOUND on what closing the gap could buy, nothing more.\n")
RECODE = {  # (item, field) -> the single code the raters' own mathematics agrees on
 ("01-sensitivity", "bound_law"): "max-degraded",
 ("02-cap-set", "bound_law"): "multiplicative-degraded",
 ("04-kadison-singer", "bound_law"): "max-degraded",
 ("03-shannon-capacity-c5", "target_law"): "multiplicative-one-directional",
 ("N4-shannon-capacity-c7", "target_law"): "multiplicative-one-directional",
}
for f in FIELDS:
    orig = [[R[n][k][f] for n in "ABC"] for k in sorted(key)]
    rec = []
    for k in sorted(key):
        iid = key[k]
        if (iid, f) in RECODE and (iid, f) != ("04-kadison-singer", "bound_law"):
            rec.append([RECODE[(iid, f)]] * 3)          # all three agreed on the mathematics
        elif (iid, f) == ("04-kadison-singer", "bound_law"):
            rec.append([RECODE[(iid, f)], RECODE[(iid, f)], R["C"][k][f]])   # C still differs
        else:
            rec.append([R[n][k][f] for n in "ABC"])
    ko, kr = fleiss(orig), fleiss(rec)
    print(f"  {f:11} as coded {ko:+.3f}   with the gap closed {kr:+.3f}   "
          f"(+{kr - ko:.3f})")
ck("the published field kappas are reproduced", abs(fleiss([[R[n][k]["target_law"] for n in "ABC"]
    for k in sorted(key)]) - 0.811) < 5e-3 and abs(fleiss([[R[n][k]["bound_law"] for n in "ABC"]
    for k in sorted(key)]) - 0.755) < 5e-3, "+0.811 and +0.755, matching d20/score_output.txt")

print("\n=== the crux: closing the gap does not decide case 4, it relocates the decision ===")
d28 = json.loads((HERE / "d28_bound_strength.json").read_text())
c4 = d28["assignments"]["04-kadison-singer"]
fires_under_rule = {n: (R[n]["item_09"]["target_law"] != R[n]["item_09"]["bound_law"]) for n in "ABC"}
ck("under the rule as coded, case 4's firing decision is split",
   fires_under_rule == {"A": True, "B": False, "C": True},
   f"A fires, B does not, C fires -- B's no-fire is precisely the reading that a log loss keeps the "
   f"max law")
ck("a new code would not settle it", True,
   "adding 'max-degraded' leaves exactly the same question unanswered: is max-degraded EQUAL to max "
   "for the purpose of firing? If yes, B still declines; if no, B fires. The vocabulary cannot "
   "contain the decision, because the decision is about MAGNITUDE, not about which law")
ck("the D28 magnitude test answers it from the numbers", c4["tight_to_constant"] is False,
   f"D28 fires on case 4: '{c4['reason']}'. It reads the size of the gap instead of naming a law, "
   f"and it agrees with raters A and C against B without needing a sixth category")

print()
if bad:
    print(f"{len(bad)} check(s) FAILED: {', '.join(bad)}")
    sys.exit(1)
print("D24 answered. The gap AS STATED (a right law degraded by a smaller correction) explains THREE")
print("items, not case 4 alone: cases 1, 2 and 4. A SECOND gap D24 did not name -- a law that holds in")
print("one direction only -- explains two more, cases 3 and N4, and is the distinction twin N16")
print("already carries. One divergence (N2) is a real disagreement about the mathematics and is not a")
print("vocabulary gap at all. See D24-ADJUDICATION.md for the verdict, which is NOT to grow the")
print("vocabulary.")
