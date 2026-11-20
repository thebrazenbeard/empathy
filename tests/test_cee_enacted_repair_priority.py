"""Synthetic CEE regression: a requested relational repair is not just a task pivot.

This selector cannot enact empathy, authenticate a speaker, or read minds.
Only explicitly host-admitted, person-scoped, fresh evidence may demand
REPAIR_FIRST ahead of an otherwise unrelated current topic request.
"""

import unittest

from empathy_research.policy import Assessment, Evidence, Policy, choose_policy

PERSON = "synthetic-person"
OTHER = "synthetic-other"
REPAIR_ID = "ev_" + "a" * 32
TOPIC_ID = "ev_" + "b" * 32


def event(kind, referent, value, *, person=PERSON, source="current",
          active=True, confidence=1.0, evidence_id=REPAIR_ID):
    return Evidence(kind=kind, referent=referent, value=value,
                    confidence=confidence, source=source, active=active,
                    scope_person_id=person, evidence_id=evidence_id)


class EnactedRepairPriorityTests(unittest.TestCase):
    def test_explicit_enacted_repair_request_precedes_unrelated_topic(self):
        request = event("repair_request", "interaction", "enact")
        topic = event("task_request", "topic", "discuss", evidence_id=TOPIC_ID)
        decision = choose_policy(Assessment(PERSON, (request, topic)))
        self.assertEqual(decision.policy, Policy.REPAIR_FIRST)
        self.assertEqual(decision.reason, "EXPLICIT_ENACTED_REPAIR_REQUEST")
        self.assertEqual(decision.evidence_ids, (REPAIR_ID,))
        self.assertEqual(decision.authority, "NONE")
        self.assertEqual(decision.persistence, "EPHEMERAL")

    def test_unrequested_inferred_repair_does_not_displace_explicit_task(self):
        inferred = event("repair_needed", "interaction", "possible")
        task = event("task_request", "topic", "discuss", evidence_id=TOPIC_ID)
        decision = choose_policy(Assessment(PERSON, (inferred, task)))
        self.assertEqual(decision.policy, Policy.TASK_DIRECT)

    def test_historical_foreign_or_inactive_request_cannot_override_topic(self):
        topic = event("task_request", "topic", "discuss", evidence_id=TOPIC_ID)
        cases = (
            event("repair_request", "interaction", "enact", source="historical"),
            event("repair_request", "interaction", "enact", person=OTHER),
            event("repair_request", "interaction", "enact", active=False),
            event("repair_request", "interaction", "enact", confidence=0.0),
        )
        for invalid in cases:
            with self.subTest(source=invalid.source, person=invalid.scope_person_id,
                              active=invalid.active, confidence=invalid.confidence):
                decision = choose_policy(Assessment(PERSON, (topic, invalid)))
                self.assertEqual(decision.policy, Policy.TASK_DIRECT)
                self.assertEqual(decision.evidence_ids, (TOPIC_ID,))

    def test_current_play_stop_still_outranks_enacted_repair(self):
        request = event("repair_request", "interaction", "enact")
        stopped = event("direct_correction", "play_frame", "stop",
                        evidence_id="ev_" + "c" * 32)
        decision = choose_policy(Assessment(PERSON, (request, stopped)))
        self.assertEqual(decision.policy, Policy.STOP_PLAY)
        self.assertEqual(decision.reason, "DIRECT_PLAY_STOP")

    def test_speculation_about_repair_does_not_count_as_explicit_request(self):
        topic = event("task_request", "topic", "discuss", evidence_id=TOPIC_ID)
        speculation = event("repair_request", "interaction", "maybe",
                            evidence_id=REPAIR_ID)
        decision = choose_policy(Assessment(PERSON, (topic, speculation)))
        self.assertEqual(decision.policy, Policy.TASK_DIRECT)


if __name__ == "__main__":
    unittest.main()
