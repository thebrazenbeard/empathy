> **License:** Source-visible, **not open source**. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Empathy — evidence-bounded response-policy research

**A Python reference selector for adapting an agent's response strategy to typed, scoped evidence without treating an inference as a fact or permission.**

Empathy explores how a host can distinguish requests for clarification, direct task handling, repair, celebration, truthful challenge, reciprocal play, and withdrawal. Its implemented research primitives operate on explicit `Assessment`, `Evidence`, and `Hypothesis` records. They do **not** infer feelings from arbitrary text, read conversation memory, run an LLM, or execute tools.

The repository also preserves a **project-specific relational-architecture research history**. That history is design context, not a generic SDK, deployed agent personality, portable person profile, or evidence of live empathy. The Python selector can be studied independently of those historical documents.

## Implemented surfaces

| Component | Supported behavior | Excluded claim |
| --- | --- | --- |
| `empathy_research.policy.choose_policy` | Deterministic response-policy choice from typed, person-scoped observations and hypotheses | Mental-state detection, psychological probability calibration, or action permission |
| `empathy_research.integration_contract.response_policy_hint` | Ephemeral `EMPATHY_RESPONSE_POLICY_HINT_V1` output with opaque supporting-evidence IDs | An authenticated observation, durable desire, standing consent, or effect authority |
| Historical conation adapter | Places appropriately shaped historical evidence into an **inactive** history-only channel | Turning old preferences into current intent or new instructions |
| Research evaluation cases | Synthetic and source-bounded tests for corrections, scope, ambiguity, high stakes, and provenance | Demonstrated real-world relational improvement or live host integration |

The current source is a standard-library Python research package in `empathy_research/`. It has no declared installable distribution, CLI, hosted API, or continuously running service in this repository.

## Run a synthetic example

From a permitted checkout with Python 3.10 or newer, run:

```python
from empathy_research import Assessment, Evidence, choose_policy

assessment = Assessment(
    person_id="person-demo",
    current_evidence=(
        Evidence(
            kind="direct_correction",
            referent="play_frame",
            value="stop",
            confidence=1.0,
            source="current",
            scope_person_id="person-demo",
            evidence_id="ev_" + "a" * 32,
        ),
    ),
)
decision = choose_policy(assessment)
assert decision.policy.value == "STOP_PLAY"
assert decision.authority == "NONE"
assert decision.persistence == "EPHEMERAL"
print(decision.policy.value, decision.reason)
```

This is **synthetic caller-supplied evidence**, not an authenticated statement by an actual person. The host must establish identity, scope, provenance, consent, and evidence currentness separately. An `ev_` identifier's syntax is not proof of authenticity or unpredictability; its private mapping must remain outside this module. The research selector uses a tentative numeric admission cutoff of `0.5` and a `HIGH_SCORE` label from caller-supplied values; neither is a calibrated probability of anyone's private experience.

## Integration boundary

1. A trusted host identifies the relevant person and admits observations under its own privacy and authorization rules.
2. It constructs a typed `Assessment`; old events remain historical and inactive, while directly scoped corrections can supersede contradicting inferences about the same referent.
3. `choose_policy` returns advisory response handling and references to eligible opaque evidence IDs. High-stakes uncertainty requests focused review; uncertainty is not silently converted to consent or obedience.
4. An independent host may consume an ephemeral response-policy hint. The host still owns any model turn, effects, persistence, audit, and verification.

**Invariant:** `EMPATHY_INFERENCE != FACT != CURRENT_CONSENT != AUTHORITY != ACTION`. A decision cannot prove another entity's internal state, guarantee empathetic behavior, or grant effect permission. See [response-policy interoperability contract](docs/RESPONSE_POLICY_INTEROP_CONTRACT_V1.md) and the [source adapter](empathy_research/integration_contract.py).

## Verification

Run the repository's deterministic synthetic tests from its root:

```sh
python -m unittest discover -s tests -v
```

The tests cover policy routes, falsifiers, provenance, integration contracts, and editor-startup source safety. Passing tests establish only the bounded behavior of this source snapshot; they are **not** a clinical validation, an independent emotional-state measurement, a production security review, a model-training result, or proof that an agent runtime uses the selector.

## Project-specific research and provenance

The original architecture was deliberately designed around a particular agent/person relationship and remains preserved as authored. This repository's current research direction maintains that provenance while distinguishing it from the reusable typed selector:

- [Historical relational architecture](VERA_REACTIVE_EMPATHY_ARCHITECTURE.md) — working foundation/design candidate, not an installed runtime.
- [Current repository direction](docs/CURRENT_DIRECTION_2026-09-06.md) — later corrections to that design.
- [Architecture artifact/status map](docs/ARCHITECTURE_STATUS.md) — provenance and qualification distinctions.
- [Research-case index](research/README.md) — source-bounded cases and evidence ceilings.

This public repository must not be used as a dumping ground for private person-model records, raw interactions, or transcripts. Demonstrations and unit tests should use fictional identifiers and synthetic events. Source files or past personal examples are not portable population-wide assumptions and must not be exported into another user's or model's identity/consent context.

## Source and deployment safety

The tracked tree contains source checks intended to prevent automatic VS Code `folderOpen` execution and executable content masquerading as font assets. Their passing result concerns the inspected checkout only; it does not establish the safety of old revisions, a user's editor configuration, or a deployed host. Do not execute unreviewed historical payloads.

**Status:** source-only research implementation and historical architecture materials. No active model integration, credentialed memory access, live empathy qualification, user-person modeling service, or protected-effect route is established by this repository.
