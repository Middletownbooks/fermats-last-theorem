# P2 — Template ablation study

Which clauses of research protocol v2.1 change what an agent *does*? Twenty arms over six clause
blocks, a planted-truth battery, two judges per run, six predictions scored mechanically.

**Never run against a live model.** The browser artifact it was ported from was tested against
mocks only (600 simulated runs). This port adds a fidelity test and exact arithmetic, and it has
not been run either. Nothing here is a result.

## Why a Python port

The published artifact was constrained by its runtime. The handoff's task 3 asked for a port that
lifts four of those limits. Three are lifted; one turned out not to exist any more.

| Artifact limit | Here |
|---|---|
| Cost estimated as characters ÷ 4 | Real `input_tokens` / `output_tokens` from `usage`, per run |
| Tiers only ("quick / default / complex") | Named models, per role |
| No system prompt | `Config.system` |
| Rate limit built for an interactive page | Own concurrency and backoff |
| Temperature not controllable | **Still not controllable.** Sampling parameters were removed from the current Claude models; sending one returns a 400. `effort` is the nearest control and is recorded per run. Say this in the write-up — do not report temperature as held constant. |

## Fidelity: the port does not quietly re-freeze anything

The handoff's instruction was to keep the frozen rules byte-identical or re-freeze and say so.
Both were done, and the claim is checkable rather than asserted:

~~~sh
python3 tests/test_fidelity.py      # runs the ARTIFACT'S OWN JavaScript and compares
python3 tests/test_checkers.py
~~~

`tools/extract_from_artifact.mjs` evaluates the artifact's script under DOM stubs and dumps its
constants; `tools/score_with_artifact.mjs` scores mock runs with the artifact's own
`predictions()`, `diff()`, `kappa()` and `outcome()`. The test compares every prediction verdict,
every detail string, every interval endpoint, every arm rate and both judge κ across 845 random
mock runs — including the NaN-handling edge cases, where JavaScript and Python disagree by default.

What deliberately differs — the placebos, the judge's extra field, the JSON schema — is listed in
`analysis/preregistration.md` §7. That table is the re-freeze declaration.

## The design

A 2^(6−2) fractional factorial, E = ABC and F = BCD, resolution IV, over six blocks of v2.1:

| | Block |
|---|---|
| A | substrate declaration |
| B | decomposition and scale |
| C | epistemic stance and tags |
| D | named failure principles |
| E | derivation discipline (content, not verdict) |
| F | adversarial audit (coverage, validity, scope check) |

§6, §8 and §9 are held fixed: with one agent their substrate is absent. Plus four controls: bare,
a length-matched formatting placebo, a length-matched generic-rigour placebo, and a **schema arm**
delivering the same E+F content as mandatory return fields rather than prose. Every arm, bare
included, ends with the same fixed return menu (a)/(b)/(c).

The schema arm is the point of the whole design. If prediction (c) holds — the scope check is
executed in under 50% of prose runs and over 80% of return-field runs — then v3 is a return form,
not more prose.

## Running it

~~~sh
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...            # or: ant auth login

python3 cli.py arms                     # the design, and what each arm costs in characters
python3 cli.py prompt --arm X16         # read a prompt before spending anything on it
python3 cli.py pilot --batch 45         # bare arm only
python3 cli.py select                   # keep problems with bare failure in [20%, 80%]
python3 cli.py freeze                   # hash and lock; commit the hash
python3 cli.py run --batch 60           # the main study, in batches
python3 cli.py score                    # the six predictions, scored as written
python3 cli.py export --csv runs.csv
python3 analysis/analyze.py power  --csv runs.csv
python3 analysis/analyze.py model  --csv runs.csv
~~~

A full main study is 600 runs and 1,800 API calls before continuations, against your own key.
`run` refuses to start until the pre-registration is frozen.

## The battery is the weak part

Fifteen textbook-grade statements: seven false, five true, three open. The seed expects many to
hit ceiling in the pilot, and the handoff's **first priority** is to replace the weakest with real
agent failures that already have a demonstrated non-zero failure rate. Those artifacts are not in
this repository — see the top-level README. `battery.load(extra_path=...)` merges them in when
they arrive.

Two ground truths are now machine-verified rather than recalled: `F1` (n = 171 divides 2^171 + 1
and is not a power of 3) and `F6` (2^n ≡ 3 mod n at Lehmer's n = 4700063497). `O3` — that
x³ + y³ + z³ = 114 is still open — is a dated claim and must be re-checked on the day of freezing.

## Files

~~~
blocks.py blocks.json      the frozen stimulus text, extracted from the artifact by evaluating it
arms.py                    the factorial and the four controls
placebo.py placebo/        length-matched, non-repeating filler for the two placebo arms
prompts.py                 prompt assembly and the judge prompt + JSON schema
checkers.py                exact arithmetic on claimed counterexamples
outcomes.py                THE FROZEN SCORING RULES — a change here is a re-freeze
battery.py                 the planted-truth battery and the slot for real-failure items
config.py harness.py       models, concurrency, the API calls
cli.py store.py            commands and run persistence
analysis/                  the pre-registered analysis; read it before unblinding
tools/                     the two Node bridges to the original artifact
reference/                 the original artifact, verbatim
~~~
