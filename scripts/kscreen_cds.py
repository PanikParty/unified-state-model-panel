#!/usr/bin/env python3
"""K-screen CDS ingest — §13 item 4/11 (AI-infrastructure pool, member-level spreads).

Runs in two modes:

  --sample          the free shape-demo endpoint (5 records). Proves the parser
                    against real wire data with no key and no spend.
  --live --issuer X pay-per-call routes, requires GLOOM_KEY. Not exercised until
                    a key exists — the script refuses rather than guesses.

Design rule (§2.1 of the Unified State Model): a number is emitted only when its
units are established. `reportedSpread` carries a `spreadNotation` code whose
mapping this script does NOT assume. Records whose notation is not in the
confirmed table are emitted as UNPARSED with their raw fields intact, never
silently converted. Confirm the code table before trusting any spread it prints.

Usage:
    python3 kscreen_cds.py --sample
    python3 kscreen_cds.py --sample --out kscreen_sample.json
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse

SAMPLE_URL = "https://api.gloom.sh/v1/datasets/cds/sample"
CURVES_URL = "https://api.gloom.sh/v1/cds/curves"
TRADES_URL = "https://api.gloom.sh/v1/cds/trades"

# Confirmed notation -> multiplier on reportedSpread yielding a decimal fraction
# (0.01 = 100bp). NOTHING is confirmed yet; the dict is empty on purpose.
# Fill it only from published documentation, never from a plausible-looking value.
CONFIRMED_NOTATION = {}

UA = {"User-Agent": "hermes-agent/kscreen (unified-state-model-panel)"}


def fetch(url, key=None, timeout=45):
    req = urllib.request.Request(url, headers=dict(UA))
    if key:
        req.add_header("Authorization", "Bearer " + key)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def records(payload):
    if isinstance(payload, dict):
        for k in ("data", "records", "results"):
            if isinstance(payload.get(k), list):
                return payload[k]
    return payload if isinstance(payload, list) else []


def classify(r):
    """Return (parsed_bps | None, reason_if_none)."""
    rs = r.get("reportedSpread")
    up = r.get("upfrontAmount")
    if rs is not None:
        note = str(r.get("spreadNotation")) if r.get("spreadNotation") is not None else None
        if note in CONFIRMED_NOTATION:
            return rs * CONFIRMED_NOTATION[note] * 10_000.0, None
        return None, f"spreadNotation={note!r} unconfirmed; raw reportedSpread={rs}"
    if up is not None:
        return None, "upfront-only record (no reported spread); needs a par-curve solve"
    return None, "no spread and no upfront"


def summarise(rows):
    out = {"n_records": len(rows), "issuers": [], "unparsed": 0}
    by = {}
    for r in rows:
        name = r.get("issuerName") or r.get("upiUnderlierName") or r.get("underlierId") or "UNKNOWN"
        bps, why = classify(r)
        notional = r.get("notionalAmount") or 0
        if bps is None:
            out["unparsed"] += 1
        e = by.setdefault(name, {"issuer": name, "n": 0, "notional": 0.0,
                                 "spreads_bps": [], "notes": set()})
        e["n"] += 1
        e["notional"] += notional
        if bps is not None:
            e["spreads_bps"].append(bps)
        if why:
            e["notes"].add(why)
    for e in by.values():
        n = e["notional"] or 0
        e["notional_weighted_bps"] = (
            round(sum(s * 1.0 for s in e["spreads_bps"]) / len(e["spreads_bps"]), 2)
            if e["spreads_bps"] else None
        )
        e["notes"] = sorted(e["notes"])
        out["issuers"].append(e)
    out["issuers"].sort(key=lambda x: -x["notional"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="free shape-demo endpoint")
    ap.add_argument("--live", action="store_true", help="pay-per-call routes (needs GLOOM_KEY)")
    ap.add_argument("--issuer", help="issuer name for --live")
    ap.add_argument("--curves", action="store_true", help="use /curves instead of /trades")
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.sample and a.live:
        sys.exit("choose one of --sample / --live")
    if a.sample:
        payload = fetch(SAMPLE_URL)
        prov = {"mode": "sample", "url": SAMPLE_URL, "cost": "free"}
    elif a.live:
        key = os.environ.get("GLOOM_KEY")
        if not key:
            sys.exit("GLOOM_KEY not set — refusing to call a paid route without it.")
        if not a.issuer:
            sys.exit("--live requires --issuer (the route takes `issuer`, not `ticker`)")
        url = (CURVES_URL if a.curves else TRADES_URL) + "?issuer=" + urllib.parse.quote(a.issuer)
        payload = fetch(url, key=key)
        prov = {"mode": "live", "url": url, "cost": "pay-per-call"}
    else:
        sys.exit("nothing to do: pass --sample or --live")

    rows = records(payload)
    if not rows:
        sys.exit("no records returned — refusing to summarise an empty payload")

    s = summarise(rows)
    s["provenance"] = prov
    s["units_rule"] = ("spreads emitted only for confirmed spreadNotation codes; "
                       "CONFIRMED_NOTATION is empty, so expect UNPARSED today")
    js = json.dumps(s, indent=2, default=str)
    if a.out:
        open(a.out, "w").write(js + "\n")
        print(f"wrote {a.out}")
    print(js)


if __name__ == "__main__":
    main()
