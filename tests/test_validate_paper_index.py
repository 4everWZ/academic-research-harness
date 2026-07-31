from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_paper_index.py"
TEMPLATE = ROOT / "assets" / "templates" / "paper_index.md"
TEMPLATE_TABLE = [line for line in TEMPLATE.read_text(encoding="utf-8").splitlines() if line.startswith("|")]
HEADER, DELIMITER, PLACEHOLDER = TEMPLATE_TABLE[:3]


class ValidatePaperIndexTests(unittest.TestCase):
    def run_validator(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paper_index.md"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--schema-only", str(path)],
                capture_output=True,
                check=False,
                text=True,
            )

    def test_accepts_escaped_pipe_and_ignores_other_tables(self) -> None:
        content = "\n".join(
            [
                "| Other | Table |",
                "|---|---|",
                "| x | y |",
                "",
                HEADER,
                DELIMITER,
                r"| smith2024 | selected | A \| B | 2024 | Journal | 2026-07-31 / v1 | background | context | peer reviewed | yes | https://example.test |",
                "",
                "| Later | Table |",
                "|---|---|",
            ]
        )
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_malformed_delimiter(self) -> None:
        content = "\n".join([HEADER, "| x | y |", PLACEHOLDER])
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid delimiter", result.stdout)

    def test_rejects_partially_populated_todo_row(self) -> None:
        content = "\n".join(
            [HEADER, DELIMITER, "| TODO | selected | Real title | 20xx | Journal | 2026-07-31 / v1 | background | TODO | reviewed | yes | TODO |"]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incomplete citation key", result.stdout)
        self.assertIn("invalid year", result.stdout)

    def test_bundled_template_contract(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--schema-only", str(TEMPLATE)],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no completed entries", result.stdout)

    def test_workspace_rejects_orphan_linked_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article{orphan2023,\n  title={Orphan}\n}\n",
                encoding="utf-8",
            )
            notes = workspace / "notes"
            notes.mkdir()
            (notes / "orphan2023.md").write_text("# Note\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references.bib: key missing", result.stdout)
        self.assertIn("selected key missing", result.stdout)
        self.assertIn("notes: key missing", result.stdout)

    def test_workspace_allows_excluded_key_without_bibtex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | excluded | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text("", encoding="utf-8")
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_direct_file_mode_checks_parent_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            index = workspace / "paper_index.md"
            index.write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text("", encoding="utf-8")
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(index)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("selected key missing", result.stdout)

    def test_bibtex_directive_does_not_satisfy_selected_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text("@comment{smith2024, ignored}\n", encoding="utf-8")
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("selected key missing", result.stdout)

    def test_rejects_truncated_bibtex_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text("@article{smith2024,\n  title={Title}\n", encoding="utf-8")
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unterminated @article", result.stdout)

    def test_rejects_row_missing_opening_pipe(self) -> None:
        content = "\n".join(
            [
                HEADER,
                DELIMITER,
                "smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected 11 cells", result.stdout)

    def test_rejects_balanced_bibtex_with_invalid_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article{smith2024, this is not a field assignment}\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid fields", result.stdout)

    def test_rejects_bibtex_fields_without_a_comma(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article{smith2024, title={Title}\n year={2024}}\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid fields", result.stdout)

    def test_accepts_bibtex_value_concatenation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                '@article{smith2024, title={Part A} # " and " # {Part B}, year=2024}\n',
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_bibtex_implicit_comments_and_quotes_in_braces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                'Implicit comment before the entry.\n@article{smith2024, title={A 6" telescope}, year=2024}\nImplicit comment after it.\n',
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_bibtex_comment_forms_and_braced_quotes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                '@comment\n@comment{opaque " comment}\n'
                '@article{smith2024, title="A {6" telescope}", year=2024}\n',
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_bibtex_string_and_preamble_directives(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            for directive in ('@string{abbr = "Journal"}', '@preamble{"Generated bibliography"}'):
                with self.subTest(directive=directive):
                    (workspace / "references.bib").write_text(
                        directive + "\n@article{smith2024, title={Title}, year=2024}\n",
                        encoding="utf-8",
                    )
                    result = subprocess.run(
                        [sys.executable, str(VALIDATOR), str(workspace)],
                        capture_output=True,
                        check=False,
                        text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("unsupported @", result.stdout)

    def test_rejects_tex_control_commands_in_bibtex_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                r"@article{smith2024, title={\input{payload}}, year=2024}" + "\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid fields", result.stdout)

    def test_rejects_repeated_trailing_commas_and_mixed_numeric_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            for bibliography in (
                "@article{smith2024, title={Title}, year=2024,,}\n",
                "@article{smith2024, title={Title}, year=123abc}\n",
            ):
                with self.subTest(bibliography=bibliography):
                    (workspace / "references.bib").write_text(bibliography, encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(VALIDATOR), str(workspace)],
                        capture_output=True,
                        check=False,
                        text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("invalid fields", result.stdout)

    def test_percent_prefix_does_not_hide_bibtex_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "% @article{smith2024, title={First}, year=2024}\n"
                "@article{smith2024, title={Second}, year=2024}\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate citation key", result.stdout)

    def test_rejects_case_only_citation_key_collisions(self) -> None:
        index_content = "\n".join(
            [
                HEADER,
                DELIMITER,
                "| Smith2024 | excluded | First | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test/1 |",
                "| smith2024 | excluded | Second | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test/2 |",
            ]
        )
        index_result = self.run_validator(index_content)
        self.assertNotEqual(index_result.returncode, 0)
        self.assertIn("case-insensitive citation key collision", index_result.stdout)

        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| Smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article{Smith2024, title={First}, year=2024}\n"
                "@article{smith2024, title={Second}, year=2024}\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            bib_result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(bib_result.returncode, 0)
        self.assertIn("case-insensitive citation key collision", bib_result.stdout)

    def test_rejects_linked_notes_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "paper"
            workspace.mkdir()
            (workspace / "paper_index.md").write_text("\n".join([HEADER, DELIMITER, PLACEHOLDER]), encoding="utf-8")
            (workspace / "references.bib").write_text("", encoding="utf-8")
            outside = root / "outside-notes"
            outside.mkdir()
            try:
                os.symlink(outside, workspace / "notes", target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory links unavailable: {exc}")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("filesystem links are not allowed", result.stdout)

    def test_rejects_linked_bibliography(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "paper"
            workspace.mkdir()
            (workspace / "paper_index.md").write_text(
                "\n".join([HEADER, DELIMITER, PLACEHOLDER]), encoding="utf-8"
            )
            outside = root / "outside.bib"
            outside.write_text("", encoding="utf-8")
            try:
                os.symlink(outside, workspace / "references.bib")
            except OSError as exc:
                self.skipTest(f"file links unavailable: {exc}")
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("filesystem links are not allowed", result.stdout)

    def test_rejects_direct_linked_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "paper"
            workspace.mkdir()
            outside = root / "outside-index.md"
            outside.write_text("\n".join([HEADER, DELIMITER, PLACEHOLDER]), encoding="utf-8")
            index = workspace / "paper_index.md"
            try:
                os.symlink(outside, index)
            except OSError as exc:
                self.skipTest(f"file links unavailable: {exc}")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(index)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("filesystem links are not allowed", result.stdout)

    def test_accepts_parenthesized_bibtex_with_parenthesis_in_braces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article(smith2024,\n  title={A ) B},\n  year={2024}\n)\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_unclosed_brace_in_parenthesized_bibtex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [HEADER, DELIMITER, "| smith2024 | selected | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |"]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text(
                "@article(smith2024, title={Unclosed )\n",
                encoding="utf-8",
            )
            (workspace / "notes").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unterminated @article", result.stdout)

    def test_ignores_table_inside_fenced_example(self) -> None:
        content = "\n".join(["```markdown", HEADER, DELIMITER, PLACEHOLDER, "```"])
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected table header not found", result.stdout)

    def test_malformed_fence_close_does_not_expose_table(self) -> None:
        content = "\n".join(
            ["```markdown", "example", "```not-a-valid-close", HEADER, DELIMITER, PLACEHOLDER]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected table header not found", result.stdout)

    def test_list_fence_cannot_close_a_top_level_fence(self) -> None:
        content = "\n".join(
            ["```markdown", "- ```", HEADER, DELIMITER, PLACEHOLDER, "```"]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected table header not found", result.stdout)

    def test_ignores_indented_code_table(self) -> None:
        content = "\n".join(f"    {line}" for line in (HEADER, DELIMITER, PLACEHOLDER))
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected table header not found", result.stdout)

    def test_comment_content_cannot_open_a_fence(self) -> None:
        content = "\n".join(["<!--", "```", "-->", HEADER, DELIMITER, PLACEHOLDER])
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inline_code_comment_marker_does_not_hide_table(self) -> None:
        content = "\n".join(["`<!--`", HEADER, DELIMITER, PLACEHOLDER])
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inline_html_comments_preserve_row_validation(self) -> None:
        valid = "\n".join(
            [
                HEADER,
                DELIMITER,
                "| smith2024 | excluded | A <!-- note --> Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        valid_result = self.run_validator(valid)
        self.assertEqual(valid_result.returncode, 0, valid_result.stdout + valid_result.stderr)

        malformed = "\n".join(
            [
                HEADER,
                DELIMITER,
                "| smith2024 | excluded | A <!-- note --> | extra | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        malformed_result = self.run_validator(malformed)
        self.assertNotEqual(malformed_result.returncode, 0)
        self.assertIn("expected 11 cells", malformed_result.stdout)

    def test_many_inline_html_comments_preserve_visible_content(self) -> None:
        title = "Title " + " ".join("<!-- note -->" for _ in range(4_000))
        content = "\n".join(
            [
                HEADER,
                DELIMITER,
                f"| smith2024 | excluded | {title} | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        result = self.run_validator(content)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_tables_in_frontmatter_raw_html_and_list_fences(self) -> None:
        variants = (
            "\n".join(["---", HEADER, DELIMITER, PLACEHOLDER, "---"]),
            "\n".join(["\ufeff---", HEADER, DELIMITER, PLACEHOLDER, "---"]),
            "\n".join(["<pre>", HEADER, DELIMITER, PLACEHOLDER, "</pre>"]),
            "\n".join(["<div>", HEADER, DELIMITER, PLACEHOLDER, "</div>"]),
            "\n".join(["<div", HEADER, DELIMITER, PLACEHOLDER]),
            "\n".join(["<div> wrapper", HEADER, DELIMITER, PLACEHOLDER]),
            "\n".join(["<script", HEADER, DELIMITER, PLACEHOLDER]),
            "\n".join(["<!DOCTYPE", HEADER, DELIMITER, PLACEHOLDER, ">"]),
            "\n".join(["<![CDATA[", HEADER, DELIMITER, PLACEHOLDER, "]]>"]),
            "\n".join(["- ```markdown", f"  {HEADER}", f"  {DELIMITER}", f"  {PLACEHOLDER}", "  ```"]),
        )
        for content in variants:
            with self.subTest(content=content.splitlines()[0]):
                result = self.run_validator(content)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("expected table header not found", result.stdout)

    def test_rejects_invalid_verification_shape(self) -> None:
        content = "\n".join(
            [
                HEADER,
                DELIMITER,
                "| smith2024 | selected | Title | 2024 | Journal | recently checked | background | context | reviewed | yes | https://example.test |",
            ]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid Verified on/version", result.stdout)

    def test_rejects_future_or_placeholder_verification(self) -> None:
        for verification in (
            "9999-12-31 / v1",
            "2026-07-31 / ---",
            "2026-07-31 / TODO",
            "2026-07-31 / TODO v2",
            "2026-07-31 / [TODO] verify",
            "2026-07-31 / unknown status",
            "2026-07-31 / unverified",
            "2026-07-31 / not verified",
            "2026-07-31 / not yet verified",
            "2026-07-31 / never checked",
            "20260731 / v1",
            "2026-W31-5 / v1",
        ):
            with self.subTest(verification=verification):
                content = "\n".join(
                    [
                        HEADER,
                        DELIMITER,
                        f"| smith2024 | selected | Title | 2024 | Journal | {verification} | background | context | reviewed | yes | https://example.test |",
                    ]
                )
                result = self.run_validator(content)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid Verified on/version", result.stdout)

    def test_rejects_placeholder_aliases_in_required_fields(self) -> None:
        base = [
            "smith2024",
            "excluded",
            "Title",
            "2024",
            "Journal",
            "2026-07-31 / v1",
            "background",
            "context",
            "reviewed",
            "unknown",
            "https://example.test",
        ]
        cases = (
            (2, "TBD", "Title"),
            (2, "TODO: fill title", "Title"),
            (2, "TODO later", "Title"),
            (4, "pending", "Formal source/status"),
            (4, "TBD after review", "Formal source/status"),
            (7, "unknown", "Claim/use"),
            (8, "[quality]", "Quality basis"),
            (10, "none", "URL/DOI"),
            (10, "TODO: add URL", "URL/DOI"),
        )
        for cell_index, placeholder, field in cases:
            with self.subTest(field=field):
                cells = base.copy()
                cells[cell_index] = placeholder
                content = "\n".join([HEADER, DELIMITER, "| " + " | ".join(cells) + " |"])
                result = self.run_validator(content)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"missing {field}", result.stdout)

    def test_rejects_placeholder_beside_completed_entry(self) -> None:
        content = "\n".join(
            [
                HEADER,
                DELIMITER,
                PLACEHOLDER,
                "| smith2024 | excluded | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("remove the placeholder row", result.stdout)

    def test_rejects_multiple_placeholder_rows(self) -> None:
        content = "\n".join([HEADER, DELIMITER, PLACEHOLDER, PLACEHOLDER])
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("only one placeholder row", result.stdout)

    def test_rejects_noncanonical_note_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join([HEADER, DELIMITER, PLACEHOLDER]), encoding="utf-8"
            )
            (workspace / "references.bib").write_text("", encoding="utf-8")
            notes = workspace / "notes"
            notes.mkdir()
            (notes / "orphan.txt").write_text("not a reading note\n", encoding="utf-8")
            (notes / "nested").mkdir()
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("noncanonical artifact: orphan.txt", result.stdout)
        self.assertIn("noncanonical artifact: nested", result.stdout)

    def test_rejects_reading_note_heading_key_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "paper_index.md").write_text(
                "\n".join(
                    [
                        HEADER,
                        DELIMITER,
                        "| smith2024 | excluded | Title | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
                    ]
                ),
                encoding="utf-8",
            )
            (workspace / "references.bib").write_text("", encoding="utf-8")
            notes = workspace / "notes"
            notes.mkdir()
            (notes / "smith2024.md").write_text(
                "# Reading Note: different-key\n", encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(workspace)],
                capture_output=True,
                check=False,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("heading key does not match filename: smith2024.md", result.stdout)

    def test_even_backslashes_do_not_escape_table_pipe(self) -> None:
        content = "\n".join(
            [
                HEADER,
                DELIMITER,
                r"| smith2024 | selected | A \\| B | 2024 | Journal | 2026-07-31 / v1 | background | context | reviewed | yes | https://example.test |",
            ]
        )
        result = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected 11 cells", result.stdout)


if __name__ == "__main__":
    unittest.main()
