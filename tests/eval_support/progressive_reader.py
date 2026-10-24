"""Emit one selected evaluation input and retain exactly what was emitted."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def read(case_dir: Path, relative: str) -> None:
    case_dir = case_dir.resolve()
    workspace = case_dir.parent.parent
    rel = Path(relative)
    if not rel.parts or rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Use a contained relative text path")
    path = (workspace / rel if rel.parts[0] == "candidate" else case_dir / rel).resolve()
    if not (path.is_relative_to(case_dir) or path.is_relative_to(workspace / "candidate")):
        raise ValueError("Outside evaluation input roots")
    if path.name in {"read.py", "trace.jsonl"}:
        raise ValueError("Read task materials and candidate instructions, not evaluation internals")
    content = path.read_text(encoding="utf-8")
    print(content, end="" if content.endswith("\n") else "\n", flush=True)
    with (case_dir / "trace.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps({
            "path": path.relative_to(workspace).as_posix(),
            "characters": len(content),
            "full_file_emitted": True,
            "content": content,
        }, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python read.py <relative-text-path>")
    try:
        read(Path(__file__).resolve().parent, sys.argv[1])
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
