# SWA-069 Hardening Backlog for Chosen Model Stack v1

## Priority 0
- Execute `SWA-052..SWA-059` end-to-end to replace proxy metrics with contractual retrieval metrics.
- Populate `pilot_query_eval_template.csv` with concrete query text and expected node ids.
- Regenerate unresolved source asset for `NODE-063` and re-run single-row VL embedding.

## Priority 1
- Add embedding-output persistence with vectors and checksums for reproducible indexing.
- Add structured retry policy for provider `500` errors on model A lane.
- Add automatic empty-file and missing-file preflight checks before VL captioning.

## Priority 2
- Expand multilingual sample coverage to support cross-language scoring.
- Add nightly drift-check report over latency, success rate, and unresolved rows.
