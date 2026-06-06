#!/usr/bin/env python3
"""Basic OpenAI/Codex skill folder validation."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")

REQUIRED_REFERENCES = [
    "references/workspace.md",
    "references/evidence-policy.md",
    "references/writing-style.md",
    "references/literature.md",
    "references/repo-to-paper.md",
    "references/citation-audit.md",
    "references/handoff.md",
]

REQUIRED_TEMPLATES = [
    "assets/templates/README.md",
    "assets/templates/venue_profile.md",
    "assets/templates/paper_index.md",
    "assets/templates/references.bib",
    "assets/templates/claims.md",
    "assets/templates/idea_log.md",
    "assets/templates/intro.md",
    "assets/templates/related_work.md",
    "assets/templates/method.md",
    "assets/templates/experiments.md",
    "assets/templates/results_tables.md",
    "assets/templates/limitations.md",
    "assets/templates/figures.md",
    "assets/templates/handoff.md",
    "assets/templates/reading_note.md",
]

REQUIRED_SCRIPTS = [
    "scripts/init_paper_workspace.py",
    "scripts/validate_workspace.py",
    "scripts/validate_paper_index.py",
]

NON_MUTATING_CONTRACTS = [
    "tmp/check_tool_name_contract.py",
    "tmp/check_literature_contract.py",
    "tmp/check_writing_style_contract.py",
    "tmp/check_route_contract.py",
    "tmp/check_dev_artifacts_contract.py",
]

MUTATING_CONTRACTS = [
    "tmp/check_script_contracts.py",
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter ---")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter closing delimiter not found")
    raw = text[4:end]
    body = text[end + len("\n---"):]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value
    return data, body


def require_files(skill_dir: Path, errors: list[str], label: str, paths: list[str]) -> None:
    for relative in paths:
        path = skill_dir / relative
        if not path.exists():
            errors.append(f"Missing required {label}: {relative}")
        elif not path.is_file():
            errors.append(f"Required {label} is not a file: {relative}")


def run_contracts(skill_dir: Path, errors: list[str], contracts: list[str]) -> None:
    for relative in contracts:
        path = skill_dir / relative
        if not path.exists():
            errors.append(f"Missing contract check: {relative}")
            continue
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=skill_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"{relative} failed:\n{result.stdout.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex skill folder.")
    parser.add_argument("skill_dir")
    parser.add_argument("--with-mutating-contracts", action="store_true", help="Also run checks that create temporary workspaces under tmp/")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    errors: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing required SKILL.md at skill folder root")
    else:
        try:
            metadata, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            keys = set(metadata)
            if keys != {"name", "description"}:
                errors.append(f"Frontmatter must contain only name and description, got: {sorted(keys)}")
            name = metadata.get("name", "")
            description = metadata.get("description", "")
            if not name:
                errors.append("Missing frontmatter name")
            elif not NAME_RE.match(name):
                errors.append("Skill name must use lowercase letters, digits, and hyphens, under 64 chars")
            if not description:
                errors.append("Missing frontmatter description")
            elif len(description) > 1024:
                errors.append("Frontmatter description should stay under 1024 characters for Codex compatibility")
            if description and not description.startswith("Use "):
                errors.append('Frontmatter description should start with "Use "')
            if not body.strip():
                errors.append("SKILL.md body is empty")
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    agent_prompt = skill_dir / "agents" / "openai.yaml"
    if not agent_prompt.exists():
        errors.append("Missing recommended agents/openai.yaml")
    else:
        prompt_text = agent_prompt.read_text(encoding="utf-8")
        if "only" not in prompt_text.lower() or "explicit" not in prompt_text.lower():
            errors.append("agents/openai.yaml should preserve the conservative explicit-request trigger boundary")

    require_files(skill_dir, errors, "reference file", REQUIRED_REFERENCES)
    require_files(skill_dir, errors, "template file", REQUIRED_TEMPLATES)
    require_files(skill_dir, errors, "script file", REQUIRED_SCRIPTS)
    run_contracts(skill_dir, errors, NON_MUTATING_CONTRACTS)
    if args.with_mutating_contracts:
        run_contracts(skill_dir, errors, MUTATING_CONTRACTS)

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
