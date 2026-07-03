#!/usr/bin/env python3
"""Local contract checks for references/literature.md."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "references" / "literature.md"
CITATION_AUDIT = ROOT / "references" / "citation-audit.md"
BIB_TEMPLATE = ROOT / "assets" / "templates" / "references.bib"
SKILL = ROOT / "SKILL.md"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    audit_text = CITATION_AUDIT.read_text(encoding="utf-8")
    bib_template_text = BIB_TEMPLATE.read_text(encoding="utf-8")
    skill_text = SKILL.read_text(encoding="utf-8")
    errors: list[str] = []

    required = [
        "Use available search/fetch tools",
        "Do not invent tool names",
        "minimal `literature` or `idea` workspace",
        "references/source-quality.md",
        "BibTeX Rules",
        "Formal-version precedence is a hard check",
        "Before adding an arXiv-only BibTeX entry",
        "use the formal proceedings or journal BibTeX as the primary entry",
        "Do not fabricate BibTeX fields",
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
    for needle in ["arXiv-only BibTeX entry when a formal version exists"]:
        if needle not in audit_text:
            errors.append(f"Citation audit missing: {needle}")
    for needle in ["Formal-version check", "prefer proceedings or journal metadata over arXiv-only entries"]:
        if needle not in bib_template_text:
            errors.append(f"BibTeX template missing: {needle}")
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
