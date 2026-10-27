"""Independent, synthetic behavioral-policy negative controls.

These test the executable, bounded decision *route*, not whether a language
model experiences emotion, understands another mind, or has deployment access.
No real person's private relationship history is used as fixture material.
"""

import itertools
import unittest

from empathy_research.policy import Assessment, Evidence, Hypothesis, Policy, choose_policy


PERSON = "synthetic-primary"
OTHER = "synthetic-other"


def observation(kind, referent, value, *, confidence=1.0, person=PERSON,
                source="current", active=True, identifier=""):
    return Evidence(kind, referent, value, confidence, source, person, active,
                    identifier)


def choice(*items, person=PERSON, stakes="low", hypotheses=(), historical=()):
    return choose_policy(Assessment(person, tuple(items), tuple(historical),
                                    tuple(hypotheses), stakes))


class BehavioralFalsifierTests(unittest.TestCase):
    def test_explicit_correction_stopping_play_is_respected(self):
        """A direct, authenticated 'stop' cannot be treated as merely ambiguous."""
        prior_inference = observation("reciprocal_play", "play_frame", "active",
                                      identifier="synthetic-play")
        stop = observation("direct_correction", "play_frame", "stop",
                           identifier="synthetic-stop")
        result = choice(prior_inference, stop)
        self.assertEqual(result.policy, Policy.STOP_PLAY)
        self.assertEqual(result.authority, "NONE")
        self.assertEqual(result.persistence, "EPHEMERAL")

    def test_high_stakes_low_confidence_task_ambiguity_is_not_discarded(self):
        """Uncertainty is a reason for caution, not always a null observation.

        The conflict is evidence of possible mistaken intent, not proof that
        the task request is invalid; high-stakes routing should seek focus.
        """
        task = observation("task_request", "task", "execute",
                           confidence=0.99, identifier="synthetic-task")
        ambiguous = observation("ambiguous", "task", "possibly_not_requested",
                                confidence=0.49, identifier="synthetic-doubt")
        result = choice(task, ambiguous, stakes="high")
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertTrue(result.focus_needed)

    def test_contradictory_live_play_states_cannot_assert_mutual_uptake(self):
        """Two opposing current appraisals cannot both justify continued play."""
        inferred_active = observation("reciprocal_play", "play_frame", "active",
                                      confidence=0.99, identifier="synthetic-on")
        inferred_inactive = observation("reciprocal_play", "play_frame", "inactive",
                                        confidence=0.99, identifier="synthetic-off")
        result = choice(inferred_active, inferred_inactive)
        self.assertNotEqual(result.policy, Policy.PRESERVE_PLAY)
        self.assertTrue(result.focus_needed)

    def test_high_stakes_route_requires_deliberative_focus_even_with_a_task(self):
        """A decisive route is not permission to skip high-stakes deliberation."""
        request = observation("task_request", "task", "calculate",
                              confidence=0.99, identifier="synthetic-task")
        result = choice(request, stakes="high")
        self.assertEqual(result.policy, Policy.TASK_DIRECT)
        self.assertTrue(result.focus_needed)

    def test_unrelated_person_additions_cannot_change_decision_or_provenance(self):
        """Person isolation is a full-output invariant, not only policy name."""
        task = observation("task_request", "task", "calculate",
                           identifier="synthetic-task-id")
        baseline = choice(task)
        foreign = (
            observation("withdrawal", "play_frame", "stop", person=OTHER,
                        identifier="synthetic-private-other-withdrawal"),
            observation("unsupported_claim", "external_fact", "unsupported",
                        person=OTHER, identifier="synthetic-private-other-fact"),
            observation("direct_correction", "task", "not_requested",
                        person=OTHER, identifier="synthetic-private-other-correction"),
        )
        for order in itertools.permutations(foreign):
            with self.subTest(order=tuple(item.kind for item in order)):
                self.assertEqual(choice(task, *order), baseline)

    def test_non_admitted_hypothesis_is_never_a_standing_desire_or_consent(self):
        """The model's own speculation cannot authorize an ongoing relation."""
        hypothesis = Hypothesis("play_frame", "active", 1.0, PERSON,
                                "synthetic-hypothesis")
        old_preference = observation("conation", "consent", "yes",
                                     source="historical")
        result = choice(hypotheses=(hypothesis,), historical=(old_preference,))
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertEqual(result.confidence_band, "NONE")
        self.assertEqual(result.evidence_ids, ())

    def test_self_appraisal_is_not_promoted_into_persons_reported_state(self):
        """Operational self-appraisal cannot displace the human's explicit task."""
        task = observation("task_request", "task", "calculate",
                           identifier="synthetic-task-id")
        self_state = observation("self_appraisal", "agent_state", "uncertain",
                                 identifier="synthetic-own-state")
        baseline = choice(task)
        self.assertEqual(choice(task, self_state), baseline)

    def test_personal_correction_does_not_suppress_independent_factual_check(self):
        unsupported = observation("unsupported_claim", "external_fact",
                                  "unsupported", identifier="ev_ffeeddccbbaa99887766554433221100")
        personal = observation("direct_correction", "utterance_meaning",
                               "joke", identifier="synthetic-correction")
        result = choice(unsupported, personal)
        self.assertEqual(result.policy, Policy.TRUTHFUL_CHALLENGE)
        self.assertEqual(result.evidence_ids, ("ev_ffeeddccbbaa99887766554433221100",))

    def test_inactive_or_wrong_source_withdrawal_is_not_promoted_to_current(self):
        play = observation("reciprocal_play", "play_frame", "active")
        old = observation("withdrawal", "play_frame", "stop", source="historical")
        disabled = observation("withdrawal", "play_frame", "stop", active=False)
        self.assertEqual(choice(play, old, disabled).policy, Policy.PRESERVE_PLAY)

    def test_zero_confidence_withdrawal_cannot_override_current_play(self):
        play = observation("reciprocal_play", "play_frame", "active", confidence=0.99)
        unsupported = observation("withdrawal", "play_frame", "stop", confidence=0.0)
        self.assertEqual(choice(play, unsupported).policy, Policy.PRESERVE_PLAY)

    def test_non_stop_withdrawal_value_cannot_assert_stop(self):
        continuation = observation("withdrawal", "play_frame", "continue", confidence=0.99)
        self.assertNotEqual(choice(continuation).policy, Policy.STOP_PLAY)

    def test_uncertain_withdrawal_semantics_pause_play_even_if_score_is_high(self):
        active = observation("reciprocal_play", "play_frame", "active", confidence=0.99)
        possible_stop = observation("withdrawal", "play_frame", "possible", confidence=0.99)
        result = choice(active, possible_stop)
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertTrue(result.focus_needed)

    def test_missing_trusted_scope_returns_no_person_bound_provenance(self):
        data = observation("task_request", "task", "calculate",
                           identifier="synthetic-private-evidence")
        speculation = Hypothesis("utterance_meaning", "private_inference", 0.9,
                                 PERSON, "synthetic-private-hypothesis")
        result = choice(data, person="", hypotheses=(speculation,))
        self.assertEqual(result.policy, Policy.CLARIFY_MEANING)
        self.assertEqual(result.evidence_ids, ())
        self.assertEqual(result.superseded_hypotheses, ())
        self.assertEqual(result.confidence_band, "NONE")

    def test_all_represented_policy_routes_are_non_authoritative(self):
        """Empathy only influences response route; never effects or persistence."""
        fixtures = (
            (observation("withdrawal", "play_frame", "stop"),),
            (observation("task_request", "task", "calculate"),),
            (observation("unsupported_claim", "external_fact", "unsupported"),),
            (observation("repair_needed", "interaction", "repair"),),
            (observation("celebration", "event", "milestone"),),
            (observation("reciprocal_play", "play_frame", "active"),),
            (observation("ambiguous", "task", "unresolved"),),
        )
        for events in fixtures:
            with self.subTest(kind=events[0].kind):
                result = choice(*events)
                self.assertEqual(result.authority, "NONE")
                self.assertEqual(result.persistence, "EPHEMERAL")
                self.assertIsInstance(result.policy, Policy)

    def test_confidence_limits_reject_nan_inf_boolean_and_out_of_range(self):
        for bad in (float("nan"), float("inf"), -0.01, 1.01, True, False):
            with self.subTest(confidence=bad):
                with self.assertRaises(ValueError):
                    observation("task_request", "task", "calculate", confidence=bad)
                with self.assertRaises(ValueError):
                    Hypothesis("task", "calculate", bad, PERSON)

    def test_string_activity_flag_cannot_become_current_withdrawal(self):
        for malformed in ("true", "false", 1, 0, None):
            with self.subTest(active=malformed):
                with self.assertRaises(ValueError):
                    observation("withdrawal", "play_frame", "stop", active=malformed)


if __name__ == "__main__":
    unittest.main()
