"""Runs the study against the Claude API.

One run is one answer plus two judge calls. Nothing here decides anything about the study: the
scoring rules live in outcomes.py and are frozen.
"""
from __future__ import annotations
import asyncio, json, random, time
from typing import Sequence

import battery as battery_mod
import checkers
import prompts
from arms import ARMS, BARE, arm_by_id
from config import Config
from store import Store


def _client():
    try:
        from anthropic import AsyncAnthropic
    except ModuleNotFoundError as e:  # pragma: no cover
        raise SystemExit(
            "The anthropic SDK is not installed. `pip install -r requirements.txt`, then set "
            "ANTHROPIC_API_KEY or run `ant auth login`.") from e
    return AsyncAnthropic(max_retries=4)


def plan(phase: str, items: list[dict], cfg: Config, store: Store,
         arm_ids: Sequence[str] | None = None) -> list[dict]:
    arms = [BARE] if phase == "pilot" else [a for a in ARMS
                                            if arm_ids is None or a.id in arm_ids]
    reps = cfg.pilot_reps if phase == "pilot" else cfg.reps
    out = []
    for a in arms:
        for p in items:
            for rep in range(1, reps + 1):
                rid = f"{phase}_{p['id']}_{a.id}_{rep}"
                run = store.get(rid) or {"id": rid, "phase": phase, "pid": p["id"],
                                         "arm": a.id, "rep": rep}
                store.put(run)
                out.append(run)
    return out


def is_done(run: dict) -> bool:
    return bool(run.get("text") and run.get("j1") and run.get("j2"))


async def _generate(client, prompt: str, cfg: Config) -> dict:
    turns = [{"role": "user", "content": prompt}]
    text, usage_in, usage_out, truncated = "", 0, 0, False
    for i in range(cfg.max_cont + 1):
        kwargs = dict(model=cfg.answer_model, max_tokens=cfg.max_tokens, messages=turns,
                      output_config={"effort": cfg.answer_effort})
        if cfg.system:
            kwargs["system"] = cfg.system
        async with client.messages.stream(**kwargs) as s:
            msg = await s.get_final_message()
        chunk = "".join(b.text for b in msg.content if b.type == "text")
        text += ("\n" if i else "") + chunk
        usage_in += msg.usage.input_tokens
        usage_out += msg.usage.output_tokens
        truncated = msg.stop_reason == "max_tokens"
        if msg.stop_reason == "refusal":
            return {"text": text, "truncated": False, "refused": True,
                    "input_tokens": usage_in, "output_tokens": usage_out,
                    "stop_reason": "refusal"}
        if not truncated:
            break
        turns = [{"role": "user", "content": prompt},
                 {"role": "assistant", "content": text},
                 {"role": "user", "content": "Continue exactly where you stopped. "
                                             "Do not repeat anything."}]
    return {"text": text, "truncated": truncated, "refused": False,
            "input_tokens": usage_in, "output_tokens": usage_out,
            "stop_reason": msg.stop_reason}


async def _judge(client, problem: dict, text: str, model: str, cfg: Config) -> dict:
    msg = await client.messages.create(
        model=model, max_tokens=4000,
        messages=[{"role": "user",
                   "content": prompts.judge_prompt(problem, text, cfg.with_witness_field)}],
        output_config={"effort": cfg.judge_effort,
                       "format": {"type": "json_schema", "schema": prompts.JUDGE_SCHEMA}},
    )
    body = next(b.text for b in msg.content if b.type == "text")
    j = json.loads(body)
    j["judge_model"] = model
    j["judge_input_tokens"] = msg.usage.input_tokens
    j["judge_output_tokens"] = msg.usage.output_tokens
    if cfg.use_checkers:
        j = checkers.apply(problem, j)
    return j


async def process_run(client, run: dict, problem: dict, cfg: Config, store: Store) -> None:
    if not run.get("text"):
        arm = arm_by_id(run["arm"])
        prompt = prompts.build_prompt(arm, problem, cfg.words, cfg.framing)
        g = await _generate(client, prompt, cfg)
        run.update(g)
        run.update({"prompt_chars": len(prompt), "chars": len(g["text"]),
                    "answer_model": cfg.answer_model, "effort": cfg.answer_effort,
                    "ts": time.time()})
        run.pop("err", None)
        store.put(run); store.save(run["phase"])
    for slot, model in (("j1", cfg.judge1_model), ("j2", cfg.judge2_model)):
        if not run.get(slot):
            run[slot] = await _judge(client, problem, run["text"], model, cfg)
            store.put(run); store.save(run["phase"])


async def run_queue(phase: str, items: list[dict], cfg: Config, store: Store,
                    batch: int, arm_ids: Sequence[str] | None = None,
                    seed: int | None = None) -> dict:
    pending = [r for r in plan(phase, items, cfg, store, arm_ids) if not is_done(r)]
    random.Random(seed).shuffle(pending)
    pending = pending[:batch]
    if not pending:
        return {"completed": 0, "message": "nothing left to run in this phase"}

    client = _client()
    sem = asyncio.Semaphore(max(1, cfg.concurrency))
    state = {"completed": 0, "stop": False, "streak": 0, "message": ""}

    async def worker(run: dict) -> None:
        if state["stop"]:
            return
        problem = battery_mod.by_id(items, run["pid"])
        async with sem:
            if state["stop"]:
                return
            try:
                await process_run(client, run, problem, cfg, store)
                state["completed"] += 1
                state["streak"] = 0
                print(f"  done {run['id']}  "
                      f"{run.get('output_tokens', 0)} output tokens", flush=True)
            except Exception as e:                      # noqa: BLE001
                name = type(e).__name__
                run["err"] = f"{name}: {e}"
                store.put(run); store.save(phase)
                state["streak"] += 1
                print(f"  FAIL {run['id']}  {name}: {e}", flush=True)
                if name in ("AuthenticationError", "PermissionDeniedError", "NotFoundError"):
                    state["stop"] = True
                    state["message"] = f"halted: {name}"
                elif state["streak"] >= 3:
                    state["stop"] = True
                    state["message"] = "three runs failed in a row; paused"

    await asyncio.gather(*(worker(r) for r in pending))
    await client.close()
    store.save(phase)
    if not state["message"]:
        state["message"] = f"batch finished: {state['completed']} of {len(pending)} runs"
    return state
