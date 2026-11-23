#!/usr/bin/env python3
"""K-screen CDS ingest — §13 item 4/11 (AI-infrastructure pool, member-level spreads).

v2 — two routes, deliberately different in what they can prove:

  --sample                 free shape-demo (5 records). Parser proof, no spend.
  --live --issuer X        paid route. Needs GLOOM_KEY (key mode) or an x402
                           client that has already settled the payment.
  --live --issuers FILE    loop a pre-registered issuer list with a hard
                           --max-spend guard.

UNIT RULE (§2.1): a spread is emitted only when its units are established.

  * `cds/curves` returns `spreadBp` — **basis points, stated in the response
    schema**. Verified by Gurney 2026-11-23 from the x402 402-block schema
    extension. Emitted directly.
  * `cds/trades` returns `reportedSpread` plus a `spreadNotation` code whose
    mapping is NOT documented. CONFIRMED_NOTATION is empty on purpose, so every
    such record is emitted UNPARSED with its raw fields intact.

The curves route is also the correct route on the evidence: the trades tape gave
1 spread, 1 upfront-only and 3 empty records out of 5 (docs/kscreen-cds-findings.md).

    python3 kscreen_cds.py --sample
    python3 kscreen_cds.py --live --issuers data/kscreen_issuers.yaml --max-spend 5.00
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

SAMPLE_URL = "https://api.gloom.sh/v1/datasets/cds/sample"
CURVES_URL = "https://api.gloom.sh/v1/cds/curves"
TRADES_URL = "https://api.gloom.sh/v1/cds/trades"
COST_PER_CURVE_CALL = 0.12  # USD, x402 lane: 4 credits x $0.03
UA = {"User-Agent": "hermes-agent/kscreen (unified-state-model-panel)"}

# code -> multiplier yielding a decimal fraction. Empty until documented.
CONFIRMED_NOTATION = {}


def fetch(url, key=None, timeout=60):
    req = urllib.request.Request(url, headers=dict(UA))
    if key:
        req.add_header("Authorization", "Bearer " + key)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def records(payload):
    if isinstance(payload, dict):
        for k in ("data", "records", "results", "curves"):
            if isinstance(payload.get(k), list):
                return payload[k]
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and any(
            k in payload for k in ("spreadBp", "spread_bp", "reportedSpread", "issuer", "issuerName")):
        return [payload]
    return []


def classify(r):
    """(bps | None, reason). Curves route first: spreadBp is stated in bp."""
    bp = r.get("spreadBp")
    if bp is None:
        bp = r.get("spread_bp")
    if bp is not None:
        try:
            return float(bp), None
        except (TypeError, ValueError):
            return None, f"spreadBp not numeric: {bp!r}"
    rs = r.get("reportedSpread")
    if rs is not None:
        note = None if r.get("spreadNotation") is None else str(r.get("spreadNotation"))
        if note in CONFIRMED_NOTATION:
            return rs * CONFIRMED_NOTATION[note] * 10_000.0, None
        return None, f"spreadNotation={note!r} unconfirmed; raw reportedSpread={rs}"
    if r.get("upfrontAmount") is not None:
        return None, "upfront-only record (no spread); needs a par-curve solve"
    return None, "no spread and no upfront"


def summarise(rows):
    by, unparsed = {}, 0
    for r in rows:
        name = (r.get("issuerName") or r.get("issuer") or r.get("upiUnderlierName")
                or r.get("underlierId") or "UNKNOWN")
        bps, why = classify(r)
        if bps is None:
            unparsed += 1
        e = by.setdefault(name, {"issuer": name, "n": 0, "notional": 0.0,
                                 "spreads_bps": [], "notes": set()})
        e["n"] += 1
        e["notional"] += r.get("notionalAmount") or 0
        if bps is not None:
            e["spreads_bps"].append(bps)
        if why:
            e["notes"].add(why)
    out = []
    for e in by.values():
        s = e["spreads_bps"]
        e["spread_bps_min"] = min(s) if s else None
        e["spread_bps_max"] = max(s) if s else None
        e["spread_bps_mean"] = round(sum(s) / len(s), 2) if s else None
        e["notes"] = sorted(e["notes"])
        out.append(e)
    out.sort(key=lambda x: -x["notional"])
    return {"n_records": len(rows), "n_unparsed": unparsed, "issuers": out}


def load_issuers(path):
    txt = open(path).read()
    names = []
    for line in txt.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("-") is False and ":" in s:
            continue
        if s.startswith("- "):
            v = s[2:].strip().strip('"').strip("'")
            if v:
                names.append(v)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--issuer")
    ap.add_argument("--issuers", help="file with a pre-registered issuer list")
    ap.add_argument("--curves", action="store_true", default=True)
    ap.add_argument("--trades", action="store_true", help="use the sparse trades route")
    ap.add_argument("--max-spend", type=float, default=0.0,
                    help="USD ceiling for the whole run; refuses to exceed it")
    ap.add_argument("--dry-run", action="store_true", help="print the call plan, spend nothing")
    ap.add_argument("--from-json", help="directory/glob of JSON responses already paid for "
                                        "(e.g. collected on the x402 host); summarised with no spend")
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.from_json:
        import glob as _glob
        files = sorted(_glob.glob(os.path.join(a.from_json, "*.json")) or _glob.glob(a.from_json))
        if not files:
            sys.exit(f"no JSON files matched {a.from_json!r}")
        agg = {"n_records": 0, "n_unparsed": 0, "issuers": [],
               "provenance": {"mode": "from-json", "files": files, "cost_usd": 0.0}}
        for f in files:
            try:
                s_ = summarise(records(json.load(open(f))))
            except Exception as exc:                     # noqa: BLE001
                agg["issuers"].append({"file": f, "error": str(exc)})
                continue
            agg["n_records"] += s_["n_records"]
            agg["n_unparsed"] += s_["n_unparsed"]
            agg["issuers"].extend(s_["issuers"])
        js = json.dumps(agg, indent=2, default=str)
        if a.out:
            open(a.out, "w").write(js + "\n")
            print(f"wrote {a.out}")
        print(js)
        return
    if a.sample:
        payload = fetch(SAMPLE_URL)
        s = summarise(records(payload))
        s["provenance"] = {"mode": "sample", "url": SAMPLE_URL, "cost_usd": 0.0}
    elif a.live:
        targets = []
        if a.issuers:
            targets = load_issuers(a.issuers)
        elif a.issuer:
            targets = [a.issuer]
        else:
            sys.exit("--live requires --issuer or --issuers")
        if not targets:
            sys.exit("issuer list is empty — refusing to run")

        base = TRADES_URL if a.trades else CURVES_URL
        est = COST_PER_CURVE_CALL * len(targets)
        print(f"plan: {len(targets)} issuers via {'trades' if a.trades else 'curves'} "
              f"route, est ${est:.2f}")
        if a.max_spend and est > a.max_spend:
            sys.exit(f"REFUSING: plan costs ~${est:.2f} > --max-spend ${a.max_spend:.2f}")
        if a.dry_run:
            for t in targets:
                print("  would call:", base + "?issuer=" + urllib.parse.quote(t))
            return

        key = os.environ.get("GLOOM_KEY")
        if not key:
            sys.exit("GLOOM_KEY not set. On the x402 lane use the repo's client "
                     "(tools/x402/x402_fetch.mjs) to settle each call, then feed the "
                     "JSON here with --from-json.")
        agg = {"n_records": 0, "n_unparsed": 0, "issuers": [], "provenance":
               {"mode": "live", "route": "trades" if a.trades else "curves",
                "cost_usd": round(est, 2), "targets": targets}}
        for t in targets:
            url = base + "?issuer=" + urllib.parse.quote(t)
            try:
                s = summarise(records(fetch(url, key=key)))
            except Exception as exc:                     # noqa: BLE001
                agg["issuers"].append({"issuer": t, "error": str(exc)})
                continue
            agg["n_records"] += s["n_records"]
            agg["n_unparsed"] += s["n_unparsed"]
            agg["issuers"].extend(s["issuers"])
        s = agg
    else:
        sys.exit("nothing to do: pass --sample or --live")

    js = json.dumps(s, indent=2, default=str)
    if a.out:
        open(a.out, "w").write(js + "\n")
        print(f"wrote {a.out}")
    print(js)


if __name__ == "__main__":
    main()
