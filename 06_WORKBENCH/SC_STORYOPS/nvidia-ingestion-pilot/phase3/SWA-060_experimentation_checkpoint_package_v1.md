# SWA-060 Experimentation Checkpoint Package v1

## Scope
- Consolidate full-corpus Phase 3 execution evidence for `SWA-049` through `SWA-051`.
- Provide gating context for Phase 4 decision work.

## Outcomes
- `SWA-049` (`baai/bge-m3`): `0/100` success; failure mode: `Something went wrong with the request.`.
- `SWA-050` (`nvidia/nv-embed-v1`): `100/100` success; `p95 latency=2633.19 ms`.
- `SWA-051` (VL caption-embed): `68/69` success; unresolved rows: `1`.

## Known Limitations
- Retrieval index and query-score tasks (`SWA-052..SWA-059`) are not yet executed.
- Query template remains unpopulated for `query_text` and `expected_node_ids`.
- Phase 4 uses execution-readiness evidence and documented waivers instead of contractual retrieval metrics.

## Evidence Artifacts
- `phase3/SWA-049_bge_m3_smoke_results_full_text_v1.json`
- `phase3/SWA-050_nv_embed_v1_smoke_results_full_text_v1.json`
- `phase3/SWA-051_vl_full_results_assembled_v2.json`
- `phase3/SWA-051_unresolved_rows_v2.csv`
- `phase3/SWA-049_051_full_execution_summary_v2.md`
