"""Real Empathy producer counterfactuals; synthetic public fixture data only."""

import unittest

from empathy_research.cognitive_donor_probe import evaluate_current_task
from empathy_research.policy import Assessment, Evidence


def task_case(kind: str, referent: str, value: str, *, source: str = "current",
              person: str = "fixture-a", confidence: float = 0.9) -> Assessment:
    return Assessment(
        person_id="fixture-a",
        current_evidence=(Evidence(
            kind=kind, referent=referent, value=value, confidence=confidence,
            source=source, scope_person_id=person, evidence_id="ev_" + "a" * 32,
        ),),
    )


class CognitiveDonorProbeTests(unittest.TestCase):
    def test_same_donor_different_current_task_observations(self):
        scenarios = (
            ("task_request", "task", "explicit", "TASK_DIRECT", "EXPLICIT_TASK"),
            ("direct_correction", "play_frame", "stop", "STOP_PLAY", "DIRECT_PLAY_STOP"),
            ("unsupported_claim", "external_fact", "unsupported", "TRUTHFUL_CHALLENGE", "UNSUPPORTED_FACT"),
            ("ambiguous", "task", "unresolved", "CLARIFY_MEANING", "TASK_INTENT_UNRESOLVED"),
        )
        encountered = set()
        for kind, referent, value, policy, reason in scenarios:
            with self.subTest(kind=kind):
                actual = evaluate_current_task(task_case(kind, referent, value))
                self.assertEqual((actual.policy, actual.reason_code), (policy, reason))
                self.assertEqual(actual.donor, "empathy")
                self.assertEqual(actual.supporting_evidence_ids, ("ev_" + "a" * 32,))
                self.assertEqual(actual.authority, "NONE")
                self.assertEqual(actual.memory_admission, "NONE")
                self.assertFalse(actual.effect_authority)
                encountered.add(actual.policy)
        self.assertEqual(len(encountered), 4)

    def test_missing_evidence_cannot_be_replaced_with_static_scores(self):
        with self.assertRaisesRegex(ValueError, "no donor value synthesized"):
            evaluate_current_task(Assessment(person_id="fixture-a"))

    def test_cross_person_evidence_rejected(self):
        with self.assertRaisesRegex(ValueError, "same-person"):
            evaluate_current_task(task_case("task_request", "task", "explicit", person="fixture-b"))

    def test_historical_currentness_spoof_rejected(self):
        with self.assertRaisesRegex(ValueError, "current"):
            evaluate_current_task(task_case("task_request", "task", "explicit", source="historical"))

    def test_untraceable_evidence_rejected(self):
        untraceable = Assessment(person_id="fixture-a", current_evidence=(
            Evidence("task_request", "task", "explicit", 0.9, "current", "fixture-a"),
        ))
        with self.assertRaisesRegex(ValueError, "opaque IDs"):
            evaluate_current_task(untraceable)

    def test_no_private_historical_context(self):
        current = task_case("task_request", "task", "explicit").current_evidence
        with self.assertRaisesRegex(ValueError, "historical"):
            evaluate_current_task(Assessment(
                person_id="fixture-a", current_evidence=current, historical_evidence=current,
            ))

    def test_duplicate_observation_ids_cannot_identify_distinct_sources(self):
        request = task_case("task_request", "task", "explicit").current_evidence[0]
        stop = Evidence(
            "direct_correction", "play_frame", "stop", 0.9, "current",
            "fixture-a", evidence_id=request.evidence_id,
        )
        with self.assertRaisesRegex(ValueError, "duplicate evidence ID"):
            evaluate_current_task(Assessment(
                person_id="fixture-a", current_evidence=(request, stop),
            ))

    def test_mutable_current_list_cannot_change_during_selection(self):
        request = task_case("task_request", "task", "explicit").current_evidence[0]
        assessment = Assessment(person_id="fixture-a", current_evidence=[request])
        with self.assertRaisesRegex(ValueError, "immutable tuple"):
            evaluate_current_task(assessment)

    def test_opaque_id_collision_same_observation_is_still_rejected(self):
        request = task_case("task_request", "task", "explicit").current_evidence[0]
        with self.assertRaisesRegex(ValueError, "duplicate evidence ID"):
            evaluate_current_task(Assessment(
                person_id="fixture-a", current_evidence=(request, request),
            ))

    def test_contradictory_same_referent_corrections_refused_as_unordered(self):
        stop = task_case("direct_correction", "play_frame", "stop").current_evidence[0]
        active = Evidence(
            "direct_correction", "play_frame", "active", 0.9, "current",
            "fixture-a", evidence_id="ev_" + "b" * 32,
        )
        with self.assertRaisesRegex(ValueError, "conflicting same-referent corrections"):
            evaluate_current_task(Assessment(
                person_id="fixture-a", current_evidence=(stop, active),
            ))


if __name__ == "__main__":
    unittest.main()
