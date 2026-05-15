# SWA Phase 3 Smoke Summary v1

## Outcomes
- **SWA-051 vl-caption-embed**
  - batch_size: `1`
  - success_count: `1`
  - fail_count: `0`
  - vector_dim_set: `[2048]`

## Notes
- bge-m3 was attempted as requested and may fail depending on current NVIDIA runtime health.
- VL lane uses vision captioning (`meta/llama-3.2-11b-vision-instruct`) then embeds caption text with `nvidia/llama-nemotron-embed-vl-1b-v2`.
