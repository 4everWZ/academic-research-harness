from __future__ import annotations

import contextlib
import io
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = ROOT / "scripts" / "init_paper_project.py"


def path_state(path: Path) -> tuple:
    """Compare contents and metadata without hashes or access-time noise."""
    info = path.lstat()
    metadata = (info.st_mode, info.st_size, info.st_mtime_ns, info.st_ino)
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        return ("link", metadata, os.readlink(path))
    if path.is_dir():
        return ("directory", metadata)
    return ("file", metadata, path.read_bytes())


def tree_state(root: Path) -> dict[str, tuple]:
    """Include Git metadata, ignored files, and empty directories; never follow links."""
    state = {".": path_state(root)}
    if state["."][0] == "directory":
        for entry in root.iterdir():
            for relative, value in tree_state(entry).items():
                name = entry.name if relative == "." else f"{entry.name}/{relative}"
                state[name] = value
    return state


class InitPaperProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_root = ROOT / "tmp"
        temporary_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="paper-project-test-", dir=temporary_root)
        self.addCleanup(temporary.cleanup)
        self.fixture = Path(temporary.name).resolve()
        self.projects = self.fixture / "projects"
        self.projects.mkdir()
        self.caller = self.fixture / "unrelated-cwd"
        self.caller.mkdir()
        template = self.fixture / "empty-git-template"
        template.mkdir()
        # In particular, inherited GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE,
        # GIT_COMMON_DIR and GIT_CONFIG_* must not redirect fixture commands.
        self.env = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
        self.env.update(
            GIT_CEILING_DIRECTORIES=str(self.fixture),
            GIT_CONFIG_NOSYSTEM="1",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_TEMPLATE_DIR=str(template),
            GIT_OPTIONAL_LOCKS="0",
            GIT_TERMINAL_PROMPT="0",
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONUTF8="1",
            TMP=str(self.fixture),
            TEMP=str(self.fixture),
            TMPDIR=str(self.fixture),
        )
        self.code = self.projects / "analysis-engine"
        self.init_repo(self.code)
        (self.code / "src").mkdir()
        (self.code / "src" / "model.py").write_bytes(b"answer = 41\n")
        (self.code / ".gitignore").write_bytes(b"cache/\n")
        self.git(self.code, "add", ".gitignore", "src/model.py")
        (self.code / "src" / "model.py").write_bytes(b"answer = 42\n")
        (self.code / "untracked.txt").write_bytes(b"keep untracked research\n")
        (self.code / "cache").mkdir()
        (self.code / "cache" / "result.bin").write_bytes(b"\x00\x01ignored output\xff")

    def git(self, cwd: Path, *arguments: str, check: bool = True, **kwargs) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *map(str, arguments)],
            cwd=cwd,
            env=kwargs.pop("env", self.env),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            **kwargs,
        )
        if check:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def init_repo(self, path: Path, *, bare: bool = False) -> Path:
        arguments = ["init", "--quiet"]
        if bare:
            arguments.append("--bare")
        self.git(self.fixture, *arguments, str(path))
        return path

    def commit_fixture(self, repo: Path) -> None:
        # Identity is scoped to the commit needed by worktree/submodule fixtures.
        identity = dict(
            self.env,
            GIT_AUTHOR_NAME="Fixture Author",
            GIT_AUTHOR_EMAIL="fixture@example.invalid",
            GIT_COMMITTER_NAME="Fixture Author",
            GIT_COMMITTER_EMAIL="fixture@example.invalid",
        )
        self.git(repo, "commit", "--quiet", "--allow-empty", "-m", "Fixture for linked checkout", env=identity)

    def source_state(self) -> tuple:
        status = self.git(self.code, "status", "--porcelain=v1", "--untracked-files=all").stdout
        return tree_state(self.code), status

    def run_initializer(
        self,
        paper: Path | str,
        *,
        code_root: Path | str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        before = self.source_state()
        result = subprocess.run(
            [sys.executable, "-B", str(INITIALIZER), str(paper), "--code-root", str(code_root or self.code)],
            cwd=self.caller,
            env=env if env is not None else self.env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(self.source_state(), before, "initializer changed source files, metadata, or Git status")
        return result

    def assert_success(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((result.stdout + result.stderr).strip(), "failure needs a diagnostic")

    def assert_independent_repo(self, paper: Path) -> None:
        self.assertTrue((paper / ".git").is_dir())
        top = Path(self.git(paper, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
        self.assertEqual(top, paper.resolve())
        for option in ("--git-dir", "--git-common-dir"):
            directory = Path(self.git(paper, "rev-parse", option).stdout.strip())
            self.assertEqual((paper / directory).resolve(), (paper / ".git").resolve())

    def assert_no_commit_or_remote(self, paper: Path) -> None:
        self.assertNotEqual(self.git(paper, "rev-parse", "--verify", "HEAD", check=False).returncode, 0)
        self.assertEqual(self.git(paper, "remote").stdout.strip(), "")
        self.assertEqual(self.git(paper, "ls-files").stdout, "", "initializer must not stage starter files")

    def assert_original_files(self, root: Path, before: dict[str, tuple]) -> None:
        for name, original in before.items():
            if original[0] != "directory":
                self.assertEqual(path_state(root / name), original, f"existing file changed: {name}")

    def test_relative_slug_is_verbatim_and_resolves_from_actual_code_root(self) -> None:
        slug = "My Paper_Évaluation.v2"
        code_argument = os.path.relpath(self.code / "src", self.caller)
        before_siblings = {entry.name for entry in self.projects.iterdir()}
        result = self.run_initializer(slug, code_root=code_argument)
        self.assert_success(result)
        paper = self.projects / slug
        self.assertEqual({entry.name for entry in self.projects.iterdir()}, before_siblings | {slug})
        self.assertEqual({entry.name for entry in paper.iterdir()}, {".git", "README.md", ".gitignore"})
        self.assertFalse((self.caller / slug).exists())
        self.assert_independent_repo(paper)
        self.assert_no_commit_or_remote(paper)

    def test_absolute_target_outside_code_siblings_is_allowed(self) -> None:
        destination = self.fixture / "separate-area"
        destination.mkdir()
        paper = destination / "Explicit Article"
        self.assert_success(self.run_initializer(paper, code_root=self.code / "src"))
        self.assert_independent_repo(paper)
        self.assert_no_commit_or_remote(paper)

    def test_relative_nested_target_uses_existing_parent(self) -> None:
        (self.projects / "papers").mkdir()
        paper = self.projects / "papers" / "Keep_This.Name"
        self.assert_success(self.run_initializer("papers/Keep_This.Name"))
        self.assert_independent_repo(paper)

    def test_sibling_with_code_name_prefix_is_not_mistaken_for_descendant(self) -> None:
        paper = self.projects / f"{self.code.name}-paper"
        self.assert_success(self.run_initializer(paper))
        self.assert_independent_repo(paper)

    def test_missing_target_parent_is_rejected_without_creating_parents(self) -> None:
        for paper in ("missing/Article", self.fixture / "absent" / "Article"):
            with self.subTest(paper=paper):
                target = self.projects / paper
                self.assert_rejected(self.run_initializer(paper))
                self.assertFalse(target.parent.exists())

    def test_existing_non_git_directory_preserves_all_original_files(self) -> None:
        paper = self.projects / "existing-paper"
        (paper / "figures").mkdir(parents=True)
        (paper / "manuscript.tex").write_bytes(b"\\documentclass{article}\r\n% author draft\r\n")
        (paper / "references.bib").write_bytes(b"@article{result, title={Existing result}}\n")
        (paper / "figures" / "final.pdf").write_bytes(b"%PDF-1.4\nkeep final figure\n")
        (paper / ".private-notes").write_bytes(b"keep hidden notes\x00\xff")
        before = tree_state(paper)
        self.assertNotEqual(self.git(paper, "rev-parse", "--show-toplevel", check=False).returncode, 0)
        self.assert_success(self.run_initializer(paper))
        self.assert_original_files(paper, before)
        self.assertEqual(
            {entry.name for entry in paper.iterdir()},
            {"figures", "manuscript.tex", "references.bib", ".private-notes", ".git", "README.md", ".gitignore"},
        )
        self.assert_independent_repo(paper)
        self.assert_no_commit_or_remote(paper)

    def test_existing_starter_files_are_never_overwritten_even_when_empty(self) -> None:
        for contents in (b"", b"author-owned\r\n\xff\x00"):
            with self.subTest(contents=contents):
                paper = self.projects / ("empty-starters" if not contents else "custom-starters")
                paper.mkdir()
                for name in ("README.md", ".gitignore"):
                    (paper / name).write_bytes(contents)
                before = tree_state(paper)
                self.assert_success(self.run_initializer(paper))
                self.assert_original_files(paper, before)
                self.assert_independent_repo(paper)

    def test_existing_independent_repo_is_reused_without_git_init(self) -> None:
        paper = self.init_repo(self.projects / "existing-repo")
        self.git(paper, "config", "paper.preserve", "local setting")
        (paper / "README.md").write_bytes(b"# Author README\r\n")
        (paper / ".gitignore").write_bytes(b"author-cache/\r\n")
        (paper / "draft.tex").write_bytes(b"keep draft\n")
        self.git(paper, "add", "draft.tex")
        (paper / "draft.tex").write_bytes(b"keep unstaged draft edit\n")
        before = tree_state(paper)
        status = self.git(paper, "status", "--porcelain=v1", "--untracked-files=all").stdout
        trace = self.fixture / "reuse-git-trace.log"
        self.assert_success(self.run_initializer(paper, env=dict(self.env, GIT_TRACE=str(trace))))
        self.assertEqual(tree_state(paper), before)
        self.assertEqual(self.git(paper, "status", "--porcelain=v1", "--untracked-files=all").stdout, status)
        self.assertNotRegex(trace.read_text(encoding="utf-8"), r"(?m)built-in: git (?:.* )?init(?:\s|$)")
        self.assert_independent_repo(paper)

    def test_existing_repo_only_adds_missing_starter_files(self) -> None:
        for existing in ((), ("README.md",), (".gitignore",)):
            with self.subTest(existing=existing):
                paper = self.init_repo(self.projects / f"missing-starters-{len(existing)}-{'readme' if 'README.md' in existing else 'ignore'}")
                for name in existing:
                    (paper / name).write_bytes(b"author file\r\n")
                (paper / "notes.txt").write_bytes(b"keep notes\n")
                before = tree_state(paper)
                git_before = tree_state(paper / ".git")
                self.assert_success(self.run_initializer(paper))
                self.assert_original_files(paper, before)
                self.assertEqual(tree_state(paper / ".git"), git_before)
                self.assertTrue((paper / "README.md").is_file())
                self.assertTrue((paper / ".gitignore").is_file())
                self.assert_no_commit_or_remote(paper)

    def test_second_invocation_is_a_no_op(self) -> None:
        paper = self.projects / "repeat-paper"
        self.assert_success(self.run_initializer(paper))
        before = tree_state(paper)
        self.assert_success(self.run_initializer(paper))
        self.assertEqual(tree_state(paper), before)

    def test_gitignore_ignores_intermediates_but_keeps_shareable_assets(self) -> None:
        paper = self.projects / "ignore-policy"
        self.assert_success(self.run_initializer(paper))
        ignored = {
            "tmp/scratch.txt", "tmp/nested/run.json", "manuscript.aux", "manuscript.log",
            "manuscript.out", "manuscript.toc", "manuscript.fls", "manuscript.fdb_latexmk",
            "manuscript.synctex.gz", "chapters/intro.aux", "chapters/intro.log",
        }
        retained = {
            "manuscript.tex", "chapters/intro.tex", "manuscript.pdf", "references.bib",
            "Bib/references.bib", "figures/final.pdf", "images/plot.png", "images/photo.jpg",
            "figures/diagram.svg", "README.md",
        }
        result = self.git(paper, "check-ignore", "--no-index", "--stdin", "-z", input="\0".join(sorted(ignored | retained)) + "\0")
        self.assertEqual(set(result.stdout.rstrip("\0").split("\0")), ignored)

    def test_readme_describes_self_contained_paper_and_relative_code_link(self) -> None:
        destination = self.fixture / "elsewhere" / "papers"
        destination.mkdir(parents=True)
        paper = destination / "Article"
        self.assert_success(self.run_initializer(paper))
        readme = (paper / "README.md").read_text(encoding="utf-8")
        self.assertRegex(readme.lower(), r"manuscript|\.tex\b")
        self.assertRegex(readme.lower(), r"bibliograph|bibtex|\.bib\b")
        self.assertRegex(readme.lower(), r"final[\s\S]{0,80}figur|figur[\s\S]{0,80}final")
        self.assertRegex(readme.lower(), r"self[ -]contained|stand[ -]?alone|without[\s\S]{0,40}code")
        normalized = unquote(readme).replace("\\", "/")
        self.assertNotIn(self.code.as_posix(), normalized)
        self.assertNotIn(self.fixture.as_posix(), normalized)
        links = re.findall(r"\[[^\]]*\]\(\s*<?([^\n)>]+)>?\s*\)", readme)
        destinations = [urlsplit(unquote(link.strip())) for link in links]
        self.assertTrue(
            any(
                not link.scheme and not link.netloc and not Path(link.path).is_absolute()
                and (paper / link.path).resolve() == self.code.resolve()
                for link in destinations
            ),
            "README needs a relative Markdown link to the actual code repository",
        )

    def test_copy_outside_sibling_layout_keeps_manuscript_bibliography_and_figure(self) -> None:
        paper = self.projects / "shareable-paper"
        self.assert_success(self.run_initializer(paper))
        (paper / "figures").mkdir()
        assets = {
            "manuscript.tex": (
                b"\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"
                b"Result~\\cite{result}.\\includegraphics{figures/final.pdf}\n"
                b"\\bibliography{references}\n\\end{document}\n"
            ),
            "references.bib": b"@article{result, title={Self-contained result}, year={2026}}\n",
            "figures/final.pdf": b"%PDF-1.4\n% final figure fixture\n%%EOF\n",
        }
        for name, content in assets.items():
            (paper / name).write_bytes(content)
        visible = self.git(paper, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
        self.assertTrue(set(assets).issubset(visible))
        shared_parent = self.fixture / "recipient" / "independent-location"
        shared_parent.mkdir(parents=True)
        shared = shared_parent / "received-paper"
        shutil.copytree(paper, shared, ignore=shutil.ignore_patterns(".git", "tmp"))
        for name, content in assets.items():
            self.assertEqual((shared / name).read_bytes(), content)
            self.assertEqual(path_state(shared / name)[0], "file")
        manuscript = (shared / "manuscript.tex").read_text(encoding="utf-8")
        figure = re.search(r"\\includegraphics\{([^}]+)\}", manuscript).group(1)
        bibliography = re.search(r"\\bibliography\{([^}]+)\}", manuscript).group(1) + ".bib"
        for name in (figure, bibliography):
            resolved = (shared / name).resolve()
            self.assertTrue(resolved.is_relative_to(shared.resolve()))
            self.assertTrue(resolved.is_file())
        self.assertFalse((shared.parent / self.code.name).exists(), "recipient must not need sibling code")
        self.assertNotEqual(self.git(shared, "rev-parse", "--show-toplevel", check=False).returncode, 0)

    def test_rejects_targets_inside_equal_to_or_ancestors_of_code(self) -> None:
        for target in (self.code / "paper", self.code / "src", self.code, self.projects, self.fixture):
            with self.subTest(target=target):
                before = tree_state(target) if target.exists() else None
                self.assert_rejected(self.run_initializer(target))
                if before is None:
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual(tree_state(target), before)

    def test_rejects_file_targets_and_file_parents(self) -> None:
        target = self.projects / "paper-file"
        target.write_bytes(b"not a directory\x00\xff")
        before = path_state(target)
        for argument in (target, target / "paper"):
            with self.subTest(argument=argument):
                self.assert_rejected(self.run_initializer(argument))
                self.assertEqual(path_state(target), before)

    def test_rejects_non_git_missing_and_file_code_roots(self) -> None:
        non_git = self.fixture / "not-code"
        non_git.mkdir()
        code_file = non_git / "source.py"
        code_file.write_bytes(b"answer = 42\n")
        for index, code in enumerate((non_git, self.fixture / "absent-code", code_file)):
            with self.subTest(code=code):
                target = self.projects / f"invalid-code-{index}"
                self.assert_rejected(self.run_initializer(target, code_root=code))
                self.assertFalse(target.exists())

    def test_rejects_bare_git_as_code_or_paper(self) -> None:
        bare = self.init_repo(self.fixture / "bare.git", bare=True)
        before = tree_state(bare)
        self.assert_rejected(self.run_initializer(bare))
        target = self.projects / "from-bare"
        self.assert_rejected(self.run_initializer(target, code_root=bare))
        self.assertFalse(target.exists())
        self.assertEqual(tree_state(bare), before)

    def test_rejects_target_enclosed_by_foreign_repository(self) -> None:
        foreign = self.init_repo(self.fixture / "foreign")
        existing = foreign / "existing-paper"
        existing.mkdir()
        (existing / "draft.tex").write_bytes(b"foreign draft\n")
        for target in (foreign / "absent-paper", existing):
            with self.subTest(target=target):
                before = tree_state(foreign)
                self.assert_rejected(self.run_initializer(target))
                self.assertEqual(tree_state(foreign), before)

    def test_rejects_independent_repo_nested_in_foreign_repository(self) -> None:
        foreign = self.init_repo(self.fixture / "foreign")
        nested = self.init_repo(foreign / "nested-paper")
        before = tree_state(foreign)
        self.assert_rejected(self.run_initializer(nested))
        self.assertEqual(tree_state(foreign), before)

    def test_rejects_worktree_paper_and_targets_inside_worktrees(self) -> None:
        owner = self.init_repo(self.fixture / "worktree-owner")
        self.commit_fixture(owner)
        worktree = self.fixture / "linked-worktree"
        self.git(owner, "worktree", "add", "--quiet", "--detach", str(worktree))
        before_owner, before_worktree = tree_state(owner), tree_state(worktree)
        for target in (worktree, worktree / "new-paper"):
            with self.subTest(target=target):
                self.assert_rejected(self.run_initializer(target))
        self.assertEqual(tree_state(owner), before_owner)
        self.assertEqual(tree_state(worktree), before_worktree)

    def test_rejects_submodule_paper_and_targets_inside_submodules(self) -> None:
        origin = self.init_repo(self.fixture / "submodule-origin")
        self.commit_fixture(origin)
        parent = self.init_repo(self.fixture / "superproject")
        self.git(parent, "-c", "protocol.file.allow=always", "submodule", "add", "--quiet", str(origin), "paper-module")
        submodule = parent / "paper-module"
        before_parent, before_origin = tree_state(parent), tree_state(origin)
        for target in (submodule, submodule / "new-paper"):
            with self.subTest(target=target):
                self.assert_rejected(self.run_initializer(target))
        self.assertEqual(tree_state(parent), before_parent)
        self.assertEqual(tree_state(origin), before_origin)

    def make_directory_link(self, link: Path, target: Path, *, junction: bool = False) -> None:
        if junction:
            if os.name != "nt":
                self.skipTest("Windows junction fixture")
            # Native PowerShell avoids requiring Windows symlink privileges.
            quote = lambda path: "'" + str(path).replace("'", "''") + "'"
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                 f"New-Item -ItemType Junction -Path {quote(link)} -Target {quote(target)} -ErrorAction Stop | Out-Null"],
                cwd=self.fixture, env=self.env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")
        self.addCleanup(lambda: link.rmdir() if junction else link.unlink())

    def check_linked_paths_rejected(self, *, junction: bool) -> None:
        destination = self.fixture / "real-destination"
        destination.mkdir()
        (destination / "keep.txt").write_bytes(b"untouched link destination\n")
        alias = self.fixture / "paper-alias"
        self.make_directory_link(alias, destination, junction=junction)
        before = tree_state(destination)
        for target in (alias, alias / "new-paper"):
            with self.subTest(target=target):
                self.assert_rejected(self.run_initializer(target))
                self.assertEqual(tree_state(destination), before)
        code_alias = self.fixture / "code-alias"
        self.make_directory_link(code_alias, self.code, junction=junction)
        for code in (code_alias, code_alias / "src"):
            with self.subTest(code=code):
                target = self.projects / "from-linked-code"
                self.assert_rejected(self.run_initializer(target, code_root=code))
                self.assertFalse(target.exists())

    def test_rejects_directory_symlinks_and_linked_ancestors(self) -> None:
        self.check_linked_paths_rejected(junction=False)

    @unittest.skipUnless(os.name == "nt", "Windows junction fixture")
    def test_rejects_junctions_and_junction_ancestors(self) -> None:
        self.check_linked_paths_rejected(junction=True)

    def test_rejects_symlinked_starter_files_without_touching_referents(self) -> None:
        for name in ("README.md", ".gitignore"):
            with self.subTest(name=name):
                paper = self.projects / ("linked-readme" if name == "README.md" else "linked-ignore")
                paper.mkdir()
                outside = self.fixture / f"original-{paper.name}"
                outside.write_bytes(b"external author file\r\n")
                try:
                    (paper / name).symlink_to(outside)
                except OSError as exc:
                    self.skipTest(f"file symlinks unavailable: {exc}")
                before, original = tree_state(paper), path_state(outside)
                self.assert_rejected(self.run_initializer(paper))
                self.assertEqual(tree_state(paper), before)
                self.assertEqual(path_state(outside), original)

    def test_rejects_dangling_target_link_without_creating_referent(self) -> None:
        target = self.projects / "dangling-paper"
        referent = self.fixture / "missing-referent"
        self.make_directory_link(target, referent)
        before = path_state(target)
        self.assert_rejected(self.run_initializer(target))
        self.assertEqual(path_state(target), before)
        self.assertFalse(referent.exists())

    def test_rejects_directory_in_place_of_starter_file_before_git_init(self) -> None:
        for name in ("README.md", ".gitignore"):
            with self.subTest(name=name):
                paper = self.projects / ("readme-directory" if name == "README.md" else "ignore-directory")
                (paper / name).mkdir(parents=True)
                (paper / name / "keep.txt").write_bytes(b"preserve directory contents\n")
                before = tree_state(paper)
                self.assert_rejected(self.run_initializer(paper))
                self.assertEqual(tree_state(paper), before)

    def test_rejects_linked_git_metadata_without_changing_either_repository(self) -> None:
        owner = self.init_repo(self.fixture / "metadata-owner")
        paper = self.projects / "linked-metadata"
        paper.mkdir()
        self.make_directory_link(paper / ".git", owner / ".git", junction=os.name == "nt")
        before_owner, before_paper = tree_state(owner), tree_state(paper)
        self.assert_rejected(self.run_initializer(paper))
        self.assertEqual(tree_state(owner), before_owner)
        self.assertEqual(tree_state(paper), before_paper)

    def test_missing_git_is_nonzero_and_preserves_existing_paper(self) -> None:
        for existing in (False, True):
            with self.subTest(existing=existing):
                paper = self.projects / f"missing-git-{existing}"
                before = None
                if existing:
                    paper.mkdir()
                    (paper / "draft.tex").write_bytes(b"precious draft\n")
                    before = tree_state(paper)
                result = self.run_initializer(paper, env=dict(self.env, PATH=str(self.fixture / "empty-path")))
                self.assert_rejected(result)
                self.assertRegex((result.stdout + result.stderr).lower(), r"git")
                if before is not None:
                    self.assert_original_files(paper, before)
                self.assertFalse((paper / "README.md").exists())

    def run_with_failed_git_init(self, paper: Path, *, missing: bool, leave_partial: bool = False) -> subprocess.CompletedProcess[str]:
        """Keep real Git discovery; inject only the init failure through run()."""
        real_run = subprocess.run
        attempts = []

        def intercepted(command, *args, **kwargs):
            if isinstance(command, (list, tuple)) and Path(str(command[0])).stem.lower() == "git" and "init" in command[1:]:
                attempts.append(command)
                if missing:
                    raise FileNotFoundError("git executable disappeared before init")
                if leave_partial:
                    partial = paper / ".git"
                    partial.mkdir(exist_ok=True)
                    (partial / "partial-init").write_bytes(b"incomplete Git initialization\n")
                message = "injected git init failure: fixture storage error"
                if kwargs.get("check"):
                    raise subprocess.CalledProcessError(73, command, output="", stderr=message)
                return subprocess.CompletedProcess(command, 73, stdout="", stderr=message)
            return real_run(command, *args, **kwargs)

        before = self.source_state()
        stdout, stderr = io.StringIO(), io.StringIO()
        arguments = [str(INITIALIZER), str(paper), "--code-root", str(self.code)]
        with (
            mock.patch.dict(os.environ, self.env, clear=True),
            mock.patch.object(sys, "argv", arguments),
            mock.patch.object(sys, "dont_write_bytecode", True),
            mock.patch.object(subprocess, "run", side_effect=intercepted),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            try:
                runpy.run_path(str(INITIALIZER), run_name="__main__")
            except SystemExit as exc:
                returncode = exc.code if isinstance(exc.code, int) else int(exc.code is not None)
                if isinstance(exc.code, str):
                    stderr.write(exc.code)
            else:
                returncode = 0
        self.assertTrue(attempts, "failure injection must exercise git init")
        self.assertEqual(self.source_state(), before)
        return subprocess.CompletedProcess(arguments, returncode, stdout.getvalue(), stderr.getvalue())

    def test_git_init_failure_preserves_original_paper_contents(self) -> None:
        for missing in (False, True):
            with self.subTest(missing=missing):
                paper = self.projects / f"failed-init-{missing}"
                (paper / "figures").mkdir(parents=True)
                (paper / "draft.tex").write_bytes(b"author manuscript\r\n")
                (paper / "README.md").write_bytes(b"author README\r\n")
                (paper / ".gitignore").write_bytes(b"author-cache/\r\n")
                (paper / "figures" / "final.pdf").write_bytes(b"%PDF-preserve figure\n")
                before = tree_state(paper)
                result = self.run_with_failed_git_init(paper, missing=missing)
                self.assert_rejected(result)
                self.assert_original_files(paper, before)
                self.assertRegex((result.stdout + result.stderr).lower(), r"git|initializ")

    def test_failed_init_reports_residual_directory_and_does_not_claim_success(self) -> None:
        for missing in (False, True):
            with self.subTest(missing=missing):
                paper = self.projects / f"partial-new-paper-{missing}"
                result = self.run_with_failed_git_init(paper, missing=missing, leave_partial=True)
                self.assert_rejected(result)
                diagnostic = result.stdout + result.stderr
                self.assertTrue(paper.is_dir(), "failed initialization retains its directory for inspection")
                self.assertIn(paper.name, diagnostic, "failure should identify the directory left for inspection")
                self.assertRegex(diagnostic.lower(), r"remain|left|inspect|retained|incomplete")
                if not missing:
                    self.assertIn("injected git init failure", diagnostic)
                    self.assertEqual(
                        (paper / ".git" / "partial-init").read_bytes(),
                        b"incomplete Git initialization\n",
                        "partial Git metadata must remain available for inspection",
                    )
                    self.assertIn(".git", diagnostic)
                for name in ("README.md", ".gitignore"):
                    self.assertFalse((paper / name).exists(), "starter files must not be written after failed git init")
                self.assertNotRegex(diagnostic.lower(), r"successfully (?:initialized|created)|(?:initialized|created) successfully")


if __name__ == "__main__":
    unittest.main()
