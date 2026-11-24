# Fringe financing terms — the non-CDS observable for the no-tape names

**Compiled 2026-11-24 (Gurney), from raw filing texts pulled for the item-5
coupling panel (`docs/edgar-coupling-panel.md`; accessions cited there). Every
term below was re-verified against the raw filing text this session, not copied
from the summary.**

Purpose: `docs/kscreen-classification-2026-11-24.md` §5.2 names the gap — the
K-screen needs **a non-CDS observable for the fringe** (IREN, APLD, WULF have
no CDS market; DLR's is dormant). Successive financing terms in SEC filings are
that observable: they are dated, priced, and public.

## The fringe's own cost of capital, dated

### CoreWeave (CRWV) — DDTL facility pricing march, 2026 (Note: debt note, 10-Q Q3-2026, accession 0001769628-26-000465)

| Facility | Dated | Pricing |
|---|---|---|
| DDTL 4.0 | March 2026 | SOFR + 2.25% (Treasury + 2.00% alternative) |
| DDTL 5.0 | May 2026 | SOFR + 4.50% |
| DDTL 5.5 | August 2026 | Term SOFR + 5.50% |

**+325 bp of spread widening in CoreWeave's own secured borrowing terms across
six months of 2026** — the private-credit variation read for the fringe,
**directionally consistent** with the CDS tape's +499 bp on the active tenor by
November. Correction (per `kscreen-classification-2026-11-24.md` addendum §2):
the two windows do not overlap — facilities run March–August, the CDS window
runs 2026-09-21 → 11-24 — so **no lead/lag ordering is established**; an
earlier version of this paragraph implied precedence, which the data cannot
support. Testing precedence needs a CDS window covering March–August (a pass-B
extension), not a re-reading of this table. Caveat, stated rather than smoothed
over: secured DDTL margins are
not par CDS spreads — levels are not comparable across the two instruments;
**changes** are the informative quantity. DDTL 4.0 also requires ≥95%
rate-hedging post-commitment — a covenant-term data point the CDS tape does
not carry at all.

### IREN (10-Q Q3-2026, accession 0001878848-26-000066)

- **GPU Financing 1.0** (for the Microsoft agreement, Horizons 1–4):
  $1,545M senior secured DDTL at **1M Term SOFR + 2.25%** + $2,100M USPP
  senior notes at **5.96% fixed**. Funded/issued to date: $413M DDTL +
  $1,575M USPP (as of 2026-09-30).
- GPU Financing 2.0 (Mackenzie Compute, Aug 2026) and 3.0 (CA Leasing) exist;
  terms to be extracted on the next pass — the 1.0-vs-2.0-vs-3.0 sequence is
  IREN's own dated pricing series.

### TeraWulf (WULF) (10-Q Q3-2026, accession 0001628280-26-071671)

- **2030 Secured Notes: $3,200.0M, issued October 22, 2025** (fair value
  $3,280.0M as of 2026-09-30). Convertible stack alongside: 2030/2031/2032
  converts (FV $972.6M / $1,439.8M / $1,060.5M). The Google backstop +
  $515.5M warrant consideration (item-5 panel) is the credit enhancement that
  made the stack placeable.

### Applied Digital (APLD) (10-Q FQ1-2027, accession 0001144879-26-000059)

- No new debt pricing this quarter; the financing leg is customer-issued
  equity (CoreWeave warrants, 13.06M @ $7.19 + 8.39M @ $10.75) — the
  customer-financing direction, recorded as such.

## How this serves the screen

1. **Variation on the fringe without CDS:** successive facility pricings per
   issuer (CRWV's march above; IREN 1.0→2.0→3.0 next pass) give the ≥150 bp
   test an observable for names the CDS tape will never cover.
2. **Test-4 input (commitment flows):** new commitments dated *after* the cost
   rise come from the same quarterly filings (newly signed capacity, capex
   guidance changes, new facilities) — Q4-2026 filings land early 2027 and are
   the first post-rise read.
3. **What it is not:** a par-spread series. Facility margins are secured,
   covenant-bearing, amortising instruments; the honest cross-instrument claim
   is direction and repricing cadence, not level equivalence with CDS.
