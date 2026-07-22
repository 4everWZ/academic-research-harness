#!/usr/bin/env python3
"""Validate the compact paper index schema and persistent identities."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


EXPECTED_COLUMNS = [
    "Key",
    "Title",
    "Year",
    "Formal source/status",
    "Role",
    "Claim/use",
    "Quality basis",
    "Code/data",
    "URL/DOI",
]


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate paper_index.md")
    parser.add_argument("paper_index")
    args = parser.parse_args()

    path = Path(args.paper_index)
    if not path.is_file():
        print(f"paper index not found: {path}")
        return 1

    table = [
        (number, line)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if line.strip().startswith("|")
    ]
    if len(table) < 2:
        print("paper index validation failed: no Markdown table found")
        return 1
    if split_row(table[0][1]) != EXPECTED_COLUMNS:
        print("paper index validation failed: unexpected header")
        return 1

    errors: list[str] = []
    keys: set[str] = set()
    for line_number, line in table[2:]:
        cells = split_row(line)
        if len(cells) != len(EXPECTED_COLUMNS):
            errors.append(f"line {line_number}: expected {len(EXPECTED_COLUMNS)} cells, got {len(cells)}")
            continue
        row = dict(zip(EXPECTED_COLUMNS, cells))
        key = row["Key"]
        if key == "TODO":
            continue
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key):
            errors.append(f"line {line_number}: invalid citation key: {key}")
        elif key in keys:
            errors.append(f"line {line_number}: duplicate citation key: {key}")
        keys.add(key)
        if not re.fullmatch(r"\d{4}", row["Year"]):
            errors.append(f"line {line_number}: invalid year: {row['Year']}")
        for field in ("Title", "Formal source/status", "Role", "Claim/use", "Quality basis", "URL/DOI"):
            if not row[field] or row[field] == "TODO":
                errors.append(f"line {line_number}: missing {field}")

    if errors:
        print("paper index validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("paper index validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
