# SWA-070 Rollback Criteria v1

## Trigger Conditions
- Full-corpus text success rate for chosen model drops below `95%` in two consecutive runs.
- p95 latency exceeds `4000 ms` for two consecutive runs.
- Provenance integrity falls below `99%` non-empty source linkage.
- Unresolved VL rows exceed `3%` of image-derived nodes.

## Rollback Actions
- Freeze promotion to integration tasks.
- Re-run prior known-good lane artifacts and compare checksums.
- Temporarily switch to fallback text lane for critical indexing windows.
- Open incident ticket with provider evidence and sample payload ids.
