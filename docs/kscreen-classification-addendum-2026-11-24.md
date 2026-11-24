# Addendum to the K-screen classification — the fringe's second instrument

**2026-11-24.** Amends `docs/kscreen-classification-2026-11-24.md` using
`docs/fringe-financing-terms.md` (Gurney, same day). The pool statuses **do not
change**; what changes is the strength of one leg and the honesty of one claim.

## 1. The fringe variation now rests on two instruments, not one

`kscreen-classification-2026-11-24.md` §2 recorded the structural problem: three
of four fringe names have no CDS market, so the variation test had a single
member on a single instrument.

Facility pricing closes that gap. CoreWeave's own secured borrowing — same
borrower, same facility family, one quarter apart:

| Facility | Dated | Margin | Change |
|---|---|---|---|
| DDTL 4.0 | Mar 2026 | SOFR + 2.25% | — |
| DDTL 5.0 | May 2026 | SOFR + 4.50% | **+225 bp** |
| DDTL 5.5 | Aug 2026 | Term SOFR + 5.50% | **+100 bp** |
| **Total, Mar → Aug** | | | **+325 bp** |

D11's test 2 admits "its members' bond yields, CDS **or loan spreads**". This is
a loan-spread series for the same borrower, and it clears the pre-registered
≥150 bp threshold **on its own instrument** — no cross-instrument comparison
required. The neocloud pool's `access-impaired` status is unchanged (CDS at
1,344 bp still trips the 1,000 bp access test); the variation leg is now
corroborated rather than single-sourced.

**What is still one member.** IREN has a facility but a single dated point
(1.0 at SOFR + 2.25%); APLD shows no new debt pricing (customer equity); WULF's
notes are dated October 2025, before any window. So the pool remains observed on
one name for variation, now on two instruments.

## 2. Correction: "facilities lead CDS" is not established

The natural reading of the two series — facilities repricing +325 bp by August,
CDS +499 bp by November — is that facility pricing *leads*, which would make it
an early-warning indicator. **That claim is not testable with these windows.**

- The facility march runs **March → August**.
- The CDS variation window runs **2026-09-21 → 2026-11-24**, i.e. it **begins
  after the facility march ended**.

Two series that do not overlap cannot order each other. What is established is
**directional consistency across the same half-year** — both instruments repriced
the same borrower's cost of capital sharply upward — and that is a weaker claim
than leadership. Testing precedence needs a CDS window covering March–August,
which is a pass-B extension, not a re-reading of what is on disk.

Recording it because "leads" is the kind of sentence that becomes a premise three
documents later.

## 3. My own pre-registration has a gap, and it blocks test 4 — not the data

D11's response test asks whether new commitments fell "by at least a
**pre-registered fraction**". **No fraction was ever registered.** It is not in
`kscreen-preregistration.md`; I wrote §2 as though the test were data-blocked,
and that was incomplete.

Consequence: even when Q4-2026 commitments arrive in early 2027, the test is
**inapplicable as filed** — there is no threshold to apply, and setting one after
seeing the flow would be the exact error the pre-registration exists to prevent.
Fixed prospectively in **amendment A2** (filed with this addendum, before any
post-rise commitment data exists).

## 4. Status table, unchanged except for the reason

| Pool | Status | Why |
|---|---|---|
| Hyperscaler-landlords | `unscreened` | variation not met at pool level (median +28 bp) |
| Silicon-systems | `unscreened` | variation not met (median +73 bp) |
| Neocloud | **`access-impaired`** | CDS 1,344 bp > 1,000 bp threshold; variation now corroborated on two instruments |
| Colocation REIT | `unscreened` | no series (dormant 1,100 days) |

**No K1, no K2, anywhere.** The response test is now known to be blocked twice —
on data (Q4 filings) and on definition (the missing fraction).
