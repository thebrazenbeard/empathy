"""Evidence of *typed-context policy discrimination*, not felt empathy."""

import unittest

from evaluation.policy_discrimination import PAIRS, evaluate


class PolicyDiscriminationBenchmarkTests(unittest.TestCase):
    def test_same_words_require_different_policies(self):
        self.assertGreaterEqual(len(PAIRS), 12)
        for item in PAIRS:
            with self.subTest(pair=item.id):
                self.assertEqual(item.left.utterance, item.right.utterance)
                self.assertNotEqual(item.left.expected, item.right.expected)

    def test_policy_distinguishes_admitted_context_from_identical_words(self):
        result = evaluate()
        self.assertFalse(result["failed_pairs"], result["failed_pairs"])
        self.assertEqual(result["cases"], result["selector_correct"])
        self.assertEqual(result["pairs"], result["selector_pairs_discriminated"])

    def test_intentionally_blind_lexical_control_cannot_discriminate(self):
        result = evaluate()
        self.assertEqual(0, result["lexical_pairs_discriminated"])
        self.assertLess(result["lexical_baseline_correct"], result["selector_correct"])


if __name__ == "__main__":
    unittest.main()
