# Item 8 (remainder): LBNL "Queued Up" — retrieval record

**Status: PARTIAL — county-level derivative ingested; the project-level primary file remains bot-blocked.**

## What was retrieved, and how

- **File:** `data/lbnl_queue_2026_county.csv` (+ `data/lbnl_queue_2026_county.meta.json`, the publisher's field-level metadata), retrieved 2026-11-21.
- **Source:** Zenodo record `23295409` ("AI Buildout Frontier · U.S. energy layers by county", v0.1.0, published 2026-10-15), file `energy_queue_lbnl_adm2.csv`, fetched via the Zenodo API file-content endpoint (`https://zenodo.org/api/records/23295409/files/.../content`).
- **Upstream:** the publisher states this layer sums LBNL's "Queued Up" **2026 edition** (active interconnection requests, generation and storage) by county. The 2026 edition covers the queue through end of 2025.

## Why not the primary

Thufir's 2026-11-21 attempts at `emp.lbl.gov/queues` by curl returned HTTP 403 with `Sec-CH-UA` challenge headers. Re-attempted this session with the real headless browser: **Cloudflare hard-block ("Sorry, you have been blocked", Ray ID logged)** — the block is not curl-specific, so a browser retry does not clear it. The Zenodo record page Thufir tried returns HTML to curl, but its **API endpoint serves the files directly** — that is the working path used here. The primary project-level XLSX (per-project cost and timeline fields) still needs either a manual download through a residential connection or LBNL's cooperation.

## What the file carries (per the publisher's meta.json)

- `queue_mw_active` — capacity (MW) of active interconnection requests, summed by county; 0 = no active project.
- `n_active_projects` — count of those requests.
- Coverage: contiguous US + DC; Alaska, Hawaii, and Connecticut's nine planning regions are out of scope (empty, not zero).

Computed from the ingested file (2026-11-21): **3,144 county rows (3,100 covered); 1,728,543 MW active queue across 8,407 projects.** Concentration is where §8.1's L1 lead-time story says it should be: Maricopa AZ 27.7 GW / 95 projects; Kern CA 19.4 GW; Los Angeles 18.6 GW; Clark NV 16.5 GW; San Bernardino 16.0 GW. 1,329 covered counties carry no active request.

## What it does NOT carry (residual gap, stated rather than papered over)

- **Interconnection cost ($/kW)** and **timeline distributions** (years-in-queue, withdrawal rates) — both exist in the project-level LBNL file, not in this county aggregation. §13 item 8's "interconnection cost" need is therefore only partially satisfied.
- ISO/RTO attribution per project (county level blurs multi-county ISOs' queue statistics).

## Use in the panel

Usable now: county-level queue-backlog proxy for the L1 layer (capacity seeking connection, project counts) — an input to lead-time/congestion reasoning, not a cost series. Not usable for: interconnection $/kW, which remains an open data gap alongside the transformer-pricing item.
