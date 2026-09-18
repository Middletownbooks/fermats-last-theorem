#!/usr/bin/env python3
"""Build the bundle a scored agent is shown. The only supported way to do so.

This program cannot read heldout/: every read goes through _read(), which refuses any path
under that directory. If you need the answers, you are not building an agent bundle.

Modes
  --set positives|twins|controls|mixed   which items to include (default: mixed)
  --telegraph                            leak table only, no board slots: the baseline arm
  --anonymise                            strip names, dates and citations (L4 probe)
  --key-out PATH                         write the positive/negative key SEPARATELY (never to stdout)

'mixed' shuffles positives, twins and controls together under opaque ids, so the agent cannot
tell a twin from a case by position. Scores are lift over --telegraph, never raw accuracy.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HELDOUT = (ROOT / "heldout").resolve()


class HeldoutAccess(Exception):
    pass


def _read(path: pathlib.Path) -> dict:
    rp = path.resolve()
    if rp == HELDOUT or HELDOUT in rp.parents:
        raise HeldoutAccess(f"refusing to read held-out answers: {rp}")
    return json.loads(rp.read_text(encoding="utf-8"))


NAME = re.compile(r"\b([A-Z][a-z]+(?:-[A-Z][a-z]+)*)\b")
YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
ARXIV = re.compile(r"arXiv:\S+|math/\d+", re.I)


def anonymise(text: str) -> str:
    if not text:
        return text
    text = ARXIV.sub("[ref]", text)
    text = YEAR.sub("[year]", text)
    # Drop capitalised surnames, but keep the mathematical vocabulary that makes the slot usable.
    keep = {"The", "A", "An", "This", "It", "Its", "No", "Each", "Any", "Every", "Both", "Same",
            "Counting", "Signed", "One", "Two", "Three", "Progress", "Game", "Size", "Dimensions",
            "There", "Cauchy", "Schwarz", "Chernoff", "Fourier", "Kakeya", "Ricci", "Euler"}
    return NAME.sub(lambda m: m.group(1) if m.group(1) in keep else "[name]", text)


def item_from_case(d: pathlib.Path, anon: bool, telegraph: bool) -> dict:
    b = _read(d / "before.json")
    out = {"source_id": b["id"], "kind": "case", "problem": b["problem"],
           "bound_then": b["bound_then"], "leak": b["leak"]}
    if not telegraph:
        out["before_board"] = {k: v for k, v in b["before_board"].items() if v}
        out["sources_before"] = [s["cite"] for s in b.get("sources_before", [])]
    if b.get("flag"):
        out["flag"] = b["flag"]
    if anon:
        out["problem"] = "[problem]"
        out.pop("sources_before", None)
        for k in ("bound_then", "leak"):
            out[k] = anonymise(out[k])
        if "before_board" in out:
            out["before_board"] = {k: anonymise(v) for k, v in out["before_board"].items()}
    return out


def item_from_twin(p: pathlib.Path, anon: bool, telegraph: bool) -> dict:
    t = _read(p)
    out = {"source_id": t["id"], "kind": "twin", "problem": t["problem"],
           "bound_then": None, "leak": t["surface_leak"]}
    if not telegraph:
        out["sources_before"] = [s["cite"] for s in t.get("sources", [])]
    if anon:
        out["problem"] = "[problem]"
        out.pop("sources_before", None)
        out["leak"] = anonymise(out["leak"])
    return out


def item_from_control(p: pathlib.Path, anon: bool, telegraph: bool) -> dict:
    c = _read(p)
    board = c.get("board", {})
    out = {"source_id": c["id"], "kind": "control", "problem": c["problem"],
           "bound_then": None, "leak": None}
    if not telegraph:
        out["before_board"] = {k: v for k, v in board.items() if k in ("S", "M", "I", "C", "T") and v}
    if anon:
        out["problem"] = "[problem]"
        if "before_board" in out:
            out["before_board"] = {k: anonymise(v) for k, v in out["before_board"].items()}
    return out


QUESTION = (
    "For each item: (1) does the leak indicate that the board must change, or is the bound "
    "essentially tight on this board? (2) If it must change, which transformation applies, or "
    "'none'? (3) Name the source problem if you recognise it, and say so explicitly if you do not."
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", help="a single item by source id")
    ap.add_argument("--set", default="mixed",
                    choices=["positives", "twins", "controls", "mixed"])
    ap.add_argument("--telegraph", action="store_true", help="leak table only (baseline arm)")
    ap.add_argument("--anonymise", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--key-out", type=pathlib.Path)
    a = ap.parse_args()

    cases = sorted(p for p in (ROOT / "cases").iterdir() if p.is_dir())
    twins = sorted((ROOT / "twins").glob("*.json"))
    controls = sorted((ROOT / "controls").glob("*.json"))

    items: list[dict] = []
    if a.set in ("positives", "mixed"):
        items += [item_from_case(d, a.anonymise, a.telegraph) for d in cases]
    if a.set in ("twins", "mixed"):
        items += [item_from_twin(p, a.anonymise, a.telegraph) for p in twins]
    if a.set in ("controls", "mixed"):
        items += [item_from_control(p, a.anonymise, a.telegraph) for p in controls]

    if a.id:
        items = [i for i in items if i["source_id"] == a.id]
        if not items:
            print(f"no such item: {a.id}", file=sys.stderr)
            return 2

    rng = random.Random(a.seed)
    rng.shuffle(items)

    key = []
    for n, it in enumerate(items, 1):
        opaque = f"I{n:02d}"
        key.append({"item": opaque, "source_id": it.pop("source_id"), "kind": it.pop("kind")})
        it["item"] = opaque

    bundle = {
        "bundle": "p1-retrodiction",
        "set": a.set,
        "arm": "telegraph-baseline" if a.telegraph else "procedure",
        "anonymised": a.anonymise,
        "seed": a.seed,
        "instructions": QUESTION,
        "note": ("Items are shuffled and re-keyed. Some are historical board changes, some are "
                 "near neighbours where the leak is real, some are cases where the board did not "
                 "change. You are not told which is which."),
        "items": items,
    }
    text = json.dumps(bundle, indent=2, ensure_ascii=False)
    bundle["digest"] = hashlib.sha256(text.encode()).hexdigest()[:16]
    print(json.dumps(bundle, indent=2, ensure_ascii=False))

    if a.key_out:
        a.key_out.write_text(json.dumps(
            {"seed": a.seed, "set": a.set, "digest": bundle["digest"], "key": key},
            indent=2) + "\n", encoding="utf-8")
        print(f"\nkey written to {a.key_out} (do not show it to a scored agent)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
