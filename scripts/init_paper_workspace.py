#!/usr/bin/env python3
"""Create only the requested artifacts in a flat paper workspace."""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


TEMPLATE_GROUPS = {
    "literature": ["paper_index.md", "references.bib"],
    "claims": ["claims.md"],
    "ideas": ["idea_log.md"],
    "venue": ["venue_profile.md"],
    "papers": [],
}


def slugify(value: str) -> str:
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.strip().lower())).strip("-")
    if not slug:
        raise ValueError("venue slug is empty after normalization")
    return slug


def parse_includes(raw_values: list[str]) -> list[str]:
    selected: list[str] = []
    for raw in raw_values:
        for item in raw.split(","):
            name = item.strip()
            if not name:
                continue
            if name not in TEMPLATE_GROUPS:
                raise ValueError(f"unknown include: {name}")
            if name not in selected:
                selected.append(name)
    return selected


def set_field(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"^- \*\*{re.escape(label)}:\*\*.*$", re.MULTILINE)
    replacement = f"- **{label}:** {value}"
    if not pattern.search(text):
        raise ValueError(f"venue profile is missing field: {label}")
    return pattern.sub(replacement, text, count=1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or extend an academic paper workspace.")
    parser.add_argument("workspace", help="Target workspace, for example docs/example-paper")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Artifacts to add: literature, papers, claims, ideas, venue. Repeat or comma-separate.",
    )
    parser.add_argument("--venue", default="", help="Target venue or outlet")
    parser.add_argument(
        "--outlet-mode",
        default="",
        choices=["", "conference", "journal", "workshop", "thesis", "technical report", "other"],
        help="Broad outlet type",
    )
    parser.add_argument(
        "--suffix-venue",
        action="store_true",
        help="Append __<venue> to the workspace name; use only for a confirmed target",
    )
    args = parser.parse_args()

    try:
        includes = parse_includes(args.include)
    except ValueError as exc:
        parser.error(str(exc))

    if args.venue or args.outlet_mode:
        if "venue" not in includes:
            includes.append("venue")
    if args.suffix_venue and not args.venue:
        parser.error("--suffix-venue requires --venue")

    workspace = Path(args.workspace)
    if args.suffix_venue:
        suffix = f"__{slugify(args.venue)}"
        if not workspace.name.endswith(suffix):
            workspace = workspace.with_name(f"{workspace.name}{suffix}")
    workspace.mkdir(parents=True, exist_ok=True)

    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    for group in includes:
        for name in TEMPLATE_GROUPS[group]:
            source = templates / name
            target = workspace / name
            if not source.is_file():
                raise FileNotFoundError(f"missing template: {source}")
            if not target.exists():
                shutil.copyfile(source, target)

    if "literature" in includes:
        (workspace / "notes").mkdir(exist_ok=True)
    if "papers" in includes:
        papers = workspace / "papers"
        papers.mkdir(exist_ok=True)
        ignore = papers / ".gitignore"
        if not ignore.exists():
            ignore.write_text("*.pdf\n*.epub\n", encoding="utf-8")

    if "venue" in includes and (args.venue or args.outlet_mode):
        profile = workspace / "venue_profile.md"
        text = profile.read_text(encoding="utf-8")
        if args.venue:
            text = set_field(text, "Status", "confirmed" if args.suffix_venue else "provisional")
            text = set_field(text, "Target venue or outlet", args.venue)
        if args.outlet_mode:
            text = set_field(text, "Outlet type", args.outlet_mode)
        profile.write_text(text, encoding="utf-8")

    print(f"Initialized paper workspace: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
