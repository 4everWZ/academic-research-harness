#!/usr/bin/env python3
"""Initialize a flat paper workspace under docs/<paper_slug>.

Usage:
  python scripts/init_paper_workspace.py docs/example_paper
  python scripts/init_paper_workspace.py docs/example_paper --venue "Target Venue" --outlet-mode conference --suffix-venue
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

REQUIRED_TEMPLATES = [
    "README.md",
    "venue_profile.md",
    "paper_index.md",
    "references.bib",
    "claims.md",
    "idea_log.md",
    "intro.md",
    "related_work.md",
    "method.md",
    "experiments.md",
    "results_tables.md",
    "limitations.md",
    "figures.md",
    "handoff.md",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise ValueError("venue slug is empty after normalization")
    return value


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a academic-research paper workspace.")
    parser.add_argument("workspace", help="Target workspace, e.g. docs/example_paper")
    parser.add_argument("--venue", default="", help="Optional target venue/outlet name to record in venue_profile.md")
    parser.add_argument(
        "--outlet-mode",
        default="",
        choices=["", "conference", "journal", "workshop", "thesis", "technical report", "undecided"],
        help="Optional broad outlet mode to record in venue_profile.md",
    )
    parser.add_argument(
        "--suffix-venue",
        action="store_true",
        help="Append __<venue> to workspace folder name. Use only after target venue/outlet is confirmed.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files if present")
    args = parser.parse_args()

    skill_root = repo_root_from_script()
    templates_dir = skill_root / "assets" / "templates"
    workspace = Path(args.workspace)

    if args.suffix_venue:
        if not args.venue:
            parser.error("--suffix-venue requires --venue")
        venue_slug = slugify(args.venue)
        if not workspace.name.endswith(f"__{venue_slug}"):
            workspace = workspace.with_name(f"{workspace.name}__{venue_slug}")

    workspace.mkdir(parents=True, exist_ok=True)

    for name in REQUIRED_TEMPLATES:
        src = templates_dir / name
        dst = workspace / name
        if not src.exists():
            raise FileNotFoundError(f"Missing template: {src}")
        if dst.exists() and not args.force:
            continue
        shutil.copyfile(src, dst)

    papers = workspace / "papers"
    papers.mkdir(exist_ok=True)
    (papers / ".gitignore").write_text("*.pdf\n*.epub\n", encoding="utf-8")
    if not (papers / "README.md").exists() or args.force:
        (papers / "README.md").write_text(
            "# Local Papers\n\nStore local PDF copies here when legally and practically appropriate. PDFs are ignored by git by default.\n",
            encoding="utf-8",
        )

    notes = workspace / "notes"
    notes.mkdir(exist_ok=True)
    if not (notes / "README.md").exists() or args.force:
        (notes / "README.md").write_text(
            "# Reading Notes\n\nUse one Markdown file per important paper, based on assets/templates/reading_note.md.\n",
            encoding="utf-8",
        )

    if args.venue:
        venue_profile = workspace / "venue_profile.md"
        text = venue_profile.read_text(encoding="utf-8")
        text = text.replace("- Target confirmed: no", "- Target confirmed: yes" if args.suffix_venue else "- Target confirmed: no")
        text = text.replace("- Target venue/outlet:", f"- Target venue/outlet: {args.venue}")
        if args.outlet_mode:
            text = text.replace(
                "- mode: conference / journal / workshop / thesis / technical report / undecided",
                f"- mode: {args.outlet_mode}",
            )
        if args.suffix_venue:
            text = text.replace("- Workspace suffix if confirmed:", f"- Workspace suffix if confirmed: __{slugify(args.venue)}")
        venue_profile.write_text(text, encoding="utf-8")

    print(f"Initialized paper workspace: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
