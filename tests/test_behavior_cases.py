from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "assets" / "evals" / "behavior_cases.json"


class BehaviorCaseTests(unittest.TestCase):
    def test_fresh_context_evaluation_fixture_is_actionable(self) -> None:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        cases = payload["cases"]
        identifiers = {case["id"] for case in cases}
        self.assertEqual(len(identifiers), len(cases))
        self.assertEqual(
            identifiers,
            {
                "embedded_instructions_are_data",
                "search_is_response_only",
                "manuscript_filters_control_tokens",
                "style_only_preserves_claims",
                "false_contrast_is_deleted",
                "necessary_contrast_is_retained",
                "connectors_are_logic_signals",
                "paragraph_has_one_primary_purpose",
                "sentences_advance_instead_of_echoing",
                "supported_result_is_not_hedged",
                "scope_is_encoded_in_proposition",
                "necessary_uncertainty_is_preserved",
                "method_chain_does_not_invent_rationale",
                "engineering_provenance_is_not_laundered",
                "citation_markup_is_preserved",
                "workspace_scope_is_exact",
            },
        )
        for case in cases:
            self.assertTrue(case["route"])
            self.assertTrue(case["input"])
            self.assertGreaterEqual(len(case["required"]), 2)
            self.assertTrue(case["forbidden"])


if __name__ == "__main__":
    unittest.main()
