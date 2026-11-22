# Data Sources for the §13 Panel-Data Build

Each entry: what it satisfies, whether it's live-tested in this cycle, cost,
and access method. "Tested" means a real HTTP call was made and returned real
data during this session (2026-11-21), not just a product page read.

## Free, tested, already wired in

| Source | Satisfies | Endpoint | Notes |
|---|---|---|---|
| Yahoo Finance chart API | Daily OHLC/close for any ticker, incl. futures (`GC=F`, `SI=F`), crypto (`BTC-USD`), indices (`^IXIC`), equities (`ANT`) | `https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={r}&interval=1d` | No key. Tested live this session — see `risk-hygiene-toolkit` repo. Powers vol/correlation/price legs of every episode row. |
| FRED (`T10YIE`, `DGS10`, `DFII10`, HY OAS series) | §5.3's rate/breakeven/credit-spread background, §4's `ν` | `https://api.stlouisfed.org/fred/series/observations` (needs a free FRED API key — registration only, no cost) or `fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES` (no key, CSV) | hermes-036/037 already verified T10YIE and Treasury CMT by hand; this just automates what Duncan did manually. |
| U.S. Treasury daily par yield curve | Same as above, primary source for CMT | `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all` | No key. |
| Mercatus GPU Index | §8's L2b/L3 pricing evidence (H100/H200/B200 rental, 50+ providers, 5-min refresh, public methodology) | `https://www.mercatus-ai.com/gpu-index` (scrape or watch for a documented API — methodology page says "API integrations"; confirm a machine-readable endpoint before building a scraper) | Free, no signup, methodology public. Directly extends §8.6's single H100 data point into a continuous series. |
| NREL Annual Technology Baseline (ATB) | §13 item 8 — LCOE by technology | `https://data.openei.org/submissions/8759` (CSV/XLSX/Parquet, OEDI data lake on AWS, CC-licensed public) | Free, federal, versioned by year. Covers every generation technology's CAPEX/OPEX/capacity-factor/LCOE. |
| LBNL "Queued Up" interconnection queue dataset | §13 item 8 — interconnection cost/timeline per ISO; also corroborates §8.1's L1 lead-time proxy | `https://emp.lbl.gov/queues` (project-level XLSX, CC BY 4.0, >50 ISOs/RTOs/balancing areas, ~98% of US generating capacity) | Free, annual edition ("Queued Up 2026" covers through end of 2025), attribution required. `interconnection.fyi` (same publisher, GridTracker) gives a free daily-updated browse layer; full export/API is a paid GridTracker subscription — see below. |
| CFTC Weekly Swaps Report / NY Fed Corporate Bond Market Distress Index | Capital-event percentile rule background (§5.3), macro credit stress corroboration | `quotelinks.com` free wrapper API, `GET /v1/credit/cds/history`, `/hqm/*` — no key | Market-wide CDS notional/volume only, **no single-name spreads**. Good for the macro base rate in Duncan's DEC-4 critique; not sufficient for member-level K-screen. |
| BIS Quarterly Review (Mar 2026), "Boom and bust of the recent silver and gold rush" | Episode #2 seed data (Jan–Feb 2026 leveraged-ETF/margin episode) — leverage rebalancing multiplier, ETF premium/discount dynamics, margin-call mechanism | `bis.org/publications/qr-202603/...` | Free, authoritative, already cited in `episodes.json` episode 2. |

## Low-cost, pay-per-call (no enterprise contract) — candidate for Alex's budget call

| Source | Satisfies | Cost model | Why it's needed |
|---|---|---|---|
| `gloom.sh` CDS API (`/v1/cds/curves`, `/v1/cds/trades`) | §13 item 11/4 — **member-level** CDS spreads for AI-infrastructure pool counterparties (the actual K-screen input; CFTC/BIS data above is aggregate-only) | Credit-based, ~4 credits/call for curves/trades, free sample endpoint exists (`/v1/datasets/cds/sample`) | This is the one item that free public data genuinely cannot satisfy — single-name spreads are commercial data everywhere (S&P Global, ICE, Bloomberg, Refinitiv all require enterprise licensing; WRDS requires academic affiliation). `gloom.sh`'s per-call pricing is the cheapest path found — likely tens of dollars to run the first K-screen pass on 5-10 names, not an enterprise contract. |
| GridTracker / `interconnection.fyi` full export | Developer-level interconnection queue detail beyond LBNL's annual snapshot (daily updates, developer names/docs) | Monthly CSV or Snowflake subscription, price not public — requires a quote | Optional upgrade over the free annual LBNL file; LBNL's "Queued Up 2026" is sufficient for a first-pass §13 item 8 build. Defer unless the annual cadence proves too coarse. |

## Needs an actual resourcing decision from Alex (not purchasable by an agent unsupervised)

- **S&P Global / ICE Data Derivatives / Bloomberg CDS terminals** — the
  institutional-grade version of the above, if the board ever needs it at
  scale (hundreds of names, intraday). Enterprise contracts, likely
  four/five-figure annual minimums. **Not recommended yet** — `gloom.sh`'s
  per-call pricing covers the first-pass K-screen §13 item 4 asks for at a
  fraction of the cost; only escalate here if that pass shows the per-call
  spend growing past the subscription breakeven.
- **Transformer/switchgear pricing data** (named in §13 item 8 alongside
  LCOE and interconnection cost) — no free public series was found this
  session. Likely needs either (a) a market-research report purchase
  (Wood Mackenzie, S&P Global Commodity Insights — one-off report cost,
  not a subscription), or (b) direct outreach to transformer OEMs/distributors
  for quote data, which is manual-collection work, not an API. Flagging as
  open; recommend Gurney's parallel-dispatch pattern be pointed at
  manufacturer/distributor public pricing pages before paying for a report.

## Ingested this session (2026-11-21, by Thufir)

- **`data/atb_2025_capex_opex_sample.csv`** — 468 rows pulled live from the
  real NREL ATB 2025 Model Parameters file
  (`2025_v1_Model_Parameters_08-27-2026.csv`, `data.openei.org/submissions/8759`),
  filtered to CAPEX/OCC/O&M rows for firm/dispatchable generation technologies
  (gas, nuclear, battery, coal, geothermal) — the technologies most relevant
  to §8.1's L1 grid-power layer for AI compute. **Correction on first pass:**
  this file carries CAPEX/OPEX cost-driver inputs, not the pre-computed LCOE
  summary metric itself — the dedicated LCOE Summary CSV is a different file
  on the same OEDI submission page, not yet located/pulled. Flagging this
  rather than presenting CAPEX as LCOE.
- **LBNL "Queued Up" (`emp.lbl.gov/queues`)** — blocked by bot protection on
  a plain `curl` (HTTP 403, `Sec-CH-UA` challenge headers present). Tried the
  Zenodo mirror found in search (`zenodo.org/records/23295409`) as a fallback
  — it returned an HTML error page, not the CSV, on a plain `curl` as well.
  Both attempts failed; this needs the browser tool (real headless browser,
  handles JS challenges and redirects) rather than another curl variant.
  Flagged as a real blocker, not silently worked around.

## Not yet checked (next pass)

- Mercatus GPU Index's actual API contract (confirmed to exist in prose;
  endpoint/auth not yet verified live).
- FRED API key registration (free, but needs an actual signup step before
  automation — a 2-minute task, not a blocker, just not done yet).
