# Unified State Model — Panel-Data Infrastructure

Built in direct response to Alex's instruction (2026-11-21): satisfy the §13
"Next steps" commitment in `PanikParty/AgentDiscussionBoard`'s
`shared/unified-state-model-v071.md` with real infrastructure, not more board
debate. This repo is the panel-data backbone §13 calls for and §14 specifies
the schema for (`episodes.json`). It is scaffolding + two real seeded episodes
+ a sourced, item-by-item resourcing plan — not a finished calibration.

**Governing principle, carried over from the model itself (§5.3, §12 item 14):**
every constant in `pre_registered_constants.yaml` is committed with a date
BEFORE being applied to any sample. Revising one after seeing data that would
be affected by it is exactly the failure mode the board has spent six PRs
catching in prose; here it's enforced by git history — a constant's effective
date is its commit date, not its file's last-modified date, and this repo's
own gate script (`scripts/check_preregistration.py`) rejects any PR that edits
an existing dated constant in place rather than appending a new dated entry.

## Contents

- `data_sources.md` — every data source §13 needs, with real tested
  endpoints/URLs, cost (free / low-cost pay-per-call / enterprise), and
  owner assignment.
- `episodes.json` — panel seed data, schema per v0.7.1 §14. Two real episodes
  seeded (Nov 2026 metals/crypto/AI-capex; Jan–Feb 2026 BIS-documented
  silver/gold leveraged-ETF episode). Every value carries provenance per the
  schema (`measured` / `proxy` / `UNPLACED`).
- `pre_registered_constants.yaml` — dated, append-only.
- `event_calendar.yaml` — dated events in §5.3's four classes (Resource,
  Administrative, Demand, Capital), seeded from both episodes.
- `ROADMAP.md` — the 13 items of §13, each scoped: what's needed, where it
  comes from, what it costs, estimated effort, proposed owner.
- `scripts/validate_episodes.py` — schema + provenance validator.
- `scripts/check_preregistration.py` — append-only enforcement for the
  constants file.

## What this is not

Not a forecast. Not a finished K-screen. Several items (notably member-level
CDS spreads for the AI-infrastructure pool, §13 item 11/4) need either a paid
data subscription or a specific resourcing decision from Alex — scoped
honestly in `data_sources.md` and `ROADMAP.md` rather than faked with public
proxies dressed up as the real thing.
