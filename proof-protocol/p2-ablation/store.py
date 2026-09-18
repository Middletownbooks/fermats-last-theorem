"""Run persistence: one JSON file per phase, rewritten atomically."""
from __future__ import annotations
import json, os, pathlib, tempfile


class Store:
    def __init__(self, root: str | pathlib.Path = "runs"):
        self.root = pathlib.Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.runs: dict[str, dict] = {}
        for p in sorted(self.root.glob("*.json")):
            for r in json.loads(p.read_text(encoding="utf-8")):
                self.runs[r["id"]] = r

    def _path(self, phase: str) -> pathlib.Path:
        return self.root / f"{phase}.json"

    def save(self, phase: str) -> None:
        rows = sorted((r for r in self.runs.values() if r["phase"] == phase),
                      key=lambda r: r["id"])
        path = self._path(phase)
        fd, tmp = tempfile.mkstemp(dir=self.root, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)
        os.replace(tmp, path)

    def get(self, run_id: str) -> dict | None:
        return self.runs.get(run_id)

    def put(self, run: dict) -> None:
        self.runs[run["id"]] = run

    def phase(self, phase: str) -> list[dict]:
        return [r for r in self.runs.values() if r["phase"] == phase]

    def judged(self, phase: str, types: dict[str, str]) -> list[dict]:
        return [r for r in self.phase(phase) if r.get("j1") and r["pid"] in types]
