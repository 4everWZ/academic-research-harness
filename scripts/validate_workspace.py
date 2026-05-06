#!/usr/bin/env python3
"""Validate the flat research-writing-harness workspace structure.

This script checks required files/directories only. It does not judge research quality.

Usage:
  python scripts/validate_workspace.py docs/my_paper
"""

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate required files for a paper workspace.")
    parser.add_argument("workspace", help="Path to docs/<paper_slug>")
    args = parser.parse_args()

    root = Path(args.workspace)
    if not root.exists():
        raise SystemExit(f"Workspace does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Workspace is not a directory: {root}")

    missing_files = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    missing_dirs = [name for name in REQUIRED_DIRS if not (root / name).is_dir()]

    if missing_files or missing_dirs:
        if missing_files:
            print("Missing files:")
            for name in missing_files:
                print(f"  - {name}")
        if missing_dirs:
            print("Missing directories:")
            for name in missing_dirs:
                print(f"  - {name}/")
        raise SystemExit(1)

    print(f"Workspace OK: {root}")


if __name__ == "__main__":
    main()
