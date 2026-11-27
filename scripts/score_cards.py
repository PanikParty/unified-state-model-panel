#!/usr/bin/env python3
"""score_cards.py — mechanical scorer for the four 2026-11-26 prediction cards.

Purpose: nobody grades themselves. Every claim whose resolution is a numeric
threshold on a named series is evaluated here. Claims that need a judgement
(policy events, CDS levels, filing facts) are listed as MANUAL with the evidence
rule that must be cited — they are resolved by a second agent, never by the
author of the claim.

Usage:
    python3 score_cards.py            # current state: OPEN / DECIDED / BROKEN
    python3 score_cards.py --at 2027-05-26   # resolution run

Rule: a claim is never "close". It resolves HIT / MISS / UNSCOREABLE, and
UNSCOREABLE must name the missing series rather than being treated as a pass.
"""
import argparse, csv, datetime, io, json, statistics, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
P1 = 1700000000


def yahoo(sym):
    u = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
         f"?period1={P1}&period2={int(datetime.datetime.now().timestamp())}&interval=1d")
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
    q = d["chart"]["result"][0]
    return {datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d"): c
            for t, c in zip(q["timestamp"], q["indicators"]["quote"][0]["close"]) if c}


def fred(series):
    u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    txt = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "curl/8.0"}),
                                 timeout=60).read().decode()
    out = {}
    for r in csv.DictReader(io.StringIO(txt)):
        v = r[series]
        if v not in ("", "."):
            out[r["observation_date"]] = float(v)
    return out


def window(s, start, end):
    return {k: v for k, v in s.items() if start <= k <= end}


def win_or_last(s, start, end):
    """Window, or the latest single observation when the window is empty.

    Futures sessions are labelled with the next calendar day, and FRED prints
    lag by days, so a wall-clock window can legitimately contain nothing. The
    current-state view falls back to the last print and says so; the resolution
    run (--at) keeps the real window.
    """
    w = window(s, start, end)
    if w:
        return w, False
    if not s:
        return {}, False
    k = max(s)
    return {k: s[k]}, True


# ---- claim table -----------------------------------------------------------
# kind: last_above | last_below | never_above | never_below | max_atleast |
#       min_atmost | ratio_min_above | ratio_min_below | corr_min | corr_max
CLAIMS = [
    # Duncan D1-D12
    ("D1", "duncan", "Gold closes above $3,600", "GC=F", "last_above", 3600, "2026-11-26", "2027-05-26"),
    ("D2", "duncan", "Gold never closes above $4,400", "GC=F", "never_above", 4400, "2026-11-26", "2027-05-26"),
    ("D3", "duncan", "Silver closes above $42", "SI=F", "last_above", 42, "2026-11-26", "2027-05-26"),
    ("D4", "duncan", "BTC closes above $62,000", "BTC-USD", "last_above", 62000, "2026-11-26", "2027-05-26"),
    ("D5", "duncan", "HY OAS reaches 4.00%", "BAMLH0A0HYM2", "max_atleast", 4.00, "2026-11-26", "2027-05-26"),
    ("D6", "duncan", "HY OAS reaches 4.50%", "BAMLH0A0HYM2", "max_atleast", 4.50, "2026-11-26", "2027-05-26"),
    ("D7", "duncan", "T10YIE exceeds 2.25%", "T10YIE", "max_atleast", 2.25, "2026-11-26", "2027-05-26"),
    ("D8", "duncan", "UNRATE reaches 4.4%", "UNRATE", "max_atleast", 4.4, "2026-11-26", "2027-05-26"),
    ("D12", "duncan", "Broad dollar (DTWEXBGS) above 126.0", "DTWEXBGS", "max_atleast", 126.0, "2026-11-26", "2027-05-26"),
    # Gurney G1-G10 (A2: G2 resolves on closes)
    ("G1", "gurney", "Gold/silver ratio never below 78", "RATIO", "ratio_min_above", 78, "2026-11-26", "2027-05-26"),
    ("G2", "gurney", "Gold never closes below $3,191 (close-based, A2)", "GC=F", "never_below", 3191, "2026-11-26", "2027-05-26"),
    ("G7", "gurney", "20d avg pairwise corr drops below 0.50", "CORR", "corr_min_below", 0.50, "2026-11-26", "2027-05-26"),
    ("G10", "gurney", "UNRATE never above 4.5%", "UNRATE", "never_above", 4.5, "2026-11-26", "2027-05-26"),
    # Thufir T1-T10
    ("T1", "thufir", "20d corr never below 0.60 through Feb", "CORR", "corr_min_above", 0.60, "2026-11-26", "2027-02-28"),
    ("T2", "thufir", "Gold/silver ratio falls below 80", "RATIO", "ratio_min_below", 80, "2026-11-26", "2027-05-26"),
    ("T3", "thufir", "Silver reaches $45", "SI=F", "max_atleast", 45, "2026-11-26", "2027-05-26"),
    ("T4", "thufir", "BTC below $50k before Feb", "BTC-USD", "min_atmost", 50000, "2026-11-26", "2027-02-28"),
    ("T7", "thufir", "HY OAS stays below 4.50% through March", "BAMLH0A0HYM2", "never_above", 4.50, "2026-11-26", "2027-03-31"),
    ("T9", "thufir", "Gold never closes below its 14-month low (3,515.40)", "GC=F", "never_below", 3515.40, "2026-11-26", "2027-03-31"),
]

