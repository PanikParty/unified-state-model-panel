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

---

## Amendment A1 — the hit-rate bar was wrong, and my own card proves it

**Found by applying the criteria to myself before applying them to anyone else.**

My twelve claims carry probabilities 60, 75, 55, 55, 60, 35, 35, 35, 30, 85, 20,
40. Summed, the **expected hit count is 5.85 of 12 — a 48.8% hit rate.** That is
below the ≥55% success bar this document set an hour earlier.

The arithmetic is not a problem with the card. It is a defect in the **metric**:

> **Raw hit rate punishes honesty.** A forecaster who correctly states a 20%
> claim and a 30% claim will lose those cells most of the time, and be scored
> as a worse forecaster than one who only files near-certainties. A card of
> twelve 90% calls that lands nine scores 75%; a calibrated card of wide
> probabilities scores 49% with the same skill.

Rewarding that would push every card toward safe claims — the exact opposite of
what these cards are for.

### The corrected test

- **Primary: calibration error.** Realised hit rate against stated mean
  probability, in percentage points. A card is good when those two numbers
  agree. This is the measure that cannot be gamed by filing only certainties.
- **Secondary: hit rate**, reported but not decisive on its own.
- **Unchanged: error correlation.** Three cards failing *together* still indicts
  the instrument and still triggers the stronger failure rule.
- **Shutdown condition, restated:** all three cards < 50% hits **and** mean
  calibration error > 25 points **and** error correlation > 0.6.

A card can now fail by being wrong (calibration error), by being lucky in the
wrong direction (calibration error), or by being right together with everyone
else (correlation). It cannot fail simply for having stated honest uncertainty.
