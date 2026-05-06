#!/usr/bin/env python3
"""Initialize a flat research-writing-harness paper workspace.

Usage:
  python scripts/init_paper_workspace.py --slug fire_mamba_paper --root docs
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

TEMPLATE_FILES = [
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a flat paper workspace under docs/<slug>.")
    parser.add_argument("--slug", required=True, help="Workspace name under docs/, e.g. fire_mamba_paper")
    parser.add_argument("--root", default="docs", help="Root docs directory. Default: docs")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files if present")
    args = parser.parse_args()

    repo_root = Path.cwd()
    harness_root = Path(__file__).resolve().parents[1]
    templates = harness_root / "templates"
    target = repo_root / args.root / args.slug

    missing_templates = [name for name in TEMPLATE_FILES if not (templates / name).exists()]
    if missing_templates:
        missing = ", ".join(missing_templates)
        raise SystemExit(f"Missing template file(s): {missing}")

    target.mkdir(parents=True, exist_ok=True)
    (target / "papers").mkdir(exist_ok=True)
    (target / "notes").mkdir(exist_ok=True)

    copied = []
    skipped = []
    for name in TEMPLATE_FILES:
        src = templates / name
        dst = target / name
        if dst.exists() and not args.force:
            skipped.append(name)
            continue
        shutil.copyfile(src, dst)
        copied.append(name)

    papers_gitignore = target / "papers" / ".gitignore"
    if args.force or not papers_gitignore.exists():
        papers_gitignore.write_text("*.pdf\n*.epub\n", encoding="utf-8")

    papers_readme = target / "papers" / "README.md"
    if args.force or not papers_readme.exists():
        papers_readme.write_text(
            "# Papers\n\nOptional local PDF storage. PDFs are ignored by default. Record metadata in ../paper_index.md.\n",
            encoding="utf-8",
        )

    print(f"Initialized paper workspace: {target}")
    if copied:
        print("Copied: " + ", ".join(copied))
    if skipped:
        print("Skipped existing files: " + ", ".join(skipped))


if __name__ == "__main__":
    main()
