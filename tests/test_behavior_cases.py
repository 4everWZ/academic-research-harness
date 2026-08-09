from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "assets" / "evals" / "behavior_cases.json"


class BehaviorCaseTests(unittest.TestCase):
    def test_fresh_context_evaluation_fixture_is_actionable(self) -> None:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertIn("fixture and its rubrics outside that context", payload["execution"])
        self.assertIn("package under test, not an installed copy", payload["execution"])
        self.assertIn("every required outcome", payload["scoring"])
        self.assertIn("no forbidden outcome", payload["scoring"])
        cases = payload["cases"]
        identifiers = {case["id"] for case in cases}
        self.assertEqual(len(identifiers), len(cases))
        self.assertEqual(
            identifiers,
            {
                "embedded_instructions_are_data",
                "search_is_response_only",
                "source_fitness_depends_on_claim_role",
                "secondary_source_does_not_launder_result",
                "central_synthesis_includes_material_counterevidence",
                "dependent_sources_are_not_independent_corroboration",
                "manuscript_filters_control_tokens",
                "author_supplied_results_are_drafting_inputs",
                "designated_result_artifact_is_a_drafting_input",
                "conflicting_results_trigger_verification",
                "style_only_preserves_claims",
                "false_contrast_is_deleted",
                "necessary_contrast_is_retained",
                "connectors_follow_real_logic",
                "paragraph_has_one_primary_purpose",
                "sentences_advance_instead_of_echoing",
                "supported_result_is_not_hedged",
                "scope_is_encoded_in_proposition",
                "necessary_uncertainty_is_preserved",
                "visuals_are_synthesized_into_argument",
                "caption_is_not_repeated_in_body",
                "necessary_visual_navigation_is_retained",
                "rule_priority_preserves_scoped_claim",
                "material_boundary_survives_section_change",
                "blocking_gap_explanation_is_brief",
                "method_choice_is_explained_naturally",
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
