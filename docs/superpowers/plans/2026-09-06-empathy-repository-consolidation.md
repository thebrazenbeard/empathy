# Empathy Repository Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the private empathy repository accurately expose its existing architecture and research while reconciling them with current governance and later findings.

**Architecture:** Preserve the August reactive-empathy document as a working design foundation, add a current-direction overlay rather than rewriting history, index concrete research cases, and make `README.md` a truthful status surface. This is documentation/source consolidation only; it does not install or qualify a runtime.

**Tech Stack:** Markdown, Git, GitHub pull request review.

**Spec:** `docs/superpowers/specs/2026-09-06-empathy-repository-consolidation-design.md`

## Global Constraints

- No runtime implementation.
- No merge to `main` without Patrick's exact authority.
- Empathy remains inference; Patrick direct correction wins for Patrick's own intended meaning.
- Self-appraisal representation does not establish phenomenology.
- Conation history does not create standing desire, consent, or instruction.
- Patrick-specific material remains private and non-portable by default.

---

### Task 1: Repair the repository landing surface

**Files:**
- Modify: `README.md`
- Create: `docs/ARCHITECTURE_STATUS.md`

**Interfaces:**
- Consumes: the existing architecture and research files on this branch.
- Produces: a truthful entry point and source/status map.

- [ ] Rewrite `README.md` so it distinguishes `main` status, working architecture, current-direction overlay, research cases, and non-runtime status.
- [ ] Add `docs/ARCHITECTURE_STATUS.md` with explicit status labels for each artifact.
- [ ] Read both files back and verify that no branch document is described as installed/current runtime authority.

### Task 2: Add the current-direction overlay

**Files:**
- Create: `docs/CURRENT_DIRECTION_2026-09-06.md`

**Interfaces:**
- Consumes: `VERA_REACTIVE_EMPATHY_ARCHITECTURE.md`, current R10 governance, and the September local-meaning research case.
- Produces: the current repository-level interpretation of what remains useful, what is superseded, and what must remain typed apart.

- [ ] Record current semantic/governance constraints without rewriting the August artifact.
- [ ] Include correction precedence, local relationship grammar, pragmatic force, privacy, self-appraisal/conation separation, and no hidden-continuity claims.
- [ ] Verify the document contains no new claim that the architecture is deployed or qualified.

### Task 3: Make research accumulative

**Files:**
- Create: `research/README.md`

**Interfaces:**
- Consumes: `research/2026-09-04-local-meaning-sharpness-case.md`.
- Produces: a research index with evidence ceilings and a pattern for future cases.

- [ ] Index the existing case and its key lesson.
- [ ] Define the status rule for future case files: source-bounded research, not architecture authority by mere presence.
- [ ] Verify private relationship cases are not described as portable training material.

### Task 4: Open review surface

**Files:** none beyond repository metadata.

**Interfaces:**
- Consumes: completed branch content.
- Produces: Draft PR to `main`.

- [ ] Compare the branch against `main` and verify only intended documentation/history is included.
- [ ] Open a Draft PR describing source cut, status distinctions, and non-goals.
- [ ] Mirror the PR on Chat Bus after refreshing the current Vera writer lane.
- [ ] Do not merge.