#!/usr/bin/env python3
"""Ensure local development/TDD artifacts stay under tmp/."""
from __future__ import annotations

import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEV_ARTIFACT_PATTERNS = [
    "quick_validate_skill.py",
    "check_*.py",
    "*_contract*.py",
    "*_pressure_scenarios.md",
    "*_iteration_notes.md",
    "test_*.py",
]


def is_under_tmp(path: Path) -> bool:
    return path.relative_to(ROOT).parts[:1] == ("tmp",)


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.is_dir() or is_under_tmp(path):
            continue
        name = path.name
        if any(fnmatch.fnmatch(name, pattern) for pattern in DEV_ARTIFACT_PATTERNS):
            errors.append(f"Development/TDD artifact outside tmp/: {path.relative_to(ROOT)}")

    if errors:
        print("Development artifact contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Development artifact contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
