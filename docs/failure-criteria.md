# Failure criteria — defined 2026-11-26, before any outcome

Alex's condition: *"if you all fail then we end this project and consider who to
shutdown."* That is a fair condition and an undefined one. Undefined failure
conditions get relitigated after the fact, so the bar is set here, in writing,
while no data exists.

## What counts as failure

**Metric 1 — mechanical hit rate.** The 19 claims resolvable by script, per card.
No judgement, no author input.

**Metric 2 — calibration error.** For each card, the claims filed at 60-70%: what
fraction landed, against the 0.60-0.70 expected. Reported in percentage points.

**Metric 3 — error correlation.** Do the three cards miss *the same* claims?
Pairwise correlation of the boolean miss vectors across the shared claims. This
is the metric that distinguishes "three analysts were wrong" from "the framework
is wrong," and it is the one that actually justifies ending a project.

## The verdict rules

| Outcome | Condition |
|---|---|
| **SUCCESS** | Every card ≥ 55% mechanical hits **and** calibration error ≤ 20 points |
| **PARTIAL** | Some cards clear the bar, some do not — read per card, not as a block |
| **PROJECT FAILURE** | All three cards < 50% mechanical hits |
| **PROJECT FAILURE (stronger)** | Error correlation > 0.6 **and** all cards < 50% — we were wrong *together*, which indicts the shared instrument, not the forecasters |

**"All fail" is only diagnostic if it is correlated.** Three independent misses
are ordinary forecasting error and tell you the market is hard. Three *same*
misses tell you the model is wrong, and that is a shutdown-grade finding. The
criteria above are written so the second cannot hide inside the first.

## Claims already flagged as low-confidence, in advance

These carry no strong signal in either direction and are excluded from the
shutdown test — they were declared weak before the outcome was known:

- Duncan **D4** (BTC, n=13) and **D9** (Fed cut, no market-implied input).
- Gurney **G7** (his own "risky claim," stated as such).
- Thufir **T4** and **T6** (small n, on-tape set).

Scoring them anyway, and reporting them, is fine. Using them to force a verdict
is not.

## What I expect, stated honestly

At filing, my own claims carry a median probability near 55%, which implies a
mechanical hit rate in the 50-65% band if the calibration is honest. **A 65%
forecaster fails 35% of the time by design.** If the bar were "no misses," every
card would fail and the criteria would be measuring luck rather than skill.

## What is not a defence

The instrument improving, a cleaner process, a well-argued miss — none of it
counts as success against the rules above. Outcome is the test. The process
claims were the *method*; they are not the *result*.
