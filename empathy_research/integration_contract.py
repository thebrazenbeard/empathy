"""Read-only cross-repository boundary for the Empathy research selector.

This adapter deliberately does not import Volition, Pre-Active, a model, or a
tool executor.  Empathy can advise a response policy; it cannot mint a current
want, attest a measurement, renew a historical conation, or grant an effect.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
import re
from typing import Iterable

from .policy import Assessment, Evidence, Policy, choose_policy


HINT_SCHEMA = "EMPATHY_RESPONSE_POLICY_HINT_V1"
_EVIDENCE_ID = re.compile(r"ev_[0-9a-f]{32}\Z")
_HYPOTHESIS_ID = re.compile(r"hyp_[0-9a-f]{32}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_DAY = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
MAX_HISTORY_EVENTS = 1000
CONATION_EVENT_KINDS = frozenset({
    "ADD", "REVISE", "CONTRADICT", "REVOKE", "COMPLETE", "REVIEW",
})


@dataclass(frozen=True, slots=True)
class ResponsePolicyHint:
    """Ephemeral policy advice to a host-owned pre-response integration point.

    The hint is not a Pre-Active event, a Volition Signal/ObservationClaim,
    permission to execute, or a claim about anyone's actual mental state.
    """

    policy: str
    reason_code: str
    confidence_band: str
    supporting_evidence_ids: tuple[str, ...]
    superseded_hypothesis_ids: tuple[str, ...]
    focus_needed: bool
    schema: str = HINT_SCHEMA
    consumer: str = "RESPONSE_POLICY_ONLY"
    authority: str = "NONE"
    persistence: str = "EPHEMERAL"
    volition_want_authority: bool = False
    effect_authority: bool = False


def response_policy_hint(assessment: Assessment) -> ResponsePolicyHint:
    """Compute policy advice from PR #7's selector; never accept a forged Decision.

    Admission, authentication, evidence recency, privacy, and response hook
    remain host responsibilities.  No raw person-model content is serialized.
    """
    if type(assessment) is not Assessment:
        raise TypeError("typed Empathy Assessment required")
    # The policy selector intentionally drops invalid references from its
    # output.  The host-facing adapter also rejects them at ingress so a
    # caller cannot silently pass instruction-bearing provenance fields.
    if any(
        item.evidence_id and not _EVIDENCE_ID.fullmatch(item.evidence_id)
        for item in assessment.current_evidence
        if isinstance(item, Evidence) and item.scope_person_id == assessment.person_id
    ):
        raise ValueError("current evidence identifier must be an opaque token")
    if any(
        item.hypothesis_id and not _HYPOTHESIS_ID.fullmatch(item.hypothesis_id)
        for item in assessment.hypotheses
        if item.scope_person_id == assessment.person_id
    ):
        raise ValueError("hypothesis identifier must be an opaque token")
    decision = choose_policy(assessment)
    if (
        decision.authority != "NONE" or decision.persistence != "EPHEMERAL"
        or not isinstance(decision.policy, Policy)
        or decision.confidence_band not in ("NONE", "TENTATIVE", "HIGH_SCORE")
    ):
        raise ValueError("Empathy decision asserted authority or an unknown policy")

    current_ids = {
        item.evidence_id for item in assessment.current_evidence
        if isinstance(item, Evidence) and item.source == "current"
        and item.active and item.scope_person_id == assessment.person_id
    }
    same_person_hypotheses = {
        item.hypothesis_id for item in assessment.hypotheses
        if item.scope_person_id == assessment.person_id
    }
    if any(value not in current_ids for value in decision.evidence_ids):
        raise ValueError("policy cited unadmitted or cross-person evidence")
    if any(value not in same_person_hypotheses for value in decision.superseded_hypotheses):
        raise ValueError("policy superseded a foreign-person hypothesis")
    if any(not _EVIDENCE_ID.fullmatch(value) for value in decision.evidence_ids) or any(
        not _HYPOTHESIS_ID.fullmatch(value)
        for value in decision.superseded_hypotheses
    ):
        raise ValueError("response evidence/hypothesis identifiers must be opaque")

    return ResponsePolicyHint(
        policy=decision.policy.value,
        reason_code=decision.reason,
        confidence_band=decision.confidence_band,
        supporting_evidence_ids=decision.evidence_ids,
        superseded_hypothesis_ids=decision.superseded_hypotheses,
        focus_needed=decision.focus_needed,
    )


def with_historical_conations(
    assessment: Assessment, events: Iterable[object]
) -> Assessment:
    """Place sanitized Conations history in *inert* historical evidence only.

    Expected input is Conations' parse_history_export/historical_context result:
    HistoricalConationEvidence(event_date, event_type, content_sha256,
    evidence_class='HISTORICAL_ONLY').  Callers must authenticate/protect the
    source and person association; this function cannot establish either.
    Neither the source fields nor status can become current evidence.
    """
    if type(assessment) is not Assessment:
        raise TypeError("typed Empathy Assessment required")
    if not isinstance(assessment.person_id, str) or not assessment.person_id.strip():
        raise ValueError("trusted person scope is required for historical attachment")
    material = []
    seen = set()
    for index, event in enumerate(events):
        if index >= MAX_HISTORY_EVENTS:
            raise ValueError("Conations historical batch exceeds bound")
        day = getattr(event, "event_date", None)
        kind = getattr(event, "event_type", None)
        digest = getattr(event, "content_sha256", None)
        evidence_class = getattr(event, "evidence_class", None)
        if (
            evidence_class != "HISTORICAL_ONLY" or type(day) is not str
            or _DAY.fullmatch(day) is None or type(kind) is not str
            or kind not in CONATION_EVENT_KINDS or type(digest) is not str
            or _SHA256.fullmatch(digest) is None
        ):
            raise ValueError("invalid or currentness-promoting Conations history")
        try:
            date.fromisoformat(day)
        except ValueError as exc:
            raise ValueError("invalid historical event date") from exc
        event_key = (day, kind, digest)
        if event_key in seen:
            continue
        seen.add(event_key)
        material.append(Evidence(
            kind="historical_conation", referent="history_only",
            value=kind, confidence=0.0, source="historical",
            scope_person_id=assessment.person_id, active=False,
            evidence_id=f"conation:{day}:{kind}:{digest}",
        ))
    return replace(
        assessment,
        historical_evidence=assessment.historical_evidence + tuple(material),
    )
