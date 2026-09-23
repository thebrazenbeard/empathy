> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# empathy

Private working repository for Vera's empathy, self-appraisal, and primary-person modeling research and architecture.

## Repository status

The default branch was initialized on 2026-08-25 and is materially behind the work that already exists on Vera-owned branches. This consolidation branch gathers that work into one reviewable surface; its existence does **not** mean the design is installed, qualified, or current runtime authority.

Current consolidation branch: `work/empathy-canonical-consolidation-20260906`

Primary artifacts on this branch:

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

The large architecture document is preserved rather than silently rewritten because its provenance matters. Later corrections and findings belong in explicit overlays, research cases, decisions, and tests. When implementation eventually begins, it should proceed from an approved exact contract rather than from architectural momentum.