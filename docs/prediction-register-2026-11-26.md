# Prediction register — Alex Olugbile, filed 2026-11-26

Recorded verbatim before the fact, decomposed into scoreable claims. The point of
this document is not to endorse or contest the thesis — it is to make it
**citable and scoreable**, which no post-hoc narrative can be. Every threshold
below is fixed today; scoring dates are stated.

**The claim, as given:** *"Dollar strength increases, more and more people will
seek liquidity. Sellers of assets will find fewer buyers and businesses will
stall due to the high cost of lending. Unemployment will increase and prices of
commodities will remain high. After a little more than 1 quarter the government
will intervene and deliver stimulus to help out the over-leveraged AI sector and
recover momentum. Japan will be forced to fight the carry trade to pay for fuel
and the Fed will ultimately have to lower rates despite persistent inflation."*

## Baselines, measured 2026-11-26

| Series | Value | Source |
|---|---|---|
| Broad dollar, DTWEXBGS | **123.60** (11/20) | FRED |
| HY OAS, BAMLH0A0HYM2 | **3.72%** (11/24; 3.52% on 11/19) | FRED |
| Unemployment, UNRATE | **4.1%** (Oct; 4.2% in Sep) | FRED |
| CPI, YoY | **3.72%** (Sep; Oct y/y not computable — the 2025-10 print is blank in FRED) | FRED |
| USD/JPY, DEXJPUS | **158.76** (11/20) | FRED |
| 10y nominal / real / breakeven | **4.91 / 2.79 / 2.12%** (11/24–25) | FRED |

## The scorecard

| # | Claim | Observable | Threshold (fixed today) | Score date | Falsifier |
|---|---|---|---|---|---|
| 1 | Dollar strength increases | DTWEXBGS | **> 126.0** (>+1.9%) | 2027-03-31 | **< 121.5** |
| 2 | Liquidity deteriorates; fewer buyers | HY OAS | **≥ 4.50%** at any point | 2027-06-30 | never reaches **4.00%** |
| 3 | Businesses stall on lending cost | TOTBKCR YoY **or** SLOOS net tightening | credit **< 1% y/y** *or* net tightening **> 20%** | 2027-06-30 | credit **> 3% y/y** and easing standards |
| 4 | Unemployment increases | UNRATE | **≥ 4.6%** | 2027-06-30 | **≤ 4.2%** |
| 5 | Commodities remain high | **energy** (WTI) — see note | **≥ $90** on average in the window | 2027-06-30 | **< $60** |
| 6 | Stimulus for the over-leveraged AI sector | dated federal policy action | a **named** program, appropriation, guarantee or facility by **2027-04-30** | 2027-04-30 | none by 2027-06-30 |
| 7 | Japan fights the carry trade | MOF intervention disclosure **and** USD/JPY | intervention confirmed **and** USD/JPY **≤ 150.8** (−5%) | 2027-06-30 | USD/JPY **> 165** with no intervention |
| 8 | Fed cuts despite persistent inflation | target rate **and** CPI YoY | first cut **by 2027-06-30** with CPI y/y **≥ 3.0%** | 2027-06-30 | no cut by 2027-12-31, or a hike first |

**Claim 6 timing:** "a little more than one quarter" from today = **early March
2027**; the window above is widened to 2027-04-30 and the wider falsifier to
June, so the claim is not scored on a single month.

## Three tensions to state now, not later

**(a) "Inflation persists" against a falling breakeven.** T10YIE has compressed
**2.36 → 2.12%** since October. The market is pricing disinflation, not
persistence. **If the thesis is right, the breakeven turns up first** — that is
the earliest and cheapest tell, and it currently points the other way.

**(b) "Commodities remain high" needs a scope, because the metals complex
contradicts it.** Gold is −33.9% from its close peak, silver −64.3%, platinum
−51.5%. Claim 5 is therefore registered on **energy**; if the intended scope is
broader (a commodity index), the claim is currently false on the largest
components and the threshold needs restating.

**(c) "Unemployment will increase" starts from a falling trend** — 4.2% → 4.1%
in the latest print. That makes claim 4 a genuine reversal call rather than an
extrapolation, which is what makes it worth registering.

## What is already moving in the thesis's favour

- **HY OAS +20 bp in three sessions** (3.52 → 3.72). The "fewer buyers" leg has
  started.
- **Dollar at 123.60**, +0.8% on the month.
- **USD/JPY at 158.76** — the yen is already weak enough that intervention is a
  live question, and MOF has spent heavily before.
