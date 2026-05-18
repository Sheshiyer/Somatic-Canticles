# SWA-079 Operational Roadmap v1

Date: 2026-05-18
Task ID: SWA-079
Issue: #118
Status: complete

## Objective
Publish v1 operational roadmap with milestone dates and owner sequencing for non-editorial graph pilot operationalization.

## Mission Continuity Lock
- This roadmap operationalizes the validated pilot mission: extracted-data embeddings plus provenance-bound relation graph retrieval.
- No editorial mutation; all milestones preserve canon boundary.

## Milestone Schedule

### MS-1: CI Pipeline Operational (SWA-075)
- Target: Week 1 post-approval
- Owner: DevOps Eng
- Dependencies: SWA-074 complete
- Exit Criteria: CI check runner executes C1-C5 against fixtures; first report generated with `overall_status=pass`
- Current State: Complete. CI runner and first report exist; `overall_status=pass`.
- Gate: DevOps Eng signoff on C1-C5

### MS-2: Drift Monitoring Deployed (SWA-076)
- Target: Week 1 post-approval (parallel with MS-1)
- Owner: DevOps Eng
- Dependencies: SWA-074 complete
- Exit Criteria: M1-M5 metrics defined; daily/weekly reporting cadence documented; alert levels assigned owners
- Current State: Complete. Drift monitoring spec and metrics matrix published.
- Gate: DevOps Eng signoff on monitoring readiness

### MS-3: Incident Playbook Published (SWA-077)
- Target: Week 2 post-approval
- Owner: QA Eng
- Dependencies: MS-1, MS-2
- Exit Criteria: SEV-1/2/3 matrix published; FC-1 through FC-4 triage flows documented; evidence template available; communication flow defined
- Current State: Complete. Incident playbook and severity matrix published.
- Gate: QA Eng signoff on playbook completeness

### MS-4: Release Checklist Verified (SWA-078)
- Target: Week 2 post-approval
- Owner: QA Eng + StoryOps Planner
- Dependencies: MS-1, MS-2, MS-3
- Exit Criteria: All six release gates pass with signoff from assigned roles
- Current State: Complete. Release checklist and gate JSON published.
- Gate: All six gate signoffs recorded

### MS-5: Operational Roadmap Published (SWA-079)
- Target: Week 3 post-approval
- Owner: StoryOps Planner
- Dependencies: MS-4
- Exit Criteria: Milestone roadmap published with dates, owners, and dependency-aware sequencing
- Current State: Complete. This document.
- Gate: StoryOps Planner signoff

### MS-6: Closeout and Lessons (SWA-080)
- Target: Week 3 post-approval
- Owner: StoryOps Planner
- Dependencies: MS-5
- Exit Criteria: Closeout package complete; lessons compiled; next-action board published
- Current State: In progress.
- Gate: StoryOps Planner signoff

## Progress Reporting Cadence
- Daily: automated CI check run (`SWA-075`) and drift metrics snapshot (`SWA-076`).
- Weekly: milestone review with status update against roadmap; drift trend analysis.
- Phase-end: closeout review per `SWA-080`.

## Checkpoint Format
- Each milestone produces a checkpoint summary in `phase5/SWA-0NN_checkpoint_summary_v1.md`.
- Checkpoints include: status, evidence, gate results, and next-step notes.

## Risk Buffer Policy
- Each milestone has a 2-day buffer before its gate deadline.
- If a milestone misses its gate by more than 2 days, escalation to StoryOps Planner for replanning.
- Parallel milestones (MS-1 and MS-2) share a combined buffer; slippage in one does not delay the other.

## Escalation Route
- Milestone owner -> StoryOps Planner -> replanning if gate missed by >2 days.
- Severity escalation per `SWA-077` for any operational incident during milestone execution.

## Definition of Done
- [x] Roadmap includes dates, owners, and dependency-aware sequencing.
- [x] Six milestones defined with exit criteria and gate requirements.
- [x] Progress reporting cadence specified.
- [x] Risk buffer policy and escalation route documented.