"""Independent synthetic decision-policy adversarial tests.

These oracles come from the repository's current-direction contract, not from
the mechanism's implementation.  They exercise policy decisions, not tone.
No real person's relationship history or identity is used as fixture data.
"""

import unittest

from empathy_research.policy import Assessment, Evidence, Hypothesis, choose_policy


PERSON = "synthetic-person-a"
OTHER = "synthetic-person-b"


def evidence(kind, referent, value, *, person=PERSON, confidence=1.0,
             source="current", active=True):
    return Evidence(
        kind=kind,
        referent=referent,
        value=value,
        confidence=confidence,
        source=source,
        scope_person_id=person,
        active=active,
    )


def decide(*current, history=(), hypotheses=(), person=PERSON, stakes="low"):
    return choose_policy(Assessment(
        person_id=person,
        current_evidence=tuple(current),
        historical_evidence=tuple(history),
        hypotheses=tuple(hypotheses),
        stakes=stakes,
    ))


def selected(decision):
    raw = decision.policy
    return raw.value if hasattr(raw, "value") else str(raw)


class AdversarialPolicyTests(unittest.TestCase):
    def assert_policy(self, wanted, decision):
        self.assertEqual(wanted, selected(decision),
                         f"decision={decision!r}; expected behavioral route {wanted}")

    def test_same_referent_direct_correction_retires_strong_historical_read(self):
        """A direct intended-meaning correction outranks an old confident guess."""
        correction = evidence("direct_correction", "utterance_meaning", "literal")
        baseline = decide(correction)
        decision = decide(
            correction,
            history=(evidence("reciprocal_play", "utterance_meaning", "joking",
                              source="historical"),),
            hypotheses=(Hypothesis("utterance_meaning", "joking", 0.99),),
        )
        self.assertNotEqual("PRESERVE_PLAY", selected(decision))
        self.assertEqual(selected(baseline), selected(decision),
                         "superseded hypothesis altered the corrected route")

    def test_correction_is_not_global_deference(self):
        """Correction of intended tone doesn't make external facts true."""
        decision = decide(
            evidence("direct_correction", "utterance_meaning", "literal"),
            evidence("unsupported_claim", "external_fact", "unsupported"),
        )
        self.assert_policy("TRUTHFUL_CHALLENGE", decision)

    def test_fresh_withdrawal_stops_old_play_frame(self):
        """Prior banter is not standing permission after the frame changes."""
        decision = decide(
            evidence("withdrawal", "play_frame", "stop"),
            history=(evidence("reciprocal_play", "play_frame", "active",
                              source="historical"),),
        )
        self.assert_policy("STOP_PLAY", decision)

    def test_recency_is_not_replaced_by_lexical_tone(self):
        """A sharp word alone cannot certify mutual play or distress."""
        decision = decide(evidence("lexical_tone", "interaction", "sharp"))
        self.assert_policy("CLARIFY_MEANING", decision)

    def test_ambiguous_interpersonal_meaning_requests_clarification(self):
        decision = decide(
            evidence("ambiguous", "utterance_meaning", "uncertain", confidence=0.4),
            stakes="high",
        )
        self.assert_policy("CLARIFY_MEANING", decision)

    def test_factual_disagreement_is_not_replaced_by_placation(self):
        decision = decide(
            evidence("unsupported_claim", "external_fact", "unsupported"),
            evidence("request", "response", "agree_with_me"),
        )
        self.assert_policy("TRUTHFUL_CHALLENGE", decision)

    def test_explicit_task_request_does_not_force_emotional_processing(self):
        decision = decide(evidence("task_request", "task", "calculate"))
        self.assert_policy("TASK_DIRECT", decision)

    def test_cross_person_evidence_cannot_trigger_target_person_policy(self):
        """No person-B private event may shape a person-A decision."""
        task = evidence("task_request", "task", "calculate", person=PERSON)
        baseline = decide(task)
        poisoned = decide(
            evidence("withdrawal", "play_frame", "stop", person=OTHER),
            task,
        )
        self.assert_policy("TASK_DIRECT", baseline)
        self.assertEqual(baseline, poisoned,
                         "foreign-person evidence changed a scoped decision")

    def test_old_want_is_not_current_consent(self):
        decision = decide(
            history=(evidence("conation", "consent", "yes",
                              source="historical"),),
        )
        self.assertNotEqual("PRESERVE_PLAY", selected(decision))

    def test_decision_is_non_authoritative_and_ephemeral(self):
        decision = decide(evidence("task_request", "task", "calculate"))
        self.assertEqual("NONE", getattr(decision, "authority", None))
        self.assertEqual("EPHEMERAL", getattr(decision, "persistence", None))


if __name__ == "__main__":
    unittest.main()
