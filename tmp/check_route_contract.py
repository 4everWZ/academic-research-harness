#!/usr/bin/env python3
"""Local route/reference consistency checks for the skill package."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    checks = {
        "SKILL.md": [
            "repo-to-paper --section <target>",
            "notes/<citation_key>.md",
            "papers/*.pdf",
            "references/source-quality.md",
            "`paper_index.md`, `references.bib`, relevant notes/sources",
            "contribution framing",
        ],
        "references/workspace.md": [
            "--section <name>",
            "--strict",
            "all route-state files and paper-section files",
        ],
        "references/repo-to-paper.md": [
            "--section method",
            "user provides numbers or you verify matching logs",
            "Other Outlet Modes",
            "same dataset, split, metric, and protocol",
        ],
        "references/citation-audit.md": [
            "needed evidence files",
            "relevant shared reference",
            "references/source-quality.md",
            "user-provided results or verified logs",
        ],
        "agents/openai.yaml": [
            "workspace setup",
            "literature indexing",
            "writing-style revision",
        ],
        "USAGE.md": [
            "Load references/repo-to-paper.md.",
            "--section results_tables",
        ],
        "README.md": [
            "package-maintainer check",
            "Runtime workspace commands stay under `scripts/`",
        ],
    }

    for relative, needles in checks.items():
        text = read(relative)
        for needle in needles:
            if needle not in text:
                errors.append(f"{relative} missing: {needle}")

    if errors:
        print("Route contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
