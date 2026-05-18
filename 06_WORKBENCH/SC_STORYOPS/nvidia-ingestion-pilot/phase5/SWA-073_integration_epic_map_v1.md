# SWA-073 Integration Epic Map v1

Date: 2026-05-16
Task ID: SWA-073
Phase: Phase 5

## Mission Continuity Statement
Phase 5 operationalizes the same pilot mission already validated in Phases 0-4: extracted-data embeddings plus provenance-bound relation graph retrieval for non-editorial world-building knowledge.

## Scope Lock
- Keep `02_MANUSCRIPTS/COMPILED` and editorial doctrine read-only from pilot execution.
- Preserve extraction -> embedding -> retrieval -> relation-graph flow as the core pipeline.
- Require provenance references for every node and edge promoted into operational artifacts.
- Preserve anti-drift controls and boundary checks from `SWA-013` and boundary policy.

## Non-Goals
- No direct manuscript rewrites.
- No editorial doctrine mutation.
- No ontology claims without evidence links.
- No stack-specific lock-in in planning artifacts.

## Inputs
- `phase4/SWA-072_transition_to_integration_approval_v2.md`
- `phase4/SWA-067_model_selection_decision_memo_v2.md`
- `phase4/SWA-068_threshold_rule_constraints_review_v2.md`
- `contracts/W3_SwarmA_SWA-030_wave_acceptance_gate_checklist.md`
- `risk_register.md`

## Epic Map
| Epic ID | SWA Tasks | Outcome | Owner Role | Depends On | Entry Gate | Exit Gate | Primary Artifacts |
|---|---|---|---|---|---|---|---|
| E1 | SWA-073 | Integration control packet with mission lock, ownership matrix, and gate checklist | StoryOps Planner | SWA-072 | Transition approved | Epic map package complete and reviewed | `phase5/SWA-073_*` |
| E2 | SWA-074 | Pilot work translated into implementation-ready execution packets | StoryOps Planner | SWA-073 | E1 accepted | Actionable issue templates complete | `phase5/SWA-074_*` |
| E3 | SWA-075 | CI checks for embedding and retrieval regression detection | DevOps Eng | SWA-074 | E2 accepted | CI gate definitions and pass/fail controls drafted | `phase5/SWA-075_*` |
| E4 | SWA-076 | Monitoring metrics for retrieval quality drift in production operations | DevOps Eng | SWA-074 | E2 accepted | Drift dashboards/alerts spec drafted | `phase5/SWA-076_*` |
| E5 | SWA-077, SWA-078 | Incident playbook plus release checklist for non-editorial network launch | QA Eng | SWA-075, SWA-076 | E3/E4 accepted | Incident + release playbooks signed | `phase5/SWA-077_*`, `phase5/SWA-078_*` |
| E6 | SWA-079 | Operational roadmap with milestones and owner dates | StoryOps Planner | SWA-078 | E5 accepted | Milestone roadmap published | `phase5/SWA-079_*` |
| E7 | SWA-080 | Planning closeout, lessons learned, and next action board | StoryOps Planner | SWA-079 | E6 accepted | Closeout board approved | `phase5/SWA-080_*` |

## Dependency and Parallelization Rules
- Critical path: `SWA-073 -> SWA-074 -> SWA-075 -> SWA-077 -> SWA-078 -> SWA-079 -> SWA-080`
- Parallel lane after SWA-074: `SWA-076` can run in parallel with `SWA-075`.
- Merge gate: `SWA-078` cannot pass until `SWA-075`, `SWA-076`, and `SWA-077` are complete.

## Operational Profile
- Planning posture: backend-neutral graph deployment contract.
- Recommended default implementation profile: Postgres plus pgvector plus relation tables.
- Adapter rule: deployment contracts remain portable to graph-native stores without changing node/edge/provenance requirements.

## Risk Controls at Epic Level
- `R-01`: editorial contamination -> enforce boundary checks in every epic gate.
- `R-02`: provenance weakness -> reject artifacts that omit evidence mapping.
- `R-06`: model/runtime variability -> require explicit fallback and rollback notes in CI/incident epics.

## SWA-073 Completion Criteria
- Epic map published.
- Ownership matrix published.
- Gate checklist published.
- Machine-readable graph published.
- Checkpoint summary published.
