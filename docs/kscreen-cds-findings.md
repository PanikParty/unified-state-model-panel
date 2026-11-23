# K-screen CDS ingest — item 4/11 status, verified 2026-11-21

Owner: Duncan (hermes). Everything below was executed, not read.

## 1. The API is real, and it is pay-per-call as documented

```
GET https://api.gloom.sh/v1                          -> 200, service manifest
GET https://api.gloom.sh/v1/datasets/cds/sample       -> 200, 5 records, free
GET https://api.gloom.sh/v1/cds/curves?ticker=NVDA    -> 402 payment_required
GET https://api.gloom.sh/v1/cds/trades?ticker=NVDA    -> 402 payment_required
```

The 402 body is informative and corrects two assumptions in `ROADMAP.md`:

- **The parameter is `issuer`, not `ticker`.** Quoted route contract:
  `/v1/cds/curves` takes `days, issuer, tenor, asOf, fields, include`;
  `/v1/cds/trades` takes `issuer, days, limit, fields, include`.
- A malformed call is **not charged** ("A payment sent with the same input is
  refused with this error and nothing is charged"), so a shape error costs
  nothing. A key is the only blocker.

## 2. The free sample is a shape demo, and it shows the data is sparse

Five records, five distinct names (Sabre, Unisys, Heineken, Compass Group,
Experian). Of those:

| Field state | Records |
|---|---|
| `reportedSpread` present (with `spreadNotation: "3"`) | 1 |
| `upfrontAmount` only, no par spread | 1 |
| Neither spread nor upfront | 3 |

**This changes the cost estimate.** The trade-dissemination tape is sparse per
name: a K-screen needs a spread per issuer per observation date, which means
either many `trades` calls per name (to accumulate enough notional), or the
`curves` route — which is built for exactly this and is the right first call.
The "~tens of dollars for 5–10 names" figure in `data_sources.md` was an
estimate; on this evidence it is optimistic for the `trades` route and
plausible for `curves`. Do not budget from the trades route.

## 3. `spreadNotation` is not guessed

Records carry `reportedSpread` with a notation code (`"3"` in the sample;
`fixedRate` of `0.05` in the same record). The mapping from code to units is
**not established** here, so `scripts/kscreen_cds.py` refuses to convert it:
`CONFIRMED_NOTATION` ships empty, and every unconfirmed record is emitted with
its raw fields and an UNPARSED note. Converting on a plausible-looking value
is how a screen reports 5.8bp for an investment-grade name and 58bp for the
same record, and §2.1 of the Unified State Model forbids exactly that. Confirm
the code table from published documentation before populating the dict.

## 4. The free upstream is down, not merely blocked

The obvious cost-avoidance path was DTCC's public price-and-volume data, which
would be the upstream for this class of dissemination record:

```
curl https://pddata.dtcc.com/ppd/api/report/cumulative/credit/MR_CUMULATIVE_CREDITS_2026_11_14.zip  -> 503
curl https://pddata.dtcc.com/                                                                    -> 503
headless browser -> https://pddata.dtcc.com/  -> "Service Unavailable ... contact your System Administrator"
```

A real browser gets the same 503, so this is a server-side outage, **not** the
bot-protection class that blocks LBNL. Retest before assuming the free path is
permanently closed; today it is closed.

## 5. What is needed

One thing: a **gloom.sh key** (or an approved spend against an account that
has one). With it:

```
GLOOM_KEY=... python3 scripts/kscreen_cds.py --live --issuer "Oracle Corp" --curves
```

and the first pass costs whatever the curves route charges per call. Without
it, this script's live mode exits rather than guessing, by design.

## 6. What the script does today

`scripts/kscreen_cds.py --sample` runs against the free endpoint and produces
`kscreen_sample.json`: per-issuer notional, record count, and a spread only
where the units are confirmed. On the sample that is **0 of 5 emitted, 5
flagged** — the correct result when the units are not established, and the
evidence for §2 above.

## 7. v2 — curves route wired, issuer list pre-registered, spend guarded

**`spreadBp` closes the notation problem.** The x402 402-block schema extension
(verified by Gurney 2026-11-23) documents that `/v1/cds/curves` returns
`spreadBp` — **basis points directly**. The parser now emits it with no
conversion table, because there is nothing to convert. `CONFIRMED_NOTATION`
stays empty and the trades route still refuses, since its notation remains
undocumented.

**Issuer list is pre-registered**: `data/kscreen_issuers.yaml`, 12 names, dated
2026-11-23 *before any data was purchased*, with the selection rule stated in
the file so it cannot be revised after seeing spreads. Names that return nothing
are recorded as NO COVERAGE and are **not** substituted with near-names.

**Spend is guarded**: `--max-spend` refuses a run whose estimated cost exceeds
the ceiling, and `--dry-run` prints the exact call plan for zero cost.

```
python3 scripts/kscreen_cds.py --live --issuers data/kscreen_issuers.yaml \
        --max-spend 2.00 --dry-run
plan: 12 issuers via curves route, est $1.44
```

**Division of labour.** The x402 wallet lives on blknode with the client in
`tools/x402/` (PR #6). Moving the key to another host to satisfy a filing
convention would be the wrong trade, so the paid calls run there and the JSON
comes back here for analysis. This script's key mode is for whoever holds a
`GLOOM_KEY`; the x402 lane needs no key at all.
