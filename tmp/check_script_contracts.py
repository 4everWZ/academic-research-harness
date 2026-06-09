#!/usr/bin/env python3
"""Local script behavior contracts for the skill package."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp" / "_script_contract_workspace"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    try:
        outlet_ws = WORK / "outlet_only"
        result = run(["scripts/init_paper_workspace.py", str(outlet_ws), "--mode", "minimal", "--outlet-mode", "conference"])
        require(result.returncode == 0, errors, f"outlet-only init failed: {result.stdout}")
        venue_profile = outlet_ws / "venue_profile.md"
        venue_lines = venue_profile.read_text(encoding="utf-8").splitlines()
        require("- mode: conference" in venue_lines, errors, "--outlet-mode without --venue was not recorded")

        repo_ws = WORK / "repo_to_paper"
        result = run(["scripts/init_paper_workspace.py", str(repo_ws), "--mode", "repo-to-paper"])
        require(result.returncode == 0, errors, f"repo-to-paper init failed: {result.stdout}")
        require((repo_ws / "claims.md").exists(), errors, "repo-to-paper missing claims.md")
        require(not (repo_ws / "method.md").exists(), errors, "repo-to-paper default created method.md")
        require(not (repo_ws / "intro.md").exists(), errors, "repo-to-paper default created intro.md")
        require(not (repo_ws / "idea_log.md").exists(), errors, "repo-to-paper created unrelated idea_log.md")
        require(not (repo_ws / "handoff.md").exists(), errors, "repo-to-paper created unrelated handoff.md")

        method_ws = WORK / "repo_to_method"
        result = run(["scripts/init_paper_workspace.py", str(method_ws), "--mode", "repo-to-paper", "--section", "method"])
        require(result.returncode == 0, errors, f"repo-to-paper section init failed: {result.stdout}")
        require((method_ws / "method.md").exists(), errors, "--section method did not create method.md")
        require((method_ws / "claims.md").exists(), errors, "--section method missing claims.md")
        require(not (method_ws / "intro.md").exists(), errors, "--section method created unrelated intro.md")
        result = run(["scripts/validate_workspace.py", str(method_ws), "--mode", "repo-to-paper", "--section", "method", "--strict"])
        require(result.returncode == 0, errors, f"strict repo-to-paper section validation failed: {result.stdout}")

        full_ws = WORK / "full"
        result = run(["scripts/init_paper_workspace.py", str(full_ws), "--mode", "full"])
        require(result.returncode == 0, errors, f"full init failed: {result.stdout}")
        require((full_ws / "idea_log.md").exists(), errors, "full missing idea_log.md")
        require((full_ws / "handoff.md").exists(), errors, "full missing handoff.md")

        ghost_ws = WORK / "ghost"
        result = run(["scripts/init_paper_workspace.py", str(ghost_ws), "--mode", "minimal"])
        require(result.returncode == 0, errors, f"minimal init failed: {result.stdout}")
        shutil.copyfile(ROOT / "assets" / "templates" / "method.md", ghost_ws / "method.md")
        result = run(["scripts/validate_workspace.py", str(ghost_ws), "--mode", "minimal", "--strict"])
        require(result.returncode != 0 and "Unexpected template file" in result.stdout, errors, "strict workspace validation did not reject ghost method.md")

        paper_index = WORK / "bad_paper_index.md"
        paper_index.write_text(
            "\n".join(
                [
                    "# Paper Index",
                    "",
                    "| Key | Title | Venue/Type | Year | Source Priority | Evidence Grade | Code | Task | Dataset/Metric | Role | Risk | PDF | URL/DOI |",
                    "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
                    "| smith2024x | X | arXiv | 2024 | TODO | strong | maybe | task | metric | baseline | risk | papers/x.pdf | url |",
                ]
            ),
            encoding="utf-8",
        )
        result = run(["scripts/validate_paper_index.py", str(paper_index)])
        require(result.returncode != 0, errors, "paper index validator accepted TODO priority and invalid Code in keyed row")
        require("line 5" in result.stdout, errors, "paper index validator did not report file-relative line number")
        require("unexpected Code" in result.stdout, errors, "paper index validator did not validate Code column")
    finally:
        if WORK.exists():
            shutil.rmtree(WORK)

    if errors:
        print("Script contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Script contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
