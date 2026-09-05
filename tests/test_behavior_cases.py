from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "assets" / "evals" / "behavior_cases.json"


class BehaviorCaseTests(unittest.TestCase):
    """Validate evaluation inputs; writing behavior is judged by independent agents."""

    def test_cases_are_complete_and_distinguishable(self) -> None:
        payload = json.loads(CASES.read_text(encoding="utf-8"))
        for field in ("execution", "scoring"):
            self.assertIsInstance(payload[field], str)
            self.assertTrue(payload[field].strip())
        cases = payload["cases"]
        self.assertTrue(cases)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual(len({case["input"] for case in cases}), len(cases))
        for case in cases:
            for field in ("id", "route", "input"):
                self.assertIsInstance(case[field], str)
                self.assertTrue(case[field].strip())
            for field in ("required", "forbidden"):
                self.assertIsInstance(case[field], list)
                self.assertTrue(case[field])
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in case[field]))
            self.assertFalse(set(case["required"]) & set(case["forbidden"]))


if __name__ == "__main__":
    unittest.main()
