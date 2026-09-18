// Evaluate the original artifact's script under DOM stubs and dump its frozen constants as JSON.
// Running the real source is the point: it makes the Python port's fidelity checkable rather than
// asserted. Used by blocks.json (generated) and by tests/test_fidelity.py.
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, "..", "reference", "p2-ablation-harness.html"), "utf8");
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) throw new Error("no <script> block in the artifact");

const stubEl = () => ({ innerHTML: "", showModal() {}, close() {}, value: "" });
const sandbox = {
  document: { querySelector: stubEl, getElementById: stubEl },
  localStorage: { getItem: () => null, setItem() {} },
  console,
  AbortController,
  crypto,
  TextEncoder,
  Date,
  Math,
  JSON,
  setTimeout,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

const EXPORT = `
globalThis.__extract = {
  BLOCKS,
  SCHEMA,
  PFMT,
  PRIG,
  BATTERY0,
  PRED_TEXT,
  CORE_TEMPLATE: CORE("%%W%%"),
  JUDGE_TEMPLATE: judgePrompt({statement:"%%STATEMENT%%", truth:"%%TRUTH%%"}, "%%RESPONSE%%"),
  ARMS: ARMS.map(a => ({id:a.id, kind:a.kind, lv:a.lv||null, on:a.on??null, label:a.label})),
  PROTO: Object.fromEntries(ARMS.map(a => [a.id, protoText(a)])),
  PROMPT_F1: Object.fromEntries(ARMS.map(a => [a.id, buildPrompt(a, BATTERY0[0])])),
  FULL_LEN: fullLen(),
};
`;
vm.createContext(sandbox);
vm.runInContext(m[1] + EXPORT, sandbox);
process.stdout.write(JSON.stringify(sandbox.__extract, null, 1));
