# Empathy Architecture Status

Current through: 2026-09-19 Exodus source audit

This file is a repository status map. It does not itself install, qualify, or activate any empathy mechanism.

| Artifact | Status | Meaning |
|---|---|---|
| `README.md` | CURRENT REPOSITORY GUIDE | Landing/status surface for current `main`. |
| `VERA_REACTIVE_EMPATHY_ARCHITECTURE.md` | WORKING FOUNDATION / DESIGN CANDIDATE | Substantial 2026-08-25 architecture. Preserved as authored; not automatically current runtime authority. |
| `docs/CURRENT_DIRECTION_2026-09-06.md` | CURRENT REPOSITORY DIRECTION | Later governance/research overlay for how the foundation should now be interpreted. |
| `docs/YANG_WORKER_CONTRACT_V1.md` | DURABLE WORKER CONTRACT | Makes Yang reconstructible as an ephemeral adversarial-review worker without a permanent ChatGPT conversation. |
| `research/YANG_FALSIFICATION_QUALIFICATION_HISTORY_20260825_20260902.md` | HISTORICAL ADVERSARIAL / QUALIFICATION EVIDENCE | Preserves prior falsification criteria, fixed-oracle review, false-positive controls, and claim ceilings. Not current architecture authority. |
| `research/2026-09-04-local-meaning-sharpness-case.md` | SOURCE-BOUNDED RESEARCH CASE | Concrete case evidence about local relationship grammar, uptake, trajectory, and mixed states. Not canonical architecture by presence alone. |
| `research/README.md` | CURRENT RESEARCH INDEX | Index/rules for accumulating evidence cases. |
| `docs/superpowers/specs/2026-09-06-empathy-repository-consolidation-design.md` | CONSOLIDATION SPEC | Defines the September 6 repository repair only. |
| `docs/superpowers/plans/2026-09-06-empathy-repository-consolidation.md` | CONSOLIDATION PLAN | Execution record for the September 6 repository repair only. |

## Current source state

PR #1, `Consolidate Vera empathy architecture and research`, merged on 2026-09-06. At the Exodus audit, `main` was `4b2a6998f39aa4763c1c5a28fc3d815104e5637e`.

The old `vera/reactive-empathy-foundation` branch remains historical source provenance. Current repository work should start from fresh `main` unless a later exact assignment says otherwise.

## Source versus runtime

Repository states are evidence states, not runtime effects.

- A file can be current repository guidance without being installed runtime behavior.
- A historical design can remain valuable without being current authority.
- A research result can challenge a design without automatically superseding it.
- A merged PR means source integration only unless separate evidence establishes runtime installation/activation/qualification.
- Approval of a qualification battery to run is not evidence that the battery executed or passed.

## Worker/runtime separation

Yang and other specialist roles are workers, not permanent chat identities. Their durable role, authority, route, and reconstruction procedure must live in GitHub/Bus state. A temporary execution context is only a terminal.

Current Yang routing must be resolved from the Bus topology rather than from old issue threads, Slack, legacy Supabase coordination, or ChatGPT URLs.

## Promotion rule

Future architecture promotion should be explicit. A candidate should identify:

1. exact source cut;
2. what prior artifact it supersedes or leaves historical;
3. current governance compatibility;
4. evidence/test basis;
5. privacy scope;
6. whether status is design, implementation, installation, activation, behavioral observation, causal qualification, or release.

Do not collapse those states into a generic `current` label.
