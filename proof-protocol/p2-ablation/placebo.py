"""Length-matched placebo text, without repetition.

The artifact padded its two placebos to the full template's length by cycling about ten
paragraphs, so an arm's prompt read "Rule 1 ... Rule 11 [the same sentence again]". A model can
see that, which weakens the control that prediction (e) turns on. Here each placebo draws from a
pool of distinct paragraphs and stops when it reaches the target length.

If the pool runs out, this raises rather than wrapping around. Write more filler; do not reintroduce
the repetition.
"""
from __future__ import annotations
import pathlib

_HERE = pathlib.Path(__file__).resolve().parent
_FILES = {"pfmt": _HERE / "placebo" / "formatting.txt",
          "prig": _HERE / "placebo" / "rigour.txt"}


class PlaceboExhausted(RuntimeError):
    pass


def paragraphs(kind: str) -> list[str]:
    text = _FILES[kind].read_text(encoding="utf-8")
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def build(kind: str, target: int) -> str:
    """Distinct paragraphs, in order, until the text reaches `target` characters."""
    ps = paragraphs(kind)
    if len(set(ps)) != len(ps):
        raise PlaceboExhausted(f"{kind}: pool contains duplicate paragraphs")
    out: list[str] = []
    n = 0
    for p in ps:
        out.append(p)
        n += len(p) + 2
        if n >= target:
            return "\n\n".join(out)
    raise PlaceboExhausted(
        f"{kind}: pool is {n} chars, target is {target}. Add filler; do not cycle.")
