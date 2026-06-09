#!/usr/bin/env python3
"""Initialize a progressive flat paper workspace under docs/<paper_slug>.

Usage:
  python scripts/init_paper_workspace.py docs/example_paper --mode literature
  python scripts/init_paper_workspace.py docs/example_paper --mode repo-to-paper
  python scripts/init_paper_workspace.py docs/example_paper --mode full --venue "Target Venue" --outlet-mode conference --suffix-venue
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

FULL_TEMPLATES = [
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

REPO_TO_PAPER_BASE_TEMPLATES = [
    "README.md",
    "venue_profile.md",
    "paper_index.md",
    "references.bib",
    "claims.md",
]

PAPER_SECTION_TEMPLATES = [
    "intro.md",
    "related_work.md",
    "method.md",
    "experiments.md",
    "results_tables.md",
    "limitations.md",
    "figures.md",
]

MODE_TEMPLATES = {
    "minimal": ["README.md", "venue_profile.md"],
    "literature": ["README.md", "venue_profile.md", "paper_index.md", "references.bib"],
    "idea": ["README.md", "venue_profile.md", "paper_index.md", "references.bib", "idea_log.md"],
    "citation-audit": ["README.md", "venue_profile.md", "claims.md"],
    "repo-to-paper": REPO_TO_PAPER_BASE_TEMPLATES,
    "handoff": ["README.md", "venue_profile.md", "handoff.md"],
    "full": FULL_TEMPLATES,
}

MODE_DIRS = {
    "minimal": [],
    "literature": ["papers", "notes"],
    "idea": ["papers", "notes"],
    "citation-audit": [],
    "repo-to-paper": ["papers", "notes"],
    "handoff": [],
    "full": ["papers", "notes"],
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise ValueError("venue slug is empty after normalization")
    return value


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_sections(raw_sections: list[str]) -> list[str]:
    section_map = {Path(name).stem: name for name in PAPER_SECTION_TEMPLATES}
    selected: list[str] = []
    for raw in raw_sections:
        for item in raw.split(","):
            key = item.strip().removesuffix(".md")
            if not key:
                continue
            if key not in section_map:
                raise ValueError(f"unknown section: {item.strip()}")
            filename = section_map[key]
            if filename not in selected:
                selected.append(filename)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an academic research paper workspace.")
    parser.add_argument("workspace", help="Target workspace, e.g. docs/example_paper")
    parser.add_argument(
        "--mode",
        default="minimal",
        choices=sorted(MODE_TEMPLATES),
        help="Workspace level to create. Defaults to minimal; use full for all paper files.",
    )
    parser.add_argument("--venue", default="", help="Optional target venue/outlet name to record in venue_profile.md")
    parser.add_argument(
        "--outlet-mode",
        default="",
        choices=["", "conference", "journal", "workshop", "thesis", "technical report", "undecided"],
        help="Optional broad outlet mode to record in venue_profile.md",
    )
    parser.add_argument(
        "--section",
        action="append",
        default=[],
        help="Section file to create for repo-to-paper mode, e.g. method or results_tables. Repeat or comma-separate.",
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
    try:
        selected_sections = parse_sections(args.section)
    except ValueError as exc:
        parser.error(str(exc))
    if selected_sections and args.mode != "repo-to-paper":
        parser.error("--section is only valid with --mode repo-to-paper")

    if args.suffix_venue:
        if not args.venue:
            parser.error("--suffix-venue requires --venue")
        venue_slug = slugify(args.venue)
        if not workspace.name.endswith(f"__{venue_slug}"):
            workspace = workspace.with_name(f"{workspace.name}__{venue_slug}")

    workspace.mkdir(parents=True, exist_ok=True)

    template_names = [*MODE_TEMPLATES[args.mode]]
    if args.mode == "repo-to-paper":
        template_names.extend(selected_sections)

    for name in template_names:
        src = templates_dir / name
        dst = workspace / name
        if not src.exists():
            raise FileNotFoundError(f"Missing template: {src}")
        if dst.exists() and not args.force:
            continue
        shutil.copyfile(src, dst)

    if "papers" in MODE_DIRS[args.mode]:
        papers = workspace / "papers"
        papers.mkdir(exist_ok=True)
        papers_gitignore = papers / ".gitignore"
        if not papers_gitignore.exists() or args.force:
            papers_gitignore.write_text("*.pdf\n*.epub\n", encoding="utf-8")
        if not (papers / "README.md").exists() or args.force:
            (papers / "README.md").write_text(
                "# Local Papers\n\nStore local PDF copies here when legally and practically appropriate. PDFs are ignored by git by default.\n",
                encoding="utf-8",
            )

    if "notes" in MODE_DIRS[args.mode]:
        notes = workspace / "notes"
        notes.mkdir(exist_ok=True)
        if not (notes / "README.md").exists() or args.force:
            notes_readme = notes / "README.md"
            notes_readme.write_text(
                "# Reading Notes\n\nUse one Markdown file per important paper, based on assets/templates/reading_note.md.\n",
                encoding="utf-8",
            )

    if args.venue or args.outlet_mode:
        venue_profile = workspace / "venue_profile.md"
        text = venue_profile.read_text(encoding="utf-8")
        if args.venue:
            text = text.replace("- Target confirmed: no", "- Target confirmed: yes" if args.suffix_venue else "- Target confirmed: no")
            text = text.replace("- Target venue/outlet:", f"- Target venue/outlet: {args.venue}")
        if args.outlet_mode:
            text = text.replace(
                "- mode: conference / journal / workshop / thesis / technical report / undecided",
                f"- mode: {args.outlet_mode}",
            )
        if args.venue and args.suffix_venue:
            text = text.replace("- Workspace suffix if confirmed:", f"- Workspace suffix if confirmed: __{slugify(args.venue)}")
        venue_profile.write_text(text, encoding="utf-8")

    print(f"Initialized paper workspace: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
