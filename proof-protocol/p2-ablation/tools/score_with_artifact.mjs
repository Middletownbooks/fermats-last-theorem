// Score a set of mock runs using the ARTIFACT'S OWN scoring code. Reads {runs:[...]} on stdin,
// writes the predictions, block effects and judge kappas as JSON. Used only by the fidelity test.
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, "..", "reference", "p2-ablation-harness.html"), "utf8");
const src = html.match(/<script>([\s\S]*)<\/script>/)[1];

const stubEl = () => ({ innerHTML: "", showModal() {}, close() {}, value: "" });
const sandbox = { document: { querySelector: stubEl, getElementById: stubEl },
  localStorage: { getItem: () => null, setItem() {} },
  console, AbortController, crypto, TextEncoder, Date, Math, JSON, setTimeout };
sandbox.window = sandbox; sandbox.globalThis = sandbox;

const EXPORT = `
globalThis.__score = (runs) => {
  S.runs = {};
  for (const r of runs) S.runs[r.id] = r;
  const R = judged("main");
  const fact = R.filter(r => armById(r.arm).kind === "fact");
  const eff = {};
  for (const b of "ABCDEF".split("")) {
    const hi = fact.filter(r => armById(r.arm).lv[b] > 0);
    const lo = fact.filter(r => armById(r.arm).lv[b] < 0);
    eff[b] = diff(hi, lo, "fail");
  }
  const armRates = {};
  for (const a of ARMS) {
    const G = R.filter(r => r.arm === a.id);
    armRates[a.id] = { n: G.length, fail: rate(G, "fail"), solved: rate(G, "solved"),
                       scope: rate(G, "scope_executed"), chars: mean(G, r => r.chars) };
  }
  return {
    n: R.length,
    predictions: predictions(R),
    effects: eff,
    armRates,
    kappaFail: kappa(R, (r, j) => outcome(r, j).fail),
    kappaScope: kappa(R, (r, j) => !!j.scope_executed),
  };
};
`;
vm.createContext(sandbox);
vm.runInContext(src + EXPORT, sandbox);

const input = JSON.parse(fs.readFileSync(0, "utf8"));
// JSON has no NaN; emit nulls for it so Python can compare like for like.
const clean = (o) => JSON.parse(JSON.stringify(o, (k, v) =>
  (typeof v === "number" && !Number.isFinite(v)) ? null : v));
process.stdout.write(JSON.stringify(clean(sandbox.__score(input.runs))));
