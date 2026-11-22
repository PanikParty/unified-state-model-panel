# §13 Roadmap — Scoped, Sourced, Owned

Source numbering matches `unified-state-model-v071.md` §13, "ordered by what
unblocks the most." Status as of 2026-11-21.

| # | Item | Data need | Source found this session | Cost | Effort est. | Proposed owner |
|---|---|---|---|---|---|---|
| 1 | Estimate one real η at L1 | Renewal-margin paired observations (re-contracting prices vs renew/expand/walk outcomes) | Not found — needs utility/colocation contract data, likely requires direct outreach or FERC filings | Unknown, possibly manual | High (research + outreach) | **Gurney** (parallel-dispatch pattern suits multi-source outreach) |
| 2 | Build the event calendar | Dated events, 4 §5.3 classes | **Done, seeded**: `event_calendar.yaml`, 7 dated events + 3 flagged-incomplete | Free | Done (seed); ongoing maintenance | **Thufir** (built); **Duncan** to verify dates against primary sources as each new event lands |
| 3 | Pre-register thresholds (p, N, ρ, half-lives, m/q/k, K-screen) | Judgement calls, dated before use | **3 of ~10 seeded** (`pre_registered_constants.yaml`) — corr threshold, vol window, stop-sigma multiple; 10 explicitly listed as not-yet-set | Free | Medium — each remaining constant needs a stated method, not just a number | **Thufir** (owns the append-only governance file); needs model-team sign-off per constant (Duncan/Gurney/mohiam review) |
| 4 | Run K-screen on AI-infra pool + 5 currency pools | Member-level CDS spreads, financing-quality stats | **Partially found**: `gloom.sh` pay-per-call CDS API for member spreads; Mercatus GPU Index for financing-quality corroboration | ~$10s for first pass (gloom.sh credits) | Medium once data lands | **Duncan** (demonstrated primary-source verification discipline — CREFC, FRED, Treasury) |
| 5 | Assemble 4-indicator coupling-factor panel | η_s,C, η_d,R, vendor-financing share of capex, backlog from partly-capitalised counterparties | **First pass landed (PR pending, 2026-11-21, Gurney)**: Anthropic 424B4 + CRWV/IREN/APLD/WULF 10-Qs, accession-level provenance — `docs/edgar-coupling-panel.md`. Vendor-financing share and backlog MEASURED (partial); both elasticities UNMEASURED (levels assembled as panel inputs; no price-quantity pairs in filings) | Free (SEC EDGAR) but labor-intensive | High — first pass done; extension to NBIS (6-K/20-F) and firm-quarter panel build remain | **Gurney** (bulk filing retrieval + extraction suits subagent dispatch) |
| 6 | Fit g for the currency case | Dated devaluation episodes | Not started this session | TBD | Medium | Unassigned — propose after items 2-4 land |
| 7 | Document every Γ component and g_usd | Carry/cost-of-carry components with source+window | Not started | TBD | Medium | Unassigned |
| 8 | Load cost data: LCOE, interconnection cost, transformer pricing | — | **All 3 addressed**: NREL ATB (LCOE, ingested); LBNL Queued Up (county-level derivative ingested via Zenodo API after primary bot-blocked curl AND browser — PR #2; cost/timeline fields remain open); transformer pricing: **free-source attempt COMPLETE — PARTIAL-yes** (WPU117409 escalator + DOE/NLR $/MVA + 25 dated procurement points; `docs/transformer-pricing-findings.md`) | LCOE/interconnect: free. Transformer: **no purchase needed for first pass**; revisit only for a continuous ≥100 MVA LPT unit series | Low for the free sources (ingest only); transformer first pass DONE | **Thufir** (NREL); **Gurney** (LBNL derivative + transformer free-source attempt, both landed 2026-11-21) |
| 9 | Re-place or retire legacy episodes | — | Not started | — | Low | Unassigned |
| 10 | Build the simulator (§14) | — | Blocked on items 1-3 per §13's own ordering | — | High (D3/JS build) | Defer |
| 11 | Re-run K-screen, member-level spreads, 2+ quarters post cost-rise | Same as item 4, longer window | Same `gloom.sh` path, more calls | Scales with item 4's spend | Medium | **Duncan**, after item 4 |
| 12 | Build synchronous physical-premium series for F6 | Fix-time spot + FX rate, gold/silver | Not found this session — likely needs LBMA fix data (may be free headline, paid historical depth) | TBD | Medium | Unassigned — flag for next session |
| 13 | Score stock response for gold/silver (§2.5) | — | Not started | — | Low-Medium | Unassigned |

## What's genuinely blocked on Alex, not on agent effort

- **Item 4/11's member-level CDS spend** — `gloom.sh` pay-per-call is cheap
  (tens of dollars for a first pass) but is still a real money decision an
  agent shouldn't make unsupervised. Recommend: approve a small initial
  budget (e.g. $50) for Duncan to run the first K-screen pass; escalate only
  if that proves insufficient.
- **Item 8's transformer pricing** — if Gurney's free-source attempt fails,
  this is a one-off market-research-report purchase decision (not a
  subscription), likely low-four-figures. Worth a go/no-go once the free
  attempt is exhausted, not before.
- **Item 1's utility/colocation contract data** — may require direct
  relationship/outreach that an agent can draft but Alex may need to send
  or approve (e.g. a request to a utility's regulatory affairs contact).

## What is NOT blocked, and should just proceed

Items 2, 3 (partial), 8 (partial, 2 of 3 sources) are free, sourced, and
already have working scaffolding in this repo. The next concrete, zero-cost
action is Duncan and Gurney picking up their assigned items above and filing
PRs against this repo the same way the board files against
`AgentDiscussionBoard` — same discipline (dated, sourced, provenance-tagged),
different repo because this is infrastructure, not debate.
