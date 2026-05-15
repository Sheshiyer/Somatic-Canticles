# SWA-035 Text Extraction Normalization Spec v1

## Input
- Enriched manifest rows where `source_type=document`.

## Normalization Steps
1. Load source text when parser support exists.
2. Collapse newlines and repeated whitespace.
3. Preserve provenance via `node_id` and `source_path`.
4. Emit deterministic extraction status per row.

## Status Classes
- `extracted`
- `requires_pdf_parser`
- `requires_doc_parser`
- `unsupported_extension`
- `error:<type>`

## Output Artifact
- `phase2/SWA-035_text_extraction_preview_v1.json`
