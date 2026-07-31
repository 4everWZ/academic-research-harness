#!/usr/bin/env python3
"""Validate the compact paper index schema and persistent identities."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


EXPECTED_COLUMNS = [
    "Key",
    "Disposition",
    "Title",
    "Year",
    "Formal source/status",
    "Verified on/version",
    "Role",
    "Claim/use",
    "Quality basis",
    "Code/data",
    "URL/DOI",
]
PLACEHOLDER_CELLS = ["TODO"] * 9 + ["unknown", "TODO"]
COMMENT_ENTRY_TYPE = "comment"
BIBTEX_FIELD_NAME = r"[A-Za-z][A-Za-z0-9_-]*"
BIBTEX_IDENTIFIER = r"[A-Za-z][A-Za-z0-9_.:+/-]*"
BIBTEX_MONTHS = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"}
COMMONMARK_BLOCK_TAGS = {
    "address", "article", "aside", "base", "basefont", "blockquote", "body", "caption",
    "center", "col", "colgroup", "dd", "details", "dialog", "dir", "div", "dl", "dt",
    "fieldset", "figcaption", "figure", "footer", "form", "frame", "frameset", "h1", "h2",
    "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "iframe", "legend", "li",
    "link", "main", "menu", "menuitem", "nav", "noframes", "ol", "optgroup", "option",
    "p", "param", "search", "section", "summary", "table", "tbody", "td", "tfoot", "th",
    "thead", "title", "tr", "track", "ul",
}


def split_row(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        return []
    cells: list[str] = []
    current: list[str] = []
    backslashes = 0
    for character in text[1:-1]:
        if character == "|" and backslashes % 2 == 0:
            cells.append("".join(current).strip().replace(r"\|", "|"))
            current = []
        else:
            current.append(character)
        backslashes = backslashes + 1 if character == "\\" else 0
    cells.append("".join(current).strip().replace(r"\|", "|"))
    return cells


def is_delimiter_row(line: str) -> bool:
    cells = split_row(line)
    return len(cells) == len(EXPECTED_COLUMNS) and all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in cells
    )


def find_table(lines: list[str]) -> tuple[int, list[tuple[int, str]]] | None:
    for index, line in enumerate(lines):
        if split_row(line) != EXPECTED_COLUMNS:
            continue
        rows: list[tuple[int, str]] = []
        for number, candidate in enumerate(lines[index:], start=index + 1):
            stripped = candidate.strip()
            if stripped.startswith("|"):
                rows.append((number, candidate))
                continue
            if stripped and "|" in stripped:
                rows.append((number, candidate))
            break
        return index + 1, rows
    return None


def parse_markdown_fence(line: str) -> tuple[str, str, bool] | None:
    container = re.match(r" {0,3}(?:(?:[-+*]|\d{1,9}[.)])[ \t]+)", line)
    content = line[container.end() :] if container else line
    leading = re.match(r"^[ \t]*", content)
    indentation = len(leading.group(0).expandtabs(4)) if leading else 0
    if indentation > 3:
        return None
    match = re.match(r"(`{3,}|~{3,})(.*)$", content[len(leading.group(0)) :])
    if not match:
        return None
    marker, remainder = match.groups()
    if marker[0] == "`" and "`" in remainder:
        return None
    return marker, remainder, container is not None


def mask_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    masked = list(line)
    position = 0
    if in_comment:
        end = line.find("-->")
        if end < 0:
            return "", True
        masked[: end + 3] = " " * (end + 3)
        position = end + 3

    code_spans = [(match.start(), match.end()) for match in re.finditer(r"(`+)(.*?)\1", line)]
    span_index = 0
    while True:
        start = line.find("<!--", position)
        if start < 0:
            return "".join(masked), False
        while span_index < len(code_spans) and code_spans[span_index][1] <= start:
            span_index += 1
        if span_index < len(code_spans) and code_spans[span_index][0] <= start < code_spans[span_index][1]:
            position = code_spans[span_index][1]
            continue
        end = line.find("-->", start + 4)
        if end < 0:
            masked[start:] = " " * (len(masked) - start)
            return "".join(masked), True
        masked[start : end + 3] = " " * (end + 3 - start)
        position = end + 3


def mask_markdown_blocks(lines: list[str]) -> list[str]:
    masked: list[str] = []
    fence: str | None = None
    in_comment = False
    raw_html_end: str | None = None
    raw_html_until_blank = False
    in_frontmatter = bool(lines and lines[0].lstrip("\ufeff").strip() == "---")
    for index, line in enumerate(lines):
        if in_frontmatter:
            masked.append("")
            if index and line.strip() in {"---", "..."}:
                in_frontmatter = False
            continue

        if fence:
            fence_match = parse_markdown_fence(line)
            masked.append("")
            if fence_match:
                marker, remainder, has_container = fence_match
                if (
                    not has_container
                    and marker[0] == fence[0]
                    and len(marker) >= len(fence)
                    and not remainder.strip()
                ):
                    fence = None
            continue

        if raw_html_end:
            masked.append("")
            if raw_html_end.casefold() in line.casefold():
                raw_html_end = None
            continue

        if raw_html_until_blank:
            masked.append("")
            if not line.strip():
                raw_html_until_blank = False
            continue

        line, in_comment = mask_html_comments(line, in_comment)

        leading = re.match(r"^[ \t]*", line)
        if leading and len(leading.group(0).expandtabs(4)) >= 4:
            masked.append("")
            continue

        visible = re.sub(r"(`+)(.*?)\1", lambda match: " " * len(match.group(0)), line)
        stripped_visible = visible.lstrip()
        html_match = re.match(r"<(pre|script|style|textarea)(?=\s|>|$)", stripped_visible, re.IGNORECASE)
        if html_match:
            masked.append("")
            tag = html_match.group(1)
            end_token = f"</{tag}"
            if end_token.casefold() not in stripped_visible[html_match.end() :].casefold():
                raw_html_end = end_token
            continue
        if stripped_visible.startswith("<?"):
            masked.append("")
            if "?>" not in stripped_visible[2:]:
                raw_html_end = "?>"
            continue
        if stripped_visible.startswith("<![CDATA["):
            masked.append("")
            if "]]>" not in stripped_visible[9:]:
                raw_html_end = "]]>"
            continue
        if re.match(r"<![A-Z]", stripped_visible):
            masked.append("")
            if ">" not in stripped_visible[2:]:
                raw_html_end = ">"
            continue
        block_tag = re.match(r"</?([A-Za-z][A-Za-z0-9-]*)(?=\s|/?>|$)", stripped_visible)
        if block_tag and block_tag.group(1).casefold() in COMMONMARK_BLOCK_TAGS:
            masked.append("")
            raw_html_until_blank = True
            continue
        if re.match(r"</?[A-Za-z][^>]*>\s*$", stripped_visible):
            masked.append("")
            raw_html_until_blank = True
            continue

        fence_match = parse_markdown_fence(line)
        if fence_match:
            fence = fence_match[0]
            masked.append("")
            continue
        masked.append(line)
    return masked


def is_filesystem_link(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(is_junction and is_junction())


def path_safety_error(path: Path, root: Path) -> str | None:
    current = path
    while True:
        if is_filesystem_link(current):
            return f"filesystem links are not allowed: {current}"
        if current == root or current.parent == current:
            break
        current = current.parent

    try:
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=False)
        resolved_path.relative_to(resolved_root)
    except (OSError, ValueError):
        return f"path escapes workspace: {path}"
    return None


def split_bibtex_fields(text: str) -> list[str]:
    fields: list[str] = []
    current: list[str] = []
    brace_depth = 0
    in_quote = False
    escaped = False
    for character in text:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "{":
            brace_depth += 1
        elif character == "}":
            brace_depth -= 1
        elif character == '"' and brace_depth == 0:
            in_quote = not in_quote
        if character == "," and not in_quote and brace_depth == 0:
            fields.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    fields.append("".join(current).strip())
    if fields and not fields[-1]:
        fields.pop()
    return fields


def consume_bibtex_group(text: str, start: int) -> int | None:
    opener = text[start]
    if opener == "{":
        depth = 0
        escaped = False
        for position in range(start, len(text)):
            character = text[position]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    return position + 1
        return None

    brace_depth = 0
    escaped = False
    for position in range(start + 1, len(text)):
        character = text[position]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "{":
            brace_depth += 1
        elif character == "}":
            if brace_depth == 0:
                return None
            brace_depth -= 1
        elif character == '"' and brace_depth == 0:
            return position + 1
    return None


def valid_bibtex_value(text: str) -> bool:
    if re.search(r"\\[A-Za-z@]+", text):
        return False
    position = 0
    expect_component = True
    while True:
        while position < len(text) and text[position].isspace():
            position += 1
        if position == len(text):
            return not expect_component

        if not expect_component:
            if text[position] != "#":
                return False
            position += 1
            expect_component = True
            continue

        if text[position] in {'{', '"'}:
            end = consume_bibtex_group(text, position)
            if end is None:
                return False
            position = end
        else:
            pattern = r"\d+" if text[position].isdigit() else BIBTEX_IDENTIFIER
            match = re.match(pattern, text[position:])
            if not match:
                return False
            if not text[position].isdigit() and match.group(0).casefold() not in BIBTEX_MONTHS:
                return False
            position += match.end()
        expect_component = False


def valid_bibtex_fields(text: str, name_pattern: str = BIBTEX_FIELD_NAME) -> bool:
    fields = split_bibtex_fields(text)
    if not fields:
        return False
    names: set[str] = set()
    for field in fields:
        name, separator, value = field.partition("=")
        normalized_name = name.strip().lower()
        if not separator or not re.fullmatch(name_pattern, normalized_name):
            return False
        if normalized_name in names or not valid_bibtex_value(value):
            return False
        names.add(normalized_name)
    return True


def parse_bibtex_keys(text: str) -> tuple[list[str], list[str]]:
    keys: list[str] = []
    errors: list[str] = []
    position = 0

    while True:
        start = text.find("@", position)
        if start < 0:
            break
        type_match = re.match(r"@([A-Za-z]+)", text[start:])
        if not type_match:
            errors.append(f"references.bib: malformed entry near character {start + 1}")
            position = start + 1
            continue

        entry_type = type_match.group(1).lower()
        opener_position = start + type_match.end()
        while opener_position < len(text) and text[opener_position].isspace():
            opener_position += 1

        if entry_type == COMMENT_ENTRY_TYPE:
            if opener_position >= len(text) or text[opener_position] not in "({":
                line_end = text.find("\n", opener_position)
                position = len(text) if line_end < 0 else line_end + 1
                continue
            opener = text[opener_position]
            closer = "}" if opener == "{" else ")"
            depth = 1
            cursor = opener_position + 1
            while cursor < len(text) and depth:
                if text[cursor] == opener:
                    depth += 1
                elif text[cursor] == closer:
                    depth -= 1
                cursor += 1
            if depth:
                errors.append(f"references.bib: unterminated @comment near character {start + 1}")
                break
            position = cursor
            continue

        if opener_position >= len(text) or text[opener_position] not in "({":
            errors.append(f"references.bib: malformed entry near character {start + 1}")
            position = start + type_match.end()
            continue

        opener = text[opener_position]
        body_start = opener_position + 1
        outer_depth = 1
        brace_depth = 0
        in_quote = False
        escaped = False
        malformed = False
        cursor = body_start
        while cursor < len(text) and outer_depth:
            character = text[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "{":
                brace_depth += 1
            elif character == "}":
                if brace_depth:
                    brace_depth -= 1
                elif opener == "{" and not in_quote:
                    outer_depth -= 1
                else:
                    malformed = True
                    break
            elif character == '"' and brace_depth == 0:
                in_quote = not in_quote
            elif not in_quote and opener == "(" and brace_depth == 0 and character == "(":
                outer_depth += 1
            elif not in_quote and opener == "(" and brace_depth == 0 and character == ")":
                outer_depth -= 1
            cursor += 1

        if outer_depth or brace_depth or in_quote or malformed:
            errors.append(f"references.bib: unterminated @{entry_type} entry near character {start + 1}")
            break

        body = text[body_start : cursor - 1]
        if entry_type in {"string", "preamble"}:
            errors.append(f"references.bib: unsupported @{entry_type} directive near character {start + 1}")
        else:
            raw_key, separator, fields = body.partition(",")
            key = raw_key.strip()
            if not separator or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key):
                errors.append(f"references.bib: invalid citation entry near character {start + 1}")
            elif not valid_bibtex_fields(fields):
                errors.append(f"references.bib: invalid fields for citation key: {key}")
            else:
                keys.append(key)
        position = cursor

    return keys, errors


def valid_verification(value: str) -> bool:
    checked_on, separator, version = value.partition("/")
    checked_on = checked_on.strip()
    version = version.strip()
    if not separator or not version:
        return False
    if not any(character.isalnum() for character in version):
        return False
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", checked_on):
        return False
    if re.search(
        r"\b(?:todo|tbd|unknown|pending|none|unverified|unchecked|unconfirmed|unresolved)\b",
        version,
        re.IGNORECASE,
    ):
        return False
    if re.search(
        r"\b(?:not(?:\s+\w+){0,2}|never)\s+(?:verified|checked|confirmed)\b",
        version,
        re.IGNORECASE,
    ):
        return False
    if re.fullmatch(r"n/?a", version, re.IGNORECASE):
        return False
    if version.startswith("[") and version.endswith("]"):
        return False
    try:
        checked_date = date.fromisoformat(checked_on)
    except ValueError:
        return False
    return checked_date <= date.today()


def is_placeholder(value: str) -> bool:
    normalized = value.strip().casefold()
    rendered = re.sub(r"<[^>]*>", "", normalized)
    return (
        not normalized
        or normalized in {"todo", "tbd", "pending", "unknown", "unverified", "none", "n/a", "na"}
        or bool(re.match(r"^(?:todo|tbd)(?:\b|[:_-])", normalized))
        or (normalized.startswith("[") and normalized.endswith("]"))
        or not any(character.isalnum() for character in rendered)
    )


def validate_linked_artifacts(
    workspace: Path, index_keys: set[str], selected_keys: set[str]
) -> list[str]:
    errors: list[str] = []
    bib_path = workspace / "references.bib"
    notes_path = workspace / "notes"

    for artifact in (workspace, bib_path, notes_path):
        safety_error = path_safety_error(artifact, workspace)
        if safety_error:
            errors.append(f"workspace: {safety_error}")

    if path_safety_error(bib_path, workspace):
        pass
    elif not bib_path.is_file():
        errors.append("workspace: references.bib not found")
    else:
        try:
            bib_keys, bib_errors = parse_bibtex_keys(bib_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"references.bib: {exc}")
            bib_keys, bib_errors = [], []
        errors.extend(bib_errors)
        bib_keys_by_case: dict[str, str] = {}
        for key in bib_keys:
            folded = key.casefold()
            previous = bib_keys_by_case.get(folded)
            if previous == key:
                errors.append(f"references.bib: duplicate citation key: {key}")
            elif previous is not None:
                errors.append(
                    f"references.bib: case-insensitive citation key collision: {previous}, {key}"
                )
            else:
                bib_keys_by_case[folded] = key
        for key in sorted(set(bib_keys) - index_keys):
            errors.append(f"references.bib: key missing from paper_index.md: {key}")
        for key in sorted(selected_keys - set(bib_keys)):
            errors.append(f"paper_index.md: selected key missing from references.bib: {key}")

    if path_safety_error(notes_path, workspace):
        pass
    elif not notes_path.is_dir():
        errors.append("workspace: notes directory not found")
    else:
        for note in sorted(notes_path.iterdir()):
            safety_error = path_safety_error(note, workspace)
            if safety_error:
                errors.append(f"notes: {safety_error}")
                continue
            if not note.is_file() or note.suffix.lower() != ".md":
                errors.append(f"notes: noncanonical artifact: {note.name}")
                continue
            if note.stem not in index_keys:
                errors.append(f"notes: key missing from paper_index.md: {note.stem}")
                continue
            try:
                first_line = note.read_text(encoding="utf-8").splitlines()[0]
            except (OSError, UnicodeError, IndexError) as exc:
                errors.append(f"notes: cannot read canonical heading for {note.name}: {exc}")
                continue
            if first_line != f"# Reading Note: {note.stem}":
                errors.append(f"notes: heading key does not match filename: {note.name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate paper_index.md")
    parser.add_argument("target", help="paper_index.md or its workspace directory")
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Validate only the index table and skip BibTeX/note linkage",
    )
    args = parser.parse_args()

    target = Path(args.target)
    path = target / "paper_index.md" if target.is_dir() else target
    workspace = None if args.schema_only else (target if target.is_dir() else target.parent)
    safety_root = workspace or path.parent
    safety_error = path_safety_error(path, safety_root)
    if safety_error:
        print(f"paper index validation failed: {safety_error}")
        return 1
    if not path.is_file():
        print(f"paper index not found: {path}")
        return 1

    try:
        lines = mask_markdown_blocks(path.read_text(encoding="utf-8").splitlines())
    except (OSError, UnicodeError) as exc:
        print(f"paper index validation failed: {exc}")
        return 1
    header_lines = [number for number, line in enumerate(lines, start=1) if split_row(line) == EXPECTED_COLUMNS]
    if len(header_lines) > 1:
        print(f"paper index validation failed: duplicate table headers at lines {header_lines}")
        return 1
    located = find_table(lines)
    if located is None:
        print("paper index validation failed: expected table header not found")
        return 1
    header_line, table = located
    if len(table) < 2 or not is_delimiter_row(table[1][1]):
        print(f"paper index validation failed: invalid delimiter after line {header_line}")
        return 1

    errors: list[str] = []
    keys: set[str] = set()
    keys_by_case: dict[str, str] = {}
    selected_keys: set[str] = set()
    completed_rows = 0
    placeholder_rows = 0
    for line_number, line in table[2:]:
        cells = split_row(line)
        if len(cells) != len(EXPECTED_COLUMNS):
            errors.append(f"line {line_number}: expected {len(EXPECTED_COLUMNS)} cells, got {len(cells)}")
            continue
        row = dict(zip(EXPECTED_COLUMNS, cells))
        key = row["Key"]
        if cells == PLACEHOLDER_CELLS:
            placeholder_rows += 1
            continue
        completed_rows += 1
        if key == "TODO":
            errors.append(f"line {line_number}: incomplete citation key")
        key_is_valid = bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key))
        if not key_is_valid:
            errors.append(f"line {line_number}: invalid citation key: {key}")
        else:
            folded = key.casefold()
            previous = keys_by_case.get(folded)
            if previous == key:
                errors.append(f"line {line_number}: duplicate citation key: {key}")
            elif previous is not None:
                errors.append(
                    f"line {line_number}: case-insensitive citation key collision: {previous}, {key}"
                )
            else:
                keys.add(key)
                keys_by_case[folded] = key
        disposition = row["Disposition"]
        if disposition not in {"selected", "excluded"}:
            errors.append(f"line {line_number}: invalid disposition: {disposition}")
        elif disposition == "selected" and key_is_valid:
            selected_keys.add(key)
        if not re.fullmatch(r"\d{4}", row["Year"]):
            errors.append(f"line {line_number}: invalid year: {row['Year']}")
        if not valid_verification(row["Verified on/version"]):
            errors.append(
                f"line {line_number}: invalid Verified on/version "
                f"(expected YYYY-MM-DD / <checked version or status>): {row['Verified on/version']}"
            )
        for field in (
            "Title",
            "Formal source/status",
            "Verified on/version",
            "Role",
            "Claim/use",
            "Quality basis",
            "URL/DOI",
        ):
            if is_placeholder(row[field]):
                errors.append(f"line {line_number}: missing {field}")

    if completed_rows and placeholder_rows:
        errors.append("remove the placeholder row once completed entries exist")
    if placeholder_rows > 1:
        errors.append("paper_index.md may contain only one placeholder row")

    if workspace:
        errors.extend(validate_linked_artifacts(workspace, keys, selected_keys))

    if errors:
        print("paper index validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.schema_only and completed_rows:
        print("paper index schema validation passed; linked artifacts not checked")
    elif args.schema_only:
        print("paper index schema validation passed; no completed entries; linked artifacts not checked")
    elif completed_rows:
        print("paper index structural validation passed; BibTeX content is not sanitized for compilation")
    else:
        print(
            "paper index schema validation passed; no completed entries; "
            "BibTeX content is not sanitized for compilation"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
