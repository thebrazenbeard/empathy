"""Adversarial cases that should not pass merely because policy names exist.

Purely synthetic input; test oracles are current repository behavioral
commitments, not a transcription of choose_policy's priority order.
"""

import unittest

from empathy_research.policy import Assessment, Evidence, Hypothesis, Policy, choose_policy


PERSON = "synthetic-person-a"
OTHER = "synthetic-person-b"


def event(kind, referent, value, confidence, evidence_id):
    return Evidence(kind, referent, value, confidence, "current", PERSON,
                    evidence_id=evidence_id)


class NegativePolicyTests(unittest.TestCase):
    def test_zero_confidence_play_does_not_activate_play(self):
        """Zero-confidence evidence cannot justify continued mutual play."""
        zero_support = event("reciprocal_play", "play_frame", "active", 0.0,
                             "synthetic-play-unknown")
        result = choose_policy(Assessment(PERSON, (zero_support,)))
        self.assertNotEqual(result.policy, Policy.PRESERVE_PLAY,
                            "unsupported play inference was activated")

    def test_uncertain_current_withdrawal_prevents_presumed_mutual_play(self):
        """Possible fresh withdrawal should pause play until meaning is clear."""
        play = event("reciprocal_play", "play_frame", "active", 0.99,
                     "synthetic-active-play")
        possible_stop = event("withdrawal", "play_frame", "stop", 0.49,
                              "synthetic-uncertain-withdrawal")
        result = choose_policy(Assessment(PERSON, (play, possible_stop)))
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING,
                         "uncertain fresh withdrawal did not suspend playful route")

    def test_unrelated_celebration_does_not_hijack_explicit_task(self):
        """Different-referent context is not itself permission to derail a task."""
        task = event("task_request", "task", "calculate", 1.0,
                     "synthetic-present-task")
        unrelated = event("celebration", "earlier_event", "proud", 1.0,
                          "synthetic-unrelated-event")
        baseline = choose_policy(Assessment(PERSON, (task,)))
        with_unrelated = choose_policy(Assessment(PERSON, (task, unrelated)))
        self.assertEqual(baseline.policy, Policy.TASK_DIRECT)
        self.assertEqual(with_unrelated.policy, Policy.TASK_DIRECT,
                         "unrelated emotional cue diverted explicit current task")

    def test_same_referent_correction_cancels_inferred_task_route(self):
        """A corrected interpretation must not remain live as a task command."""
        inferred_task = event("task_request", "utterance_intent", "calculate",
                              0.95, "synthetic-task-inference")
        direct_correction = event("direct_correction", "utterance_intent",
                                  "not_a_task_request", 1.0,
                                  "synthetic-correction")
        result = choose_policy(Assessment(PERSON, (inferred_task, direct_correction)))
        self.assertNotEqual(result.policy, Policy.TASK_DIRECT,
                            "direct correction failed to retire the task inference")

    def test_evidence_ids_represent_decisive_support_not_all_admitted_input(self):
        """Provenance of the chosen route must not cite unrelated observations."""
        task = event("task_request", "task", "calculate", 1.0,
                     "ev_00112233445566778899aabbccddeeff")
        unrelated = event("context_note", "unrelated_topic", "noted", 1.0,
                          "synthetic-unrelated-context")
        result = choose_policy(Assessment(PERSON, (task, unrelated)))
        self.assertEqual(result.policy, Policy.TASK_DIRECT)
        self.assertEqual(result.evidence_ids, ("ev_00112233445566778899aabbccddeeff",),
                         "decision provenance includes non-supporting context")

    def test_cross_person_hypothesis_cannot_leak_through_supersession(self):
        """Hypotheses need person scope before their raw values can be returned."""
        foreign = Hypothesis(
            "utterance_meaning", "synthetic-private-other-person-marker", 0.99,
            scope_person_id=OTHER,
        )
        correction = event("direct_correction", "utterance_meaning", "literal",
                           1.0, "synthetic-own-correction")
        result = choose_policy(Assessment(PERSON, (correction,),
                                          hypotheses=(foreign,)))
        self.assertNotIn(foreign, result.superseded_hypotheses)
        self.assertNotIn("synthetic-private-other-person-marker", repr(result),
                         "another person's hypothetical content crossed scope")


if __name__ == "__main__":
    unittest.main()
