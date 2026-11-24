# K-screen classification — 2026-11-24 run

Applying `docs/kscreen-preregistration.md` (filed 2026-11-23, amended A1 2026-11-24)
to `data/results/{kscreen_pass_a,pass_b_variation}.json`.

Reproduce: `python3 scripts/classify_kscreen.py` (same directory, no network).

## Method

- Pools are the four role groups in `data/kscreen_issuers.yaml`, screened
  **separately** per D11 ("a market is never given one K").
- Variation is computed on **one tenor, 2031-12-20**, for every issuer. The
  2031-06-20 CoreWeave rows are excluded: splicing tenors across a benchmark
  roll would manufacture a change that is partly a different instrument.
- Pool variation is the **median member change**, not the max — one member
  repricing is not the pool's cost rising.

## Result: no pool reaches K1 or K2-observed

| Pool | Members on tape | Max level | Median change (180d) | Variation | Status |
|---|---|---|---|---|---|
| Hyperscaler-landlords | 5 of 5 | 360 bp (ORCL) | **+28.0 bp** | not met | `unscreened` |
| Silicon-systems | 2 of 2 | 195 bp (AVGO) | +73.0 bp | not met | `unscreened` |
| Neocloud | **1 of 4** | **1,344 bp (CRWV)** | +499.0 bp | met | **`access-impaired`** |
| Colocation REIT | 0 of 1 | — | no series | no series | `unscreened` |

## 1. The neocloud pool is access-impaired — trapped, not insensitive

CoreWeave's 5-year spread went **845.3 → 1,344.3 bp (+499 bp)** between 2026-09-21
and 2026-11-24, and it tripped the pre-registered 1,000 bp access threshold.

Per the mapping fixed on 2026-11-23, that is **`access-impaired`: recorded as a
§5.3 Capital event, not K2.** D11's own wording is the reason — *"a borrower that
cannot cut commitments because it is locked in, and cannot refinance, is
trapped, not insensitive."* A spread of 1,344 bp is not evidence that demand
ignores the cost of capital; it is evidence the borrower is losing access to it.

**And the honest limit:** one member is not a pool. The neocloud group is
screened on CoreWeave alone because the other three have no tape (below), so the
status is `access-impaired` *for the pool as observed*, not a statement that
every neocloud is locked out.

## 2. The coverage gap is the finding, and it is systematic

Three of the four fringe names have **no CDS market at all** — IREN, Applied
Digital, TeraWulf return "has no CDS on the tape". Digital Realty's reference
entity exists but has printed no 5-year level in **1,100 days**.

That is not a data inconvenience. **The CDS tape under-samples the layer where
stress appears first**, by construction: a pool that borrows privately — vendor
paper, project finance, private credit — has no single-name CDS to observe.
Using CDS as the K-screen input therefore builds in a bias toward pools that
already have public bond markets, which are the *most* transparent and
generally the *least* fragile members of the chain.

**Consequence for the model:** a K-screen run on CDS alone can never classify the
partly-capitalised fringe, which is precisely the pool §5.6 and §8 identify as
the coupling risk. The screen needs a non-CDS observable for that layer
(loan spreads, private-credit marks, or covenant terms from Gurney's item-5
panel) before it can answer the question it was built for.

## 3. Oracle is the outlier worth watching

Every hyperscaler moved ≤29 bp except **Oracle at +152.1 bp** (level 360 bp).
It cleared the 150 bp variation threshold individually while the pool median was
+28 bp.

Individually that is *not* a pool classification — the pool test is the median.
But it is the one landlord whose own cost of capital has materially repriced,
consistent with its debt-financed data-centre buildout being read differently
from the other five. Worth a named watch item rather than a footnote.

## 4. What this run does not say

- **No K1, no K2, anywhere.** The response test (D11 test 4) needs *new*
  commitments dated after the cost rise over ≥2 quarters. No CDS series contains
  that, and RPO/backlog are explicitly inadmissible ("stocks of past commitments
  are not evidence either way"). CoreWeave's +499 bp landed alongside a $132.3B
  RPO — the co-movement is recorded as a hypothesis for the successor, **not** as
  evidence of insensitivity.
- **No claim about the AI-compute layer as a whole.** Four pools, none
  classified; the layer's K is still open.
- **No trend claim from two dates.** 180 days, one comparison per issuer.

## 5. What would finish the screen

1. **Commitment flows** — the admissible input for test 4, from item 5's EDGAR
   panel (new issuance, newly signed capacity, capex guidance dated after the
   rise). This is the binding gap, not more CDS calls.
2. **A non-CDS observable for the fringe** — loan/private-credit spreads for
   IREN, Applied Digital, TeraWulf. Without it the neocloud pool is screened on
   one name forever.
3. **A second variation window** — one more 180-day comparison, to check that a
   single 45-day sample is not the whole story.
