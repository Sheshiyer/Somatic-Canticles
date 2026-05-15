# SWA-014 Contract: Provenance Field Requirements

## Required Node Fields
- `node_id`
- `source_path`
- `source_type`
- `extracted_at`
- `extractor_model`
- `provenance_ref`

## Required Relation Fields
- `relation_type`
- `source_node_id`
- `target_node_id`
- `evidence_ref`
- `confidence`
- `created_at`

## Validation Rules
1. `source_path` must exist at ingestion time.
2. `provenance_ref` must map to artifact or extraction record.
3. `confidence` must be numeric and bounded [0,1].
4. Missing provenance fields fail batch acceptance.