MANUAL = [
    ("D9", "duncan", "Any Fed cut by 2027-05-26", "FOMC statement — cite date and target range"),
    ("D10", "duncan", "CoreWeave stays >800bp or restructures", "CDS pull + any restructuring filing"),
    ("D11", "duncan", "Named federal AI-sector programme", "Named statute/appropriation/facility"),
    ("G3", "gurney", "BTC underperforms gold over the window", "two series, same dates — automatable later"),
    ("G4", "gurney", "Shanghai premium fires +1% (F6)", "SGE fix vs spot at fix time, synchronous"),
    ("G5", "gurney", "DLR renewal spreads >= +3% both prints", "DLR 10-Q cash releasing spread"),
    ("G6", "gurney", "Four mega-caps CDS < 250bp (A1 scope)", "CDS pull per name"),
    ("G8", "gurney", "CoreWeave restructures rather than recovers", "filing evidence"),
    ("G9", "gurney", "Hike then hold", "FOMC decisions, both directions"),
    ("T5", "thufir", "CoreWeave access-impaired through Feb", "CDS pull"),
    ("T6", "thufir", "Second AI-infra name crosses 1,000bp", "CDS pull, on-tape set only"),
    ("T8", "thufir", "BoJ hike or MoF intervention by June", "BoJ statement or MOF disclosure"),
    ("T10", "thufir", "Fed hikes at 12/8-9 FOMC", "FOMC statement"),
]