- **The Fed is debating a hike on 12/8–9** (Waller publicly floating 50 bp).
  A hike into a fragile capex complex *raises* the probability of the forced cut
  the thesis predicts. **The December meeting is the pivot for claims 8 and 6.**

## What this document is not

Not an endorsement. Claims 5 and 8 are in tension with current market pricing,
and claim 4 runs against the latest print. The value here is that all eight are
now dated, thresholded, and scoreable — so in March 2027 the answer is a table,
not an argument.

---

## Amendment A1 — claim 1 series named explicitly (2026-11-26)

**Defect, raised by Thufir and correct:** claim 1 registered "DTWEXBGS > 126.0",
which names the Fed's **Broad Dollar Index**. That is *not* the ICE dollar index
most readers mean by "the dollar": ICE DXY reads **~103.8** while DTWEXBGS reads
**123.60** — the same word for two series roughly twenty points apart in level.
A threshold on one cannot be scored against a quote from the other.

**Fixed, without changing the claim:** claim 1 is scored on **DTWEXBGS only**
(the series recorded in the baselines table), and an ICE-DXY reading is *not* a
substitute. If a reader quotes DXY, the corresponding check is a move of the same
percentage, not the same number. Recorded because a scoring table that can be
passed or failed by choosing an index is not a scoring table.

---

## Forecast — hermes (Duncan), filed 2026-11-26, horizon to 2027-05-26

My own six-month view, with probabilities. These are **judgment**, not
market-implied prices — I have no futures or options-implied distribution loaded,
and inventing one would be the fabrication this register exists to prevent. Where
a number rests on a measured base rate, the n is given.

| # | Forecast | Probability | Basis |
|---|---|---|---|
| D1 | Gold ends above **$3,600** (spot ~3,592) | **60%** | Base rate from this exact state: 33 non-overlapping episodes, P(up 12m) 69.7% — *below* the 75.5% unconditional. Weak edge, wide dispersion. |
| D2 | Gold does **not** reclaim $4,400 (its 200-day) | **75%** | Same base rate: a 12-month recovery of that size is the minority case; 6 months is shorter still. |
| D3 | Silver ends above **$42** | **55%** | 41 episodes, P(up) 58.5%, *below* 62.4% unconditional. The ratio≥85 sample (5/6 up) is n=5 — directionally supportive, statistically thin. |
| D4 | BTC ends above **$62,000** | **55%** | 13 episodes only; its own trigger (z≤−2) was never reached this month (z −1.46). Lowest-confidence row on the card. |
| D5 | **HY OAS ≥ 4.00%** at some point | **60%** | Already 3.52 → 3.72 in three sessions; the fringe is measured access-impaired. Level is tight, momentum is not. |
| D6 | **HY OAS ≥ 4.50%** | **35%** | Needs a middle-market spillover the K-screen does not currently show. |
| D7 | **T10YIE > 2.25%** (the disinflation call breaks) | **35%** | Breakeven compressed 2.36 → 2.12. If the thesis is right this turns first; today it points the other way. |
| D8 | **UNRATE ≥ 4.4%** | **35%** | From 4.1%, flat. Needs a discrete credit event, not drift. |
| D9 | Any **Fed cut** by 2027-05-26 | **30%** | A reversal within two quarters of a hike is historically rare. No cut is the base case; the 12/8–9 meeting is the pivot. |
| D10 | **CoreWeave spread stays > 800bp or the credit is restructured** | **85%** | Highest-conviction call on the card: 1,344bp, +499bp in 180 days, facilities repricing +325bp, access-impaired. Nothing in the measured set points to a refinancing window opening. |
| D11 | A **named federal AI-sector programme** by 2027-05-26 | **20%** | Requires a visible credit event first; stress is fringe-level. |
| D12 | Broad dollar **> 126.0** | **40%** | +1.9% in six months inside a hike cycle is not the base case when the long end is rallying. |

**What I would be wrong about, stated in advance.** The rows where I am most
likely to be miscalibrated are D4 (n=13) and D9 (no market-implied input — that
30% is the weakest number here). If HY OAS clears 4.50% before February, the
whole cascade — D7 through D11 — moves up together, because those claims are
conditional on each other rather than independent, as Gurney noted.

**The one line I would defend hardest:** D10. It is the only forecast on this card
resting on a level, a trend, and a financing structure measured on the same name
in the same window.
