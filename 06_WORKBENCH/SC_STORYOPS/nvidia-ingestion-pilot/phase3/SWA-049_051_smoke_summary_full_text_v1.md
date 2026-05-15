# SWA Phase 3 Smoke Summary v1

## Outcomes
- **SWA-049 bge-m3**
  - batch_size: `100`
  - success_count: `0`
  - fail_count: `100`
  - vector_dim_set: `[]`
- **SWA-050 nv-embed-v1**
  - batch_size: `100`
  - success_count: `100`
  - fail_count: `0`
  - vector_dim_set: `[4096]`

## Notes
- bge-m3 was attempted as requested and may fail depending on current NVIDIA runtime health.
- VL lane uses vision captioning (`meta/llama-3.2-11b-vision-instruct`) then embeds caption text with `nvidia/llama-nemotron-embed-vl-1b-v2`.
