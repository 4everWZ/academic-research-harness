#!/usr/bin/env python3
"""Create only the requested artifacts in a flat paper workspace."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import tempfile
import unicodedata
from pathlib import Path


TEMPLATE_GROUPS = {
    "literature": ["paper_index.md", "references.bib"],
    "claims": ["claims.md"],
    "ideas": ["idea_log.md"],
    "venue": ["venue_profile.md"],
    "papers": [],
}
VENUE_PROFILE_FIELDS = [
    "Status",
    "Decision authority/date",
    "Target venue or outlet",
    "Outlet type",
    "Subfield and audience",
    "Formatting constraints",
    "Writing emphasis",
]
VENUE_PROFILE_HEADER = "# Venue / Outlet Profile"


def slugify(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ascii_value.strip().lower())).strip("-")
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
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"venue profile must contain exactly one field: {label}")
    return pattern.sub(lambda _: replacement, text, count=1)


def parse_venue_profile(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if lines:
        lines[0] = lines[0].lstrip("\ufeff")
    if len(lines) < len(VENUE_PROFILE_FIELDS) + 2 or lines[0] != VENUE_PROFILE_HEADER or lines[1].strip():
        raise ValueError("venue profile must use the canonical visible header and field block")

    values: dict[str, str] = {}
    for offset, label in enumerate(VENUE_PROFILE_FIELDS, start=2):
        pattern = re.compile(rf"^- \*\*{re.escape(label)}:\*\*[ \t]*(.*)$")
        match = pattern.fullmatch(lines[offset])
        all_matches = [line for line in lines if pattern.fullmatch(line)]
        if match is None or len(all_matches) != 1:
            raise ValueError(f"venue profile must contain one canonical visible field: {label}")
        values[label] = match.group(1).strip()
    return values


def validate_single_line(label: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be blank")
    if len(value.splitlines()) != 1 or any(
        ord(character) < 32
        or ord(character) == 127
        or character in "\u0085\u2028\u2029"
        or unicodedata.category(character) == "Cf"
        for character in value
    ):
        raise ValueError(f"{label} must be a single line without control characters")
    if any(token in value for token in ("<!--", "-->", "```", "~~~", "<", ">", "[", "]", "`", "**", "__")):
        raise ValueError(f"{label} must not contain Markdown control syntax")


def is_filesystem_link(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(is_junction and is_junction())


def reject_linked_path(path: Path) -> None:
    for candidate in (path, *path.parents):
        if is_filesystem_link(candidate):
            raise ValueError(f"filesystem links are not allowed in workspace paths: {candidate}")


def atomic_write_bytes(path: Path, data: bytes, mode: int | None = None) -> None:
    existing_mode = path.stat().st_mode if mode is None and path.exists() else mode
    descriptor, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(raw_temp)
    try:
        stream = os.fdopen(descriptor, "wb")
        descriptor = -1
        with stream:
            stream.write(data)
        if existing_mode is not None:
            os.chmod(temp_path, existing_mode)
        os.replace(temp_path, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temp_path.unlink(missing_ok=True)


def atomic_write_text(path: Path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def rollback_created(files: list[Path], directories: list[Path]) -> list[Path]:
    residual: list[Path] = []
    for path in reversed(files):
        try:
            path.unlink(missing_ok=True)
        except OSError:
            residual.append(path)
    for path in reversed(directories):
        try:
            path.rmdir()
        except OSError:
            residual.append(path)
    return residual


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or extend an academic paper workspace.")
    parser.add_argument("workspace", help="Target workspace, for example docs/example-paper")
    parser.add_argument(
        "--workspace-root",
        default=".",
        help="Allowed root for the workspace path; defaults to the current directory",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Artifacts to add: literature, papers, claims, ideas, venue. Repeat or comma-separate.",
    )
    parser.add_argument("--venue", default="", help="Target venue or outlet")
    parser.add_argument(
        "--venue-status",
        default="",
        choices=["", "provisional", "confirmed"],
        help="Venue decision status, independent of workspace naming",
    )
    parser.add_argument(
        "--venue-authority",
        default="",
        help="Authority and date for a confirmed venue decision",
    )
    parser.add_argument(
        "--venue-slug",
        default="",
        help="Explicit ASCII slug for --suffix-venue",
    )
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
        if args.venue:
            args.venue = unicodedata.normalize("NFC", args.venue.strip())
            validate_single_line("venue", args.venue)
        if args.venue_authority:
            args.venue_authority = unicodedata.normalize("NFC", args.venue_authority.strip())
            validate_single_line("venue authority", args.venue_authority)
        if args.venue_slug:
            args.venue_slug = args.venue_slug.strip().lower()
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.venue_slug):
                raise ValueError("venue slug must use lowercase ASCII letters, digits, and single hyphens")
    except ValueError as exc:
        parser.error(str(exc))

    try:
        includes = parse_includes(args.include)
    except ValueError as exc:
        parser.error(str(exc))

    if args.venue or args.outlet_mode:
        if "venue" not in includes:
            includes.append("venue")
    if args.venue_status and not args.venue:
        parser.error("--venue-status requires --venue")
    if args.venue_status == "confirmed" and not args.venue_authority:
        parser.error("--venue-status confirmed requires --venue-authority")
    if args.venue_authority and args.venue_status != "confirmed":
        parser.error("--venue-authority requires --venue-status confirmed")
    if args.venue_slug and not args.suffix_venue:
        parser.error("--venue-slug requires --suffix-venue")
    if args.suffix_venue and not args.venue:
        parser.error("--suffix-venue requires --venue")
    if args.suffix_venue and args.venue_status != "confirmed":
        parser.error("--suffix-venue requires --venue-status confirmed")
    if not includes:
        parser.error("no artifacts or venue update requested")

    root_input = Path(args.workspace_root)
    requested_workspace = Path(args.workspace)
    try:
        reject_linked_path(root_input)
        workspace_root = root_input.resolve(strict=True)
        if not workspace_root.is_dir():
            raise ValueError(f"workspace root is not a directory: {workspace_root}")
        candidate = requested_workspace if requested_workspace.is_absolute() else workspace_root / requested_workspace
        reject_linked_path(candidate)
        workspace = candidate.resolve(strict=False)
        workspace.relative_to(workspace_root)
    except (OSError, ValueError) as exc:
        parser.error(f"workspace must stay within --workspace-root: {exc}")

    if args.suffix_venue:
        try:
            suffix = f"__{args.venue_slug or slugify(args.venue)}"
        except ValueError as exc:
            parser.error(str(exc))
        if not workspace.name.endswith(suffix):
            if workspace.exists():
                parser.error("--suffix-venue cannot rename an existing workspace")
            workspace = workspace.with_name(f"{workspace.name}{suffix}")
        try:
            workspace.relative_to(workspace_root)
        except ValueError:
            parser.error("venue-suffixed workspace must stay within --workspace-root")

    try:
        reject_linked_path(workspace)
    except ValueError as exc:
        parser.error(str(exc))
    if workspace.exists() and not workspace.is_dir():
        parser.error(f"workspace path is not a directory: {workspace}")

    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    copies: list[tuple[Path, Path]] = []
    for group in includes:
        for name in TEMPLATE_GROUPS[group]:
            source = templates / name
            target = workspace / name
            if not source.is_file():
                parser.error(f"missing template: {source}")
            if is_filesystem_link(source) or is_filesystem_link(target):
                parser.error(f"filesystem links are not allowed for artifacts: {target}")
            if target.exists() and not target.is_file():
                parser.error(f"artifact path is not a file: {target}")
            copies.append((source, target))

    notes_path = workspace / "notes"
    papers_path = workspace / "papers"
    if "literature" in includes:
        if is_filesystem_link(notes_path):
            parser.error(f"filesystem links are not allowed for artifacts: {notes_path}")
        if notes_path.exists() and not notes_path.is_dir():
            parser.error(f"artifact path is not a directory: {notes_path}")
    if "papers" in includes:
        if is_filesystem_link(papers_path):
            parser.error(f"filesystem links are not allowed for artifacts: {papers_path}")
        if papers_path.exists() and not papers_path.is_dir():
            parser.error(f"artifact path is not a directory: {papers_path}")

    profile_text: str | None = None
    profile_original_text: str | None = None
    profile = workspace / "venue_profile.md"
    profile_exists = profile.is_file()
    if "venue" in includes:
        source = profile if profile_exists else templates / "venue_profile.md"
        try:
            profile_original_text = source.read_text(encoding="utf-8")
            profile_text = profile_original_text
            profile_values = parse_venue_profile(profile_text)
            if profile_exists and profile_values["Status"] not in {"provisional", "confirmed"}:
                raise ValueError(f"invalid venue profile status: {profile_values['Status']}")
            if (
                profile_exists
                and profile_values["Status"] == "confirmed"
                and (
                    not profile_values["Target venue or outlet"]
                    or not profile_values["Decision authority/date"]
                )
                and not (args.venue and args.venue_status == "confirmed" and args.venue_authority)
            ):
                raise ValueError(
                    "an incomplete confirmed venue profile requires --venue, --venue-status confirmed, "
                    "and --venue-authority"
                )
            if not profile_exists:
                profile_text = set_field(profile_text, "Status", "provisional")
            if args.venue:
                current_venue = profile_values["Target venue or outlet"]
                if profile_exists and current_venue and current_venue != args.venue and not args.venue_status:
                    raise ValueError("--venue-status is required when changing an existing venue")
                if args.venue_status:
                    profile_text = set_field(profile_text, "Status", args.venue_status)
                profile_text = set_field(profile_text, "Target venue or outlet", args.venue)
            if args.venue_authority:
                profile_text = set_field(profile_text, "Decision authority/date", args.venue_authority)
            if args.outlet_mode:
                profile_text = set_field(profile_text, "Outlet type", args.outlet_mode)
        except (OSError, UnicodeError, ValueError) as exc:
            parser.error(str(exc))

    created_files: list[Path] = []
    created_directories: list[Path] = []
    profile_rollback: tuple[bool, bytes | None, int | None] | None = None
    missing_workspace_directories: list[Path] = []
    candidate = workspace
    while not candidate.exists():
        missing_workspace_directories.append(candidate)
        candidate = candidate.parent

    try:
        for directory in reversed(missing_workspace_directories):
            try:
                directory.mkdir()
            except FileExistsError:
                if not directory.is_dir() or is_filesystem_link(directory):
                    raise OSError(f"workspace path became unsafe: {directory}")
            else:
                created_directories.append(directory)
            reject_linked_path(directory)

        for source, target in copies:
            if profile_text is not None and target == profile:
                continue
            reject_linked_path(target)
            if not target.exists():
                with source.open("rb") as source_stream, target.open("xb") as target_stream:
                    created_files.append(target)
                    shutil.copyfileobj(source_stream, target_stream)

        if "literature" in includes:
            reject_linked_path(notes_path)
            if is_filesystem_link(notes_path):
                raise OSError(f"filesystem links are not allowed for artifacts: {notes_path}")
            if not notes_path.exists():
                notes_path.mkdir()
                created_directories.append(notes_path)
            if is_filesystem_link(notes_path):
                raise OSError(f"artifact directory became a filesystem link: {notes_path}")
        if "papers" in includes:
            reject_linked_path(papers_path)
            if is_filesystem_link(papers_path):
                raise OSError(f"filesystem links are not allowed for artifacts: {papers_path}")
            if not papers_path.exists():
                papers_path.mkdir()
                created_directories.append(papers_path)
            if is_filesystem_link(papers_path):
                raise OSError(f"artifact directory became a filesystem link: {papers_path}")

        if profile_text is not None and (
            not profile_exists or profile_text != profile_original_text
        ):
            reject_linked_path(profile)
            profile_was_missing = not profile.exists()
            profile_rollback = (
                profile_was_missing,
                None if profile_was_missing else profile.read_bytes(),
                None if profile_was_missing else profile.stat().st_mode,
            )
            atomic_write_text(profile, profile_text)
    except BaseException as exc:
        residual: list[Path] = []
        if profile_rollback is not None:
            profile_was_missing, previous_bytes, previous_mode = profile_rollback
            try:
                if profile_was_missing:
                    profile.unlink(missing_ok=True)
                elif previous_bytes is not None:
                    atomic_write_bytes(profile, previous_bytes, previous_mode)
            except OSError:
                residual.append(profile)
        residual.extend(rollback_created(created_files, created_directories))
        if isinstance(exc, (OSError, UnicodeError, ValueError)):
            detail = str(exc)
            if residual:
                detail += "; rollback could not remove: " + ", ".join(str(path) for path in residual)
            parser.error(detail)
        if residual and hasattr(exc, "add_note"):
            exc.add_note("rollback could not remove: " + ", ".join(str(path) for path in residual))
        raise

    print(f"Initialized paper workspace: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
