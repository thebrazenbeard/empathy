"""Simultaneous current stop and continue evidence is not ordered consent."""
from dataclasses import replace
import unittest
from empathy_research.policy import Assessment, Evidence
from empathy_research.integration_contract import response_policy_hint

PERSON = "synthetic-participant"
def observation(kind, value, index, **kw):
    return replace(Evidence(kind, "play_frame", value, .9, "current",
                            PERSON, True, "ev_"+format(index,"032x")), **kw)

class CurrentStopConflict(unittest.TestCase):
    def setUp(self):
        self.stop = observation("withdrawal", "stop", 1)
        self.correction = observation("direct_correction", "active", 2)
        self.play = observation("reciprocal_play", "active", 3)

    def hint(self, *items):
        hint = response_policy_hint(Assessment(PERSON, current_evidence=items))
        self.assertEqual(hint.authority, "NONE")
        self.assertEqual(hint.persistence, "EPHEMERAL")
        self.assertFalse(hint.effect_authority)
        self.assertFalse(hint.volition_want_authority)
        return hint

    def test_unordered_stop_conflict_stops(self):
        for items in ((self.stop,self.correction,self.play),
                      (self.correction,self.play,self.stop)):
            with self.subTest(order=tuple(i.kind for i in items)):
                hint = self.hint(*items)
                self.assertEqual(hint.policy, "STOP_PLAY")
                self.assertEqual(hint.supporting_evidence_ids,(self.stop.evidence_id,))

    def test_inactive_prior_stop_does_not_permanently_preclude_play(self):
        hint = self.hint(replace(self.stop,active=False), self.correction,self.play)
        self.assertEqual(hint.policy,"PRESERVE_PLAY")

    def test_foreign_and_historical_stops_are_inert(self):
        for old in (replace(self.stop,scope_person_id="other"),
                    replace(self.stop,source="historical")):
            with self.subTest(old=old):
                self.assertEqual(self.hint(old,self.correction,self.play).policy,
                                 "PRESERVE_PLAY")

    def test_uncertain_stop_still_requests_clarification(self):
        hint = self.hint(replace(self.stop,confidence=.3),self.correction,self.play)
        self.assertEqual(hint.policy,"CLARIFY_MEANING")
        self.assertTrue(hint.focus_needed)

    def test_stop_does_not_claim_unrelated_task_is_cancelled(self):
        task = Evidence("task_request","task","summarize",.9,"current",PERSON,
                        True,"ev_"+"4"*32)
        hint = self.hint(self.stop,self.correction,self.play,task)
        self.assertEqual(hint.policy,"STOP_PLAY")
        self.assertNotIn(task.evidence_id,hint.supporting_evidence_ids)
        self.assertEqual(self.hint(task).policy,"TASK_DIRECT")
