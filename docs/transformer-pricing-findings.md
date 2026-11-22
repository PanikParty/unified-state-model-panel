# Item 8 — Free Public Pricing Data: Power Transformers & Switchgear

**Compiled 2026-11-21 (dispatched research; parent spot-verified FRED WPU117409 against fredgraph.csv — 2026-10 = 390.436, exact).** Environment notes from the collector: general search engines were blocked or poisoned from the collection host; data below was pulled from direct APIs and known public document portals (USAspending API, regulations.gov API, FRED, OSTI, City of Tacoma/TPU).

## (a) Verified dated price points

### Federal procurement — USAspending API (free, no key; award pages public)
Source API: `POST https://api.usaspending.gov/api/v2/search/spending_by_award/` (NAICS 335311 / PSC 6120). Award page pattern `https://www.usaspending.gov/award/<generated_internal_id>` verified (HTTP 200).

| Date | Spec | Price (contract value) | Source |
|---|---|---|---|
| 2026-02-20 | GSU transformers, Oahe & Fort Peck Dams (multi-unit, USACE) | $56,977,893.50 (PAF Electrical) | usaspending.gov/award/CONT_AWD_W9128F26CA013_9700_-NONE-_-NONE- |
| 2025-03-20 | Wolf Creek Powerplant GSU transformer | $30,540,706.29 (Yellowstone Electric) | USAspending API, NAICS 335311 query |
| 2025-06-25 | "Transformer for FT2" (DoE/WAPA) | $3,500,000 (G&RK Consulting) | usaspending.gov/award/CONT_AWD_89503425PWA002074_8900_-NONE-_-NONE- (URL verified 200) |
| 2023-09-26 | Mobile transformer 115/69/34.5 kV, 40 MVA (WAPA) | $925,922 | usaspending.gov/award/CONT_AWD_89503223CWA000089_8900_-NONE-_-NONE- |
| 2022-09-27 | Groton substation transformer, 3-ph, 115–69 kV, 30/40/50 MVA (WAPA) | $654,559 | usaspending.gov/award/CONT_AWD_89503422PWA001488_8900_-NONE-_-NONE- |
| 2021-09-29 | NDMO mobile substation 115×69–12.47 kV (WAPA) | $2,000,497 | usaspending.gov/award/CONT_AWD_89503421CWA000054_8900_-NONE-_-NONE- |
| 2021-09-27 | Sioux City 2 KU1A autotransformer replacement (WAPA) | $975,000 | USAspending API |
| 2019-11-21 | Nixa autotransformer #1 replacement (WAPA/SWPA) | $667,159 | USAspending API |
| 2019-09-20 | 230 kV spare transformer, MNA (USACE; ABB Inc) | $1,677,255 | USAspending API |
| 2019-07-17 | Transformer supply, Robert S. Kerr Powerhouse (USACE) | $4,414,187.95 | USAspending API |
| 2019-07-01 | 5 MVA 34.5/24.9 kV station-class transformer, North Cody (WAPA) | $323,501 | usaspending.gov/award/CONT_AWD_89503219PWA000166_8900_-NONE-_-NONE- |
| 2018-09-07 | Two transformers, Denison Powerhouse (USACE) | $8,389,081 | USAspending API |
| 2018-09-25 | Fort Thompson 2 KU1B autotransformer replacement (WAPA) | $1,948,444.30 | USAspending API |
| 2016-09-24 | 50 MVA 115/69/12.47 kV transformer, Big George sub (WAPA) | $695,323 | usaspending.gov/award/CONT_AWD_DEWA0003482_8900_-NONE-_-NONE- |
| 2023-11-02 | Replace SPS switchgear with GIS, Bldg 1507 (US Navy; Siemens) | $14,071,103 | USAspending API (switchgear) |

(USAspending remains queryable by NAICS 335311/335313, PSC 5925/6120, any date range.)

### Municipal procurement — City of Tacoma / Tacoma Public Utilities (tacoma.gov bid results + mytpu.org board agendas; all PDFs public)

| Date | Spec | Price | Source |
|---|---|---|---|
| 2026-01-14 | ONE autotransformer 230/115 kV, 300/400/500 MVA (Iljin Electrics USA) — unit price | $7,710,000 + tax (Resolution U-11574) | mytpu.org/wp-content/uploads/Agenda-20260114.pdf |
| 2026-02-11 | Substation power transformers contract increase (Iljin) | $3,000,000 (projected contract total $13,000,000) (U-11583) | mytpu.org/wp-content/uploads/Agenda-20260211.pdf |
| 2026-06-10 | 1-ph padmount distribution transformers, 3-yr contracts (General Pacific; Anixter) | $1,000,000 each (options to $2,000,000 each) | mytpu.org/wp-content/uploads/Agenda-20260610.pdf |
| 2026-06-10 | 115 kV unitized transmission switches (Cleaveland Price) | $685,560.87 (projected $2,000,000) | same agenda |
| 2026-10-14 | 3-ph padmount distribution transformers, 3-yr (General Pacific) | $5,000,000 + tax | mytpu.org/wp-content/uploads/Agenda-20261014.pdf |
| 2024-01-16 (results 2024-06-11) | 3-ph padmounted distribution transformers, annual contract — 7 bids, low $1,221,448 (Eaglerise, mineral oil) – $2,881,007 (Irby, ester) | bid totals | cms.tacoma.gov/Purchasing/FormalBidResults/06-11-2024_PT24-0123F.pdf |
| 2024-06-04 | 1-ph overhead distribution transformers — bids $318,930.07 (PulseMac) – $2,226,250 | bid totals | cms.tacoma.gov/Purchasing/FormalBidResults/06-04-2024_PT24-0111F.pdf |
| 2024-07-02 | 15 kV padmount switchgear — Wesco $925,325.30; General Pacific $942,358; Irby $943,960; Scott Mfg $1,717,293 | bid totals | cms.tacoma.gov/Purchasing/FormalBidResults/07-02-2024_PT24-0117F.pdf |
| 2025-10-14 | High-voltage circuit breakers — Border States $1,379,077; Carlson $1,507,539 | bid totals | cms.tacoma.gov/purchasing/formalbidresults/10-14-2025_RFB_PT25-0125F.pdf |

