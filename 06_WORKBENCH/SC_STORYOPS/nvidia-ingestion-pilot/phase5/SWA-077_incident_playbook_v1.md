# SWA-077 Incident Playbook v1

Date: 2026-05-18
Task ID: SWA-077
Issue: #116
Status: complete

## Objective
Define incident playbook for ingestion, embedding, and retrieval failures in the non-editorial graph pilot.

## Mission Continuity Lock
- This incident playbook preserves the pilot mission boundary: no editorial mutation, provenance-bound operations only.
- Incident response actions may not modify canon or editorial doctrine surfaces.

## Incident Severity Matrix

### SEV-1: Service-Stopping
- Definition: retrieval pipeline completely down or producing garbage results for all queries.
- Examples: embedding API total outage; vector index corruption; provenance chain fully broken.
- Response time: 30 minutes acknowledgment; 4 hours containment or rollback.
- Escalation: StoryOps Planner + DevOps Eng immediate war room.
- Rollback: automatic per `SWA-070` criteria.

### SEV-2: Degraded
- Definition: retrieval pipeline functional but quality below contractual thresholds.
- Examples: recall@10 below 0.90 but above 0.80; hierarchy coherence below 2.50 but above 2.00; VL rate 3-5%.
- Response time: 4 hours acknowledgment; 24 hours containment or rollback.
- Escalation: DevOps Eng leads; StoryOps Planner informed.
- Rollback: conditional per `SWA-075` C3 thresholds.

### SEV-3: Watch
- Definition: metrics deviating from baseline but within safe operating range.
- Examples: recall@10 trending down but above 0.92; hierarchy trending down but above 2.60; VL rate 1-3%.
- Response time: next reporting cycle acknowledgment; 72 hours assessment.
- Escalation: DevOps Eng monitors; no planner escalation needed.
- Rollback: not triggered.

## Triage Flow by Failure Class

### FC-1: Provider Failure (NVIDIA API)
1. Diagnose: check API status, request IDs, error codes (500, 503, timeout).
2. Contain: switch to fallback embedding model if available; otherwise pause ingestion.
3. Evidence: capture request IDs, timestamps, error bodies.
4. Recover: re-run failed batch after provider recovery.
5. Close: verify metrics return to baseline; log provider incident ID.

### FC-2: Data Quality Failure (content)
1. Diagnose: check extraction quality flags (`SWA-035`, `SWA-037`).
2. Contain: quarantine affected nodes; prevent promotion to graph.
3. Evidence: capture node IDs, quality flags, original source paths.
4. Recover: re-extract from source or mark node as permanently unresolved.
5. Close: verify quarantined nodes are excluded; update unresolved rate.

### FC-3: Provenance Failure (missing or invalid refs)
1. Diagnose: run provenance completeness scan (`SWA-075` C4).
2. Contain: prevent affected nodes from entering graph edges.
3. Evidence: capture node IDs with missing or null `provenance_ref` fields.
4. Recover: backfill provenance from source manifest or mark as unsourced.
5. Close: re-run C4 check; verify 100% provenance coverage.

### FC-4: Schema Failure (format or dimension mismatch)
1. Diagnose: check vector dimensions, index format, and checksum matches.
2. Contain: prevent malformed vectors from entering retrieval index.
3. Evidence: capture dimension mismatches, format errors, checksum failures.
4. Recover: regenerate vectors from correct embedding model; re-index.
5. Close: re-run C1 and C2 checks; verify index integrity.

## Rollback and Containment Actions by Severity

| Severity | Containment | Rollback | Data Recovery |
|---|---|---|---|
| SEV-1 | Immediately halt ingestion + retrieval | Revert to last known-good index snapshot | Restore from checksummed artifacts |
| SEV-2 | Pause ingestion; throttle retrieval | Conditional rollback if metrics don't recover in 24h | Re-run affected batch from source |
| SEV-3 | Log and monitor; no action needed | No rollback | N/A |

## Evidence Capture Template
```
incident_id: INC-YYYY-MM-DD-NNN
severity: [SEV-1 | SEV-2 | SEV-3]
failure_class: [FC-1 | FC-2 | FC-3 | FC-4]
detection_time: YYYY-MM-DDTHH:MM:SSZ
affected_artifacts: [paths]
affected_nodes: [node IDs]
request_ids: [NVIDIA request IDs if applicable]
checksums_before: [SHA-256 values]
checksums_after: [SHA-256 values if changed]
drift_metrics_snapshot: [M1-M5 values at detection time]
containment_action: [description]
recovery_action: [description]
closure_time: YYYY-MM-DDTHH:MM:SSZ
closure_review: [pass/fail]
```

## Communication Flow
- SEV-1: Immediate notification to StoryOps Planner; hourly status updates until containment.
- SEV-2: Notification within 4 hours; daily status updates until resolution.
- SEV-3: Logged in drift report; discussed in weekly review.

## Closure Review Checklist
- [ ] Root cause identified and documented.
- [ ] Metrics returned to baseline or above warning thresholds.
- [ ] CI checks (`SWA-075` C1-C5) pass.
- [ ] Provenance integrity verified.
- [ ] Incident evidence captured and stored in `phase5/incidents/`.
- [ ] Post-incident review scheduled (SEV-1) or completed (SEV-2/3).

## Handoff to SWA-075
- Any C1-C4 failure in CI checks triggers this playbook automatically.
- C5 warning becomes mandatory context for severity triage.

## Definition of Done
- [x] Incident playbook is actionable and references SWA-075 controls.
- [x] Every incident class has owner, containment, and recovery steps.
- [x] Evidence capture template defined.
- [x] Communication flow specified by severity level.
- [x] Closure review checklist defined.