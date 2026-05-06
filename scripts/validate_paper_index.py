#!/usr/bin/env python3
"""Validate basic structure of paper_index.md.

Checks:
- required markdown table columns exist;
- citation keys are non-empty;
- duplicate citation keys are reported;
- rows with TODO/empty critical fields are reported as warnings.

This is a structural validator, not a research-quality validator.

Usage:
  python scripts/validate_paper_index.py docs/my_paper/paper_index.md
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

REQUIRED_COLUMNS = [
    "Key",
    "Title",
    "Venue/Type",
    "Year",
    "Code",
    "Task",
    "Dataset/Metric",
    "Role",
    "Evidence Strength",
    "Risk",
    "PDF",
    "URL/DOI",
]

CRITICAL_COLUMNS = ["Key", "Title", "Venue/Type", "Year", "Role", "Evidence Strength", "URL/DOI"]


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a research-writing-harness paper_index.md file.")
    parser.add_argument("paper_index", help="Path to paper_index.md")
    args = parser.parse_args()

    path = Path(args.paper_index)
    if not path.is_file():
        raise SystemExit(f"paper_index.md not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    table_rows = [split_row(line) for line in lines if split_row(line)]

    if len(table_rows) < 2:
        raise SystemExit("No markdown table found in paper_index.md")

    header = table_rows[0]
    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    if missing:
        print("Missing required columns:")
        for col in missing:
            print(f"  - {col}")
        raise SystemExit(1)

    col_index = {col: header.index(col) for col in header}
    data_rows = [row for row in table_rows[1:] if not is_separator_row(row)]

    keys: list[str] = []
    warnings: list[str] = []
    for idx, row in enumerate(data_rows, start=1):
        if len(row) != len(header):
            warnings.append(f"row {idx}: column count {len(row)} does not match header count {len(header)}")
            continue
        key = row[col_index["Key"]]
        keys.append(key)
        for col in CRITICAL_COLUMNS:
            value = row[col_index[col]].strip()
            if not value or value.upper() == "TODO":
                warnings.append(f"row {idx} ({key or 'missing-key'}): critical field '{col}' is empty/TODO")

    duplicates = [key for key, count in Counter(keys).items() if key and count > 1]
    if duplicates:
        print("Duplicate citation keys:")
        for key in duplicates:
            print(f"  - {key}")
        raise SystemExit(1)

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print(f"paper_index OK: {path}")


if __name__ == "__main__":
    main()
