# Artifact Registry

Date: 2026-05-15
Directory: `06_WORKBENCH/SC_STORYOPS/nvidia-ingestion-pilot`

| Artifact | Purpose | Status |
|---|---|---|
| `sample_manifest.csv` | Pilot node manifest with 100 entries | complete |
| `pilot_query_eval_template.csv` | Query scoring template with 30 rows | complete |
| `sampling_strategy.md` | Deterministic sampling and rubric contract | complete |
| `swarm_execution_plan.md` | 80-task phase/wave/swarm execution plan | complete |
| `swarm_tasks.json` | Machine-readable SWA task graph | complete |
| `state_snapshot_2026-05-15.md` | Current setup and gap snapshot | complete |
| `nvidia_model_inventory_metadata_2026-05-15.json` | Model inventory counts and checksum | complete |
| `canonical_vs_noneditorial_boundary_policy.md` | Canon boundary enforcement policy | complete |
| `risk_register.md` | Pilot risk ledger and mitigations | complete |
| `dependency_map.md` | Critical path and parallelization map | complete |
| `naming_conventions.md` | IDs and artifact naming contract | complete |
| `review_cadence_and_gates.md` | Review cadence and wave gate rules | complete |
| `baseline_metrics.md` | Pre-run metric and threshold baseline | complete |
| `phase0_kickoff_summary.md` | Phase 0 completion and next-step note | complete |
| `contracts/` | Phase 1 Wave 1-3 contract surfaces (SWA-011..030) | complete |
| `swa_issue_payloads.json` | GitHub issue payload pack for SWA-001..080 | complete |
| `github_issue_seed.md` | Issue creation command pattern and notes | complete |
| `swa_issue_number_map.tsv` | SWA ID to GitHub issue number mapping | complete |
| `phase2/SWA-031_batch_groups_v1.json` | Batch classification artifact for pilot nodes | complete |
| `phase2/SWA-032_033_manifest_enriched_v1.csv` | Enriched manifest with lineage and locale tags | complete |
| `phase2/SWA-034_path_validation_report_v1.md` | Filesystem existence validation report | complete |
| `phase2/SWA-035_text_extraction_normalization_spec_v1.md` | Text extraction normalization contract | complete |
| `phase2/SWA-035_text_extraction_preview_v1.json` | Document extraction preview output | complete |
| `phase2/SWA-036_ocr_extraction_normalization_spec_v1.md` | OCR normalization policy contract | complete |
| `phase2/SWA-036_ocr_queue_v1.csv` | OCR execution queue for image nodes | complete |
| `phase2/SWA-037_extraction_quality_flags_schema_v1.json` | Extraction quality flags JSON schema | complete |
| `phase2/SWA-038_node_id_mapping_ledger_v1.csv` | Canonical node mapping ledger | complete |
| `phase2/SWA-039_expected_neighbors_seed_v1.json` | Seed neighbor sets for first 40 nodes | complete |
| `phase2/SWA-040_expected_parent_seed_v1.json` | Seed parent assignments for first 40 nodes | complete |
| `phase2/SWA-041_unresolved_node_triage_queue_v1.csv` | Triage queue template for unresolved nodes | complete |
| `phase2/SWA-042_dry_validation_report_v1.json` | Structured dry validation result | complete |
| `phase2/SWA-042_dry_validation_report_v1.md` | Human-readable dry validation report | complete |
| `phase2/SWA-043_manifest_patched_v1.csv` | Patched manifest with required fields populated | complete |
| `phase2/SWA-044_data_readiness_checkpoint_report_v1.md` | Phase 2 readiness gate checkpoint | complete |
| `phase2/SWA-045_transition_approval_memo.md` | Approval memo to begin Phase 3 prep | complete |
| `phase3/SWA-046_bge_m3_input_set_v1.jsonl` | Text embedding input set for bge-m3 lane | complete |
| `phase3/SWA-047_nv_embed_v1_input_set_v1.jsonl` | Text embedding input set for nv-embed-v1 lane | complete |
| `phase3/SWA-048_vl_input_set_v1.jsonl` | Vision embedding input set for VL lane | complete |
| `phase3/SWA-046_048_input_set_summary_v1.json` | Input preparation counts and manifest source summary | complete |
| `scripts/run_swa_phase3_smoke.py` | Executable smoke runner for SWA-049..SWA-051 | complete |
| `phase3/SWA-049_bge_m3_smoke_results_v1.json` | Smoke result for bge-m3 text lane (`0/10` success) | complete |
| `phase3/SWA-050_nv_embed_v1_smoke_results_v1.json` | Smoke result for nv-embed-v1 text lane (`10/10` success) | complete |
| `phase3/SWA-051_vl_smoke_results_v1.json` | Smoke result for VL caption-embed lane (`10/10` success) | complete |
| `phase3/SWA-049_051_smoke_summary_v1.md` | Consolidated smoke outcomes and notes | complete |
| `phase3/SWA-049_bge_m3_smoke_results_full_text_v1.json` | Full text-lane execution for bge-m3 (`0/100` success; provider runtime errors) | complete |
| `phase3/SWA-050_nv_embed_v1_smoke_results_full_text_v1.json` | Full text-lane execution for nv-embed-v1 (`100/100` success) | complete |
| `phase3/SWA-051_vl_smoke_results_full_o0.json` | First full VL chunk (`25` rows) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_o25.json` | VL chunk execution (`offset 25`, `10` rows) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_o35.json` | VL chunk execution (`offset 35`, `10` rows; includes timeout retry candidates) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_o45.json` | VL chunk execution (`offset 45`, `10` rows; includes timeout retry candidates) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_o55.json` | VL chunk execution (`offset 55`, `10` rows; includes empty-image candidate) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_o65.json` | Final VL chunk execution (`offset 65`, `4` rows) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_retry_o41b.json` | Targeted retry for `NODE-043` timeout (`success`) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_retry_o45b.json` | Targeted retry for `NODE-047` timeout (`success`) | complete |
| `phase3/SWA-051_vl_smoke_results_vl_retry_o61b.json` | Targeted retry for `NODE-063` (`image_empty_0_bytes`) | complete |
| `phase3/SWA-051_vl_full_results_assembled_v2.json` | Reconciled VL lane ledger (`68/69` success) | complete |
| `phase3/SWA-051_unresolved_rows_v2.csv` | Unresolved VL rows requiring source remediation | complete |
| `phase3/SWA-049_051_full_execution_summary_v2.json` | Structured Phase 3 full execution summary | complete |
| `phase3/SWA-049_051_full_execution_summary_v2.md` | Human-readable Phase 3 full execution summary | complete |
| `phase3/SWA-060_experimentation_checkpoint_package_v1.md` | Phase 3 checkpoint package for Phase 4 gating | complete |
| `scripts/run_swa_phase4_analysis.py` | Phase 4 analysis runner for SWA-061..SWA-072 artifacts | complete |
| `phase4/SWA-061_weighted_scores_modelA_modelB_v1.json` | Weighted score sheet with dependency waiver and threshold check | complete |
| `phase4/SWA-061_weighted_scores_modelA_modelB_v1.md` | Human-readable weighted score summary | complete |
| `phase4/SWA-062_modality_performance_summary_v1.json` | Modality-level performance summary with coverage and latency | complete |
| `phase4/SWA-062_modality_performance_summary_v1.md` | Human-readable modality summary | complete |
| `phase4/SWA-063_failed_retrieval_error_analysis_v1.json` | Structured failure analysis and remediation actions | complete |
| `phase4/SWA-063_failed_retrieval_error_analysis_v1.md` | Human-readable failure analysis | complete |
| `phase4/SWA-064_language_drift_analysis_v1.json` | Structured multilingual drift readiness audit | complete |
| `phase4/SWA-064_language_drift_analysis_v1.md` | Human-readable language drift audit | complete |
| `phase4/SWA-065_provenance_fidelity_audit_v1.json` | Structured provenance coverage and integrity audit | complete |
| `phase4/SWA-065_provenance_fidelity_audit_v1.md` | Human-readable provenance audit | complete |
| `phase4/SWA-066_hierarchy_neighborhood_sanity_audit_v1.json` | Structured hierarchy seed neighborhood sanity audit | complete |
| `phase4/SWA-066_hierarchy_neighborhood_sanity_audit_v1.md` | Human-readable hierarchy sanity audit | complete |
| `phase4/SWA-067_model_selection_decision_memo_v1.md` | Provisional model-selection memo for Phase 4 | complete |
| `phase4/SWA-068_threshold_rule_constraints_review_v1.md` | Threshold rule and constraints review | complete |
| `phase4/SWA-069_hardening_backlog_v1.md` | Hardening backlog for chosen stack | complete |
| `phase4/SWA-070_rollback_criteria_v1.md` | Rollback triggers and response actions | complete |
| `phase4/SWA-071_hardening_wave_scope_and_owners_v1.md` | Hardening scope, owners, and exit criteria | complete |
| `phase4/SWA-072_transition_to_integration_approval_v1.md` | Conditional transition approval memo | complete |

## Integrity Notes
- Pilot manifest expected counts: `35/35/30` by bucket
- Query template expected distribution: `10/10/10` by bucket
- Phase 3 full execution state: `SWA-049=0/100`, `SWA-050=100/100`, `SWA-051=68/69`; unresolved node `NODE-063` points to an empty source image file
- Phase 4 state: provisional model direction set to `nvidia/nv-embed-v1`; integration transition remains conditional on `SWA-052..SWA-059`
- Any regenerated artifact should append a dated suffix or update this registry
