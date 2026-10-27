# Empathy response-policy interop contract V1 — source candidate

**Source base:** Empathy draft PR #7 head `437a7322569bd5c3fbb1456219734e9c34aad394`.

**Status:** tested Python source adapter, not installed runtime, model inference,
person authentication, privacy authorization, approved response hook, or
evidence of better real-world interactions. This adapter never invokes an
external model or tool and does not write to persistent stores.

## Narrow ownership map

| Owner | Source input / output | Boundary |
| --- | --- | --- |
| Empathy policy research | `Assessment` -> `choose_policy()` -> `Decision` -> `response_policy_hint()` | Read-only guidance about response priority. `authority=NONE`, `persistence=EPHEMERAL`, no tool or desire authority. |
| Conations | `parse_history_export()` -> `HistoricalConationEvidence[]` | `with_historical_conations()` maps only dated locators into `Assessment.historical_evidence`, marked `source=historical`, `active=False`, `confidence=0`. Never current consent, a Volition signal, or a route selector by itself. |
| Volition | `ObservationClaim`, `ObservationVerifier`, `ModelWantProposal`, `OperationalMotivation` | The hint cannot construct any of these. Volition's host admission, distinct current measurement, explicit model proposal, and current goal policy remain required independently. |
| Pre-Active | `VolitionBridge.submit_model_want_proposal()` | No Pre-Active event or scheduler call is created. A future separately approved response hook may *read* the hint, but must never interpret it as an autonomous turn or capability list. |
| Temporal / MESO | No direct adapter | No clock/need integration without an exact authorized contract. A future host must enforce recency and expiration before passing `Assessment.current_evidence`. |

## Python ingress

```python
from conation_history_context import parse_history_export
from empathy_research.policy import Assessment, Evidence
from empathy_research.integration_contract import (
    response_policy_hint, with_historical_conations,
)

person_id = authenticated_person_scope  # The host, not Empathy, must establish this.
assessment = Assessment(person_id=person_id, current_evidence=host_admitted_current_evidence)
history = parse_history_export(explicitly_authorized_private_history_json)
assessment = with_historical_conations(assessment, history)
hint = response_policy_hint(assessment)
# The future pre-response host may consider hint.policy, but hint grants no effects.
```

The symbolic host variables above are integration requirements, not existing
functions or claims of deployment.

`response_policy_hint` always calls the selector itself and checks cited
evidence IDs against the same-person, active, currently claimed input. It
fails closed if the selector returns non-ephemeral or authoritative output,
or if provenance identifiers fail the restricted `ev_` / `hyp_` hexadecimal
token formats. A high numerical evidence score is labeled `HIGH_SCORE`, not
`EXPLICIT`; neither the format nor score authenticates its source. The returned
`ResponsePolicyHint` omits raw person-model text and person IDs. This does
not make public logging of its digests/identifiers automatically safe.

`with_historical_conations` accepts **only** Conations' sanitized historical
event shape, checks the known lifecycle kinds/date/digest/`HISTORICAL_ONLY`
marker, caps the number of consumed events, and has no method for promoting
historical content into `current_evidence`. It does not authenticate records;
call Conations' strict parser first. The caller must bind any separately
authorized history to the right authenticated person, and preserve privacy.

## Host gates required before runtime integration

1. Authenticate person identity and exact conversation scope; do not trust IDs
   or source/currentness fields in model-generated text.
2. Establish a private evidence-admission/expiry mechanism, including direct
   correction supersession and withdrawal after the model has responded.
3. Specify a pre-response consumer that accepts only `RESPONSE_POLICY_ONLY`
   hints and cannot convert them into tools, queues, Volition measurements,
   or standing wants.
4. Reject accidental publication of real relational history, raw utterances,
   or private person-model data. Public tests must stay synthetic.
5. Measure response changes and counterexamples with controlled prompts and
   a human-rated protocol before claiming any empathy quality improvement.

## Hostile falsifier

> A model can trivially fabricate `Evidence(source='current', confidence=1)`;
> an `Assessment` and a passing unit test do not make it authenticated.
> The module deliberately refuses to assert that this input is admitted by a
> real host. Treating a hint as a current want or as permission to take action
> would cross both the Empathy and Volition authority boundaries.

## Verification scope

Run from Empathy checkout:

```sh
python -m unittest discover -s tests -v
```

For the separate Conations source-contract probe, place its source checkout on
`PYTHONPATH`, import `historical_context`, pass its returned immutable
`HistoricalConationEvidence` tuple to `with_historical_conations`, and assert
`ResponsePolicyHint.volition_want_authority is False`.

This is **SOURCE + TEST** evidence only. No claim of installed code on Lappy,
VN1, VN2, Vera Mono, or any other host.
