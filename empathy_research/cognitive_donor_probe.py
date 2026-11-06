"""A read-only *actual Empathy* invocation for a host's admitted task observations.

No static proxy donor scores: the policy and reason come from response_policy_hint,
which runs the canonical choose_policy selector in this repository. All input
provenance and currentness remain host claims, not authenticated by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .integration_contract import response_policy_hint
from .policy import Assessment, Evidence


_OPAQUE_EVIDENCE = re.compile(r"ev_[0-9a-f]{32}\Z")


@dataclass(frozen=True, slots=True)
class CognitiveDonorResult:
    donor: str
    policy: str
    reason_code: str
    confidence_band: str
    focus_needed: bool
    supporting_evidence_ids: tuple[str, ...]
    provenance: str = "CALLER_SUPPLIED_CURRENT_EVIDENCE_UNVERIFIED"
    evaluation: str = "CANONICAL_EMPATHY_RESPONSE_POLICY_HINT_EXECUTED"
    source_proof: str = "SOURCE_ONLY_NOT_HOST_ATTESTED"
    authority: str = "NONE"
    memory_admission: str = "NONE"
    effect_authority: bool = False
    model_identity: str = "UNQUALIFIED"


def evaluate_current_task(assessment: Assessment) -> CognitiveDonorResult:
    """Run Empathy on typed host-admitted *current* evidence only.

    A caller must resolve user/person scope and source truth separately. This
    function intentionally requires at least one current same-person observation
    and refuses history, hypotheses, mixed-person and forged evidence. It cannot
    derive semantic categories from raw text or attest host-authored fields.
    """
    if type(assessment) is not Assessment:
        raise TypeError("canonical Empathy Assessment required")
    if assessment.historical_evidence or assessment.hypotheses:
        raise ValueError("private/historical evidence excluded from donor probe")
    if not assessment.person_id or not assessment.person_id.strip():
        raise ValueError("host-admitted person scope required")
    if not assessment.current_evidence:
        raise ValueError("no current task evidence: no donor value synthesized")
    for observed in assessment.current_evidence:
        if (type(observed) is not Evidence
                or observed.source != "current"
                or observed.active is not True
                or observed.scope_person_id != assessment.person_id
                or type(observed.evidence_id) is not str
                or _OPAQUE_EVIDENCE.fullmatch(observed.evidence_id) is None):
            raise ValueError("only active typed current same-person evidence with opaque IDs permitted")
    selected = response_policy_hint(assessment)
    return CognitiveDonorResult(
        donor="empathy",
        policy=selected.policy,
        reason_code=selected.reason_code,
        confidence_band=selected.confidence_band,
        focus_needed=selected.focus_needed,
        supporting_evidence_ids=selected.supporting_evidence_ids,
    )
