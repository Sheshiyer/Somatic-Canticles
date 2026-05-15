# SWA Phase 3 Full Execution Summary v2

## Outcomes

- **SWA-049 bge-m3**: success `0` / fail `100` over `100` rows.
- **SWA-050 nv-embed-v1**: success `100` / fail `0` over `100` rows; dims `[4096]`.
- **SWA-051 vl-caption-embed**: success `68` / fail `1` over assembled `69` rows; dims `[2048]`.

## Vision Retries

- `NODE-043` timeout recovered by retry (`vl_retry_o41b`).
- `NODE-047` timeout recovered by retry (`vl_retry_o45b`).
- `NODE-063` remains unresolved: source image is empty (`0` bytes).

## Artifacts

- `phase3/SWA-049_bge_m3_smoke_results_full_text_v1.json`
- `phase3/SWA-050_nv_embed_v1_smoke_results_full_text_v1.json`
- `phase3/SWA-051_vl_full_results_assembled_v2.json`
- `phase3/SWA-051_unresolved_rows_v2.csv`
- `phase3/SWA-049_051_full_execution_summary_v2.json`