### Used/surplus market (label: USED, secondary signal)

| Date | Spec | Price | Source |
|---|---|---|---|
| 2020-07-10 | Crescent Substation transformer (surplus sale, City of Tacoma) | $23,950 (Transformer Technologies, winning bid) | cms.tacoma.gov/Purchasing/InformalBidResults/PT20-0208N_BidTab.pdf |
| 2026-09-16 | Surplus overhead transformers, lot (winning T&R Electric) | $14,087.50 (other bids $12,057.76 / $11,286.00) | cms.tacoma.gov/purchasing/informalbidresults/PT26-0204N_BidResults.pdf |

### DOE / national-lab price statements
NLR, *Large Power Transformer Supply Chain Gap Analysis… Supplemental Report*, 2026-05-06, DOI 10.2172/3363379 (osti.gov/servlets/purl/3363379):
- New LPT procurement ≈ **$15,000–$21,000 per MVA (2024 USD)** → ~$1.5–2.1M per 100-MVA unit; customized units up to ~$40/kWac (~$4M/100 MVA); single LPT "as high as $10 million" (citing USITC 2024).
- LPT prices 2025 ≈ **+80% vs 2014–2021 plateau** (FRED PPI WPU117409); +50–70% vs 2019 (Wood Mackenzie — PAYWALLED, secondary).
- Lead times 12–18 mo → 30–36 mo; EHV up to 60 mo; ~70% of recent LPT installs imported.

**Repeatable free index: FRED WPU117409** (BLS PPI, Electric Power & Specialty Transformer Mfg: Power & Distribution Transformers). Free CSV, monthly, verified live: 1999-12=100 → 384.957 (2026-08/09) → **390.436 (2026-10)**. `fred.stlouisfed.org/graph/fredgraph.csv?id=WPU117409`

## (b) Channel-by-channel repeatability
1. **Public procurement — YES, repeatable.** USAspending API (federal, free, machine-readable, 2000–present; NAICS 335311/335313, PSC 6120/5925) gives dated contract values incl. per-unit WAPA transformer buys. Municipal: Tacoma publishes every bid result + board award memo free (recurring padmount/polemount/switchgear buys); other munis (Chelan/SnoPUD blocked by WAF from the collection host but public) follow the same pattern. Unit-price level available in board memos (e.g., Iljin 500-MVA autotransformer $7.71M).
2. **DOE/lab reports — YES (index + ranges), not a unit-price series.** OSTI API free; FRED WPU117409 is the durable monthly series. DOE EERE distribution-transformer rulemaking (docket EERE-2019-BT-STD-0018, final rule Apr 2024) contains TSD + engineering spreadsheets with manufacturer selling prices by kVA class — attachment downloads returned 403/empty from the collection host; page: regulations.gov/document/EERE-2019-BT-STD-0018-0165 — **EXISTS, DOWNLOAD UNVERIFIED from here**.
3. **PUC rate-case/IRP filings — UNVERIFIED in this session** (search engines unavailable; no docket-system crawl completed). Mechanism plausible but no price point collected; treat as open.
4. **OEM/distributor list prices — quote-gated.** Hitachi Energy power-transformer pages = marketing + "Contact us" (verified). Siemens Energy = marketing page. GE Vernova /transformers 404 (wrong path). Eaton catalog timed out. Wesco 403. Graybar loads but prices login-gated (UNVERIFIED detail). Schneider shop.se.com shows list prices only for LV catalog items; grid-scale = quote. **No free grid-scale OEM list prices.**
5. **Used/reconditioned — YES, thin but real.** Utility surplus auctions (Tacoma tabs above), GovDeals/PublicSurplus (public results pages — bot-blocked from the collection host, UNVERIFIED here but known-public), dealer sites (Maddox/Sunbelt Solomon) are quote-gated.

## (c) Verdict
**PARTIAL — sufficient for a first-pass grid-scale cost series.**
- Free data CAN anchor: (i) a monthly transformer price index 1999–present (FRED WPU117409); (ii) $/MVA ranges for LPTs ($15–21k/MVA 2024-USD, NLR/DOE); (iii) dated point prices for substation-class units ($0.3M–$7.7M, WAPA/Tacoma/USACE 2015–2026) and distribution-class contract totals; (iv) switchgear bid totals ($0.9M–$14M).
- Gaps: no free continuous unit-price series for ≥100 MVA LPTs (NEMA/Wood Mackenzie paywalled; OEMs quote-gated); PUC line-item channel unproven here; EERE distribution price tables exist but need a browser download (blocked from the collection host).
- Recommended first-pass: WPU117409 as the escalator, calibrated to NLR $/MVA range + Tacoma/WAPA unit points.
- Adjacent candidate noted 2026-11-21 (not yet evaluated): Gloom Datasets hosts `power` and `awards` datasets (pay-per-call via x402 or plan); the `power` sample carries grid connection/load-application records. Check samples against this gap before any report purchase is recommended.
