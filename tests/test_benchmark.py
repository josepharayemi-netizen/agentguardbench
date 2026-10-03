from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentguardbench.agent import MockAgent
from agentguardbench.evaluator import evaluate, load_scenarios, summarise


class AgentGuardBenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = load_scenarios(ROOT / "data" / "scenarios.jsonl")

    def test_dataset_has_expected_size_and_unique_ids(self):
        self.assertEqual(len(self.scenarios), 120)
        self.assertEqual(len({case.id for case in self.scenarios}), 120)

    def test_language_variants_have_distinct_text(self):
        cases = [
            case for case in self.scenarios
            if case.category == "prompt_injection" and case.sector == "banking"
        ]
        self.assertEqual({case.language for case in cases}, {"en", "fr", "sw", "yo"})
        self.assertEqual(len({case.prompt for case in cases}), 4)

    def test_strict_policy_blocks_injection(self):
        case = next(c for c in self.scenarios if c.category == "prompt_injection")
        self.assertEqual(MockAgent("strict").run(case).action, "refuse")

    def test_strict_policy_outperforms_permissive_policy(self):
        strict = summarise(evaluate(self.scenarios, "strict"))
        permissive = summarise(evaluate(self.scenarios, "permissive"))
        self.assertGreater(strict["overall_pass_rate"], permissive["overall_pass_rate"])
        self.assertLess(strict["privacy_leakage_rate"], permissive["privacy_leakage_rate"])


if __name__ == "__main__":
    unittest.main()
