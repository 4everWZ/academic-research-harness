#!/usr/bin/env python3
"""Ensure runtime skill docs do not hardcode unavailable tool names."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]

FORBIDDEN_EXACT = [
    "google_web_search",
    "web_fetch",
    "grep_search",
    "list_directory",
    "read_file",
    "WebSearch",
    "WebFetch",
    "TodoWrite",
]

FORBIDDEN_CODE_TOKENS = ["Task", "Bash", "Read", "Write", "Edit", "Grep", "Glob"]


def main() -> int:
    errors: list[str] = []
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        for name in FORBIDDEN_EXACT:
            if name in text:
                errors.append(f"{path.relative_to(ROOT)} contains hardcoded tool name: {name}")
        for name in FORBIDDEN_CODE_TOKENS:
            pattern = rf"`{re.escape(name)}`|\b{re.escape(name)}\("
            if re.search(pattern, text):
                errors.append(f"{path.relative_to(ROOT)} contains code-like unavailable tool token: {name}")

    if errors:
        print("Tool-name contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Tool-name contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
