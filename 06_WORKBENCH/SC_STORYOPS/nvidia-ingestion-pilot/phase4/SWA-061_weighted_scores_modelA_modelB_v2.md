# SWA-061 Weighted Scores for Model A and B v2

## Contractual Inputs
- `phase3/SWA-058_recall_match_metrics_v1.json`
- `phase3/SWA-059_hierarchy_coherence_metrics_v1.json`
- `phase4/SWA-065_provenance_fidelity_audit_v1.json`

## Result
- Model A (`baai/bge-m3`): `0.495`
- Model B (`nvidia/nv-embed-v1`): `2.8176`
- Margin (`B - A`): `2.3226`
- Threshold (`>= 0.4`): `pass`

## Note
- Cross-language score remains `0.0` for both lanes because pilot corpus is monolingual (`en`).
