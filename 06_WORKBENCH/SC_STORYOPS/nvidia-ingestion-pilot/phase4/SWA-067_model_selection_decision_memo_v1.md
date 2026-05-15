# SWA-067 Model Selection Decision Memo v1

## Decision
- **Select `nvidia/nv-embed-v1` as provisional text embedding baseline** for pilot continuation.

## Rationale
- Model A (`baai/bge-m3`) failed full corpus execution (`0/100`) with consistent provider runtime errors.
- Model B (`nvidia/nv-embed-v1`) completed full corpus execution (`100/100`) with stable dimensional consistency (`4096`).
- Proxy weighted score margin (`model_b - model_a`) is `3.0`, exceeding threshold `0.4`.

## Caveats
- Contractual retrieval-weight metrics are blocked until `SWA-052..SWA-059` are completed.
- Cross-language signal is not evaluable in this pilot because language distribution is monolingual (`en` only).

## Evidence
- `phase4/SWA-061_weighted_scores_modelA_modelB_v1.json`
- `phase4/SWA-062_modality_performance_summary_v1.json`
- `phase4/SWA-063_failed_retrieval_error_analysis_v1.json`
- `phase4/SWA-065_provenance_fidelity_audit_v1.json`
- `phase4/SWA-066_hierarchy_neighborhood_sanity_audit_v1.json`
