"""Focused contract tests independent of prose rendering or hosted memory."""

import unittest

from empathy_research.policy import Assessment, Evidence, Hypothesis, Policy, choose_policy


def item(kind, referent, value, *, person="synthetic-a", source="current"):
    return Evidence(kind, referent, value, 0.9, source, person)


class PolicyContractTests(unittest.TestCase):
    def test_no_authenticated_person_scope_fails_closed(self):
        result = choose_policy(Assessment("", (item("task_request", "task", "calculate"),)))
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertEqual(result.reason, "MISSING_TRUSTED_PERSON_SCOPE")
        self.assertTrue(result.focus_needed)

    def test_historical_source_in_current_slot_is_not_fresh(self):
        result = choose_policy(Assessment("synthetic-a", (
            item("reciprocal_play", "play_frame", "active", source="historical"),
        )))
        self.assertNotEqual(result.policy, Policy.PRESERVE_PLAY)

    def test_direct_correction_discards_same_referent_current_inference(self):
        result = choose_policy(Assessment("synthetic-a", (
            item("reciprocal_play", "utterance_meaning", "joking"),
            item("direct_correction", "utterance_meaning", "literal"),
        ), hypotheses=(Hypothesis("utterance_meaning", "joking", 0.99,
                                 scope_person_id="synthetic-a", hypothesis_id="h1"),)))
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertEqual(result.superseded_hypotheses, ("h1",))

    def test_referent_scoped_correction_preserves_unrelated_current_play(self):
        result = choose_policy(Assessment("synthetic-a", (
            item("reciprocal_play", "play_frame", "active"),
            item("direct_correction", "different_referent", "literal"),
        )))
        self.assertEqual(result.policy, Policy.PRESERVE_PLAY)
        # The correction was not applied to the unrelated playful evidence.
        self.assertEqual(result.superseded_hypotheses, ())

    def test_cannot_use_invalid_confidence(self):
        with self.assertRaises(ValueError):
            Evidence("task_request", "task", "calculate", float("nan"),
                     "current", "synthetic-a")


if __name__ == "__main__":
    unittest.main()
