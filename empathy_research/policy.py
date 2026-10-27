"""Bounded response-policy selection from *typed, admitted* observations.

This module does not infer emotions from text, authenticate users, retrieve
memory, issue commands, or persist conclusions.  The caller owns person-scope
authentication, evidence admission, and any eventual response-generation hook.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite
import re


# A provenance reference is an opaque host-generated token, never utterance
# text, a memory excerpt, or a descriptive filename. This is a syntax gate,
# not cryptographic proof of unpredictability: the host must generate tokens
# with sufficient entropy and retain any private mapping outside this module.
_EVIDENCE_ID = re.compile(r"ev_[0-9a-f]{32}\Z")
_HYPOTHESIS_ID = re.compile(r"hyp_[0-9a-f]{32}\Z")


def _safe_opaque_id(value: str, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


class Policy(str, Enum):
    CLARIFY_MEANING = "CLARIFY_MEANING"
    TASK_DIRECT = "TASK_DIRECT"
    REPAIR_FIRST = "REPAIR_FIRST"
    CELEBRATE_FIRST = "CELEBRATE_FIRST"
    TRUTHFUL_CHALLENGE = "TRUTHFUL_CHALLENGE"
    PRESERVE_PLAY = "PRESERVE_PLAY"
    STOP_PLAY = "STOP_PLAY"


@dataclass(frozen=True)
class Evidence:
    kind: str
    referent: str
    value: str
    confidence: float
    source: str
    scope_person_id: str
    active: bool = True
    evidence_id: str = ""

    def __post_init__(self):
        if (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("confidence must be finite and between 0 and 1")
        if self.source not in ("current", "historical"):
            raise ValueError("evidence source must be current or historical")
        if type(self.active) is not bool:
            raise ValueError("evidence active flag must be a boolean")


@dataclass(frozen=True)
class Hypothesis:
    referent: str
    value: str
    confidence: float
    scope_person_id: str = ""  # Unscoped hypotheses are inadmissible.
    hypothesis_id: str = ""  # Opaque provenance; raw values never go to Decision.

    def __post_init__(self):
        if (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("hypothesis confidence must be finite and between 0 and 1")


@dataclass(frozen=True)
class Assessment:
    """The person_id must come from a trusted host, not utterance text."""

    person_id: str
    current_evidence: tuple[Evidence, ...] = ()
    historical_evidence: tuple[Evidence, ...] = ()
    hypotheses: tuple[Hypothesis, ...] = ()
    stakes: str = "low"


@dataclass(frozen=True)
class Decision:
    policy: Policy
    reason: str
    confidence_band: str
    evidence_ids: tuple[str, ...] = ()
    superseded_hypotheses: tuple[str, ...] = ()
    focus_needed: bool = False
    authority: str = "NONE"
    persistence: str = "EPHEMERAL"


def choose_policy(assessment: Assessment) -> Decision:
    """Select a research policy, *never* an authorized action or mental-state fact.

    Only active, explicitly current, same-person observations select a route.
    Historical evidence and hypotheses can inform later research but cannot
    establish standing consent or override fresh corrections/withdrawal.
    """
    if not isinstance(assessment.person_id, str) or not assessment.person_id.strip():
        return Decision(Policy.CLARIFY_MEANING, "MISSING_TRUSTED_PERSON_SCOPE", "NONE", focus_needed=True)
    if assessment.stakes not in ("low", "medium", "high"):
        return Decision(Policy.CLARIFY_MEANING, "UNKNOWN_STAKES", "NONE", focus_needed=True)

    observed = tuple(
        item for item in assessment.current_evidence
        if item.scope_person_id == assessment.person_id
        and item.source == "current"
        and item.active
    )
    admitted = tuple(item for item in observed if item.confidence >= 0.5)
    # Uncertain withdrawal cannot *prove* a stop, but must inhibit confident
    # continuation of the same play frame until meaning is clarified.
    uncertain_withdrawals = tuple(
        item for item in observed
        if item.kind == "withdrawal" and (
            (item.value == "stop" and 0.0 < item.confidence < 0.5)
            or (item.value == "possible" and item.confidence > 0.0)
        )
    )
    corrections = tuple(item for item in admitted if item.kind == "direct_correction")
    # A fresh first-person correction supersedes contradicted *inferences* for
    # its referent. It cannot erase external fact-checking or unrelated tasks.
    inferred_kinds = {
        "reciprocal_play", "celebration", "repair_needed", "lexical_tone",
        "task_request", "withdrawal", "ambiguous",
    }
    current = tuple(
        item for item in admitted
        if item.kind not in inferred_kinds or not any(
            correction.referent == item.referent and correction.value != item.value
            for correction in corrections
        )
    )
    superseded = tuple(
        hypothesis.hypothesis_id for hypothesis in assessment.hypotheses
        if hypothesis.scope_person_id == assessment.person_id
        and _safe_opaque_id(hypothesis.hypothesis_id, _HYPOTHESIS_ID)
        and any(
            correction.referent == hypothesis.referent
            and correction.value != hypothesis.value
            for correction in corrections
        )
    )

    def support(kind: str, referent: str | None = None,
                value: str | None = None) -> tuple[Evidence, ...]:
        return tuple(item for item in current if item.kind == kind
                     and (referent is None or item.referent == referent)
                     and (value is None or item.value == value))

    def has(kind: str, referent: str | None = None, value: str | None = None) -> bool:
        return bool(support(kind, referent, value))

    def decide(policy: Policy, reason: str, basis: tuple[Evidence, ...] = (),
               *, focus: bool = False) -> Decision:
        # Preserve provenance only for evidence actually supporting this route.
        used_ids = tuple(
            item.evidence_id for item in basis
            if _safe_opaque_id(item.evidence_id, _EVIDENCE_ID)
        )
        # Confidence is a caller-supplied *score*, not proof of direct
        # testimony, verified fact, or phenomenological access.
        strength = "HIGH_SCORE" if basis and all(item.confidence >= 0.8 for item in basis) else "TENTATIVE"
        # High stakes are an escalation condition irrespective of the selected
        # response category.  In particular, a task route is not permission to
        # silently bypass focused review when consequences are significant.
        return Decision(policy, reason, strength if basis else "NONE", used_ids,
                        superseded, focus or assessment.stakes == "high")

    # Present withdrawal is stronger than an inherited playful relationship.
    # A current direct correction that the play frame has stopped must not be
    # treated as a mere semantic clarification while play may continue.
    if has("direct_correction", "play_frame", "stop"):
        return decide(Policy.STOP_PLAY, "DIRECT_PLAY_STOP",
                      support("direct_correction", "play_frame", "stop"))
    if has("withdrawal", "play_frame", "stop"):
        return decide(Policy.STOP_PLAY, "CURRENT_WITHDRAWAL",
                      support("withdrawal", "play_frame", "stop"))
    possible_stop = tuple(
        item for item in uncertain_withdrawals
        if any(play.referent == item.referent for play in support("reciprocal_play"))
    )
    if possible_stop:
        return decide(Policy.CLARIFY_MEANING, "POSSIBLE_WITHDRAWAL", possible_stop, focus=True)
    # First-person correction changes the corrected referent, not external truth.
    if has("unsupported_claim", "external_fact"):
        return decide(Policy.TRUTHFUL_CHALLENGE, "UNSUPPORTED_FACT", support("unsupported_claim", "external_fact"))
    if has("ambiguous", "task"):
        return decide(Policy.CLARIFY_MEANING, "TASK_INTENT_UNRESOLVED", support("ambiguous", "task"), focus=True)
    # The experimental 0.5 admission cutoff is not evidence that lower-score
    # uncertainty is false.  In high-stakes cases even a weak, nonzero,
    # same-person current doubt about task intent should halt the task route
    # for deliberation.  Zero-score and historical speculation are ineligible.
    uncertain_task_intent = tuple(
        item for item in observed
        if item.kind == "ambiguous" and item.referent == "task"
        and 0.0 < item.confidence < 0.5
        and not any(
            correction.referent == item.referent and correction.value != item.value
            for correction in corrections
        )
    )
    if assessment.stakes == "high" and has("task_request") and uncertain_task_intent:
        return decide(Policy.CLARIFY_MEANING, "HIGH_STAKES_TASK_INTENT_DOUBT",
                      support("task_request") + uncertain_task_intent, focus=True)
    if has("task_request"):
        return decide(Policy.TASK_DIRECT, "EXPLICIT_TASK", support("task_request"))
    if has("repair_needed"):
        return decide(Policy.REPAIR_FIRST, "SUPPORTED_REPAIR", support("repair_needed"))
    if has("celebration"):
        return decide(Policy.CELEBRATE_FIRST, "CURRENT_CELEBRATION", support("celebration"))
    if has("ambiguous") or has("lexical_tone") and not has("reciprocal_play"):
        return decide(Policy.CLARIFY_MEANING, "MEANING_UNRESOLVED",
                      support("ambiguous") + support("lexical_tone"),
                      focus=assessment.stakes == "high")
    if has("reciprocal_play", value="active"):
        active_play = support("reciprocal_play", value="active")
        # Conflicting fresh accounts of the *same* play frame do not justify
        # confident mutuality, even if one account was high-confidence.
        if any(
            item.referent == active.referent and item.value != "active"
            for item in support("reciprocal_play")
            for active in active_play
        ):
            return decide(Policy.CLARIFY_MEANING, "CONFLICTING_PLAY_EVIDENCE",
                          support("reciprocal_play"), focus=True)
        return decide(Policy.PRESERVE_PLAY, "CURRENT_MUTUAL_UPTAKE", active_play)
    if corrections:
        return decide(Policy.CLARIFY_MEANING, "CORRECTION_ACCEPTED", corrections, focus=assessment.stakes == "high")
    return decide(Policy.CLARIFY_MEANING, "NO_CURRENT_POLICY_EVIDENCE", focus=assessment.stakes == "high")
