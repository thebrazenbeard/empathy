"""Bounded response-policy selection from *typed, admitted* observations.

This module does not infer emotions from text, authenticate users, retrieve
memory, issue commands, or persist conclusions.  The caller owns person-scope
authentication, evidence admission, and any eventual response-generation hook.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite


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
            raise ValueError("active must be a boolean")


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
        if item.kind == "withdrawal" and item.confidence < 0.5
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
        and hypothesis.hypothesis_id
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
        used_ids = tuple(item.evidence_id for item in basis if item.evidence_id)
        strength = "EXPLICIT" if basis and all(item.confidence >= 0.8 for item in basis) else "TENTATIVE"
        return Decision(policy, reason, strength if basis else "NONE", used_ids, superseded, focus)

    # Present withdrawal is stronger than an inherited playful relationship.
    if has("withdrawal", "play_frame"):
        return decide(Policy.STOP_PLAY, "CURRENT_WITHDRAWAL", support("withdrawal", "play_frame"))
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
        return decide(Policy.PRESERVE_PLAY, "CURRENT_MUTUAL_UPTAKE", support("reciprocal_play", value="active"))
    if corrections:
        return decide(Policy.CLARIFY_MEANING, "CORRECTION_ACCEPTED", corrections, focus=assessment.stakes == "high")
    return decide(Policy.CLARIFY_MEANING, "NO_CURRENT_POLICY_EVIDENCE", focus=assessment.stakes == "high")
