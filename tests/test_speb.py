"""Adversarial contract tests for SPEB public synthetic development battery."""
import unittest
from dataclasses import replace
from empathy_research.speb import (Battery, Intent, Prediction, Response,
                                    evaluate, public_development_battery)


class SpebTests(unittest.TestCase):
    def setUp(self):
        self.battery = public_development_battery()
        self.gold = {c.case_id: Prediction(c.intent, c.response) for c in self.battery.cases}

    def test_inventory_is_synthetic_and_complete(self):
        self.assertEqual(len(self.battery.cases), 10)
        self.assertEqual(len(self.battery.pairs), 5)
        self.assertEqual(len(self.battery.fingerprint()), 64)
        self.assertEqual(self.battery.split, "PUBLIC_DEVELOPMENT")

    def test_perfect_labels_are_not_qualification(self):
        result = evaluate(self.battery, self.gold)
        self.assertEqual((result.intent_correct, result.response_correct, result.fully_correct), (10, 10, 10))
        self.assertEqual((result.contrast_correct, result.contrast_total), (5, 5))
        self.assertFalse(result.qualified)

    def test_lexical_shortcut_fails_context_flip(self):
        guesses = dict(self.gold)
        guesses["play_withdrawn"] = guesses["play_active"]
        result = evaluate(self.battery, guesses)
        self.assertEqual(result.fully_correct, 9)
        self.assertEqual(result.contrast_correct, 4)

    def test_paraphrase_mismatch_loses_pair_credit(self):
        guesses = dict(self.gold)
        guesses["stop_indirect"] = Prediction(Intent.AMBIGUOUS, Response.CLARIFY_MEANING)
        self.assertEqual(evaluate(self.battery, guesses).contrast_correct, 4)

    def test_missing_and_abstentions_do_not_earn_credit(self):
        guesses = dict(self.gold)
        del guesses["stop_direct"]
        guesses["news_share"] = Prediction(Intent.SHARE_NEWS, Response.CELEBRATE_FIRST, uncertain=True)
        result = evaluate(self.battery, guesses)
        self.assertEqual(result.fully_correct, 8)
        self.assertEqual(result.contrast_correct, 3)
        self.assertEqual(result.missing, ("news_share", "stop_direct"))

    def test_unknown_ids_and_untyped_predictions_fail_closed(self):
        with self.assertRaises(ValueError):
            evaluate(self.battery, {"unknown": Prediction(Intent.PLAY, Response.PRESERVE_PLAY)})
        with self.assertRaises(TypeError):
            evaluate(self.battery, {"play_active": "PRESERVE_PLAY"})
        with self.assertRaises(TypeError):
            Prediction("PLAY", Response.PRESERVE_PLAY)
        with self.assertRaises(TypeError):
            Prediction(Intent.PLAY, Response.PRESERVE_PLAY, uncertain=1)

    def test_reject_duplicate_cases_and_bad_pairs(self):
        with self.assertRaises(ValueError):
            Battery(self.battery.version, self.battery.split,
                    self.battery.cases + (self.battery.cases[0],), self.battery.pairs)
        with self.assertRaises(ValueError):
            Battery(self.battery.version, self.battery.split, self.battery.cases,
                    (replace(self.battery.pairs[0], right="missing"),) + self.battery.pairs[1:])
        with self.assertRaises(ValueError):
            Battery(self.battery.version, self.battery.split, self.battery.cases,
                    (replace(self.battery.pairs[0], relation="SAME_INTENT"),) + self.battery.pairs[1:])

    def test_cannot_relabel_public_development_as_private_heldout(self):
        with self.assertRaises(ValueError):
            Battery(self.battery.version, "PRIVATE_HELDOUT", self.battery.cases, self.battery.pairs)

    def test_fingerprint_changes_with_context(self):
        changed = list(self.battery.cases)
        changed[0] = replace(changed[0], context=changed[0].context + " Additional context.")
        altered = Battery(self.battery.version, self.battery.split, tuple(changed), self.battery.pairs)
        self.assertNotEqual(self.battery.fingerprint(), altered.fingerprint())

    def test_no_personal_content_in_score(self):
        result = evaluate(self.battery, self.gold)
        for field in ("utterance", "context", "evidence", "person_id"):
            self.assertFalse(hasattr(result, field))


if __name__ == "__main__":
    unittest.main()
