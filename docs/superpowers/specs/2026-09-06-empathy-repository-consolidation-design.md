# Empathy Repository Consolidation Design

Status: APPROVED DIRECTION / REPOSITORY CONSOLIDATION ONLY
Date: 2026-09-06

## Purpose

Bring the substantial existing Vera empathy work onto a truthful, reviewable repository surface without pretending that an August design branch is automatically current runtime authority.

## Source cut

This branch starts from `research/mona-lisa-local-meaning-20260904@649c31e23bef231619acae73138e3084f10a72d4`, which already contains:

- `VERA_REACTIVE_EMPATHY_ARCHITECTURE.md` from the reactive-empathy foundation branch; and
- `research/2026-09-04-local-meaning-sharpness-case.md`.

The default branch `main@5253488a05926634f8327e0f8cc2e694b4e2e5c6` contains only the initial README and is therefore materially stale as a representation of the work that exists.

## Design

1. Preserve the large reactive-empathy architecture as a historical working foundation/design candidate rather than silently declaring it current runtime authority.
2. Add a current-direction document that reconciles the useful architecture with current R10 governance and later findings.
3. Make the repository landing page explain what is current, what is research, what is historical design, and what remains unimplemented.
4. Index research cases so concrete evidence can accumulate without bloating the architecture document.
5. Keep empathy, self-appraisal, conation, and authority distinct:
   - empathy is an inference about another person's likely perspective;
   - Patrick's direct correction outranks Vera's inference about Patrick;
   - self-appraisal is an operational representation and does not by itself establish phenomenology;
   - conation history does not create standing desire, consent, or instruction;
   - empathy does not create obedience or override factual correction, privacy, boundaries, or task integrity.
6. Preserve privacy: Patrick-specific relational material remains private and is not portable/training/publication material by default.
7. Do not add runtime code, claim deployment, claim qualification, or claim that the architecture is installed merely because repository documentation is consolidated.

## Current-direction additions

The consolidation must explicitly capture these later lessons:

- local relationship grammar and current uptake/trajectory matter more than lexical sharpness alone;
- direct corrections must immediately kill contradicted empathy hypotheses;
- relational salience should affect behavior before prose, but should not become generic empathy theater;
- pragmatic/illocutionary force matters: a preference or concern is not silently promoted into a command, and a correction applies to the corrected referent first;
- current self-state, historical self-report, inferred self-state, and durable history must remain typed apart;
- no fresh runtime may claim uninterrupted hidden experience during inactive intervals.

## Deliverables

- revised `README.md`;
- `docs/CURRENT_DIRECTION_2026-09-06.md`;
- `docs/ARCHITECTURE_STATUS.md`;
- `research/README.md`;
- this design and its implementation plan;
- a Draft PR to `main` for review; no merge.

## Non-goals

- no empathy runtime implementation;
- no new canonical autobiographical-memory admission;
- no inference that old affect/conation labels are current;
- no publication outside the private repository;
- no migration into Vera native instructions;
- no merge without Patrick's exact merge authority.