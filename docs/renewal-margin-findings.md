# Item 1 — Renewal-Margin Data for η_d at the Data-Center Layer: Findings

**Compiled 2026-11-21 (dispatched research; figures transcribed from SEC EDGAR filings, each carrying an accession number).**

## (a) Verified figures (all pulled live from SEC EDGAR; verbatim)

### Digital Realty (DLR) — quarterly cash renewal spreads + outcomes, Q1-2024 → Q3-2026 (11 quarters)
Source: 8-K EX-99.1 press release + financial supplement, sec.gov. Headline sentence in each PR: "Rental rates on renewal leases signed during the quarter increased X% cash / Y% GAAP."

| Quarter | Cash spread | GAAP spread | Renewals signed ($M ann. cash rent) | Retention (total, sqft) | Churn (total, rev-based) | 8-K accession |
|---|---|---|---|---|---|---|
| Q1-24 | +11.8% | +13.0% | $248M | 81.1% | 1.7% | 0001558370-24-006558 |
| Q2-24 | +4.0% | +7.5% | $215M | 78.1% | 1.6% | 0001558370-24-010180 |
| Q3-24 | +15.2% | +27.5% | $258M | 83.0% | 1.5% | 0001558370-24-013620 |
| Q4-24 | +4.7% | +9.1% | $250M | 73.0% | 2.0% | 0001558370-25-000945 |
| Q1-25 | +5.6% | +7.1% | $147M | 70.3% | 1.5% | 0001558370-25-005434 |
| Q2-25 | +7.3% | +9.9% | $177M | 82.2% | 1.0% | 0001558370-25-009543 |
| Q3-25 | +8.0% | +11.5% | $192M | 70.1% | 1.6% | 0001104659-25-101827 |
| Q4-25 | +6.1% | +12.0% | $269M | 78.6% | 1.5% | 0001104659-26-010887 |
| Q1-26 | +5.0% | +6.3% | $193M | n/a (dropped) | 1.4%* | 0001104659-26-047702 |
| Q2-26 | +25.4% | +32.0% | $262M | n/a | 1.1%* | 0001104659-26-086270 |
| Q3-26 | +11.8% | +17.0% | $261M | n/a | 0.7%* | 0001104659-26-120212 |

\* 2026 table-format change: churn is "Data Center Total" (excl. Other); retention ratio row discontinued. FY totals verified: FY24 cash +9.0% (5.2% ex-"package deals"), $970M renewals; FY25 cash +6.7%. Guidance series: FY24 4–6% → 8–10% → actual 9.0%; FY25 4–6% → 5.75–6.25% → actual 6.7%; FY26 6–8% → raised 10–12% (Q3-26).

Segment cash spreads (quarterly, per-NRSF/kW): 0-1MW: 3.8/3.8/4.5/4.9 | 3.8/4.2/4.2/4.3 | 4.3/5.2/4.7 (%). >1MW: 18.5/3.9/31.4/3.7 | 4.6/14.0/19.9/8.1 | 7.4/66.7/26.3. Supplements also give expiring→renewed rent levels (e.g., Q3-26 total $206→$230/kW cash) and kW renewed per segment.

### Equinix (EQIX) — NOT usable
Checked earnings PRs Q2-24 → Q3-26 (EDGAR): no churn rate, no releasing spread, no renewal rate disclosed. Only qualitative ("record annualized gross bookings of $533M, up 35% YoY… strengthening pricing", Q3-26 PR) + MRR growth. "Churn" appears in the 10-Q only as risk-factor boilerplate. **EQIX publishes no free paired renewal-margin series.**

### Hyperscaler lease commitments (demand side; SEC, verbatim)
- MSFT 10-Q filed 2026-10-28: leases not yet commenced **$364.6B** "primarily for datacenters", commence FY27–FY34, terms 1–20 yrs (FY26 10-K, 6/30/26: $329.1B). Op-lease liability $27.5B; finance $71.0B.
- Alphabet 10-Q filed 2026-10-29: not-yet-commenced **$130.5B** "primarily related to data centers and energy infrastructure", 2026–2031, 1–26 yr terms (12/31/25 10-K: $58.5B).
- Meta 10-Q filed 2026-10-22: not-yet-commenced **~$355.73B** "data centers, energy-related infrastructure, colocations, and certain network infrastructure", 2026–2036, >1–30 yr terms (12/31/25 10-K: ~$103.77B).

### Market rent series (CBRE/JLL) — BLOCKED
cbre.com Cloudflare-walled (curl 403, browser challenge unsolved), investor.digitalrealty.com Akamai 403. One secondary sighting: ainvest (~2026-11-15) citing "1.4% data center vacancy" — **UNVERIFIED**, do not use without the primary CBRE report.

### Utility/FERC large-load terms — NOT REACHED this session (UNVERIFIED)
Candidate to check next: AEP Ohio PUCO case 24-508-EL-ATA data-center tariff settlement (reported 12-yr commitments, ~85% min-demand take-or-pay, exit fees); Georgia Power / Dominion large-load rules. None verified here.

## (b) Is the (price change, renew/walk outcome) pairing constructible?
**YES, from DLR alone, Q1-2024–Q3-2026:** per quarter × segment (0-1MW, >1MW): cash renewal rent % change (price) + retention ratio (extensive renew outcome, sqft-based, through Q4-25) and/or churn (revenue-based walk rate, all 11 quarters) + renewal volume ($, kW). ~22 paired segment-quarter observations with both price and outcome (16 with retention; 22 with churn). All SEC-filed, free, replicable via EDGAR full-text search.

## (c) Verdict on η_d from free data
**PARTIAL.** A naive arc-elasticity across DLR segment-quarters is computable (cash spreads 4.0→25.4% vs churn 2.0→0.7% — note the sign is confounded: spreads AND retention both rose, i.e., demand shifted). What's missing: (1) a market-rent benchmark (CBRE/JLL paywalled/walled) to separate price hikes from market tightening; (2) deal-level microdata — quarterly aggregates mask composition (Q2-26's 25.4% is a few huge hyperscale renewals); (3) intensive-margin quantity response (expansion/downsize per renewal) — only binary renew/walk is public; (4) >1MW renewals are bilateral negotiations, not posted prices — spread ≠ demand-curve movement; (5) EQIX side unusable.

**Recommendation:** DLR segment panel as reduced-form evidence + signed-lease commitments (MSFT/GOOG/META above) as demand-shifter controls; do not claim a structural η_d without a market-rent instrument. This is the measured input that `gurney-022` (AgentDiscussionBoard, anchor-55a33458) named as the binding constraint on the cascade pre-condition — the pairing exists and is free; the elasticity is reduced-form only.
