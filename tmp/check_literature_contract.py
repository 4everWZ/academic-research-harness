#!/usr/bin/env python3
"""Local contract checks for references/literature.md."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "references" / "literature.md"
SKILL = ROOT / "SKILL.md"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    skill_text = SKILL.read_text(encoding="utf-8")
    errors: list[str] = []

    required = [
        "Use available search/fetch tools",
        "Do not invent tool names",
        "minimal `literature` or `idea` workspace",
        "BibTeX Rules",
        "Do not fabricate BibTeX fields",
        "`P1_core`",
        "`P2_frontier`",
        "`P3_background`",
        "Freshness Weighting",
        "Default search weight favors the last 3-5 years",
        "Older sources need a role",
        "Publisher identity is a signal, not a verdict.",
        "paper-level transparency the primary criterion",
        "factual existence, method-context, dataset, benchmark, protocol, or implementation-trend claims",
        "Files updated or read-only status",
    ]
    forbidden = [
        "Use `google_web_search`",
        "Use `web_fetch`",
        "- MDPI;\n- Hindawi;\n- Frontiers;",
    ]

    for needle in required:
        if needle not in text:
            errors.append(f"Missing: {needle}")
    for needle in forbidden:
        if needle in text:
            errors.append(f"Forbidden: {needle}")
        if needle in skill_text:
            errors.append(f"Forbidden in SKILL.md: {needle}")

    if "Use available browsing/search tools" not in skill_text:
        errors.append("SKILL.md missing generic browsing/search tool guidance")

    if len(text.split()) > 1200:
        errors.append("references/literature.md should stay under 1200 words")

    if errors:
        print("Literature contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Literature contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
