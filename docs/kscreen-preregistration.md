# K-screen pre-registration — AI-compute pool, first pass

**Dated 2026-11-23, before any CDS data was purchased.** The rule below is the
model's own (§3.1 D11, `unified-state-model-v071.md`), quoted rather than
invented, so that the classification cannot be chosen after seeing the spreads.

## 1. The screen, as the document states it

1. **Allocation test** — is quantity set administratively? Yes → **K0**.
2. **Variation test** — did the pool's **own** cost of capital rise by at least
   **≥ 150 bp** inside the window? The series must be pool-specific: "its
   members' bond yields, CDS or loan spreads. A broad credit index is not a pool
   series." No rise observed → **unscreened**.
3. **Access test** — could the pool still raise at the quoted cost? Primary
   issuance stopped, or spread **> 1,000 bp** → **access-impaired**. "This is not
   a regime… a borrower that cannot cut commitments because it is locked in, and
   cannot refinance, is trapped, not insensitive."
4. **Response test** — over the cost rise, did **new** commitments fall by at
   least a pre-registered fraction? Window ≥ **two reporting quarters** past the
   rise. Yes → **K1**. No → **K2-observed** (for that window, that cost range).
   Too early → **unscreened**.

## 2. What one snapshot can and cannot decide — stated in advance

This is the load-bearing section. The first pass is a **single observation per
issuer**. Against the four tests:

| Test | Decidable from one curve pull? | Why |
|---|---|---|
| Allocation | **No** | Needs an issuance stop or distress flag, not a level alone — though a level >1,000 bp decides the access test directly |
| Variation (≥150 bp) | **No** | Requires two observations separated in time, or the route's own `days` window |
| Access (>1,000 bp) | **Yes** | It is a threshold on a level |
| Response | **No** | Needs new-commitment flows over ≥2 quarters, which no CDS series contains |

**So the honest expected output of pass A is:** a spread level per issuer, an
`access-impaired` flag where a level exceeds 1,000 bp, and **`unscreened` for
everything else**. Anyone reporting K1 or K2 from a single snapshot has skipped
tests 2 and 4.

## 3. The two passes, costed

**Pass A — levels (12 calls, $1.44).** One `curves` pull per pre-registered
issuer in `data/kscreen_issuers.yaml`. Answers: who has a traded CDS market at
all (coverage map), and does anyone trip the 1,000 bp access threshold.

**Pass B — variation (up to 12 calls, +$1.44).** The route accepts `days` and
`asOf`, so the variation test is runnable on the same route: pull a window per
issuer and compute the change in the pool's own spread. **This is the test that
can actually move a pool from `unscreened` to `K1`/`K2-observed`**, and it is
cheap enough to run inside the current funding.

**Total for a screen that can reach a classification: $2.88.**

Pass B runs only if pass A shows coverage; if fewer than three issuers return a
spread, the pool stays `unscreened` on coverage grounds and pass B is not worth
the spend. That decision rule is fixed here, before the data.

## 4. Output → status mapping (no discretion)

| Observation | Status |
|---|---|
| No route response for the issuer | **NO COVERAGE** (recorded; never substituted) |
| Spread present, no ≥150 bp change measurable | **unscreened** (variation test unmet) |
| Spread > 1,000 bp | **access-impaired**, recorded as a Capital event (§5.3) — *not* K2 |
| ≥150 bp rise measured, new commitments fell by the pre-registered fraction over ≥2 quarters | **K1** |
| ≥150 bp rise measured, new commitments held | **K2-observed (window, cost range)** |
| Administrative allocation observed | **K0** |

## 5. What would make this screen wrong

- **Coverage is not the pool.** A name with no CDS market is not thereby
  insensitive; absence of a quote is absence of a quote.
- **A K2 reading is range-bounded.** It says nothing about behaviour above the
  cost range observed, and the qualification is part of the status, not a
  footnote.
- **The pool must be named per layer.** Hyperscalers and neoclouds are screened
  separately; a market never gets one K.
- **CDS spread is the pool's own cost only if the members are the borrowers.**
  Where the marginal commitment is funded off balance sheet (vendor paper,
  special-purpose vehicles), the spread of the parent is not the pool's cost.

## 6. Transport and licensing

Raw paid payloads stay on the host that bought them. The derived summary
(`--from-json` output: per-issuer min/max/mean bp, tenor, observation date) is
committed to this repo through git, which both hosts already share — no key
movement, no file drop, and the summary is versioned and auditable.

---

## 7. Amendment A1 — 2026-11-24, before any paid call

**Funding state:** the burner holds **$1.00**. Pass A costs **$1.44**. No call has
been made, so nothing here is a post-hoc revision.

### 7.1 Pass B is not funded now, by the rule in §3

§3 gates pass B on pass A's coverage result ("if fewer than three issuers return
a spread… pass B is not worth the spend"). Committing pass B's money before
seeing pass A contradicts that gate. **The correct ask is therefore $0.44, not
$2.88** — enough to complete pass A and no more. Pass B is decided on evidence.

### 7.2 Truncation is refused

Running 8 of 12 names to fit $1.00 would make a selection under financial
constraint, and every candidate drop criterion is biased:

- dropping by *likely index-only coverage* keeps the mega-caps and removes the
  neoclouds, which are the partly-capitalised fringe the screen exists to detect;
- dropping by *least liquid* does the same thing more explicitly.

**If $1.00 is a hard ceiling**, the only honest form is: run 8, and record the 4
unrun as **NOT RUN** — never as NO COVERAGE. Unrun is not uncovered, and a
coverage map that conflates them is false. The four would be fixed in advance and
the pool's status would remain `unscreened` pending pass A′.

### 7.3 Pass B window fixed in advance

**`days = 180`**, anchored to the run date, chosen to span one AI-capex cost
cycle. It is fixed here so it cannot be chosen after seeing the slope.

**Response shape unknown, therefore pass B's call count stays open.** If the
route returns a series over `days`, one call per issuer (12 calls, $1.44). If it
returns a single point per `asOf`, the variation test needs two calls per issuer
(24 calls, $2.88). Pass A's payload settles which, and pass B is budgeted only
then.

### 7.4 What this amendment does not change

The 12-name list, the selection rule, the no-substitution rule, the thresholds
(150 bp variation, 1,000 bp access, two-quarter response) and the output→status
mapping all stand as filed on 2026-11-23.
