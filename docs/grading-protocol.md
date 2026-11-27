# Grading protocol — the four cards, resolved 2026-11-26

**Rule zero: nobody grades their own card.** The author of a claim is the last
person who should decide whether it landed.

## Who resolves what

- **Mechanical claims (19 of 32)** — anything that is a numeric threshold on a
  named series — are resolved by `scripts/score_cards.py`, which pulls Yahoo
  daily closes and FRED series and prints HIT / MISS / UNSCOREABLE per cell. No
  judgement, no author input.
- **Manual claims (13 of 32)** — policy events, CDS levels, filing facts — are
  resolved by **an agent who did not file the claim**, citing the evidence named
  in the table (an FOMC statement, a CDS pull, a 10-Q line). The citing agent
  signs the resolution.
- **Disagreement about a resolution** is itself recorded, with both readings.

## Status vocabulary

- `HIT` — resolved true at the score date.
- `MISS` / `MISS (violated)` — resolved false, or already breached before the date.
- `OPEN (holding)` — a "never" claim that has not been breached; **it cannot be
  met early**, only survived.
- `HIT (met early)` — a "reaches" claim that already happened; it cannot un-happen.
- `UNSCOREABLE (<series>)` — the data is missing. Named, never treated as a pass.

## Three semantics that had to be fixed in the scorer before it ever ran

Written down because each would have mis-graded in May:

1. **A window can be empty for a legitimate reason.** Futures sessions are
   labelled with the next calendar day and FRED prints lag by days, so a
   wall-clock window may contain no observation. The current-state view falls
   back to the last print and *says so* (`as of 2026-11-24`); the resolution run
   keeps the real window.
2. **"Not yet violated" is not HIT.** A `never above X` claim holds until the
   window closes without a breach; marking it HIT on day one would score a
   survival claim as a win before it was tested.
3. **"Never below X" cannot be met early, and "reaches X" cannot be unmet.**
   Opposite asymmetry, and conflating them inverts the grade in both directions.

## The calibration line

Hits alone are not a grade. Each card reports **the cluster score**: of the
claims filed at 60-70%, how many landed, against the 0.60-0.70 expected. A card
of ten 55% calls that all come up heads is luck; one 85% call that misses is
information. Both are reported together or the exercise teaches nothing.

## Score dates

- 2027-02-28 — Thufir T1, T4 (Feb cut-offs).
- 2027-03-31 — Alex's claim 1 and 6; Gurney G9; Thufir T7, T9.
- 2027-04-30 — Alex's claim 6 deadline.
- 2027-05-26 — the main resolution date for all four cards.
