# SWA-073 Ownership Matrix v1

Date: 2026-05-16
Task ID: SWA-073

## Role Definitions
- StoryOps Planner: scope control, sequencing, and gate approval.
- DevOps Eng: CI and operational monitoring controls.
- QA Eng: incident, release, and validation contracts.
- Data Eng: provenance and schema integrity consultation.
- Backend Eng: runtime and model-lane implementation consultation.

## RACI by Phase 5 Task
| SWA Task | Responsible | Accountable | Consulted | Informed | Input Artifacts | Output Artifacts |
|---|---|---|---|---|---|---|
| SWA-073 | StoryOps Planner | StoryOps Planner | DevOps Eng, QA Eng, Data Eng | Backend Eng | `phase4/SWA-072_transition_to_integration_approval_v2.md`, `risk_register.md` | `phase5/SWA-073_*` |
| SWA-074 | StoryOps Planner | StoryOps Planner | DevOps Eng, QA Eng | Data Eng, Backend Eng | `phase5/SWA-073_integration_epic_map_v1.md`, `phase5/SWA-073_gate_checklist_v1.md` | `phase5/SWA-074_*` |
| SWA-075 | DevOps Eng | StoryOps Planner | Backend Eng, QA Eng | Data Eng | `phase5/SWA-074_implementation_issue_translation_v1.md` | `phase5/SWA-075_*` |
| SWA-076 | DevOps Eng | StoryOps Planner | QA Eng, Data Eng | Backend Eng | `phase3/SWA-058_recall_match_metrics_v1.json`, `phase3/SWA-059_hierarchy_coherence_metrics_v1.json` | `phase5/SWA-076_*` |
| SWA-077 | QA Eng | StoryOps Planner | DevOps Eng, Backend Eng | Data Eng | `phase5/SWA-075_*` | `phase5/SWA-077_*` |
| SWA-078 | QA Eng | StoryOps Planner | DevOps Eng, Data Eng | Backend Eng | `phase5/SWA-075_*`, `phase5/SWA-076_*`, `phase5/SWA-077_*` | `phase5/SWA-078_*` |
| SWA-079 | StoryOps Planner | StoryOps Planner | QA Eng, DevOps Eng | Data Eng, Backend Eng | `phase5/SWA-078_*` | `phase5/SWA-079_*` |
| SWA-080 | StoryOps Planner | StoryOps Planner | QA Eng, DevOps Eng | Data Eng, Backend Eng | `phase5/SWA-079_*` | `phase5/SWA-080_*` |

## Handoff Rules
- Every handoff includes artifact path, completion status, and unresolved risk notes.
- No downstream task starts without explicit dependency closure evidence.
- Accountability for phase transition remains with StoryOps Planner.
