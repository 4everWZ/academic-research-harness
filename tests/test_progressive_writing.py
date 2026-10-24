from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from eval_support.progressive_writing import FIXTURE, ROOT, SUITE, audit, prepare, record


class ProgressiveWritingTests(unittest.TestCase):
    """Check retained cases and evidence tooling, not language-model behavior."""

    def setUp(self) -> None:
        temp_root = (ROOT / "tmp").resolve()
        self.assertTrue(temp_root.is_relative_to(ROOT.resolve()))
        temp_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="progressive-tests-", dir=temp_root)
        self.addCleanup(temporary.cleanup)
        self.sandbox = Path(temporary.name)
        self.workspace = self.sandbox / "working"

    def read(self, case: str, path: str, *, succeeds: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            [sys.executable, "read.py", path],
            cwd=self.workspace / "cases" / case,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode == 0, succeeds, result.stderr)
        return result

    def test_cases_cover_seven_routes_with_contained_materials(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cases = fixture["cases"]
        self.assertEqual({case["id"] for case in cases}, {
            "draft", "revise", "literature", "claim_check", "method_spec", "material_links", "reading_note",
        })
        self.assertEqual(len({case["route"] for case in cases}), len(cases))
        for case in cases:
            self.assertTrue(case["request"].strip())
            self.assertTrue(case["outputs"])
            self.assertTrue(case["files"])
            for name in {*case["files"], *case["outputs"]}:
                self.assertFalse(Path(name).anchor)
                self.assertNotIn("..", Path(name).parts)
                self.assertNotIn(name, {"request.txt", "read.py", "trace.jsonl"})

    def test_prepare_keeps_review_guidance_out_of_worker_inputs(self) -> None:
        prepare(self.workspace)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        prompts = json.loads((self.workspace / "worker_prompts.json").read_text(encoding="utf-8"))
        for case in fixture["cases"]:
            folder = self.workspace / "cases" / case["id"]
            self.assertEqual((folder / "request.txt").read_text(encoding="utf-8"), case["request"])
            for name, content in case["files"].items():
                self.assertEqual((folder / name).read_text(encoding="utf-8"), content)
            self.assertIn(folder.as_posix(), prompts[case["id"]])
            self.assertNotIn("writing-style.md", prompts[case["id"]])
            self.assertNotIn(fixture["scoring"], prompts[case["id"]])
            self.assertFalse((folder / "trace.jsonl").exists())
        self.assertFalse((self.workspace / "candidate" / "assets" / "evals").exists())
        with self.assertRaises(FileExistsError):
            prepare(self.workspace)
        with self.assertRaises(ValueError):
            prepare(ROOT / "assets" / "unexpected-evaluation-workspace")

    def test_reader_emits_full_unicode_text_and_rejects_parent_access(self) -> None:
        prepare(self.workspace)
        request = (self.workspace / "cases" / "draft" / "request.txt").read_text(encoding="utf-8")
        result = self.read("draft", "request.txt")
        self.assertEqual(result.stdout, request + "\n")
        trace = self.workspace / "cases" / "draft" / "trace.jsonl"
        row = json.loads(trace.read_text(encoding="utf-8"))
        self.assertEqual(row["content"], request)
        self.assertEqual(row["characters"], len(request))
        self.assertTrue(row["full_file_emitted"])
        for path in ("../revise/request.txt", "candidate/../fixture.json", "trace.jsonl"):
            self.read("draft", path, succeeds=False)
        self.assertEqual(len(trace.read_text(encoding="utf-8").splitlines()), 1)

    def test_audit_requires_payload_and_preserves_missing_evidence(self) -> None:
        prepare(self.workspace)
        folder = self.workspace / "cases" / "draft"
        style = (self.workspace / "candidate" / "references" / "writing-style.md").read_text(encoding="utf-8")
        (folder / "trace.jsonl").write_text(json.dumps({
            "path": "candidate/references/writing-style.md", "characters": len(style), "full_file_emitted": True,
        }) + "\n", encoding="utf-8")
        self.assertFalse(audit(self.workspace)["cases"][0]["checks"]["full_style_emitted"])
        self.read("draft", "candidate/references/writing-style.md")
        report = audit(self.workspace)
        self.assertTrue(report["cases"][0]["checks"]["full_style_emitted"])
        self.assertFalse(report["cases"][0]["checks"]["outputs_present"])
        self.assertFalse(report["evidence_checks_passed"])
        (folder / "results.md").write_text("Changed source", encoding="utf-8")
        self.assertFalse(audit(self.workspace)["cases"][0]["checks"]["source_inputs_unchanged"])
        for path in (self.workspace / "candidate" / "references").glob("*.md"):
            self.read("draft", "candidate/references/" + path.name)
        self.assertFalse(audit(self.workspace)["cases"][0]["checks"]["selective_references"])

    def test_record_retains_incomplete_runs_without_inventing_a_pass(self) -> None:
        prepare(self.workspace)
        self.read("draft", "candidate/references/writing-style.md")
        output = self.workspace / "cases" / "draft" / "results.tex"
        output.write_text("Test artifact, not a model output.\n", encoding="utf-8")
        saved = record(self.workspace, "incomplete", runs_root=self.sandbox / "runs")
        self.assertEqual((saved / "cases" / "draft" / "results.tex").read_text(encoding="utf-8"), output.read_text(encoding="utf-8"))
        self.assertEqual((saved / "cases" / "draft" / "trace.jsonl").read_bytes(), (output.parent / "trace.jsonl").read_bytes())
        self.assertTrue((saved / "fixture.json").is_file())
        self.assertTrue((saved / "candidate" / "SKILL.md").is_file())
        self.assertEqual(json.loads((saved / "review.json").read_text(encoding="utf-8"))["status"], "not_reviewed")
        self.assertFalse(json.loads((saved / "audit.json").read_text(encoding="utf-8"))["evidence_checks_passed"])
        self.assertTrue(self.workspace.is_dir())
        with self.assertRaises(FileExistsError):
            record(self.workspace, "incomplete", runs_root=self.sandbox / "runs")

    def test_complete_evidence_does_not_override_a_failed_behavior_review(self) -> None:
        prepare(self.workspace)
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for case in fixture["cases"]:
            self.read(case["id"], "candidate/references/writing-style.md")
            for name in case["outputs"]:
                output = self.workspace / "cases" / case["id"] / name
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text("Synthetic unit-test artifact.\n", encoding="utf-8")
        self.assertTrue(audit(self.workspace)["evidence_checks_passed"])
        assessment = {"status": "fail", "evidence": "Synthetic review for this tool test."}
        review = self.sandbox / "review.json"
        review.write_text(json.dumps(assessment), encoding="utf-8")
        saved = record(self.workspace, "review-failed", review, self.sandbox / "runs")
        self.assertEqual(json.loads((saved / "review.json").read_text(encoding="utf-8")), assessment)

    def test_malformed_traces_remain_archivable_as_failed_evidence(self) -> None:
        prepare(self.workspace)
        trace = self.workspace / "cases" / "draft" / "trace.jsonl"
        trace.write_text("not JSON\n", encoding="utf-8")
        self.assertFalse(audit(self.workspace)["cases"][0]["checks"]["trace_valid"])
        saved = record(self.workspace, "malformed", runs_root=self.sandbox / "runs")
        self.assertEqual((saved / "cases" / "draft" / "trace.jsonl").read_bytes(), trace.read_bytes())
        self.assertFalse(json.loads((saved / "audit.json").read_text(encoding="utf-8"))["evidence_checks_passed"])

    def test_historical_review_has_artifacts_and_explicit_recovery_limits(self) -> None:
        run = SUITE / "runs" / "2026-10-25"
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        review = json.loads((run / "review.json").read_text(encoding="utf-8"))
        recovery = json.loads((run / "recovery.json").read_text(encoding="utf-8"))
        self.assertEqual({row["case"] for row in review["cases"]}, {case["id"] for case in fixture["cases"]})
        expected_outputs = {
            case["id"]: {f"outputs/{case['id']}/{name}" for name in case["outputs"]}
            for case in fixture["cases"]
        }
        for row in review["cases"]:
            self.assertTrue(row["evidence"])
            self.assertEqual(set(row["outputs"]), expected_outputs[row["case"]])
            for name in row["outputs"]:
                self.assertTrue((run / name).is_file())
        for artifact in recovery["artifacts"]:
            text = (run / artifact["recovered_path"]).read_text(encoding="utf-8")
            self.assertEqual(len(text), artifact["reconstructed_characters"])
        self.assertFalse(recovery["trace_recovery"]["original_jsonl_recovered"])
        self.assertFalse((run / "traces").exists())


if __name__ == "__main__":
    unittest.main()
