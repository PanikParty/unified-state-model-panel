#!/usr/bin/env node
// Pass A driver: one paid curves call per pre-registered issuer.
// Hard cap: exactly the names in data/kscreen_issuers.yaml, at most 12 calls.
// Outputs: cds_raw/NN-<slug>.json (API body), cds_raw/receipts.ndjson (envelopes),
//          cds_raw/manifest.json (per-issuer outcome incl. NO COVERAGE).
import { readFileSync, writeFileSync, mkdirSync, appendFileSync, existsSync } from "node:fs";
import { spawn } from "node:child_process";
import path from "node:path";

const REPO = "/root/unified-state-model-panel";
const CLIENT = "/root/x402-client/x402_fetch.mjs";
const OUTDIR = "/root/cds_raw";
const MAX_CALLS = 12;

const names = readFileSync(path.join(REPO, "data/kscreen_issuers.yaml"), "utf8")
  .split("\n")
  .map((l) => l.trim())
  .filter((l) => l.startsWith("- "))
  .map((l) => l.slice(2).trim().replace(/^["']|["']$/g, ""));
if (names.length === 0) { console.error("issuer list empty — refusing"); process.exit(2); }
if (names.length > 12) { console.error(`issuer list has ${names.length} > 12 — refusing (pre-registered spend is 12)`); process.exit(2); }

mkdirSync(OUTDIR, { recursive: true });
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const manifest = [];
let calls = 0;

for (const [i, name] of names.entries()) {
  if (calls >= MAX_CALLS) { manifest.push({ issuer: name, outcome: "SKIPPED: call cap reached" }); continue; }
  const url = `https://api.gloom.sh/v1/cds/curves?issuer=${encodeURIComponent(name)}`;
  const file = path.join(OUTDIR, `${String(i + 1).padStart(2, "0")}-${slug(name)}.json`);
  calls += 1;
  const res = await new Promise((resolve) => {
    const p = spawn("node", [CLIENT, url], { timeout: 120_000 });
    let out = "", err = "";
    p.stdout.on("data", (d) => (out += d));
    p.stderr.on("data", (d) => (err += d));
    p.on("close", (code) => resolve({ code, out, err }));
  });
  appendFileSync(path.join(OUTDIR, "receipts.ndjson"), JSON.stringify({ issuer: name, call_n: calls, stderr: res.err.trim() }) + "\n");
  if (res.code === 0 && res.out.trim()) {
    writeFileSync(file, res.out);
    let n = null;
    try { n = (JSON.parse(res.out).data || []).length; } catch { n = "unparseable"; }
    manifest.push({ issuer: name, outcome: "OK", file, records: n });
  } else {
    const empty = res.err.includes("no data") || res.err.includes("not found");
    manifest.push({ issuer: name, outcome: empty ? "NO COVERAGE" : "ERROR", detail: res.err.trim().slice(0, 400) });
  }
  console.log(`[${calls}/${names.length}] ${name}: ${manifest[manifest.length - 1].outcome}`);
}
writeFileSync(path.join(OUTDIR, "manifest.json"), JSON.stringify({ pass: "A", calls_made: calls, est_cost_usd: calls * 0.12, results: manifest }, null, 2) + "\n");
console.log(`done: ${calls} calls, est $${(calls * 0.12).toFixed(2)}`);
