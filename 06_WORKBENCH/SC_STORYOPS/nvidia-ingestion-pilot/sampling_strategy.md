# NVIDIA Ingestion Pilot Sampling Strategy

Date: 2026-05-15
Root corpus: `/Users/sheshnarayaniyer/Documents/noesis/Research`

## Goal

Create a deterministic 100-node pilot set for embedding evaluation focused on non-editorial worldbuilding data:

- 35 `bio_field_charts`
- 35 `interpretation_maps`
- 30 `cross_integration_histories`

## Outputs

- Sample manifest: `06_WORKBENCH/SC_STORYOPS/nvidia-ingestion-pilot/sample_manifest.csv`
- Query scoring sheet: `06_WORKBENCH/SC_STORYOPS/nvidia-ingestion-pilot/pilot_query_eval_template.csv`

## Corpus Snapshot (at generation time)

- Total files: `583`
- Images: `378`
- Text/docs: `186` (`.md`, `.pdf`, `.doc`, `.docx`, `.txt`)

## Deterministic Selection Rules

Selection seed: `42`

### 1) Build pools

- Image extensions: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.tif`, `.tiff`, `.bmp`, `.heic`
- Text/document extensions: `.md`, `.txt`, `.doc`, `.docx`, `.pdf`

Keyword routing:

- `bio_field_charts` keyword regex:
  - `(bio|field|chart|graph|plot|hrv|impedance|ecg|spectrum|wave)`
- `interpretation_maps` keyword regex:
  - `(map|matrix|framework|model|system|topology|network|diagram|architecture)`
- `cross_integration_histories` keyword regex:
  - `(history|origin|timeline|evolution|integration|cross|synthesis|interpret|analysis|article|paper)`

### 2) Fill target buckets

- Select from primary keyword pool first.
- If pool is short, backfill from fallback pool while avoiding duplicates:
  - Chart/map fallback: `other_imgs`
  - Histories fallback: `other_text`

### 3) Write manifest rows

Each row includes:

- `node_id` (`NODE-001`..`NODE-100`)
- `bucket_type`
- `source_path`
- `source_type` (`image` or `document`)
- `language_hint`
- evaluation placeholders for neighbors, parent, provenance, and model scoring

## Evaluation Plan (Model A vs Model B)

Text models:

- Model A: `baai/bge-m3`
- Model B: `nvidia/nv-embed-v1`

Vision model for image-derived nodes:

- `nvidia/llama-nemotron-embed-vl-1b-v2`

Weighted decision rubric:

- Recall@10 relevance: `35%`
- Cross-language alignment: `30%`
- Hierarchy coherence: `25%`
- Provenance traceability: `10%`

Decision rule:

- Keep `baai/bge-m3` unless `nvidia/nv-embed-v1` wins by `>= 0.4` weighted points.
- Keep VL model for chart/map image lane regardless of text winner.

## QA Checks Before Embedding

- Confirm `sample_manifest.csv` has exactly 100 rows.
- Confirm per-bucket counts are 35/35/30.
- Spot-check at least 10 rows from each bucket for semantic fit.
- Remove obvious out-of-scope editorial items if discovered.
