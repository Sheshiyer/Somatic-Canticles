# SWA-067 Model Selection Decision Memo v2

## Decision
- Select `nvidia/nv-embed-v1` as the text embedding baseline for integration execution.

## Evidence
- `phase4/SWA-061_weighted_scores_modelA_modelB_v2.json`
- `phase3/SWA-058_recall_match_metrics_v1.json`
- `phase3/SWA-059_hierarchy_coherence_metrics_v1.json`

## Rationale
- Model A index build is blocked by persistent provider runtime failures.
- Model B retrieval quality is strong (`recall@10 = 0.9333`) with higher hierarchy coherence (`2.7575`).
- Weighted margin (`B - A`) = `2.3226`, exceeding threshold `0.4`.

## Residual Risks
- Cross-language evaluation remains incomplete until multilingual samples are added.
