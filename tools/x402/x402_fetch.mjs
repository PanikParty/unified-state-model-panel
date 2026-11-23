#!/usr/bin/env node
// x402 pay-per-call fetch for Gloom Datasets (docs: gloom.sh/datasets/docs/x402.md)
// Usage: node x402_fetch.mjs <url> [--dry-run]
//   stdout: the API response body, raw (parseable JSON on success) — redirectable
//           straight into cds_raw/*.json for scripts/kscreen_cds.py --from-json.
//   stderr: provenance envelope (status, PAYMENT-RESPONSE receipt, timestamp).
//   --dry-run: no payment; prints the 402 payment terms to stdout, zero spend.
// Key file: X402_KEY_FILE (default /root/.gloom-x402-key), mode 600,
// hex private key of a DEDICATED low-balance Base wallet. Never a main wallet.
import { readFileSync, statSync } from "node:fs";
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const url = process.argv[2];
const dryRun = process.argv.includes("--dry-run");
if (!url) { console.error("usage: node x402_fetch.mjs <url> [--dry-run]"); process.exit(2); }

if (dryRun) {
  const r = await fetch(url, { headers: { "User-Agent": "hermes-agent/kscreen (unified-state-model-panel)" } });
  console.log(await r.text());
  process.exit(0);
}

const keyFile = process.env.X402_KEY_FILE || "/root/.gloom-x402-key";
const mode = statSync(keyFile).mode & 0o777;
if (mode !== 0o600) { console.error(`key file ${keyFile} must be mode 600, is ${mode.toString(8)}`); process.exit(2); }
let key = readFileSync(keyFile, "utf8").trim();
if (!key.startsWith("0x")) key = "0x" + key;

const client = new x402Client();
registerExactEvmScheme(client, { signer: privateKeyToAccount(key) });
const pay = wrapFetchWithPayment(fetch, client);

const r = await pay(url, { headers: { "User-Agent": "hermes-agent/kscreen (unified-state-model-panel)" } });
const text = await r.text();

// provenance to stderr: status, on-chain receipt, timestamp, final URL
console.error(JSON.stringify({
  status: r.status,
  payment_response: r.headers.get("payment-response"),
  ts: new Date().toISOString(),
  url,
}));

if (!r.ok) {
  // error body goes to stderr, NOT stdout — stdout stays clean for the pipeline
  console.error(text.slice(0, 2000));
  process.exit(1);
}
process.stdout.write(text);