def corr_series(a, b, n=20):
    dates = sorted(set(a) & set(b))
    ra = {dates[i]: a[dates[i]] / a[dates[i - 1]] - 1 for i in range(1, len(dates))}
    rb = {dates[i]: b[dates[i]] / b[dates[i - 1]] - 1 for i in range(1, len(dates))}
    out = {}
    ds = sorted(ra)
    for i in range(n, len(ds) + 1):
        w = ds[i - n:i]
        out[ds[i - 1]] = statistics.correlation([ra[d] for d in w], [rb[d] for d in w])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", default=None, help="resolution date YYYY-MM-DD")
    a = ap.parse_args()

    cache = {}
    def get(name):
        if name not in cache:
            cache[name] = yahoo(name) if name.endswith(("=F", "-USD", "IXIC")) else fred(name)
        return cache[name]

    today = datetime.date.today().isoformat()

    def status_for(kind, settled, violated):
        """A claim can only resolve HIT at its end date; until then it is OPEN
        unless it has already been violated, which resolves it MISS early."""
        if violated:
            return "MISS (violated)"
        return "HIT" if settled else "OPEN"

    results = []
    for cid, owner, text, series, kind, thr, start, end in CLAIMS:
        cut = a.at or today
        settled = cut >= end
        try:
            if series in ("RATIO", "CORR"):
                if series == "RATIO":
                    g, s_ = get("GC=F"), get("SI=F")
                    series_map = {d: g[d] / s_[d] for d in set(g) & set(s_)}
                else:
                    cols = [get(x) for x in ("GC=F", "SI=F", "BTC-USD", "^IXIC")]
                    pairs = [corr_series(cols[i], cols[j]) for i in range(4) for j in range(i + 1, 4)]
                    common = sorted(set.intersection(*[set(p) for p in pairs]))
                    series_map = {d: statistics.fmean(p[d] for p in pairs) for d in common}
                w, fell_back = win_or_last(series_map, start, min(cut, end))
                if not w:
                    results.append((cid, owner, text, None, "UNSCOREABLE (no observations)")); continue
                lo, hi = min(w.values()), max(w.values())
                cur = lo
                if kind == "ratio_min_above":      # never below thr
                    met, violated = lo >= thr, lo < thr
                elif kind == "ratio_min_below":    # reaches below thr
                    met, violated = lo < thr, False
                elif kind == "corr_min_above":     # never below thr
                    met, violated = lo >= thr, lo < thr
                elif kind == "corr_min_below":     # drops below thr
                    met, violated = lo < thr, False
                else:
                    results.append((cid, owner, text, None, "UNSCOREABLE (kind)")); continue
                never_kind = kind in ("ratio_min_above", "corr_min_above")
                if met and never_kind:
                    # a "never below X" claim cannot be met early: it holds until
                    # the window closes without a breach.
                    st = "HIT" if settled else "OPEN (holding)"
                elif met:
                    st = "HIT" if settled else "HIT (met early)"
                elif violated:
                    st = "MISS (violated)"
                else:
                    st = "MISS" if settled else "OPEN"
                if fell_back and st == "OPEN":
                    st = f"OPEN (as of {max(w)})"
                results.append((cid, owner, text, round(cur, 3), st))
                continue
            s_ = get(series)
            w, fell_back = win_or_last(s_, start, min(cut, end))
            if not w:
                results.append((cid, owner, text, None, "UNSCOREABLE (no observations)")); continue
            last_d = max(w); last = w[last_d]
            lo, hi = min(w.values()), max(w.values())
            if kind == "last_above":
                cur, violated = last, False
            elif kind == "last_below":
                cur, violated = last, False
            elif kind == "never_above":
                cur, violated = hi, hi > thr
            elif kind == "never_below":
                cur, violated = lo, lo < thr
            elif kind == "max_atleast":
                cur, violated = hi, hi >= thr
            elif kind == "min_atmost":
                cur, violated = lo, lo <= thr
            else:
                results.append((cid, owner, text, None, "UNSCOREABLE (kind)")); continue
            if kind in ("max_atleast", "min_atmost"):
                st = "HIT (met)" if violated else ("MISS" if settled else "OPEN")
            else:
                st = status_for(kind, settled, violated)
            if fell_back and st.startswith("OPEN"):
                st = f"OPEN (as of {last_d})"
            results.append((cid, owner, text, round(cur, 4), st))
        except Exception as e:
            results.append((cid, owner, text, None, f"UNSCOREABLE ({type(e).__name__})"))

    print(f"{'id':4} {'owner':7} {'current':>10}  {'status':10} claim")
    for cid, owner, text, val, status in results:
        print(f"{cid:4} {owner:7} {str(val):>10}  {status:10} {text}")
    print(f"\nMANUAL cells (never self-scored; second agent cites evidence): {len(MANUAL)}")
    for cid, owner, text, rule in MANUAL:
        print(f"  {cid:4} {owner:7} {text}  [evidence: {rule}]")
    print(f"\nmechanical claims: {len(CLAIMS)} | manual: {len(MANUAL)} | total: {len(CLAIMS)+len(MANUAL)}")


if __name__ == "__main__":
    main()
