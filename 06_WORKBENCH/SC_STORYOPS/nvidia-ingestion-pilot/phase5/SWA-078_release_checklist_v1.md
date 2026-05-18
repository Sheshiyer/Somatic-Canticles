# SWA-078 Release Checklist v1

Date: 2026-05-18
Task ID: SWA-078
Issue: #117
Status: complete

## Objective
Define release checklist for non-editorial network launch with all dependency gates and signoff roles.

## Mission Continuity Lock
- This release checklist enforces the pilot mission boundary: no editorial mutation, provenance-bound operations only.
- Release approval requires verification that no canon or editorial doctrine surfaces have been modified.

## Pre-Release Gate Requirements

### Gate 1: CI Regression Checks Pass (from SWA-075)
- [ ] C1 - Fixture Integrity: all fixture paths exist; checksums match expected values.
- [ ] C2 - Embedding Lane Health: model-B `row_count=100`, `success_count=100`, `vector_dim=4096`; multimodal `row_count=69`, `success_count>=68`, `vector_dim=2048`.
- [ ] C3 - Retrieval Quality Regression: `recall_at_10 >= 0.90`; `mean_match_count >= 1.20`; `mean_hierarchy_score_0_5 >= 2.50`.
- [ ] C4 - Provenance Completeness: every index row has non-empty `provenance_ref`; no null anchors in query results.
- [ ] C5 - Rollback Trigger Probe: unresolved VL rate `<= 0.03`.

### Gate 2: Drift Monitoring Active (from SWA-076)
- [ ] M1-M5 metrics defined with baselines, warning thresholds, and critical thresholds.
- [ ] Daily provenance scan and VL rate check are operational.
- [ ] Weekly recall and hierarchy evaluation cadence is scheduled.
- [ ] Alert severity levels (INFO, WARN, CRITICAL, ROLLBACK) are documented and assigned owners.
- [ ] Drift alert log output path is configured.

### Gate 3: Incident Playbook Ready (from SWA-077)
- [ ] SEV-1/2/3 severity matrix is published and accessible.
- [ ] FC-1 through FC-4 triage flows are documented.
- [ ] Evidence capture template is available in `phase5/incidents/`.
- [ ] Communication flow is defined by severity level.
- [ ] Closure review checklist is defined and accessible.

### Gate 4: Boundary Policy Verification
- [ ] No modification to `02_MANUSCRIPTS/COMPILED` or editorial doctrine surfaces.
- [ ] Boundary policy from `SWA-013` enforced: all node/edge artifacts carry provenance references.
- [ ] Anti-drift controls verified: no ontology claims without evidence links.

### Gate 5: Rollback Trigger Validation (from SWA-070)
- [ ] Rollback criteria are documented and mapped to SWA-076 critical thresholds.
- [ ] Rollback actions R-01 through R-04 are tested against fixtures.
- [ ] Last known-good index snapshot is checksummed and stored.

### Gate 6: Provenance Completeness Check
- [ ] 100% of nodes have valid `provenance_ref` fields.
- [ ] 100% of edges trace to source evidence links.
- [ ] Provenance completeness scan produces clean report.

## Final Signoff Matrix

| Gate | Signoff Role | Required |
|---|---|---|
| Gate 1 (CI) | DevOps Eng | Yes |
| Gate 2 (Drift) | DevOps Eng | Yes |
| Gate 3 (Incident) | QA Eng | Yes |
| Gate 4 (Boundary) | StoryOps Planner | Yes |
| Gate 5 (Rollback) | DevOps Eng | Yes |
| Gate 6 (Provenance) | QA Eng | Yes |

- Release requires all six gates to pass with signoff from the assigned role.
- Any gate failure blocks release; incident playbook activation is required per `SWA-077`.

## Post-Release Verification
- Run full CI check suite within 24 hours of release.
- Verify drift metrics remain within INFO thresholds for the first 7 days.
- Confirm incident playbook is reachable and evidence capture templates are populated.

## Definition of Done
- [x] Release checklist includes all dependency gates and signoff roles.
- [x] Checklist can be executed without external assumptions.
- [x] Boundary policy verification is a required gate.
- [x] Post-release verification steps are defined.