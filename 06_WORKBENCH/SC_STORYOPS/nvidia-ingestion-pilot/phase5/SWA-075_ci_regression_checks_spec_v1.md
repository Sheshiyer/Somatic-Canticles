# SWA-075 CI Regression Checks Spec v1

Date: 2026-05-16
Task ID: SWA-075
Issue: #114
Status: in_progress (execution artifact started)

## Objective
Define CI checks that detect embedding and retrieval regressions before any non-editorial graph promotion.

## Mission Continuity Lock
- This CI spec enforces the same pilot mission: extracted-data embeddings plus provenance-bound relation graph retrieval.
- Canon and editorial surfaces remain out-of-scope for mutation.

## Baseline Inputs (Fixtures)
- `phase3/SWA-053_modelB_retrieval_index_v1.json`
- `phase3/SWA-053_modelB_vectors_v1.npy`
- `phase3/SWA-054_multimodal_index_v1.json`
- `phase3/SWA-054_multimodal_vectors_v1.npy`
- `phase3/SWA-058_recall_match_metrics_v1.json`
- `phase3/SWA-059_hierarchy_coherence_metrics_v1.json`
- `phase3/SWA-052_059_artifact_checksums_v1.json`

## CI Check Set (v1)

### C1 - Fixture Integrity (hard fail)
- Verify required fixture paths exist.
- Verify fixture checksums match expected values where available.
- Fail if any fixture is missing or mismatched.

### C2 - Embedding Lane Health (hard fail)
- Verify model-B index lane still reports:
  - `row_count = 100`
  - `success_count = 100`
  - `fail_count = 0`
  - `vector_dim = 4096`
- Verify multimodal lane remains bounded and explicit:
  - `row_count = 69`
  - `success_count >= 68`
  - `fail_count <= 1`
  - `vector_dim = 2048`

### C3 - Retrieval Quality Regression (hard fail)
- From `SWA-058` model-B lane:
  - `recall_at_10 >= 0.90`
  - `mean_match_count >= 1.20`
- From `SWA-059` model-B lane:
  - `mean_hierarchy_score_0_5 >= 2.50`
  - `bio_field_charts >= 3.50`
  - `interpretation_maps >= 2.40`
  - `cross_integration_histories >= 1.70`

### C4 - Provenance Completeness (hard fail)
- Verify every index row contains non-empty `provenance_ref`.
- Verify query results and metrics artifacts map back to query/node IDs without null anchors.

### C5 - Rollback Trigger Probe (warning -> incident handoff)
- Calculate unresolved VL rate from `SWA-054` index and compare with rollback criterion (`> 3%` is trigger).
- Emit warning and handoff ticket marker if threshold is exceeded.

## Reporting Contract
- Emit CI summary markdown plus JSON:
  - `phase5/SWA-075_ci_check_report_latest.md`
  - `phase5/SWA-075_ci_check_report_latest.json`
- Include:
  - check ID
  - pass/fail/warn
  - observed value(s)
  - threshold(s)
  - artifact source path(s)

## Artifact Retention Policy
- Keep latest report plus last five report snapshots.
- Persist failed-run reports and raw check logs for incident forensics.

## Handoff to SWA-077
- Any C1-C4 failure triggers incident playbook activation candidate.
- Any C5 warning becomes mandatory context in incident severity triage.

## Next Execution Steps
1. Implement a small validator runner (`scripts/run_swa_phase5_ci_checks.py`).
2. Execute checks against current fixtures and publish first CI report pair.
3. Post evidence update to issue `#114` with pass/fail outputs.
