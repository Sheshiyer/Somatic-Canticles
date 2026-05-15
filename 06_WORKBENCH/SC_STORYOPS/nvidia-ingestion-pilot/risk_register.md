# Risk Register - NVIDIA Ingestion Pilot

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|
| R-01 | Editorial contamination enters non-editorial graph | High | Medium | Enforce boundary policy and schema gates | StoryOps Planner |
| R-02 | Provenance fields missing or weak | High | Medium | Mandatory source/evidence fields per node/edge | Data Eng |
| R-03 | Multilingual retrieval mismatch | Medium | Medium | Use bge-m3 baseline and language drift scoring | QA Eng |
| R-04 | Vision extraction semantic drift | High | Medium | OCR plus VL embedding plus corroboration checks | Backend Eng |
| R-05 | Tracker drift between plan and execution | Medium | Medium | Weekly checkpoint + todo reconciliation | StoryOps Planner |
| R-06 | Model availability changes mid-run | Medium | High | Keep fallback model lane and re-probe before batches | DevOps Eng |
| R-07 | Overfitting to pilot sample | Medium | Medium | Add post-pilot holdout validation set | QA Eng |
| R-08 | Undetected duplicate nodes skew graph | Medium | Medium | Canonical node-id ledger + dedupe checks | Data Eng |

## Gate Condition
- No phase transition without risk review update and owner acknowledgment.
