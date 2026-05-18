# SWA-075 CI Check Report (latest)

Generated at: `2026-05-18T12:04:26.226838+00:00`
Overall status: `pass`

| Check | Severity | Status |
|---|---|---|
| C1_fixture_integrity | hard_fail | pass |
| C2_embedding_lane_health | hard_fail | pass |
| C3_retrieval_quality_regression | hard_fail | pass |
| C4_provenance_completeness | hard_fail | pass |
| C5_rollback_trigger_probe | warn | pass |

## Check Details

### C1_fixture_integrity
- Severity: `hard_fail`
- Status: `pass`
- Details:

```json
{
  "fixture_count": 7,
  "missing": [],
  "checksum_mismatches": []
}
```

### C2_embedding_lane_health
- Severity: `hard_fail`
- Status: `pass`
- Details:

```json
{
  "failures": [],
  "observed": {
    "model_b": {
      "row_count": 100,
      "success_count": 100,
      "fail_count": 0,
      "vector_dim": 4096
    },
    "multimodal": {
      "row_count": 69,
      "success_count": 68,
      "fail_count": 1,
      "vector_dim": 2048
    }
  }
}
```

### C3_retrieval_quality_regression
- Severity: `hard_fail`
- Status: `pass`
- Details:

```json
{
  "failures": [],
  "observed": {
    "recall_at_10": 0.9333,
    "mean_match_count": 1.2667,
    "mean_hierarchy_score_0_5": 2.7575,
    "bucket_mean_scores": {
      "bio_field_charts": 3.775,
      "interpretation_maps": 2.6475,
      "cross_integration_histories": 1.85
    }
  }
}
```

### C4_provenance_completeness
- Severity: `hard_fail`
- Status: `pass`
- Details:

```json
{
  "failures": [],
  "observed": {
    "provenance_rows": 169,
    "provenance_non_empty": 169,
    "provenance_ratio": 1.0,
    "null_anchor_query_count": 0
  }
}
```

### C5_rollback_trigger_probe
- Severity: `warn`
- Status: `pass`
- Details:

```json
{
  "observed": {
    "unresolved_vl_rate": 0.014493,
    "fail_count": 1,
    "row_count": 69
  },
  "threshold": 0.03,
  "source_contract": "phase4/SWA-070_rollback_criteria_v1.md"
}
```
