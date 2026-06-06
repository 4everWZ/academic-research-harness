#!/usr/bin/env python3
"""Local contract checks for concise, paper-prose-oriented skill writing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.exists():
        raise FileNotFoundError(relative)
    return path.read_text(encoding="utf-8")


def require_contains(errors: list[str], relative: str, needles: list[str]) -> None:
    try:
        haystack = read(relative)
    except FileNotFoundError:
        errors.append(f"Missing file: {relative}")
        return
    for needle in needles:
        if needle not in haystack:
            errors.append(f"{relative} missing: {needle}")


def require_absent(errors: list[str], relative: str, needles: list[str]) -> None:
    try:
        haystack = read(relative)
    except FileNotFoundError:
        errors.append(f"Missing file: {relative}")
        return
    for needle in needles:
        if needle in haystack:
            errors.append(f"{relative} should not contain: {needle}")


def require_word_limit(errors: list[str], relative: str, limit: int) -> None:
    text = read(relative)
    count = len(text.split())
    if count > limit:
        errors.append(f"{relative} too long: {count} words > {limit}")


def require_low_pressure_terms(errors: list[str], relative: str, limit: int) -> None:
    text = read(relative)
    terms = re.findall(r"\b(defensive|rebuttal|objection|attack|confession)\b", text, flags=re.IGNORECASE)
    if len(terms) > limit:
        errors.append(f"{relative} has high defensive/rebuttal term density: {len(terms)} > {limit}")


def main() -> int:
    errors: list[str] = []

    require_contains(
        errors,
        "references/writing-style.md",
        [
            "Paper prose is not rebuttal.",
            "Contribution framing",
            "Public prose vs internal ledger",
            "Limitations and Scope",
            "Research taste",
            "Do not omit material limitations",
            "load `references/evidence-policy.md`",
        ],
    )
    require_contains(
        errors,
        "SKILL.md",
        [
            "references/writing-style.md",
            "over-defensive prose",
        ],
    )
    require_contains(
        errors,
        "references/repo-to-paper.md",
        [
            "references/writing-style.md",
            "paper-prose mode",
            "reviewer-response style",
        ],
    )
    require_contains(
        errors,
        "references/evidence-policy.md",
        [
            "Evidence control is not rebuttal prose.",
        ],
    )
    require_contains(
        errors,
        "assets/templates/claims.md",
        [
            "Public-facing handling",
            "Internal review notes",
            "omit_from_public_prose",
        ],
    )
    require_contains(
        errors,
        "assets/templates/intro.md",
        [
            "Contribution Focus",
            "Evidence-Calibrated Claims",
        ],
    )
    require_absent(
        errors,
        "assets/templates/intro.md",
        ["Unsupported / Needs Evidence"],
    )
    require_contains(
        errors,
        "assets/templates/related_work.md",
        ["Evidence Boundaries"],
    )
    require_absent(
        errors,
        "assets/templates/related_work.md",
        ["Unsupported / Needs Evidence"],
    )
    require_contains(
        errors,
        "assets/templates/limitations.md",
        [
            "Interpretive Boundaries",
            "Reader Impact",
        ],
    )
    require_absent(
        errors,
        "assets/templates/limitations.md",
        ["Claims Not Yet Allowed"],
    )
    require_contains(
        errors,
        "assets/templates/venue_profile.md",
        [
            "Mode Emphasis",
            "focus: central contribution",
        ],
    )
    require_contains(
        errors,
        "tmp/quick_validate_skill.py",
        ["references/writing-style.md"],
    )

    for relative, limit in {
        "SKILL.md": 650,
        "references/literature.md": 1200,
        "references/repo-to-paper.md": 850,
        "references/evidence-policy.md": 450,
        "references/workspace.md": 550,
        "references/writing-style.md": 700,
        "assets/templates/venue_profile.md": 260,
        "USAGE.md": 320,
    }.items():
        require_word_limit(errors, relative, limit)

    for relative, limit in {
        "SKILL.md": 3,
        "references/repo-to-paper.md": 4,
        "references/evidence-policy.md": 2,
        "references/writing-style.md": 4,
        "assets/templates/venue_profile.md": 0,
    }.items():
        require_low_pressure_terms(errors, relative, limit)

    for relative in ["SKILL.md", "references/literature.md", "references/repo-to-paper.md", "references/workspace.md", "references/writing-style.md", "assets/templates/venue_profile.md"]:
        require_absent(
            errors,
            relative,
            [
                "Anti-Bloat Rule",
                "Strict Minimalism Enforcement",
                "No Ghost Files",
                "invite hallucinations",
                "anticipated attacks",
                "reviewer objections",
                "confession list",
                "plausible attack",
                "Do not turn every possible reviewer objection into visible prose.",
            ],
        )

    if errors:
        print("Writing-style contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Writing-style contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
