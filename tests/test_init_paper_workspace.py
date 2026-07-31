from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = ROOT / "scripts" / "init_paper_workspace.py"
AUTHORITY = "user confirmation, 2026-07-31"


def load_initializer_module():
    spec = importlib.util.spec_from_file_location("init_paper_workspace_under_test", INITIALIZER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load initializer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InitPaperWorkspaceTests(unittest.TestCase):
    def run_initializer(self, workspace: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INITIALIZER),
                str(workspace),
                "--workspace-root",
                str(workspace.parent),
                *arguments,
            ],
            capture_output=True,
            check=False,
            text=True,
        )

    def test_creates_requested_artifacts_and_preserves_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--include", "literature,claims")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((workspace / "paper_index.md").is_file())
            self.assertTrue((workspace / "references.bib").is_file())
            self.assertTrue((workspace / "claims.md").is_file())
            self.assertTrue((workspace / "notes").is_dir())

            references = workspace / "references.bib"
            references.write_text("preserve me\n", encoding="utf-8")
            result = self.run_initializer(workspace, "--include", "literature")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(references.read_text(encoding="utf-8"), "preserve me\n")

    def test_venue_status_is_independent_of_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--include",
                "venue",
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            profile = (workspace / "venue_profile.md").read_text(encoding="utf-8")
            self.assertIn("**Status:** confirmed", profile)
            self.assertIn(f"**Decision authority/date:** {AUTHORITY}", profile)

    def test_suffix_rejects_existing_unsuffixed_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            result = self.run_initializer(
                workspace,
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
                "--suffix-venue",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot rename an existing workspace", result.stderr)

    def test_suffix_creates_new_venue_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
                "--suffix-venue",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((workspace.parent / "paper__target-venue" / "venue_profile.md").is_file())

    def test_explicit_slug_supports_non_latin_venue(self) -> None:
        module = load_initializer_module()
        self.assertEqual(module.slugify("Café"), module.slugify("Cafe\u0301"))
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "科学通报",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
                "--venue-slug",
                "science-bulletin",
                "--suffix-venue",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((workspace.parent / "paper__science-bulletin" / "venue_profile.md").is_file())

    def test_invalid_venue_slug_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "!!!",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
                "--suffix-venue",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("venue slug is empty", result.stderr)

    def test_suffix_requires_confirmed_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--venue", "Target Venue", "--suffix-venue")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires --venue-status confirmed", result.stderr)

    def test_confirmed_status_requires_decision_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires --venue-authority", result.stderr)
            self.assertFalse(workspace.exists())

    def test_changed_venue_requires_explicit_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            result = self.run_initializer(workspace, "--venue", "Renamed Venue")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--venue-status is required", result.stderr)
            profile = (workspace / "venue_profile.md").read_text(encoding="utf-8")
            self.assertIn("**Status:** confirmed", profile)
            self.assertIn("**Target venue or outlet:** Target Venue", profile)

    def test_confirmed_blank_profile_requires_explicit_rebinding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            profile = workspace / "venue_profile.md"
            profile.write_text(
                (ROOT / "assets" / "templates" / "venue_profile.md")
                .read_text(encoding="utf-8")
                .replace("provisional | confirmed", "confirmed"),
                encoding="utf-8",
            )
            result = self.run_initializer(workspace, "--venue", "Target Venue")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("incomplete confirmed venue profile", result.stderr)
            self.assertNotIn("Target Venue", profile.read_text(encoding="utf-8"))

            result = self.run_initializer(
                workspace,
                "--venue",
                "Target Venue",
                "--venue-status",
                "confirmed",
                "--venue-authority",
                AUTHORITY,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Target Venue", profile.read_text(encoding="utf-8"))

    def test_bare_venue_profile_can_be_completed_later(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--include", "venue")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            profile = (workspace / "venue_profile.md").read_text(encoding="utf-8")
            self.assertIn("**Status:** provisional", profile)
            self.assertNotIn("provisional | confirmed", profile)

            result = self.run_initializer(workspace, "--venue", "Target Venue")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            profile = (workspace / "venue_profile.md").read_text(encoding="utf-8")
            self.assertIn("**Status:** provisional", profile)
            self.assertIn("**Target venue or outlet:** Target Venue", profile)

    def test_venue_only_rerun_does_not_rewrite_existing_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--include", "venue")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            profile = workspace / "venue_profile.md"
            original = profile.read_bytes().replace(b"\n", b"\r\n")
            profile.write_bytes(original)
            profile.chmod(stat.S_IREAD)
            try:
                result = self.run_initializer(workspace, "--include", "venue")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(profile.read_bytes(), original)
            finally:
                profile.chmod(stat.S_IWRITE)

    def test_workspace_must_stay_within_allowed_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "allowed"
            root.mkdir()
            escaped = root.parent / "escaped"
            result = subprocess.run(
                [
                    sys.executable,
                    str(INITIALIZER),
                    str(escaped),
                    "--workspace-root",
                    str(root),
                    "--include",
                    "claims",
                ],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("workspace must stay within --workspace-root", result.stderr)
            self.assertFalse(escaped.exists())

    def test_malformed_profile_fails_before_other_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            (workspace / "venue_profile.md").write_text("# Invalid\n", encoding="utf-8")
            result = self.run_initializer(
                workspace,
                "--include",
                "literature",
                "--venue",
                "Target Venue",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((workspace / "paper_index.md").exists())
            self.assertFalse((workspace / "references.bib").exists())
            self.assertFalse((workspace / "notes").exists())

    def test_rejects_empty_operation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no artifacts or venue update requested", result.stderr)
            self.assertFalse(workspace.exists())

    def test_papers_include_does_not_write_git_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--include", "papers")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((workspace / "papers").is_dir())
            self.assertFalse((workspace / "papers" / ".gitignore").exists())

    def test_hard_linked_profile_is_replaced_without_external_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "paper"
            workspace.mkdir()
            outside = root / "outside.md"
            original = (ROOT / "assets" / "templates" / "venue_profile.md").read_text(encoding="utf-8").replace(
                "provisional | confirmed", "provisional"
            )
            outside.write_text(original, encoding="utf-8")
            try:
                os.link(outside, workspace / "venue_profile.md")
            except OSError as exc:
                self.skipTest(f"hard links unavailable: {exc}")

            result = self.run_initializer(workspace, "--venue", "Target Venue")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(outside.read_text(encoding="utf-8"), original)
            self.assertIn(
                "**Target venue or outlet:** Target Venue",
                (workspace / "venue_profile.md").read_text(encoding="utf-8"),
            )

    def test_late_profile_failure_rolls_back_new_artifacts(self) -> None:
        module = load_initializer_module()
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            profile = workspace / "venue_profile.md"
            profile.write_text(
                (ROOT / "assets" / "templates" / "venue_profile.md")
                .read_text(encoding="utf-8")
                .replace("provisional | confirmed", "provisional"),
                encoding="utf-8",
            )
            arguments = [
                str(INITIALIZER),
                str(workspace),
                "--workspace-root",
                str(workspace.parent),
                "--include",
                "literature",
                "--venue",
                "Target Venue",
            ]
            with (
                mock.patch.object(module, "atomic_write_text", side_effect=OSError("simulated late failure")),
                mock.patch.object(sys, "argv", arguments),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                module.main()
            self.assertFalse((workspace / "paper_index.md").exists())
            self.assertFalse((workspace / "references.bib").exists())
            self.assertFalse((workspace / "notes").exists())

    def test_partial_workspace_creation_failure_rolls_back_parent(self) -> None:
        module = load_initializer_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "new-parent" / "paper"
            real_mkdir = Path.mkdir

            def fail_on_workspace(path: Path, *args, **kwargs):
                if path == workspace:
                    raise OSError("simulated final-directory failure")
                return real_mkdir(path, *args, **kwargs)

            arguments = [
                str(INITIALIZER),
                str(workspace),
                "--workspace-root",
                str(root),
                "--include",
                "claims",
            ]
            with (
                mock.patch.object(module.Path, "mkdir", autospec=True, side_effect=fail_on_workspace),
                mock.patch.object(sys, "argv", arguments),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                module.main()
            self.assertFalse((root / "new-parent").exists())

    def test_keyboard_interrupt_rolls_back_created_workspace(self) -> None:
        module = load_initializer_module()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "paper"
            arguments = [
                str(INITIALIZER),
                str(workspace),
                "--workspace-root",
                str(root),
                "--include",
                "literature",
            ]
            with (
                mock.patch.object(module.shutil, "copyfileobj", side_effect=KeyboardInterrupt),
                mock.patch.object(sys, "argv", arguments),
                self.assertRaises(KeyboardInterrupt),
            ):
                module.main()
            self.assertFalse(workspace.exists())

    def test_interrupt_after_profile_replace_restores_existing_profile(self) -> None:
        module = load_initializer_module()
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            profile = workspace / "venue_profile.md"
            original = (ROOT / "assets" / "templates" / "venue_profile.md").read_text(
                encoding="utf-8"
            ).replace("provisional | confirmed", "provisional")
            profile.write_text(original, encoding="utf-8")
            real_atomic_write = module.atomic_write_text

            def replace_then_interrupt(path: Path, text: str) -> None:
                real_atomic_write(path, text)
                raise KeyboardInterrupt

            arguments = [
                str(INITIALIZER),
                str(workspace),
                "--workspace-root",
                str(workspace.parent),
                "--include",
                "claims",
                "--venue",
                "Target Venue",
            ]
            with (
                mock.patch.object(module, "atomic_write_text", side_effect=replace_then_interrupt),
                mock.patch.object(sys, "argv", arguments),
                self.assertRaises(KeyboardInterrupt),
            ):
                module.main()
            self.assertEqual(profile.read_text(encoding="utf-8"), original)
            self.assertFalse((workspace / "claims.md").exists())

    def test_backslash_in_venue_is_written_literally(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--venue", "A\\B")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            profile = (workspace / "venue_profile.md").read_text(encoding="utf-8")
            self.assertIn("**Target venue or outlet:** A\\B", profile)

    def test_rejects_existing_linked_artifact_directories(self) -> None:
        for artifact, include in (("notes", "literature"), ("papers", "papers")):
            with self.subTest(artifact=artifact), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                workspace = root / "paper"
                workspace.mkdir()
                outside = root / f"outside-{artifact}"
                outside.mkdir()
                try:
                    os.symlink(outside, workspace / artifact, target_is_directory=True)
                except OSError as exc:
                    self.skipTest(f"directory links unavailable: {exc}")
                result = self.run_initializer(workspace, "--include", include)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("filesystem links are not allowed", result.stderr)

    def test_rejects_control_characters_in_venue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(workspace, "--venue", "Injected\n- **Status:** confirmed")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("single line without control characters", result.stderr)
            self.assertFalse(workspace.exists())

    def test_rejects_unicode_line_separators_in_venue(self) -> None:
        for separator in ("\u0085", "\u2028", "\u2029"):
            with self.subTest(separator=ord(separator)), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "paper"
                result = self.run_initializer(workspace, "--venue", f"First{separator}Second")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("single line without control characters", result.stderr)
                self.assertFalse(workspace.exists())

    def test_rejects_markdown_and_bidi_controls_in_venue(self) -> None:
        cases = (("Target<!-- hidden -->", "Markdown control syntax"), ("Target\u202eabc", "control characters"))
        for venue, message in cases:
            with self.subTest(venue=venue), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "paper"
                result = self.run_initializer(workspace, "--venue", venue)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertFalse(workspace.exists())

    def test_rejects_hidden_venue_profile_fields(self) -> None:
        canonical = (
            (ROOT / "assets" / "templates" / "venue_profile.md")
            .read_text(encoding="utf-8")
            .replace("provisional | confirmed", "confirmed")
            .replace("**Decision authority/date:**", f"**Decision authority/date:** {AUTHORITY}")
            .replace("**Target venue or outlet:**", "**Target venue or outlet:** Target Venue")
        )
        variants = (f"<!--\n{canonical}\n-->\n", f"```markdown\n{canonical}\n```\n", f"<div>\n{canonical}\n</div>\n")
        for content in variants:
            with self.subTest(prefix=content.splitlines()[0]), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "paper"
                workspace.mkdir()
                (workspace / "venue_profile.md").write_text(content, encoding="utf-8")
                result = self.run_initializer(workspace, "--include", "venue")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("canonical visible header and field block", result.stderr)

    def test_rejects_blank_venue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            result = self.run_initializer(
                workspace,
                "--venue",
                "   ",
                "--venue-status",
                "confirmed",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("venue must not be blank", result.stderr)
            self.assertFalse(workspace.exists())

    def test_rejects_duplicate_venue_profile_fields_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "paper"
            workspace.mkdir()
            profile = (
                (ROOT / "assets" / "templates" / "venue_profile.md")
                .read_text(encoding="utf-8")
                .replace("provisional | confirmed", "provisional")
            )
            (workspace / "venue_profile.md").write_text(
                profile + "\n- **Status:** confirmed\n",
                encoding="utf-8",
            )
            result = self.run_initializer(
                workspace,
                "--include",
                "literature",
                "--venue",
                "Target Venue",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("canonical visible field: Status", result.stderr)
            self.assertFalse((workspace / "paper_index.md").exists())


if __name__ == "__main__":
    unittest.main()
