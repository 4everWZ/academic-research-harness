from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_frontmatter_and_token_budget(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        keys = {line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line}
        self.assertEqual(keys, {"name", "description"})
        self.assertLessEqual(len(text.split()), 300)
        self.assertLessEqual(len(text), 4_000)
        for reference in (ROOT / "references").glob("*.md"):
            self.assertLessEqual(len(reference.read_text(encoding="utf-8")), 6_000)

    def test_all_local_markdown_links_resolve(self) -> None:
        markdown_files = [ROOT / "SKILL.md", *(ROOT / "references").glob("*.md")]
        for markdown in markdown_files:
            text = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target:
                    continue
                resolved = (markdown.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"broken link in {markdown}: {target}")

    def test_markdown_prose_is_not_hard_wrapped(self) -> None:
        markdown_files = [
            ROOT / "SKILL.md",
            *(ROOT / "references").glob("*.md"),
            *(ROOT / "assets" / "templates").glob("*.md"),
        ]
        for markdown in markdown_files:
            in_fence = False
            in_frontmatter = False
            previous_textual = False
            for line_number, line in enumerate(markdown.read_text(encoding="utf-8").splitlines(), start=1):
                stripped = line.strip()
                if line_number == 1 and stripped == "---":
                    in_frontmatter = True
                    previous_textual = False
                    continue
                if in_frontmatter:
                    if stripped == "---":
                        in_frontmatter = False
                    continue
                if stripped.startswith("```"):
                    in_fence = not in_fence
                    previous_textual = False
                    continue
                if in_fence:
                    continue
                is_list_item = bool(re.match(r"^(?:[-+*]|\d+[.)])\s+", stripped))
                is_structural = (
                    not stripped
                    or stripped.startswith(("#", "|", ">"))
                    or stripped == "---"
                    or line.startswith("    ")
                    or is_list_item
                )
                is_plain = not is_structural
                self.assertFalse(
                    is_plain and previous_textual,
                    f"hard-wrapped Markdown prose in {markdown}:{line_number}",
                )
                previous_textual = is_plain or is_list_item

    def test_ui_metadata_and_package_shape(self) -> None:
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Academic Research Harness"', metadata)
        self.assertIn("$academic-research-harness", metadata)
        self.assertRegex(metadata, r'short_description: "[^"\n]{25,64}"')
        self.assertFalse((ROOT / "README.md").exists())

        allowed = {
            ".git",
            ".gitignore",
            "SKILL.md",
            "VERSION",
            "LICENSE",
            "agents",
            "assets",
            "references",
            "scripts",
            "tests",
        }
        self.assertFalse({path.name for path in ROOT.iterdir()} - allowed)
        runtime_payload = sum(
            path.stat().st_size
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and not path.is_relative_to(ROOT / "tests")
            and not path.is_relative_to(ROOT / "assets" / "evals")
        )
        self.assertLessEqual(runtime_payload, 80_000)

    def test_route_reference_budgets(self) -> None:
        route_bundles = {
            "manuscript_drafting": ("results-to-paper.md", "writing-style.md"),
            "implementation_question": ("repo-to-paper.md",),
            "literature_index": ("literature.md", "evidence-and-citations.md", "workspace.md"),
            "claim_audit": ("evidence-and-citations.md", "literature.md", "repo-to-paper.md"),
        }
        for route, names in route_bundles.items():
            size = sum((ROOT / "references" / name).stat().st_size for name in names)
            self.assertLessEqual(size, 15_000, route)

    def test_supporting_references_are_reachable(self) -> None:
        pending = [ROOT / "SKILL.md"]
        visited: set[Path] = set()
        while pending:
            path = pending.pop().resolve()
            if path in visited:
                continue
            visited.add(path)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" not in target and target.endswith(".md"):
                    pending.append((path.parent / target).resolve())
        for reference in (ROOT / "references").glob("*.md"):
            self.assertIn(reference.resolve(), visited, f"unreachable reference: {reference}")


if __name__ == "__main__":
    unittest.main()
