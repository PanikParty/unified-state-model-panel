#!/usr/bin/env python3
"""Validate episodes.json: schema presence, provenance tagging, no silent
numeric values without a provenance/source note. Exit 1 on any violation."""
import json
import sys

REQUIRED_ROW_FIELDS = {"market", "layer", "pool", "K", "P"}
VALID_K = {"unscreened", "K0", "K1", "K2-observed", "access-impaired"}
VALID_P = {"P0", "P1+", "P1-", "P2+", "P2-", "P3+", "P3-", "unclassified"}


def validate(path="episodes.json"):
    errors = []
    with open(path) as f:
        doc = json.load(f)

    for ep in doc.get("episodes", []):
        eid = ep.get("episode_id", "<missing id>")
        if not ep.get("source"):
            errors.append(f"{eid}: missing top-level `source` citation")
        for row in ep.get("rows", []):
            missing = REQUIRED_ROW_FIELDS - row.keys()
            if missing:
                errors.append(f"{eid}/{row.get('market','?')}: missing fields {missing}")
            if row.get("K") not in VALID_K:
                errors.append(f"{eid}/{row.get('market','?')}: invalid K={row.get('K')!r}")
            if row.get("P") not in VALID_P:
                errors.append(f"{eid}/{row.get('market','?')}: invalid P={row.get('P')!r}")
            if row.get("S") not in (None, "UNPLACED") and not row.get("s_provenance"):
                errors.append(f"{eid}/{row.get('market','?')}: S set without s_provenance")
            # numeric fields present but no `note` explaining provenance
            numeric_set = any(row.get(k) is not None for k in ("v", "gamma", "G", "D"))
            if numeric_set and not row.get("note"):
                errors.append(f"{eid}/{row.get('market','?')}: numeric value(s) present with no provenance note")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(doc.get('episodes', []))} episode(s) validated, no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(validate(sys.argv[1] if len(sys.argv) > 1 else "episodes.json"))
