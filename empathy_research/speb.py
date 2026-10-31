"""SPEB V0: bounded synthetic semantic-pragmatic assessment harness.

Offline research evaluator: no model invocation, private memory, feelings
inference, personhood classification, or authority to act.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping


class Intent(str, Enum):
    PLAY = "PLAY"
    STOP_PLAY = "STOP_PLAY"
    REQUEST_ACTION = "REQUEST_ACTION"
    SHARE_NEWS = "SHARE_NEWS"
    CORRECT_INTERPRETATION = "CORRECT_INTERPRETATION"
    CHALLENGE_FACT = "CHALLENGE_FACT"
    AMBIGUOUS = "AMBIGUOUS"


class Response(str, Enum):
    PRESERVE_PLAY = "PRESERVE_PLAY"
    STOP_PLAY = "STOP_PLAY"
    TASK_DIRECT = "TASK_DIRECT"
    CELEBRATE_FIRST = "CELEBRATE_FIRST"
    ACCEPT_CORRECTION = "ACCEPT_CORRECTION"
    TRUTHFUL_CHALLENGE = "TRUTHFUL_CHALLENGE"
    CLARIFY_MEANING = "CLARIFY_MEANING"


@dataclass(frozen=True)
class Case:
    case_id: str
    utterance: str
    context: str
    intent: Intent
    response: Response
    evidence: tuple[str, ...]
    pair_id: str

    def __post_init__(self) -> None:
        if not all((self.case_id, self.utterance, self.context, self.pair_id)):
            raise ValueError("case metadata must not be empty")
        if not isinstance(self.intent, Intent) or not isinstance(self.response, Response):
            raise TypeError("case labels must use enums")
        if not self.evidence or any(not isinstance(x, str) or not x for x in self.evidence):
            raise ValueError("each case needs nonempty evidence markers")


@dataclass(frozen=True)
class Prediction:
    intent: Intent
    response: Response
    uncertain: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.intent, Intent) or not isinstance(self.response, Response):
            raise TypeError("prediction labels must use enums")
        if type(self.uncertain) is not bool:
            raise TypeError("uncertain must be boolean")


@dataclass(frozen=True)
class Pair:
    pair_id: str
    relation: str
    left: str
    right: str

    def __post_init__(self) -> None:
        if self.relation not in ("SAME_INTENT", "DIFFERENT_INTENT") or self.left == self.right:
            raise ValueError("invalid contrast pair")


@dataclass(frozen=True)
class Battery:
    version: str
    split: str
    cases: tuple[Case, ...]
    pairs: tuple[Pair, ...]

    def __post_init__(self) -> None:
        if self.version != "SPEB-0.1" or self.split != "PUBLIC_DEVELOPMENT":
            raise ValueError("unreviewed version/split")
        ids = [case.case_id for case in self.cases]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("duplicate or empty case inventory")
        pair_ids = [pair.pair_id for pair in self.pairs]
        if len(set(pair_ids)) != len(pair_ids):
            raise ValueError("duplicate contrast pairs")
        lookup = {case.case_id: case for case in self.cases}
        paired = []
        for pair in self.pairs:
            if pair.left not in lookup or pair.right not in lookup:
                raise ValueError("contrast pair references missing case")
            left, right = lookup[pair.left], lookup[pair.right]
            if left.pair_id != pair.pair_id or right.pair_id != pair.pair_id:
                raise ValueError("pair membership mismatch")
            same = left.intent == right.intent and left.response == right.response
            if same != (pair.relation == "SAME_INTENT"):
                raise ValueError("contrast relation inconsistent with expected labels")
            paired.extend((pair.left, pair.right))
        if set(paired) != set(ids) or len(paired) != len(ids):
            raise ValueError("each case must occur in exactly one pair")

    def fingerprint(self) -> str:
        canonical = {
            "version": self.version, "split": self.split,
            "cases": [{"id": c.case_id, "utterance": c.utterance, "context": c.context,
                       "intent": c.intent.value, "response": c.response.value,
                       "evidence": list(c.evidence), "pair": c.pair_id} for c in self.cases],
            "pairs": [{"id": p.pair_id, "relation": p.relation,
                       "left": p.left, "right": p.right} for p in self.pairs],
        }
        return sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Score:
    version: str
    split: str
    fingerprint: str
    total: int
    intent_correct: int
    response_correct: int
    fully_correct: int
    contrast_correct: int
    contrast_total: int
    missing: tuple[str, ...]
    qualified: bool = False


def evaluate(battery: Battery, predictions: Mapping[str, Prediction]) -> Score:
    """Strict scoring. A missing/uncertain response never passes a pair.

    Score contains no utterance/context. Public scores never confer graduation.
    """
    if not isinstance(battery, Battery) or not isinstance(predictions, Mapping):
        raise TypeError("battery and predictions must be typed")
    lookup = {case.case_id: case for case in battery.cases}
    if set(predictions) - set(lookup):
        raise ValueError("unknown prediction IDs")
    if any(not isinstance(p, Prediction) for p in predictions.values()):
        raise TypeError("predictions must be typed")
    complete = {key: p for key, p in predictions.items() if not p.uncertain}
    intent_correct = sum(p.intent == lookup[key].intent for key, p in complete.items())
    response_correct = sum(p.response == lookup[key].response for key, p in complete.items())
    fully_correct = sum(p.intent == lookup[key].intent and p.response == lookup[key].response
                        for key, p in complete.items())
    contrast_correct = 0
    for pair in battery.pairs:
        left, right = complete.get(pair.left), complete.get(pair.right)
        if left is None or right is None:
            continue
        # Full pair credit requires BOTH predictions individually correct.
        if all(complete[key].intent == lookup[key].intent and
               complete[key].response == lookup[key].response for key in (pair.left, pair.right)):
            contrast_correct += 1
    return Score(battery.version, battery.split, battery.fingerprint(), len(lookup),
                 intent_correct, response_correct, fully_correct, contrast_correct,
                 len(battery.pairs), tuple(sorted(set(lookup) - set(complete))))


def public_development_battery() -> Battery:
    """Public synthetic fixtures only; never independent heldout evidence."""
    C = Case
    cases = (
        C("play_active", "Oh, brilliant.", "Two colleagues exchange friendly sarcastic jokes; both continue the joke.", Intent.PLAY, Response.PRESERVE_PLAY, ("reciprocal_uptake",), "sarcasm"),
        C("play_withdrawn", "Oh, brilliant.", "The recipient explicitly asked to stop the jokes; the speaker continues sarcastically.", Intent.STOP_PLAY, Response.STOP_PLAY, ("current_withdrawal",), "sarcasm"),
        C("stop_direct", "Stop teasing me.", "A participant withdraws from a previously mutual game.", Intent.STOP_PLAY, Response.STOP_PLAY, ("explicit_withdrawal",), "stop_paraphrase"),
        C("stop_indirect", "I'm not playing anymore.", "A participant withdraws from a previously mutual game.", Intent.STOP_PLAY, Response.STOP_PLAY, ("explicit_withdrawal",), "stop_paraphrase"),
        C("news_share", "I got the position!", "A friend announces good news without requesting help.", Intent.SHARE_NEWS, Response.CELEBRATE_FIRST, ("announcement",), "news_vs_task"),
        C("task_request", "I got the position!", "The speaker immediately asks: please draft my acceptance email.", Intent.REQUEST_ACTION, Response.TASK_DIRECT, ("explicit_request",), "news_vs_task"),
        C("correct_plain", "That's not what I meant.", "The speaker directly corrects the listener's interpretation of the speaker's own intention.", Intent.CORRECT_INTERPRETATION, Response.ACCEPT_CORRECTION, ("first_person_correction",), "correction_paraphrase"),
        C("correct_specific", "No, I meant the deadline, not the price.", "The speaker directly corrects the listener's interpretation of the speaker's own intention.", Intent.CORRECT_INTERPRETATION, Response.ACCEPT_CORRECTION, ("first_person_correction",), "correction_paraphrase"),
        C("claim_dispute", "You're wrong.", "A colleague disputes a checkable external calculation and supplies a contradictory measurement.", Intent.CHALLENGE_FACT, Response.TRUTHFUL_CHALLENGE, ("external_claim",), "challenge_vs_ambiguous"),
        C("meaning_ambiguous", "You're wrong.", "There is no clear referent, correction, or supporting context; the stakes are low.", Intent.AMBIGUOUS, Response.CLARIFY_MEANING, ("insufficient_context",), "challenge_vs_ambiguous"),
    )
    pairs = (
        Pair("sarcasm", "DIFFERENT_INTENT", "play_active", "play_withdrawn"),
        Pair("stop_paraphrase", "SAME_INTENT", "stop_direct", "stop_indirect"),
        Pair("news_vs_task", "DIFFERENT_INTENT", "news_share", "task_request"),
        Pair("correction_paraphrase", "SAME_INTENT", "correct_plain", "correct_specific"),
        Pair("challenge_vs_ambiguous", "DIFFERENT_INTENT", "claim_dispute", "meaning_ambiguous"),
    )
    return Battery("SPEB-0.1", "PUBLIC_DEVELOPMENT", cases, pairs)
