#!/usr/bin/env python3
"""K-screen classification — applies docs/kscreen-preregistration.md to the
2026-11-24 run artifacts. Computational only; the statuses follow the table in
§4 of the pre-registration and are printed with the evidence behind each one.
"""
import json, statistics

A = json.load(open("kscreen_pass_a.json"))
V = json.load(open("pass_b_variation.json"))

# pool membership, fixed in the pre-registration (data/kscreen_issuers.yaml roles)
POOLS = {
    "hyperscaler-landlords": ["Oracle", "Microsoft", "Amazon", "Meta", "Alphabet"],
    "silicon-systems": ["NVIDIA", "Broadcom"],
    "neocloud": ["CoreWeave", "IREN", "Applied Digital", "TeraWulf"],
    "colocation-reit": ["Digital Realty"],
}

def match(name, keys):
    return any(k.lower() in name.lower() for k in keys)

levels = {}
for e in A["issuers"]:
    s = e.get("spreads_bps") or []
    if s:
        levels[e["issuer"]] = {"n": e["n"], "min": min(s), "max": max(s),
                               "mean": round(statistics.fmean(s), 1), "count": len(s)}

# variation, active tenor only (2031-12-20) to avoid splicing
var = {}
for r in V["rows"]:
    if r["maturity"] != "2031-12-20":
        continue
    var[r["file"]] = r

def var_for(name):
    key = name.lower().split()[0].split(".")[0].rstrip(",")
    for f, r in var.items():
        if key in f.lower():
            return r
    return None

print("=== levels (pass A) ===")
for k, v in sorted(levels.items(), key=lambda x: -x[1]["max"]):
    print(f"  {k:26} n={v['n']:5} records={v['count']:4}  min {v['min']:8.1f}  "
          f"mean {v['mean']:8.1f}  max {v['max']:8.1f}  bp")

print("\n=== variation, tenor 2031-12-20, window 180d ===")
for f, r in sorted(var.items(), key=lambda x: -x[1]["change_bp"]):
    print(f"  {f:26} {r['first_date']} {r['first_bps']:8.1f} -> {r['last_date']} "
          f"{r['last_bps']:8.1f}  = {r['change_bp']:+8.1f} bp   (n_days {r['n_days']})")

print("\n=== pool status per pre-registration §4 ===")
for pool, members in POOLS.items():
    covered, uncovered = [], []
    for m in members:
        hit = [k for k in levels if match(k, [m])]
        (covered if hit else uncovered).append(m if not hit else hit[0])
    changes = []
    for k in covered:
        r = var_for(k)
        if r:
            changes.append((k, r["change_bp"]))
    maxlv = max((levels[k]["max"] for k in covered), default=None)
    med = round(statistics.median([c for _, c in changes]), 1) if changes else None
    access = "ACCESS-IMPAIRED" if (maxlv is not None and maxlv > 1000) else "access-ok"
    variation = ("met" if (med is not None and med >= 150)
                 else ("not-met" if med is not None else "no-series"))
    print(f"\n  {pool}")
    print(f"    covered   : {covered}")
    print(f"    no tape   : {uncovered}")
    print(f"    max level : {maxlv} bp  -> {access}")
    print(f"    member chg: {changes}")
    print(f"    pool median change: {med} bp -> variation {variation}")
    if access == "ACCESS-IMPAIRED":
        print("    STATUS    : access-impaired — recorded as a §5.3 Capital event, "
              "NOT K2 (pre-registration §4; D11: 'trapped, not insensitive')")
    elif variation == "met":
        print("    STATUS    : unscreened — variation met, response test needs new "
              "commitment flows over >=2 quarters (D11 test 4); stocks are not evidence")
    else:
        print("    STATUS    : unscreened — variation test not met at pool level")
