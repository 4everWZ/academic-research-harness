#!/usr/bin/env python3
"""Initialize an already selected paper directory independently of its code repo."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote


GITIGNORE = """# Temporary work and build intermediates; keep final PDFs and images tracked.
/tmp/
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.fls
*.fdb_latexmk
*.synctex.gz
*.blg
*.bcf
*.run.xml
"""


class ProjectError(ValueError):
    """An unsafe destination, Git failure, or incomplete initialization."""


def reject_links(path: Path) -> None:
    for candidate in (path, *path.parents):
        is_junction = getattr(candidate, "is_junction", None)
        if candidate.is_symlink() or (is_junction and is_junction()):
            raise ProjectError(f"filesystem links are not allowed in project paths: {candidate}")


def git_environment() -> dict[str, str]:
    environment = os.environ.copy()
    # Repo overrides could silently direct an operation to the caller's index or Git dir.
    for key in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    ):
        environment.pop(key, None)
    environment.update(LC_ALL="C", GIT_OPTIONAL_LOCKS="0")
    return environment


def run_git(directory: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(directory), *arguments],
        env=git_environment(), capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=False,
    )


def git_value(directory: Path, *arguments: str) -> str:
    result = run_git(directory, *arguments)
    if result.returncode:
        raise ProjectError(result.stderr.strip() or f"Git failed in {directory}")
    return result.stdout.strip()


def repository_root(directory: Path) -> Path | None:
    result = run_git(directory, "rev-parse", "--is-bare-repository")
    if result.returncode:
        if "not a git repository" in result.stderr.lower():
            return None
        raise ProjectError(result.stderr.strip() or f"Cannot determine Git ownership: {directory}")
    if result.stdout.strip() == "true":
        raise ProjectError(f"bare repositories cannot be paper or code working directories: {directory}")
    return Path(git_value(directory, "rev-parse", "--show-toplevel")).resolve()


def check_independent_repository(paper: Path) -> None:
    marker = paper / ".git"
    reject_links(marker)
    if not marker.is_dir():
        raise ProjectError(f"paper Git must be local and independent, not a worktree or submodule: {paper}")
    git_dir = Path(git_value(paper, "rev-parse", "--absolute-git-dir")).resolve()
    common_raw = Path(git_value(paper, "rev-parse", "--git-common-dir"))
    common_dir = (paper / common_raw).resolve()
    if git_dir != marker.resolve() or common_dir != git_dir:
        raise ProjectError(f"paper repository shares or redirects Git metadata: {paper}")
    if git_value(paper, "rev-parse", "--show-superproject-working-tree"):
        raise ProjectError(f"paper repository is a submodule: {paper}")


def readme_text(paper: Path, code: Path) -> str:
    try:
        relative_code = Path(os.path.relpath(code, paper)).as_posix()
    except ValueError as exc:
        raise ProjectError(
            "Cannot create a README-relative code link across filesystem volumes; "
            "choose a sibling paper location or provide an existing README with accessible material links"
        ) from exc
    return (
        f"# {paper.name}\n\n"
        "Independent paper project. Maintain the manuscript, bibliography, and final figures "
        "and tables here, adding files as needed and following the manuscript's existing format.\n\n"
        "Keep temporary work in `tmp/`. Track final figure PDFs and images alongside the "
        "manuscript and references so collaborators can use the paper without the code checkout.\n\n"
        "## Research materials\n\n"
        f"Code project: [code repository]({quote(relative_code, safe='/.-_~')}/)\n"
    )


def initialize_project(destination: str, code_location: str) -> tuple[Path, bool]:
    if shutil.which("git") is None:
        raise ProjectError("Git is required; no project files were created")
    code_input = Path(code_location).absolute()
    reject_links(code_input)
    if not code_input.is_dir():
        raise ProjectError(f"code location is not a directory: {code_input}")
    code = repository_root(code_input)
    if code is None:
        raise ProjectError(f"code location is not in a Git working tree: {code_input}")
    reject_links(code)
    requested = Path(destination)
    candidate = requested if requested.is_absolute() else code.parent / requested
    reject_links(candidate)
    paper = candidate.resolve()
    if paper.is_relative_to(code) or code.is_relative_to(paper):
        raise ProjectError(f"paper must be outside, and not contain, the code repository: {paper}")
    if paper.exists() and not paper.is_dir():
        raise ProjectError(f"paper path is not a directory: {paper}")
    if not paper.parent.is_dir():
        raise ProjectError(f"paper parent directory must already exist: {paper.parent}")

    owner = repository_root(paper if paper.exists() else paper.parent)
    if owner is not None and owner != paper:
        raise ProjectError(f"paper path belongs to another repository ({owner}); ask the author: {paper}")
    if owner == paper:
        enclosing = repository_root(paper.parent)
        if enclosing is not None:
            raise ProjectError(f"paper repository is nested inside another repository ({enclosing}); ask the author")
        check_independent_repository(paper)
    elif (paper / ".git").exists() or (paper / ".git").is_symlink():
        raise ProjectError(f"unresolved Git metadata at {paper / '.git'}; ask the author")

    artifacts = {"README.md": None, ".gitignore": GITIGNORE}
    for name in artifacts:
        target = paper / name
        reject_links(target)
        if target.exists() and not target.is_file():
            raise ProjectError(f"project artifact is not a file: {target}")
    if not (paper / "README.md").exists():
        artifacts["README.md"] = readme_text(paper, code)

    try:
        paper.mkdir(exist_ok=True)
        if owner is None:
            # Do not import user Git templates or create unrelated files/hooks.
            git_value(paper, "init", "--quiet", "--template=")
            if repository_root(paper) != paper:
                raise ProjectError("Git initialization did not produce the intended working tree")
            check_independent_repository(paper)
        for name, content in artifacts.items():
            if content is None:
                continue
            target = paper / name
            reject_links(target)
            try:
                with target.open("x", encoding="utf-8", newline="\n") as stream:
                    stream.write(content)
            except FileExistsError:
                if not target.is_file():
                    raise ProjectError(f"project artifact became invalid: {target}")
    except (OSError, ValueError) as exc:
        present = ", ".join(name for name in (".git", *artifacts) if (paper / name).exists())
        raise ProjectError(
            f"{exc}\nInitialization incomplete at {paper}; retained project entries: "
            f"{present or '(none)'}. Existing contents were not overwritten or removed."
        ) from exc
    return paper, owner == paper


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_dir", help="Selected paper slug relative to the code root's parent, or an absolute path")
    parser.add_argument("--code-root", required=True, help="Code repository root or one of its subdirectories")
    args = parser.parse_args()
    try:
        paper, reused = initialize_project(args.paper_dir, args.code_root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"{'Reused' if reused else 'Initialized'} independent paper repository: {paper}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
