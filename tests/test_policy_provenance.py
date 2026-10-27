"""Synthetic hostile controls for output provenance and score labeling."""

import unittest

from empathy_research.policy import Assessment, Evidence, Hypothesis, Policy, choose_policy


PERSON = "synthetic-person"
EVIDENCE_ID = "ev_0123456789abcdef0123456789abcdef"
HYPOTHESIS_ID = "hyp_fedcba9876543210fedcba9876543210"


class ProvenanceSafetyTests(unittest.TestCase):
    def test_inferred_play_high_score_is_not_explicit_testimony(self):
        inferred_play = Evidence("reciprocal_play", "play_frame", "active", 0.99,
                                 "current", PERSON, evidence_id=EVIDENCE_ID)
        result = choose_policy(Assessment(PERSON, (inferred_play,)))
        self.assertEqual(result.policy, Policy.PRESERVE_PLAY)
        self.assertEqual(result.confidence_band, "HIGH_SCORE")
        self.assertNotEqual(result.confidence_band, "EXPLICIT")

    def test_raw_evidence_id_is_never_echoed(self):
        raw_id = "PRIVATE RAW OTHER-PERSON CONTEXT"
        request = Evidence("task_request", "task", "calculate", 0.95,
                           "current", PERSON, evidence_id=raw_id)
        result = choose_policy(Assessment(PERSON, (request,)))
        self.assertEqual(result.policy, Policy.TASK_DIRECT)
        self.assertEqual(result.evidence_ids, ())
        self.assertNotIn(raw_id, repr(result))

    def test_raw_hypothesis_id_is_never_echoed(self):
        correction = Evidence("direct_correction", "meaning", "literal", 1.0,
                              "current", PERSON)
        guess = Hypothesis("meaning", "joking", 0.9, PERSON,
                           "PRIVATE RAW HYPOTHESIS NOTE")
        result = choose_policy(Assessment(PERSON, (correction,),
                                          hypotheses=(guess,)))
        self.assertEqual(result.superseded_hypotheses, ())
        self.assertNotIn(guess.hypothesis_id, repr(result))

    def test_only_correctly_namespaced_fixed_length_tokens_survive(self):
        bad_values = (
            "", "private_note", "ev_0123456789abcdef", "ev_0123456789abcdef0123456789abcdef ",
            "hyp_0123456789abcdef0123456789abcde", "ev_0123456789ABCDEf0123456789abcdef",
        )
        correction = Evidence("direct_correction", "meaning", "literal", 1.0,
                              "current", PERSON, evidence_id=EVIDENCE_ID)
        for bad in bad_values:
            with self.subTest(bad=bad):
                guess = Hypothesis("meaning", "joking", 0.9, PERSON, bad)
                result = choose_policy(Assessment(PERSON, (correction,),
                                                  hypotheses=(guess,)))
                self.assertEqual(result.evidence_ids, (EVIDENCE_ID,))
                self.assertEqual(result.superseded_hypotheses, ())
        valid = Hypothesis("meaning", "joking", 0.9, PERSON, HYPOTHESIS_ID)
        result = choose_policy(Assessment(PERSON, (correction,),
                                          hypotheses=(valid,)))
        self.assertEqual(result.superseded_hypotheses, (HYPOTHESIS_ID,))


if __name__ == "__main__":
    unittest.main()
