# SWA-022 Contract: Image-Derived Nodes

## Required Additions
- `image_fingerprint`
- `ocr_text_excerpt`
- `visual_embedding_model`
- `extraction_quality`

## Rules
- No image-derived ontology claim without evidence excerpt.
- If OCR confidence is low, mark for manual review queue.
- Vision and text lanes must both preserve provenance references.
