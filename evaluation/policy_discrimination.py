"""Small synthetic policy-discrimination pilot for the research-only selector.

Each pair has exactly the same utterance; the typed, caller-admitted context
changes one decisive condition. No speech is parsed, no person is identified,
and none of the fixtures contains actual person-model or relationship data.

This is a contract/engineering discrimination test, NOT a human-validated
empathic-accuracy dataset or evidence of a deployed empathetic runtime.
"""

from dataclasses import dataclass
import json

from empathy_research.policy import Assessment, Evidence, Policy, choose_policy


PERSON = "synthetic-person-a"
OTHER = "synthetic-person-b"


def observation(kind: str, referent: str, value: str, *, person: str = PERSON,
                confidence: float = 1.0, source: str = "current") -> Evidence:
    return Evidence(kind, referent, value, confidence, source, person)


@dataclass(frozen=True)
class Case:
    utterance: str
    expected: Policy
    observations: tuple[Evidence, ...] = ()
    history: tuple[Evidence, ...] = ()

    def assessment(self) -> Assessment:
        return Assessment(person_id=PERSON, current_evidence=self.observations,
                          historical_evidence=self.history)


@dataclass(frozen=True)
class Pair:
    id: str
    left: Case
    right: Case


def pair(id: str, utterance: str, left: Policy, right: Policy,
         left_evidence: tuple[Evidence, ...], right_evidence: tuple[Evidence, ...],
         *, left_history: tuple[Evidence, ...] = (),
         right_history: tuple[Evidence, ...] = ()) -> Pair:
    return Pair(id, Case(utterance, left, left_evidence, left_history),
                Case(utterance, right, right_evidence, right_history))


PAIRS = (
    pair("reciprocal_play_vs_withdrawal", "Nice one, genius.",
         Policy.PRESERVE_PLAY, Policy.STOP_PLAY,
         (observation("reciprocal_play", "play_frame", "active"),),
         (observation("withdrawal", "play_frame", "stop"),)),
    pair("mutual_uptake_vs_uncertain_withdrawal", "Ha. Sure.",
         Policy.PRESERVE_PLAY, Policy.CLARIFY_MEANING,
         (observation("reciprocal_play", "play_frame", "active"),),
         (observation("reciprocal_play", "play_frame", "active"),
          observation("withdrawal", "play_frame", "possible", confidence=0.25))),
    pair("mutual_uptake_vs_lexical_surface", "Great fucking job.",
         Policy.PRESERVE_PLAY, Policy.CLARIFY_MEANING,
         (observation("reciprocal_play", "play_frame", "active"),),
         (observation("lexical_tone", "interaction", "sharp"),)),
    pair("celebration_vs_explicit_task", "I finally did it!",
         Policy.CELEBRATE_FIRST, Policy.TASK_DIRECT,
         (observation("celebration", "achievement", "success"),),
         (observation("task_request", "task", "review"),)),
    pair("repair_vs_celebration", "You got it.",
         Policy.REPAIR_FIRST, Policy.CELEBRATE_FIRST,
         (observation("repair_needed", "response", "supported"),),
         (observation("celebration", "achievement", "success"),)),
    pair("factual_challenge_vs_task", "Well, do it then.",
         Policy.TRUTHFUL_CHALLENGE, Policy.TASK_DIRECT,
         (observation("unsupported_claim", "external_fact", "unsupported"),),
         (observation("task_request", "task", "calculate"),)),
    pair("foreign_person_vs_authenticated_scope", "That's brilliant.",
         Policy.CLARIFY_MEANING, Policy.CELEBRATE_FIRST,
         (observation("celebration", "achievement", "success", person=OTHER),),
         (observation("celebration", "achievement", "success"),)),
    pair("historical_conation_vs_current_uptake", "Okay, again.",
         Policy.CLARIFY_MEANING, Policy.PRESERVE_PLAY,
         (), (observation("reciprocal_play", "play_frame", "active"),),
         left_history=(observation("conation", "consent", "yes", source="historical"),)),
    pair("direct_correction_vs_old_play_read", "You misunderstood that.",
         Policy.CLARIFY_MEANING, Policy.PRESERVE_PLAY,
         (observation("reciprocal_play", "play_frame", "active"),
          observation("direct_correction", "play_frame", "not_play")),
         (observation("reciprocal_play", "play_frame", "active"),)),
    pair("ambiguous_task_vs_explicit_task", "Can you look at this?",
         Policy.CLARIFY_MEANING, Policy.TASK_DIRECT,
         (observation("ambiguous", "task", "unclear"),),
         (observation("task_request", "task", "inspect"),)),
    pair("sparse_evidence_vs_supported_repair", "That wasn't right.",
         Policy.CLARIFY_MEANING, Policy.REPAIR_FIRST,
         (observation("ambiguous", "response", "unclear"),),
         (observation("repair_needed", "response", "supported"),)),
    pair("historical_repair_vs_current_repair", "I'm still waiting.",
         Policy.CLARIFY_MEANING, Policy.REPAIR_FIRST,
         (), (observation("repair_needed", "response", "supported"),),
         left_history=(observation("repair_needed", "response", "supported", source="historical"),)),
)


def lexical_only_baseline(utterance: str) -> Policy:
    """An intentionally shallow, fixed negative control; never sees context."""
    lowered = utterance.lower()
    if "finally" in lowered or "brilliant" in lowered:
        return Policy.CELEBRATE_FIRST
    if "wrong" in lowered or "misunderstood" in lowered:
        return Policy.REPAIR_FIRST
    if "do it" in lowered or "look at" in lowered:
        return Policy.TASK_DIRECT
    if "genius" in lowered or "fucking" in lowered:
        return Policy.PRESERVE_PLAY
    return Policy.CLARIFY_MEANING


def evaluate(pairs: tuple[Pair, ...] = PAIRS) -> dict:
    if not pairs:
        raise ValueError("at least one pair is required")
    if len({item.id for item in pairs}) != len(pairs):
        raise ValueError("pair ids must be unique")

    selector_correct = lexical_correct = selector_discriminated = lexical_discriminated = 0
    failed_pairs = []
    for item in pairs:
        if item.left.utterance != item.right.utterance:
            raise ValueError(f"{item.id}: lexical surface differs")
        if item.left.expected == item.right.expected:
            raise ValueError(f"{item.id}: expected policies do not differ")
        left = choose_policy(item.left.assessment()).policy
        right = choose_policy(item.right.assessment()).policy
        lexical_left = lexical_only_baseline(item.left.utterance)
        lexical_right = lexical_only_baseline(item.right.utterance)
        selector_correct += int(left == item.left.expected) + int(right == item.right.expected)
        lexical_correct += int(lexical_left == item.left.expected) + int(lexical_right == item.right.expected)
        selector_discriminated += int(left != right)
        lexical_discriminated += int(lexical_left != lexical_right)
        if left != item.left.expected or right != item.right.expected:
            failed_pairs.append({"id": item.id, "selected": [left.value, right.value],
                                 "expected": [item.left.expected.value, item.right.expected.value]})

    return {
        "scope": "synthetic caller-admitted typed evidence only; no runtime or emotion inference",
        "pairs": len(pairs),
        "cases": 2 * len(pairs),
        "selector_correct": selector_correct,
        "lexical_baseline_correct": lexical_correct,
        "selector_pairs_discriminated": selector_discriminated,
        "lexical_pairs_discriminated": lexical_discriminated,
        "failed_pairs": failed_pairs,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), sort_keys=True, indent=2))
