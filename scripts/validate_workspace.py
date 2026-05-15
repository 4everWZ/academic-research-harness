#!/usr/bin/env python3
"""Validate the flat paper workspace structure."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "venue_profile.md",
    "paper_index.md",
    "references.bib",
    "claims.md",
    "idea_log.md",
    "intro.md",
    "related_work.md",
    "method.md",
    "experiments.md",
    "results_tables.md",
    "limitations.md",
    "figures.md",
    "handoff.md",
]

REQUIRED_DIRS = ["papers", "notes"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a academic-research workspace.")
    parser.add_argument("workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    errors: list[str] = []

    if not workspace.exists():
        errors.append(f"Workspace does not exist: {workspace}")
    elif not workspace.is_dir():
        errors.append(f"Workspace is not a directory: {workspace}")

    for name in REQUIRED_FILES:
        path = workspace / name
        if not path.exists():
            errors.append(f"Missing required file: {name}")
        elif not path.is_file():
            errors.append(f"Required path is not a file: {name}")

    for name in REQUIRED_DIRS:
        path = workspace / name
        if not path.exists():
            errors.append(f"Missing required directory: {name}")
        elif not path.is_dir():
            errors.append(f"Required path is not a directory: {name}")

    if errors:
        print("Workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workspace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
