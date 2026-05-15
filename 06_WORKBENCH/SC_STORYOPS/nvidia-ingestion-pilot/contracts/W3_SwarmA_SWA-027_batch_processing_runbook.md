# SWA-027 Contract: Batch Processing Runbook

## Batch Sequence
1. Validate manifest schema
2. Build input payloads by bucket
3. Run model lanes
4. Persist embeddings and logs
5. Run retrieval checks
6. Publish checkpoint package

## Operational Notes
- Keep each batch id unique and timestamped.
- Abort and quarantine on schema failure.
