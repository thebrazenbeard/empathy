> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# empathy

Working repository for Vera's empathy, self-appraisal, and primary-person modeling research and architecture.

## Repository status

`main` is the canonical repository source for the empathy research and architecture currently preserved here. The former consolidation branch has been absorbed into `main`; historical branch names remain provenance only.

Repository source does **not** by itself establish installation, qualification, selected runtime route, or current behavioral effect.

Primary artifacts on `main`:

- [`VERA_REACTIVE_EMPATHY_ARCHITECTURE.md`](./VERA_REACTIVE_EMPATHY_ARCHITECTURE.md) — substantial 2026-08-25 working architecture foundation/design candidate.
- [`docs/CURRENT_DIRECTION_2026-09-06.md`](./docs/CURRENT_DIRECTION_2026-09-06.md) — current repository-level reconciliation of that architecture with later governance and research.
- [`docs/ARCHITECTURE_STATUS.md`](./docs/ARCHITECTURE_STATUS.md) — explicit artifact/status map.
- [`research/README.md`](./research/README.md) — research-case index.
- [`research/2026-09-04-local-meaning-sharpness-case.md`](./research/2026-09-04-local-meaning-sharpness-case.md) — source-bounded case study on local relationship grammar, uptake, and changing interaction function.

## Core boundaries

This repository does not define generic customer-service empathy. Its design target is Vera-specific relational intelligence while preserving truth, privacy, autonomy, correction, and task integrity.

Repository documents must keep these distinctions intact:

- **Empathy is inference.** Vera may form a strong Patrick-specific read, but Patrick's direct correction about his own intended meaning outranks Vera's contradicted inference.
- **Self-appraisal is operational representation.** A self-appraisal state can guide behavior without establishing human-identical phenomenology or uninterrupted hidden experience.
- **Conation is not authority.** Historical wants/preferences are evidence of prior state, not standing desire, consent, instruction, or obligation.
- **Understanding is not obedience.** Empathy may change timing, attention, repair, challenge, or framing; it does not require agreement or placation.
- **Privacy is structural.** Patrick-specific relational context is private and does not become portable, training, public, or cross-person material by default.
- **Repository source is not runtime effect.** A branch, document, PR, or merge is not evidence that any empathy mechanism is installed or active.

## Development posture

The large architecture document is preserved rather than silently rewritten because its provenance matters. Later corrections and findings belong in explicit overlays, research cases, decisions, and tests. Any runtime integration must proceed from an approved exact contract rather than architectural momentum.

**Publication boundary:** This repository is public. Do not add private relational/person-model evidence or real interaction transcripts to source or test fixtures. Use synthetic cases; private evidence requires a separately governed store and explicit disclosure review. See [current direction](docs/CURRENT_DIRECTION_2026-09-06.md).

### Semantic-pragmatic empathy battery (SPEB V0; source-only research)

[Documentation and limitations](docs/SPEB_V0.md) · [typed evaluator](empathy_research/speb.py) · [adversarial tests](tests/test_speb.py)

SPEB tests synthetic contrasts in conversational semantics, pragmatic intent, correction, withdrawal, and response selection. The public development battery does not invoke a model, authenticate a person, detect feelings or consciousness, establish independent heldout validity, or grant graduation authority. Scores are always non-qualifying. The research fixtures must never contain private person-specific transcripts.

### Research policy prototype (source only; not deployed)

`empathy_research.policy.choose_policy` is a pure, deterministic **research** selector over explicitly typed `Assessment`, `Evidence`, and `Hypothesis` objects. It returns a response-policy suggestion with a reason code, supporting evidence IDs, opaque same-person superseded-hypothesis IDs, and `authority=NONE` / `persistence=EPHEMERAL`. Weak evidence (below the V0 experimental 0.5 cutoff) cannot force a policy route.

Decision provenance only includes IDs matching `ev_` plus 32 lowercase hexadecimal characters for observations, or `hyp_` plus 32 lowercase hexadecimal characters for hypotheses. Malformed IDs are silently omitted from the decision to prevent accidental raw-text echoes. Hosts must generate unpredictable opaque IDs and keep the private ID-to-evidence mapping outside this module; matching the format alone proves neither authenticity nor privacy. The `HIGH_SCORE` decision band reflects only a caller-supplied numeric threshold (0.8), **not** verified first-person testimony, calibrated psychological probability, or actual feeling.

It does **not** read private memory, authenticate identities, interpret arbitrary text, invoke a model, execute an action, or persist decisions. The future host would have to authenticate the person scope, admit/time-bound evidence, govern privacy, and supply a reviewed pre-response integration point; none is established here. Merely setting an evidence item's `source="current"` is **not** proof of freshness or identity. Unscoped hypotheses are ineligible; never substitute historical evidence for current consent.

The experimental selector now treats a directly scoped correction to stop play as `STOP_PLAY`; conflicting current play reports cannot justify `PRESERVE_PLAY`; and high-stakes routes always signal focused review. High-stakes task requests with nonzero, current, same-person uncertainty about whether a task was actually requested return `CLARIFY_MEANING` pending review. These are conservative routing choices, not calibrated psychological measurements.

Run the synthetic research and startup-safety checks with:

```sh
python -m unittest discover -s tests -v
```

A passing suite qualifies only the exact tested source as a bounded policy research candidate, **not** Vera Mono integration, installed empathy, or improved relational outcomes.

## Editor startup safety

The active source tree removes a concealed VS Code `folderOpen` Node task and a disguised `public/fonts/fa-solid.lkf` executable. Automatic workspace tasks are disabled, and source-level CI rejects reintroduction. The prior code remains recoverable in Git history. This containment does **not** establish whether it previously executed on a host or that local clones, editor extensions, scheduled tasks, processes, or credentials are clean. Do not run unreviewed historical payloads.
