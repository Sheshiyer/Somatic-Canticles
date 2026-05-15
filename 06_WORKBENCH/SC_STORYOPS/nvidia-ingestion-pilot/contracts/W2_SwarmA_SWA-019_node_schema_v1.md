# SWA-019 Contract: Node Schema v1

## Required Fields
- `node_id`
- `bucket_type`
- `source_path`
- `source_type`
- `language_hint`
- `expected_neighbors`
- `expected_parent`
- `provenance_ref`

## Optional Fields
- `summary`
- `confidence_notes`
- `quality_flags`

## Validation
- Missing required fields fail ingest batch.
- `node_id` must be globally unique in pilot manifest.
