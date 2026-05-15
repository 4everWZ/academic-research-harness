#!/usr/bin/env python3
"""Validate paper_index.md table structure and common fields."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

EXPECTED_COLUMNS = [
    "Key",
    "Title",
    "Venue/Type",
    "Year",
    "Source Priority",
    "Evidence Grade",
    "Code",
    "Task",
    "Dataset/Metric",
    "Role",
    "Risk",
    "PDF",
    "URL/DOI",
]

VALID_PRIORITIES = {"P1_core", "P2_frontier", "P3_background", "downgraded", "excluded", "TODO"}
VALID_GRADES = {"strong", "medium", "weak", "low_confidence", "reject", "TODO"}
VALID_ROLES = {
    "baseline",
    "competing_method",
    "supporting_mechanism",
    "background",
    "dataset_metric_reference",
    "implementation_reference",
    "weak_signal",
    "TODO",
}


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def validate_enum(
    errors: list[str],
    *,
    line_number: int,
    field: str,
    value: str,
    valid_values: set[str],
    allow_template_placeholder: bool,
) -> None:
    if value in valid_values:
        return
    if allow_template_placeholder and "/" in value:
        return
    errors.append(f"line {line_number}: unexpected {field}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate paper_index.md")
    parser.add_argument("paper_index")
    args = parser.parse_args()

    path = Path(args.paper_index)
    if not path.exists():
        print(f"paper_index not found: {path}")
        return 1

    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        print("paper_index validation failed: no Markdown table found")
        return 1

    header = split_row(table_lines[0])
    if header != EXPECTED_COLUMNS:
        print("paper_index validation failed: unexpected header")
        print("Expected:", EXPECTED_COLUMNS)
        print("Actual:  ", header)
        return 1

    keys: set[str] = set()
    errors: list[str] = []

    for idx, line in enumerate(table_lines[2:], start=3):
        cells = split_row(line)
        if len(cells) != len(EXPECTED_COLUMNS):
            errors.append(f"line {idx}: expected {len(EXPECTED_COLUMNS)} cells, got {len(cells)}")
            continue
        row = dict(zip(EXPECTED_COLUMNS, cells))
        key = row["Key"]
        if key and key != "TODO":
            if not re.match(r"^[A-Za-z][A-Za-z0-9_-]*$", key):
                errors.append(f"line {idx}: suspicious key format: {key}")
            if key in keys:
                errors.append(f"line {idx}: duplicate key: {key}")
            keys.add(key)
        allow_template_placeholder = key == "TODO"
        validate_enum(
            errors,
            line_number=idx,
            field="Source Priority",
            value=row["Source Priority"],
            valid_values=VALID_PRIORITIES,
            allow_template_placeholder=allow_template_placeholder,
        )
        validate_enum(
            errors,
            line_number=idx,
            field="Evidence Grade",
            value=row["Evidence Grade"],
            valid_values=VALID_GRADES,
            allow_template_placeholder=allow_template_placeholder,
        )
        validate_enum(
            errors,
            line_number=idx,
            field="Role",
            value=row["Role"],
            valid_values=VALID_ROLES,
            allow_template_placeholder=allow_template_placeholder,
        )

    if errors:
        print("paper_index validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("paper_index validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
