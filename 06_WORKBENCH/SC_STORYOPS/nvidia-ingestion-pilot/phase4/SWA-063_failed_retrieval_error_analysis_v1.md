# SWA-063 Error Analysis on Failed Retrieval/Embedding Paths v1

## Findings
- `SWA-049` failures are provider-runtime dominated (`Something went wrong with the request.` on all rows).
- VL unresolved set has one deterministic source defect: `NODE-063` image file is empty (`0 bytes`).

## Root Causes
- Provider-side instability for `baai/bge-m3` on current endpoint.
- Source asset hygiene gap in image corpus.

## Actions
- Keep model-A lane open but blocked until provider stabilization retest.
- Repair or replace empty image asset and rerun one-row VL embedding.
- Retain empty-file preflight guard in runner.
