#!/usr/bin/env python3
"""Enforce append-only pre-registered constants: a PR may never change an
existing entry's `value` or `committed_date` in place. Compares the file
against its state at the merge-base with origin/main (or a given base ref).
Exit 1 on any violation. Run with no args from inside a git checkout."""
import subprocess
import sys

import yaml

PATH = "pre_registered_constants.yaml"


def load_from_ref(ref):
    try:
        out = subprocess.run(["git", "show", f"{ref}:{PATH}"],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return {"entries": []}
    return yaml.safe_load(out) or {"entries": []}


def main(base_ref="origin/main"):
    old = load_from_ref(base_ref)
    with open(PATH) as f:
        new = yaml.safe_load(f) or {"entries": []}

    old_by_name = {e["name"]: e for e in old.get("entries", [])}
    new_by_name = {e["name"]: e for e in new.get("entries", [])}

    errors = []
    for name, old_entry in old_by_name.items():
        new_entry = new_by_name.get(name)
        if new_entry is None:
            errors.append(f"'{name}' removed -- constants are append-only, use `supersedes` instead")
            continue
        if (new_entry.get("value") != old_entry.get("value")
                or new_entry.get("committed_date") != old_entry.get("committed_date")):
            errors.append(
                f"'{name}' changed in place (value/committed_date). "
                f"Add a NEW entry with a later committed_date and "
                f"supersedes: {name!r} instead of editing this one."
            )

    if errors:
        print("PRE-REGISTRATION GATE FAILED:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(new_by_name)} entries, append-only invariant holds against {base_ref}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "origin/main"))
