"""Prompt assembly. The factorial and E+F arms are byte-identical to the artifact."""
from __future__ import annotations
from arms import Arm
import blocks, placebo

# Appended to the artifact's judge prompt. The judge still decides `valid`; this field lets code
# re-check the arithmetic itself (see checkers.py), which the artifact could not do.
JUDGE_EXTRA = """
"claimed_witness": if and only if the response offers an explicit numerical or symbolic witness (a counterexample, a specific integer, a specific tuple), the witness as a flat string of assignments separated by commas, for example "n=171" or "a=1/2, b=1/2, c=4" or "x=-1, y=2, z=3". Copy the values exactly as the response gives them; do not simplify, evaluate or correct them. Use null if no explicit witness is offered."""


def proto_text(arm: Arm) -> str:
    if arm.kind == "fact":
        return "\n\n".join(blocks.BLOCKS[b] for b in blocks.BLOCK_IDS if arm.lv[b] > 0)
    if arm.kind == "ef":
        return blocks.BLOCKS["E"] + "\n\n" + blocks.BLOCKS["F"]
    if arm.kind == "schema":
        return blocks.SCHEMA
    return placebo.build(arm.kind, blocks.FULL_LEN)


def build_prompt(arm: Arm, problem: dict, words: int = 1200, framing: str = "prove") -> str:
    proto = proto_text(arm)
    task = ("Prove the following statement." if framing == "prove"
            else "Determine whether the following statement is true, and prove your answer.")
    head = f"PROTOCOL — follow it while working the task below.\n\n{proto}\n\n" if proto else ""
    return f"{head}TASK\n{task}\n\nStatement: {problem['statement']}\n\n{blocks.core(words)}"


def judge_prompt(problem: dict, text: str, with_witness: bool = True) -> str:
    base = blocks.judge_prompt(problem, text)
    return base + JUDGE_EXTRA if with_witness else base


# The judge's reply is constrained by this schema rather than by hope. Every field the artifact
# asked for in prose is required here; "claimed_witness" is the one addition.
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "return_class": {"type": "string", "enum": ["a", "b", "c", "between", "none"]},
        "valid": {"type": "boolean"},
        "small_instance_shown": {"type": "boolean"},
        "scope_executed": {"type": "boolean"},
        "scope_discriminating": {"type": "boolean"},
        "validity_executed": {"type": "boolean"},
        "verdict_without_content": {"type": "boolean"},
        "stale_verdict": {"type": "boolean"},
        "tags_used": {"type": "boolean"},
        "unenforced_labelled": {"type": "boolean"},
        "note": {"type": "string"},
        "claimed_witness": {"type": ["string", "null"]},
    },
    "required": ["return_class", "valid", "small_instance_shown", "scope_executed",
                 "scope_discriminating", "validity_executed", "verdict_without_content",
                 "stale_verdict", "tags_used", "unenforced_labelled", "note", "claimed_witness"],
    "additionalProperties": False,
}
