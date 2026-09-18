# Defects in the published instrument

Defects in the harness **as published**, distinct from the deviations this port introduced
deliberately (those are `analysis/preregistration.md` §7). A defect here changes what the published
artifact *would have reported*, so it belongs in the write-up as a property of the instrument, not
as a port-time improvement.

## DEFECT-1 — judge 2's exported column falls back to judge 1

**Status: confirmed, present in the published artifact, fixed in this port.**

`outcome()` opens with a fallback:

~~~js
function outcome(r, j) { j = j || r.j1; if (!j) return null; /* ... */ }
~~~

and `exportData` calls it as `outcome(r, r.j2)`. On every row where the second judge did not run,
`r.j2` is `undefined`, the fallback fires, and **judge 2's exported column is scored from judge 1's
judgement**. Those rows then agree with judge 1 by construction.

**Consequence.** Any inter-judge agreement computed from the exported CSV is inflated toward 1, in
proportion to how many rows are missing a second judge. Rows missing a second judge are exactly the
rows where a batch was interrupted, rate-limited or halted — so the inflation is largest in
precisely the runs that were cut short. `tests/test_export_defect.py` demonstrates it on a fixture
where the two judges disagree on every row that has both: the exported column reports 50%
agreement where the truth is 0%.

The κ tables shown *inside* the page are not affected — `kappa()` filters on `r.j1 && r.j2` before
pairing. The defect is confined to the CSV export, which is the artefact an analysis would actually
be run on.

**The fix is at the call site, not in the rule.** `outcome()` is one of the six pre-registered
frozen rules; changing it would be a re-freeze. Guard the caller instead:

~~~js
const o2 = r.j2 ? outcome(r, r.j2) : null;
~~~

This port does that in `cli.py`, and `tests/test_fidelity.py` still passes, confirming the frozen
rule is untouched.

**For the write-up.** If any results were ever exported from the published page, their inter-judge
agreement is an overestimate and must be recomputed from rows that carry both judgements. No such
results exist yet, so nothing needs retracting — but the instrument was defective before it was
ever run, and that is worth saying plainly rather than quietly shipping the fix.
