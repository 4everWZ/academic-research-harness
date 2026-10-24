"""Prepare, inspect and retain progressive-disclosure behavioral evaluations.

This tool never runs or grades a language model. Fresh writers and an independent
reviewer perform the behavioral evaluation described by the retained protocol.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "assets" / "evals" / "progressive_writing"
FIXTURE = SUITE / "cases.json"
READER = Path(__file__).with_name("progressive_reader.py")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def contained(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if not rel.parts or rel.anchor or ".." in rel.parts:
        raise ValueError(f"Expected a contained relative path: {relative}")
    path = (root / rel).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path leaves its root: {relative}")
    return path


def read_trace(path: Path) -> tuple[list[dict], list[str]]:
    rows, errors = [], []
    if not path.exists():
        return rows, errors
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeError:
        return rows, ["Trace is not UTF-8"]
    for number, line in enumerate(lines, start=1):
        try:
            row = json.loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                raise ValueError("Expected a read record with a path")
            rows.append(row)
            if not isinstance(row.get("content"), str) or row.get("characters") != len(row["content"]) or row.get("full_file_emitted") is not True:
                errors.append(f"Trace line {number} lacks complete emitted-content evidence")
        except ValueError:
            errors.append(f"Trace line {number} is not a valid read record")
    return rows, errors


def prepare(workspace: Path, skill_root: Path = ROOT) -> dict:
    workspace = workspace.resolve()
    temp_root = (ROOT / "tmp").resolve()
    if workspace == temp_root or not workspace.is_relative_to(temp_root):
        raise ValueError("Evaluation workspace must be a new directory under repository tmp/")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    workspace.mkdir(parents=True, exist_ok=False)
    candidate = workspace / "candidate"
    candidate.mkdir()
    for name in ("SKILL.md", "VERSION"):
        shutil.copyfile(skill_root / name, candidate / name)
    for name in ("references", "scripts", "agents"):
        shutil.copytree(skill_root / name, candidate / name)
    shutil.copytree(skill_root / "assets" / "templates", candidate / "assets" / "templates")
    prompts = {}
    for case in fixture["cases"]:
        folder = contained(workspace / "cases", case["id"])
        folder.mkdir(parents=True)
        (folder / "request.txt").write_text(case["request"], encoding="utf-8")
        for name, content in case["files"].items():
            target = contained(folder, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        for name in case["outputs"]:
            contained(folder, name)
        shutil.copyfile(READER, folder / "read.py")
        prompts[case["id"]] = fixture["writer_prompt"].format(case_dir=folder.as_posix())
    write_json(workspace / "fixture.json", fixture)
    write_json(workspace / "worker_prompts.json", prompts)
    write_json(workspace / "run.json", {
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "skill_version": (candidate / "VERSION").read_text(encoding="utf-8").strip(),
    })
    return {"workspace": str(workspace), "worker_prompts": str(workspace / "worker_prompts.json")}


def audit(workspace: Path) -> dict:
    workspace = workspace.resolve()
    fixture = json.loads((workspace / "fixture.json").read_text(encoding="utf-8"))
    style = (workspace / "candidate" / "references" / "writing-style.md").read_text(encoding="utf-8")
    references = {
        path.relative_to(workspace).as_posix()
        for path in (workspace / "candidate" / "references").glob("*.md")
    }
    results = []
    for case in fixture["cases"]:
        folder = contained(workspace / "cases", case["id"])
        rows, trace_errors = read_trace(folder / "trace.jsonl")
        reference_reads = [row["path"] for row in rows if row["path"] in references]
        unchanged = all(
            contained(folder, name).exists() and contained(folder, name).read_text(encoding="utf-8") == text
            for name, text in case["files"].items() if name not in case["outputs"]
        )
        checks = {
            "trace_valid": bool(rows) and not trace_errors,
            "full_style_emitted": any(
                row["path"] == "candidate/references/writing-style.md"
                and row.get("full_file_emitted") is True
                and row.get("characters") == len(style)
                and row.get("content") == style
                for row in rows
            ),
            "selective_references": bool(reference_reads) and set(reference_reads) != references,
            "source_inputs_unchanged": unchanged,
            "outputs_present": all(contained(folder, name).is_file() for name in case["outputs"]),
        }
        results.append({"id": case["id"], "reference_reads": reference_reads, "trace_errors": trace_errors, "checks": checks})
    return {
        "evidence_checks_passed": all(all(case["checks"].values()) for case in results),
        "behavior_review": "required separately; evidence checks do not grade prose or prove model attention",
        "cases": results,
    }


def record(workspace: Path, run_name: str, review: Path | None = None, runs_root: Path = SUITE / "runs") -> Path:
    workspace = workspace.resolve()
    if not run_name or Path(run_name).name != run_name or Path(run_name).anchor or run_name in {".", ".."}:
        raise ValueError("Use a single directory name for a retained run")
    report = audit(workspace)
    fixture = json.loads((workspace / "fixture.json").read_text(encoding="utf-8"))
    assessment = json.loads(review.read_text(encoding="utf-8")) if review else {"status": "not_reviewed"}
    destination = contained(runs_root, run_name)
    destination.mkdir(parents=True, exist_ok=False)
    for name in ("fixture.json", "run.json"):
        shutil.copyfile(workspace / name, destination / name)
    shutil.copytree(workspace / "candidate", destination / "candidate")
    for case in fixture["cases"]:
        folder = contained(workspace / "cases", case["id"])
        for name in dict.fromkeys([*case["files"], *case["outputs"], "response.md", "trace.jsonl"]):
            source = contained(folder, name)
            if source.is_file():
                target = contained(destination / "cases" / case["id"], name)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    write_json(destination / "audit.json", report)
    write_json(destination / "review.json", assessment)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("prepare")
    setup.add_argument("workspace", type=Path)
    setup.add_argument("--skill-root", type=Path, default=ROOT)
    inspect = commands.add_parser("audit")
    inspect.add_argument("workspace", type=Path)
    save = commands.add_parser("record")
    save.add_argument("workspace", type=Path)
    save.add_argument("run_name")
    save.add_argument("--review", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.workspace, args.skill_root)
    elif args.command == "audit":
        result = audit(args.workspace)
    else:
        result = {"retained_run": str(record(args.workspace, args.run_name, args.review))}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "audit" and not result["evidence_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
