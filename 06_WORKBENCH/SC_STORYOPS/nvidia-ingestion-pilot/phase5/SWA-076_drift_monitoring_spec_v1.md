# SWA-076 Drift Monitoring Spec v1

Date: 2026-05-18
Task ID: SWA-076
Issue: #115
Status: complete

## Objective
Define operational monitoring metrics for retrieval-quality drift detection in non-editorial graph operations.

## Mission Continuity Lock
- This monitoring spec enforces the same pilot mission: extracted-data embeddings plus provenance-bound relation graph retrieval.
- Canon and editorial surfaces remain out-of-scope for mutation.

## Metrics Registry

### M1 - Recall@10 Drift
- Metric: `recall_at_10` on model-B lane
- Baseline: `0.9333` (from `SWA-058`)
- Warning threshold: `< 0.92` (2σ degradation)
- Critical threshold: `< 0.90` (rollback trigger per `SWA-070`)
- Measurement: weekly batch evaluation against `SWA-055` query set
- Owner: DevOps Eng

### M2 - Hierarchy Coherence Drift
- Metric: `mean_hierarchy_score_0_5` on model-B lane
- Baseline: `2.7575` (from `SWA-059`)
- Warning threshold: `< 2.60` (seasonal drift indicator)
- Critical threshold: `< 2.50` (rollback trigger per `SWA-070`)
- Measurement: weekly batch evaluation against `SWA-059` seed neighborhoods
- Owner: DevOps Eng

### M3 - Unresolved VL Rate
- Metric: unresolved vision-language row rate
- Baseline: `1/69 ≈ 0.014493` (from `SWA-054`)
- Warning threshold: `> 0.03` (per `SWA-075` C5)
- Critical threshold: `> 0.05` (rollback trigger)
- Measurement: daily count from active VL embedding run
- Owner: DevOps Eng

### M4 - Provenance Integrity
- Metric: ratio of nodes with valid `provenance_ref` fields
- Baseline: `1.0` (100% from `SWA-053` and `SWA-054`)
- Warning threshold: `< 0.99` (data integrity concern)
- Critical threshold: `< 0.95` (rollback trigger)
- Measurement: daily provenance completeness scan
- Owner: QA Eng

### M5 - Embedding Dimension Consistency
- Metric: `vector_dim` for model-B and multimodal lanes
- Baseline: model-B `= 4096`, multimodal `= 2048`
- Warning threshold: any deviation from baseline
- Critical threshold: N/A (immediate investigation required)
- Measurement: per-run dimension check in CI pipeline
- Owner: DevOps Eng

## Alert Severity Levels

| Level | Trigger | Response Window | Escalation |
|---|---|---|---|
| INFO | Metric within 1σ of baseline | Next reporting cycle | None |
| WARN | Metric crosses warning threshold | 24 hours | DevOps Eng reviews |
| CRITICAL | Metric crosses critical threshold | 4 hours | StoryOps Planner + DevOps Eng |
| ROLLBACK | SWA-070 rollback criterion met | Immediate | Full incident playbook activation |

## Rolling-Window Thresholds
- Short window (7 days): detect acute regressions; `1σ` degradation triggers INFO.
- Medium window (30 days): detect seasonal drift; `2σ` degradation triggers WARN.
- Long window (90 days): detect model staleness; trend reversal triggers review.

## Reporting Cadence
- Daily: automated provenance scan (M4) and VL rate check (M3).
- Weekly: full recall and hierarchy evaluation (M1, M2) with CI check runner (`SWA-075`).
- Monthly: trend report comparing current metrics to baseline with seasonality annotation.

## Output Paths
- `phase5/SWA-076_metrics_report_YYYY-MM-DD.md`
- `phase5/SWA-076_metrics_report_YYYY-MM-DD.json`
- `phase5/SWA-076_drift_alert_log_YYYY-MM-DD.json`

## Alignment with SWA-070 Rollback Criteria
- M1 critical threshold (`< 0.90`) triggers `SWA-070` rollback action R-01.
- M2 critical threshold (`< 2.50`) triggers `SWA-070` rollback action R-02.
- M3 critical threshold (`> 0.05`) triggers `SWA-070` rollback action R-03.
- M4 critical threshold (`< 0.95`) triggers `SWA-070` rollback action R-04.

## Definition of Done
- [x] Drift-monitoring spec includes thresholds, owners, and alert logic.
- [x] Metrics map to baseline artifacts and contractual rubric fields.
- [x] Alert severity levels defined with response windows and escalation paths.
- [x] Reporting cadence and output paths specified.
- [x] Rollback trigger alignment with `SWA-070` documented.