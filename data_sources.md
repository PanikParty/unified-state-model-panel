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
|| LBNL "Queued Up" interconnection queue dataset | §13 item 8 — interconnection cost/timeline per ISO; also corroborates §8.1's L1 lead-time proxy | `https://emp.lbl.gov/queues` (project-level XLSX, CC BY 4.0) | Free, annual edition ("Queued Up 2026" covers through end of 2025). **Primary XLSX bot-blocked (Cloudflare) to both curl and headless browser, 2026-11-21.** County-level derivative of the 2026 edition ingested via Zenodo API — see `data/lbnl_queue_2026_county.csv` and `docs/interconnection-queue-findings.md`. Cost/timeline fields remain open. |
| CFTC Weekly Swaps Report / NY Fed Corporate Bond Market Distress Index | Capital-event percentile rule background (§5.3), macro credit stress corroboration | `quotelinks.com` free wrapper API, `GET /v1/credit/cds/history`, `/hqm/*` — no key | Market-wide CDS notional/volume only, **no single-name spreads**. Good for the macro base rate in Duncan's DEC-4 critique; not sufficient for member-level K-screen. |
|| USAspending.gov award API | §13 item 8 — transformer/switchgear procurement price points (federal: WAPA, USACE, Navy) | `POST https://api.usaspending.gov/api/v2/search/spending_by_award/` (NAICS 335311/335313, PSC 6120/5925) | No key. Tested live 2026-11-21 — 15+ dated federal awards with specs pulled; award pages return 200. Repeatable series channel. |
|| FRED `WPU117409` (BLS PPI: power & distribution transformers) | §13 item 8 — transformer price escalator, monthly 1999–present | `fred.stlouisfed.org/graph/fredgraph.csv?id=WPU117409` | No key. Verified live: 2026-10 = 390.436 (base 1999-12=100). The durable free index. |
|| OSTI (DOE/NLR reports) | §13 item 8 — LPT $/MVA ranges and lead-time statements | `osti.gov` API, e.g. DOI 10.2172/3363379 (2026 LPT supply-chain supplement) | Free. Index + ranges, not a unit-price series. |
|| City of Tacoma / TPU bid results + board agendas | §13 item 8 — municipal procurement price points incl. unit-priced LPT | `cms.tacoma.gov/Purchasing/`, `mytpu.org/wp-content/uploads/` agenda PDFs | Free, public, recurring. Other munis follow the same pattern (some WAF-blocked from agent hosts but public). |
|| SEC EDGAR (full-text search + Archives document endpoints) | §13 items 5, 1 — AI-infra filings (S-1/424B4/10-Q) for the coupling-factor panel; DLR/EQIX 8-K earnings supplements for renewal-margin data | `efts.sec.gov/LATEST/search-index?q=...`, `www.sec.gov/Archives/edgar/data/...` | Free. Requires a descriptive `User-Agent` header (contact email) or 403. Tested live 2026-11-21: Anthropic 424B4 (0001628280-26-074944, 14.4 MB), CRWV/IREN/APLD/WULF 10-Qs, DLR 8-K series — see `docs/edgar-coupling-panel.md` and `docs/renewal-margin-findings.md`. |
|| BIS Quarterly Review (Mar 2026), "Boom and bust of the recent silver and gold rush" | Episode #2 seed data (Jan–Feb 2026 leveraged-ETF/margin episode) — leverage rebalancing multiplier, ETF premium/discount dynamics, margin-call mechanism | `bis.org/publications/qr-202603/...` | Free, authoritative, already cited in `episodes.json` episode 2. |

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
  LCOE and interconnection cost) — **free-source attempt COMPLETE, verdict
  PARTIAL-yes** (2026-11-21, Gurney; full record in
  `docs/transformer-pricing-findings.md`, point data in
  `data/transformer_price_points.csv`). Free channels anchor a first-pass
  series: FRED `WPU117409` (monthly PPI escalator, verified live,
  2026-10 = 390.436), DOE/NLR LPT report ($15–21k/MVA, 2024 USD), and 25+
  dated procurement price points (USAspending API; Tacoma PUB incl. a
  unit-priced 500 MVA autotransformer at $7.71M, 2026-01). No free
  continuous unit-price series for ≥100 MVA LPTs exists (OEMs quote-gated,
  Wood Mackenzie/NEMA paywalled). **A report purchase is NOT needed for the
  first pass**; revisit only if the panel later requires a continuous LPT
  unit-price series.

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

## Ingested 2026-11-21 (second pass, by Gurney)

- **`data/lbnl_queue_2026_county.csv`** (+ `.meta.json`) — LBNL "Queued Up"
  2026 edition, county-summed, retrieved via Zenodo record `23295409`'s API
  file endpoint after the primary domain hard-blocked both curl (Thufir) and
  a real headless browser (this session, Cloudflare Ray ID logged). Full
  provenance, coverage caveats (no AK/HI/CT), computed national totals
  (~1.73 TW active across 8,407 projects), and the residual cost/timeline
  gap are documented in `docs/interconnection-queue-findings.md`. The
  transformer-pricing free-source hunt runs as a separate dispatched work
  package; findings land as their own PR.

## Not yet checked (next pass)

- Mercatus GPU Index's actual API contract (confirmed to exist in prose;
  endpoint/auth not yet verified live).
- FRED API key registration (free, but needs an actual signup step before
  automation — a 2-minute task, not a blocker, just not done yet).
