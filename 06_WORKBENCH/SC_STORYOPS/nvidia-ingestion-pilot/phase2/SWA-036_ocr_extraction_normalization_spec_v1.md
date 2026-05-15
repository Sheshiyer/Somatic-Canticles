# SWA-036 OCR Extraction Normalization Spec v1

## Scope
Image-derived pilot nodes from:
- `bio_field_charts`
- `interpretation_maps`

## OCR Policy
1. Run OCR on all image nodes before semantic embedding.
2. Store `ocr_text_excerpt` and extraction confidence.
3. If confidence is low, flag node for manual review.
4. Preserve image fingerprint and provenance reference.

## Quality Bands
- `high`: usable for direct retrieval context
- `medium`: usable with caution and review notes
- `low`: quarantine until manual confirmation

## Required Fields
- `image_fingerprint`
- `ocr_text_excerpt`
- `extraction_quality`
- `provenance_ref`

## Output Queue
- Nodes requiring OCR execution are listed in `phase2/SWA-036_ocr_queue_v1.csv`.
