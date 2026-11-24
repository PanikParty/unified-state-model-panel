# K-screen run record — passes A and B, executed 2026-11-24 (Gurney, blknode)

Execution of `docs/kscreen-preregistration.md` (as amended by A1, PR #11) on the
x402 lane. Payments: x402 v2, USDC on Base, from dedicated burner
`0xe7e3804D68fF0D8484cF4AB6E1982B67d1A654D8`. **Raw paid payloads are NOT in
this repo** (licensing); they live on the executing host. What follows is the
derived, committable record. On-chain receipts: `cds_meta*/receipts.ndjson` on
the executing host.

## Spend ledger (settled on-chain; balance-verified)

| Item | Calls | Settled |
|---|---|---|
| Pass A — levels (`curves`, 12 pre-registered issuers) | 12 attempted | **$0.96** (8 × $0.12; four 404s settled nothing) |
| Pass B — variation (`days=180`, the 8 covered issuers; gate ≥3 met) | 8 | **$0.96** |
| **Total** | | **$1.92** of $2.00 funded; $0.08 remains |

## Pass A — coverage map (the pre-registered 12, no substitutions)

- **Covered (8):** Oracle Corp (370 records), Amazon.com Inc (219), Broadcom Inc
  (169), Meta Platforms (170), Alphabet Inc (162), Microsoft Corp (156),
  CoreWeave Inc (108), NVIDIA Corp (104). Parsed via the `spreadBp` shape —
  **0 of 1,458 records unparsed**; the notation-table blocker does not apply to
  the curves route.
- **NO COVERAGE (4), definitive, from the dataset's own 404 bodies:**
  IREN ("IREN (IRE:BIT) has no CDS on the tape"), Applied Digital ("(APLD) has
  no CDS on the tape"), TeraWulf ("TERAWULF INC. (WULF) has no CDS on the tape")
  — three of the four neocloud/fringe names simply have no traded CDS market.
  Digital Realty Trust LP: the reference entity resolves, but it "has no 5Y
  level on the tape in the 730 days asked for, nor any in the 1100 days a curve
  reaches back" — a dormant CDS market, which is itself a datum.
- **Coverage finding:** the partly-capitalised fringe this screen exists to
  detect is **mostly invisible to the CDS tape** — of the four
  neocloud/REIT-fringe names, only CoreWeave has a live market.

## Pass A — levels and the access flag (per the pre-registered mapping)

| Issuer | min bp | mean bp | max bp | Flag |
|---|---|---|---|---|
| Microsoft | 27.0 | 44.5 | 59.0 | |
| Amazon | 20.0 | 54.1 | 101.6 | |
| Alphabet | 35.6 | 60.4 | 96.0 | |
| Meta | 53.0 | 83.4 | 126.5 | |
| NVIDIA | 43.0 | 88.9 | 146.0 | |
| Broadcom | 28.9 | 92.8 | 195.0 | |
| Oracle | 34.0 | 143.1 | 360.1 | |
| **CoreWeave** | **364.9** | **832.9** | **1,344.3** | **ACCESS-IMPAIRED (>1,000 bp)** |

Per the pre-registered mapping: the >1,000 bp observation records
**access-impaired** for the CoreWeave layer and a **Capital event (§5.3)** — not
K2. All other names: `unscreened` (variation test unmet on a single
observation). Tenor decomposition of the flag is the analyst's step.

## Pass B — variation window (days=180), mechanical extraction only

`data/results/pass_b_variation.json`. Headline rows (first → last, window):

- **CoreWeave 2031-12-20: 845.3 → 1,344.3 bp = +499.0 bp** (09-21 → 11-24);
  the 2031-06-20 tenor ran 585.0 → 810.9 (+225.9 bp, 07-06 → 09-18). **Both
  tenors moved ≥150 bp inside the window.** Note for the analyst: the active
  tenor rolls mid-September (06-20 series ends 09-18, 12-20 series begins
  09-21) — do not splice tenors naively.
- **Oracle 2031-12-20: 208.0 → 360.1 bp = +152.1 bp** — at the ≥150 bp
  threshold, on the boundary.
- Broadcom +84.3 bp; NVIDIA +61.8 bp; Meta, Alphabet, Amazon, Microsoft all
  below the threshold (full table in the JSON).

## What this run does not do

- **No K1/K2 classification is asserted here or implied by the data files.**
  The response test (new-commitment flows over ≥2 quarters) needs sources no
  CDS series contains; the pool-layer mapping (§5 of the pre-registration:
  hyperscalers and neoclouds screen separately) is the analyst's pass.
- Entity-resolution lookups (`/v1/cds/entities`, $0.06/call) were **not**
  purchased: every 404 resolved definitively from the error bodies alone, so
  the question never arose.
