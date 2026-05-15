# Baseline Metrics

Date: 2026-05-15

## Dataset Baseline
- Total corpus files scanned: `583`
- Pilot manifest nodes: `100`
- Query template rows: `30`

## Model Baseline Inputs
- Candidate text model A: `baai/bge-m3`
- Candidate text model B: `nvidia/nv-embed-v1`
- Vision lane model: `nvidia/llama-nemotron-embed-vl-1b-v2`

## Score Baseline (pre-run placeholders)
- Recall@10: TBD
- Cross-language alignment: TBD
- Hierarchy coherence: TBD
- Provenance traceability: TBD

## Decision Threshold
- Switch from model A only if model B wins weighted score by `>= 0.4`.
