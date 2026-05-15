# SWA-023 Contract: Retrieval Evaluation Rubric

## Weighted Metrics
- Recall@10 relevance: `35%`
- Cross-language alignment: `30%`
- Hierarchy coherence: `25%`
- Provenance traceability: `10%`

## Scoring Range
- Each metric scored `0-5` per query batch.
- Weighted aggregate used for model decision.

## Decision Rule
- Keep model A unless model B exceeds by `>= 0.4` weighted points.
