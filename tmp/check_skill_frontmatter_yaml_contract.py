#!/usr/bin/env python3
"""Check that SKILL.md frontmatter avoids YAML plain-scalar traps."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter_lines(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    for idx, line in enumerate(lines[1:], start=2):
        if line == "---":
            return list(enumerate(lines[1 : idx - 1], start=2))
    raise ValueError("SKILL.md frontmatter is not closed")


def is_quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}


def main() -> int:
    errors: list[str] = []
    for line_number, line in frontmatter_lines(ROOT / "SKILL.md"):
        if not line.strip() or ":" not in line:
            continue
        _, value = line.split(":", 1)
        value = value.strip()
        if value and not is_quoted(value) and ": " in value:
            errors.append(f"line {line_number}: quote frontmatter values containing ': '")

    if errors:
        print("Skill frontmatter YAML contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill frontmatter YAML contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
