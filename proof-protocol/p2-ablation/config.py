"""Study configuration. Frozen into the pre-registration hash, so changing it after freezing
voids the pre-registration.

What the Python port fixes, relative to the published artifact:
  * real token counts from usage, instead of characters divided by four;
  * named models, instead of "quick / default / complex" tiers;
  * a system prompt, which the artifact could not set;
  * its own rate limiting, instead of a limit built for an interactive page.

What it does NOT fix: temperature. The handoff asked for temperature control, but sampling
parameters (temperature, top_p, top_k) were removed from the current Claude models along with
fixed thinking budgets; sending one is a 400. `effort` is the nearest available control and is
recorded per run. Say this in the write-up rather than reporting temperature as held constant.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict

ANSWER_MODEL = "claude-opus-5"
JUDGE1_MODEL = "claude-opus-5"
JUDGE2_MODEL = "claude-sonnet-5"


@dataclass
class Config:
    answer_model: str = ANSWER_MODEL
    judge1_model: str = JUDGE1_MODEL
    judge2_model: str = JUDGE2_MODEL
    answer_effort: str = "high"          # low | medium | high | xhigh | max
    judge_effort: str = "medium"
    system: str | None = None            # None keeps the artifact's behaviour (no system prompt)
    words: int = 1200                    # the word cap inside the fixed return menu
    framing: str = "prove"               # prove | decide
    reps: int = 2
    pilot_reps: int = 3
    max_cont: int = 1                    # continuations when a reply is cut off
    max_tokens: int = 16000
    concurrency: int = 4
    use_checkers: bool = True            # exact arithmetic overrides the judge's `valid`
    with_witness_field: bool = True      # ask the judge to extract the witness

    def to_dict(self) -> dict:
        return asdict(self)


JUDGE_BIAS_NOTE = (
    "judge1 and judge2 default to different model families (Opus and Sonnet), which reduces "
    "same-model judging bias but does not remove it: both are Claude models from one vendor. A "
    "genuinely independent second judge means another vendor's model or a human, neither of which "
    "this harness implements. Judges also CANNOT be blinded to arm: the protocol's own tags "
    "(UNENFORCED, DERIVED HERE) and the numbered return fields leak the condition into the text "
    "being graded. Record this; do not report the judges as blind."
)
