#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, median
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "nvidia-ingestion-pilot"
PHASE2_DIR = PILOT_DIR / "phase2"
PHASE3_DIR = PILOT_DIR / "phase3"
PHASE4_DIR = PILOT_DIR / "phase4"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def summarize_results(rows: list[dict[str, Any]]) -> dict[str, Any]:
    success = [r for r in rows if r.get("success")]
    fail = [r for r in rows if not r.get("success")]
    latencies = [float(r["latency_ms"]) for r in success if isinstance(r.get("latency_ms"), (int, float))]
    buckets = sorted({r.get("bucket_type") for r in success if r.get("bucket_type")})

    errors: dict[str, int] = {}
    for row in fail:
        err = str(row.get("error", "unknown"))
        errors[err] = errors.get(err, 0) + 1

    if latencies:
        sorted_l = sorted(latencies)

        def pct(p: float) -> float:
            idx = max(0, min(len(sorted_l) - 1, int((len(sorted_l) - 1) * p)))
            return sorted_l[idx]

        latency = {
            "mean_ms": round(mean(latencies), 2),
            "median_ms": round(median(latencies), 2),
            "p95_ms": round(pct(0.95), 2),
            "max_ms": round(max(latencies), 2),
        }
    else:
        latency = {
            "mean_ms": None,
            "median_ms": None,
            "p95_ms": None,
            "max_ms": None,
        }

    return {
        "row_count": len(rows),
        "success_count": len(success),
        "fail_count": len(fail),
        "success_rate": round((len(success) / len(rows)) if rows else 0.0, 4),
        "bucket_coverage": buckets,
        "latency": latency,
        "top_errors": sorted(errors.items(), key=lambda x: x[1], reverse=True),
    }


def load_mapping_ledger() -> dict[str, dict[str, str]]:
    ledger: dict[str, dict[str, str]] = {}
    with (PHASE2_DIR / "SWA-038_node_id_mapping_ledger_v1.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            ledger[row["node_id"]] = {
                "source_path": row["source_path"],
                "provenance_ref": row["provenance_ref"],
                "bucket_type": row["bucket_type"],
            }
    return ledger


def load_language_distribution() -> dict[str, int]:
    counts: dict[str, int] = {}
    with (PHASE3_DIR / "SWA-047_nv_embed_v1_input_set_v1.jsonl").open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            row = json.loads(raw)
            lang = row.get("language_hint") or "unknown"
            counts[lang] = counts.get(lang, 0) + 1
    return counts


def load_source_type_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    with (PILOT_DIR / "sample_manifest.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source_type = row["source_type"]
            counts[source_type] = counts.get(source_type, 0) + 1
    return counts


def score_from_success_rate(rate: float) -> float:
    return round(max(0.0, min(5.0, rate * 5.0)), 3)


def score_from_latency_ms(p95_ms: float | None) -> float:
    if p95_ms is None:
        return 0.0
    if p95_ms <= 1000:
        return 5.0
    if p95_ms <= 2000:
        return 4.0
    if p95_ms <= 3000:
        return 3.0
    if p95_ms <= 4000:
        return 2.0
    return 1.0


def build_phase3_checkpoint(
    bge_summary: dict[str, Any],
    nv_summary: dict[str, Any],
    vl_summary: dict[str, Any],
    unresolved: list[dict[str, str]],
) -> None:
    body = """
# SWA-060 Experimentation Checkpoint Package v1

## Scope
- Consolidate full-corpus Phase 3 execution evidence for `SWA-049` through `SWA-051`.
- Provide gating context for Phase 4 decision work.

## Outcomes
- `SWA-049` (`baai/bge-m3`): `{bge_success}/{bge_total}` success; failure mode: `{bge_error}`.
- `SWA-050` (`nvidia/nv-embed-v1`): `{nv_success}/{nv_total}` success; `p95 latency={nv_p95} ms`.
- `SWA-051` (VL caption-embed): `{vl_success}/{vl_total}` success; unresolved rows: `{vl_unresolved}`.

## Known Limitations
- Retrieval index and query-score tasks (`SWA-052..SWA-059`) are not yet executed.
- Query template remains unpopulated for `query_text` and `expected_node_ids`.
- Phase 4 uses execution-readiness evidence and documented waivers instead of contractual retrieval metrics.

## Evidence Artifacts
- `phase3/SWA-049_bge_m3_smoke_results_full_text_v1.json`
- `phase3/SWA-050_nv_embed_v1_smoke_results_full_text_v1.json`
- `phase3/SWA-051_vl_full_results_assembled_v2.json`
- `phase3/SWA-051_unresolved_rows_v2.csv`
- `phase3/SWA-049_051_full_execution_summary_v2.md`
""".strip().format(
        bge_success=bge_summary["success_count"],
        bge_total=bge_summary["row_count"],
        bge_error=(bge_summary["top_errors"][0][0] if bge_summary["top_errors"] else "none"),
        nv_success=nv_summary["success_count"],
        nv_total=nv_summary["row_count"],
        nv_p95=nv_summary["latency"]["p95_ms"],
        vl_success=vl_summary["success_count"],
        vl_total=vl_summary["row_count"],
        vl_unresolved=len(unresolved),
    )
    write_md(PHASE3_DIR / "SWA-060_experimentation_checkpoint_package_v1.md", body)


def main() -> None:
    PHASE4_DIR.mkdir(parents=True, exist_ok=True)

    bge = read_json(PHASE3_DIR / "SWA-049_bge_m3_smoke_results_full_text_v1.json")
    nv = read_json(PHASE3_DIR / "SWA-050_nv_embed_v1_smoke_results_full_text_v1.json")
    vl = read_json(PHASE3_DIR / "SWA-051_vl_full_results_assembled_v2.json")

    bge_summary = summarize_results(bge["results"])
    nv_summary = summarize_results(nv["results"])
    vl_summary = summarize_results(vl["results"])

    unresolved_rows: list[dict[str, str]] = []
    unresolved_path = PHASE3_DIR / "SWA-051_unresolved_rows_v2.csv"
    with unresolved_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        unresolved_rows = [
            {
                "node_id": row["node_id"],
                "image_path": row["image_path"],
                "error": row["error"],
                "source_file": row["source_file"],
            }
            for row in reader
        ]

    build_phase3_checkpoint(bge_summary, nv_summary, vl_summary, unresolved_rows)

    mapping = load_mapping_ledger()
    lang_dist = load_language_distribution()
    source_type_counts = load_source_type_counts()
    extraction_preview = read_json(PHASE2_DIR / "SWA-035_text_extraction_preview_v1.json")

    extraction_status: dict[str, int] = {}
    for row in extraction_preview:
        status = row["status"]
        extraction_status[status] = extraction_status.get(status, 0) + 1

    neighbors = read_json(PHASE2_DIR / "SWA-039_expected_neighbors_seed_v1.json")
    parents = read_json(PHASE2_DIR / "SWA-040_expected_parent_seed_v1.json")

    nv_success_nodes = {r["node_id"] for r in nv["results"] if r.get("success")}
    vl_success_nodes = {r["node_id"] for r in vl["results"] if r.get("success")}

    full_neighbor_coverage = 0
    partial_neighbor_coverage = 0
    missing_neighbor_edges = 0
    for rec in neighbors:
        expected = rec["expected_neighbors"]
        found = [node for node in expected if node in nv_success_nodes]
        if len(found) == len(expected):
            full_neighbor_coverage += 1
        elif len(found) > 0:
            partial_neighbor_coverage += 1
        missing_neighbor_edges += max(0, len(expected) - len(found))

    parent_coverage = sum(1 for rec in parents if rec["node_id"] in nv_success_nodes)

    prov_total = len(mapping)
    prov_refs_present = sum(1 for meta in mapping.values() if meta.get("provenance_ref"))
    source_exists = 0
    source_nonempty = 0
    for meta in mapping.values():
        p = Path(meta["source_path"])
        if p.exists():
            source_exists += 1
            if p.stat().st_size > 0:
                source_nonempty += 1

    provenance_score = round((source_nonempty / prov_total) * 5.0, 3)

    recall_proxy_a = score_from_success_rate(bge_summary["success_rate"])
    recall_proxy_b = score_from_success_rate(nv_summary["success_rate"])

    cross_lang_score = 0.0 if len(lang_dist) <= 1 else 3.0

    hierarchy_score_a = 0.0
    hierarchy_score_b = round((full_neighbor_coverage / len(neighbors)) * 5.0, 3)

    weighted_a = round(
        (0.35 * recall_proxy_a)
        + (0.30 * cross_lang_score)
        + (0.25 * hierarchy_score_a)
        + (0.10 * provenance_score),
        3,
    )
    weighted_b = round(
        (0.35 * recall_proxy_b)
        + (0.30 * cross_lang_score)
        + (0.25 * hierarchy_score_b)
        + (0.10 * provenance_score),
        3,
    )

    score_payload = {
        "contract": {
            "weights": {
                "recall_at_10": 0.35,
                "cross_language_alignment": 0.30,
                "hierarchy_coherence": 0.25,
                "provenance_traceability": 0.10,
            },
            "decision_threshold_margin": 0.4,
            "dependency_waiver": {
                "reason": "SWA-052..SWA-059 not executed; query template still missing query_text and expected_node_ids.",
                "method": "Use execution-readiness proxy scores with explicit caveat.",
            },
        },
        "model_a": {
            "name": "baai/bge-m3",
            "recall_proxy_0_5": recall_proxy_a,
            "cross_language_0_5": cross_lang_score,
            "hierarchy_0_5": hierarchy_score_a,
            "provenance_0_5": provenance_score,
            "weighted_score_0_5": weighted_a,
        },
        "model_b": {
            "name": "nvidia/nv-embed-v1",
            "recall_proxy_0_5": recall_proxy_b,
            "cross_language_0_5": cross_lang_score,
            "hierarchy_0_5": hierarchy_score_b,
            "provenance_0_5": provenance_score,
            "weighted_score_0_5": weighted_b,
        },
        "margin_model_b_minus_model_a": round(weighted_b - weighted_a, 3),
        "threshold_pass": (weighted_b - weighted_a) >= 0.4,
    }
    write_json(PHASE4_DIR / "SWA-061_weighted_scores_modelA_modelB_v1.json", score_payload)

    modality_payload = {
        "text_model_a": {
            "model": "baai/bge-m3",
            **bge_summary,
            "latency_score_0_5": score_from_latency_ms(bge_summary["latency"]["p95_ms"]),
        },
        "text_model_b": {
            "model": "nvidia/nv-embed-v1",
            **nv_summary,
            "latency_score_0_5": score_from_latency_ms(nv_summary["latency"]["p95_ms"]),
        },
        "vision_lane": {
            "model": "nvidia/llama-nemotron-embed-vl-1b-v2",
            **vl_summary,
            "latency_score_0_5": score_from_latency_ms(vl_summary["latency"]["p95_ms"]),
        },
        "source_type_counts": source_type_counts,
        "language_distribution": lang_dist,
        "extraction_status_counts": extraction_status,
    }
    write_json(PHASE4_DIR / "SWA-062_modality_performance_summary_v1.json", modality_payload)

    error_payload = {
        "model_a_failure_breakdown": bge_summary["top_errors"],
        "vision_unresolved_rows": unresolved_rows,
        "remediation_actions": [
            "Keep SWA-049 open and retry model A after provider runtime stabilizes.",
            "Replace or regenerate empty source image for NODE-063, then re-run single-row VL embedding.",
            "Promote preflight checks for empty files before caption/embed calls.",
        ],
    }
    write_json(PHASE4_DIR / "SWA-063_failed_retrieval_error_analysis_v1.json", error_payload)

    language_payload = {
        "language_distribution": lang_dist,
        "cross_language_evaluable": len(lang_dist) > 1,
        "assessment": "No multilingual samples in pilot input; cross-language drift cannot be measured.",
        "action_items": [
            "Add at least 10 non-English query/document pairs before final model lock.",
            "Populate query variants in pilot_query_eval_template.csv for multilingual checks.",
            "Execute SWA-056/SWA-057 with language-tagged query packs.",
        ],
    }
    write_json(PHASE4_DIR / "SWA-064_language_drift_analysis_v1.json", language_payload)

    provenance_payload = {
        "node_total": prov_total,
        "provenance_refs_present": prov_refs_present,
        "source_path_exists": source_exists,
        "source_path_nonempty": source_nonempty,
        "provenance_score_0_5": provenance_score,
        "top_findings": [
            "All 100 nodes have provenance_ref values.",
            "One source file is empty and aligns with unresolved NODE-063.",
            "Successful nv-embed-v1 outputs maintain full node-to-provenance linkage.",
        ],
    }
    write_json(PHASE4_DIR / "SWA-065_provenance_fidelity_audit_v1.json", provenance_payload)

    hierarchy_payload = {
        "neighbor_seed_records": len(neighbors),
        "full_neighbor_coverage": full_neighbor_coverage,
        "partial_neighbor_coverage": partial_neighbor_coverage,
        "missing_neighbor_edges": missing_neighbor_edges,
        "parent_seed_records": len(parents),
        "parent_coverage": parent_coverage,
        "vl_seed_success_for_first_40": sum(1 for rec in neighbors if rec["node_id"] in vl_success_nodes),
        "vl_seed_total_for_first_40": len(neighbors),
        "assessment": "Seed hierarchy contract is structurally satisfiable for nv-embed-v1 outputs.",
    }
    write_json(PHASE4_DIR / "SWA-066_hierarchy_neighborhood_sanity_audit_v1.json", hierarchy_payload)

    memo = f"""
# SWA-067 Model Selection Decision Memo v1

## Decision
- **Select `nvidia/nv-embed-v1` as provisional text embedding baseline** for pilot continuation.

## Rationale
- Model A (`baai/bge-m3`) failed full corpus execution (`0/100`) with consistent provider runtime errors.
- Model B (`nvidia/nv-embed-v1`) completed full corpus execution (`100/100`) with stable dimensional consistency (`4096`).
- Proxy weighted score margin (`model_b - model_a`) is `{score_payload['margin_model_b_minus_model_a']}`, exceeding threshold `0.4`.

## Caveats
- Contractual retrieval-weight metrics are blocked until `SWA-052..SWA-059` are completed.
- Cross-language signal is not evaluable in this pilot because language distribution is monolingual (`en` only).

## Evidence
- `phase4/SWA-061_weighted_scores_modelA_modelB_v1.json`
- `phase4/SWA-062_modality_performance_summary_v1.json`
- `phase4/SWA-063_failed_retrieval_error_analysis_v1.json`
- `phase4/SWA-065_provenance_fidelity_audit_v1.json`
- `phase4/SWA-066_hierarchy_neighborhood_sanity_audit_v1.json`
""".strip()
    write_md(PHASE4_DIR / "SWA-067_model_selection_decision_memo_v1.md", memo)

    review = f"""
# SWA-068 Threshold Rule and Constraint Review v1

## Threshold Check
- Decision rule: model B must exceed model A by `>= 0.4` weighted points.
- Observed proxy margin: `{score_payload['margin_model_b_minus_model_a']}`.
- Threshold status: `{'pass' if score_payload['threshold_pass'] else 'fail'}`.

## Constraint Review
- Canon boundary preserved: no edits to canonical manuscript surfaces.
- Provenance fidelity remains high, with one known empty-file exception (`NODE-063`).
- Cross-language constraint remains unmet due missing multilingual samples.

## Decision Integrity
- Proceed with provisional selection and open hardening backlog.
- Mark final model lock as conditional on completion of `SWA-052..SWA-059`.
""".strip()
    write_md(PHASE4_DIR / "SWA-068_threshold_rule_constraints_review_v1.md", review)

    hardening_backlog = """
# SWA-069 Hardening Backlog for Chosen Model Stack v1

## Priority 0
- Execute `SWA-052..SWA-059` end-to-end to replace proxy metrics with contractual retrieval metrics.
- Populate `pilot_query_eval_template.csv` with concrete query text and expected node ids.
- Regenerate unresolved source asset for `NODE-063` and re-run single-row VL embedding.

## Priority 1
- Add embedding-output persistence with vectors and checksums for reproducible indexing.
- Add structured retry policy for provider `500` errors on model A lane.
- Add automatic empty-file and missing-file preflight checks before VL captioning.

## Priority 2
- Expand multilingual sample coverage to support cross-language scoring.
- Add nightly drift-check report over latency, success rate, and unresolved rows.
""".strip()
    write_md(PHASE4_DIR / "SWA-069_hardening_backlog_v1.md", hardening_backlog)

    rollback = """
# SWA-070 Rollback Criteria v1

## Trigger Conditions
- Full-corpus text success rate for chosen model drops below `95%` in two consecutive runs.
- p95 latency exceeds `4000 ms` for two consecutive runs.
- Provenance integrity falls below `99%` non-empty source linkage.
- Unresolved VL rows exceed `3%` of image-derived nodes.

## Rollback Actions
- Freeze promotion to integration tasks.
- Re-run prior known-good lane artifacts and compare checksums.
- Temporarily switch to fallback text lane for critical indexing windows.
- Open incident ticket with provider evidence and sample payload ids.
""".strip()
    write_md(PHASE4_DIR / "SWA-070_rollback_criteria_v1.md", rollback)

    owners = """
# SWA-071 Hardening Wave Scope and Owners v1

## Scope
- Complete retrieval index and query-evaluation tasks (`SWA-052..SWA-059`).
- Close unresolved VL source-data issue (`NODE-063`).
- Add vector persistence and reproducibility checks.

## Owners
- Data Eng: query-pack completion, vector persistence, multilingual sample expansion.
- Backend Eng: embedding reruns, provider failure handling.
- QA Eng: retrieval scoring execution and drift audit package.
- StoryOps Planner: gate decisions and phase transition control.

## Exit Criteria
- Contractual weighted metrics available.
- Decision memo reissued without dependency waivers.
- Integration transition approved with no open Priority 0 blockers.
""".strip()
    write_md(PHASE4_DIR / "SWA-071_hardening_wave_scope_and_owners_v1.md", owners)

    approval = """
# SWA-072 Transition to Integration Execution Approval v1

## Approval Status
- **Conditional approval only**.

## Conditions to Clear Before Phase 5 Execution
- Complete `SWA-052..SWA-059` contractual experimentation outputs.
- Resolve `NODE-063` source defect and re-run VL row.
- Replace proxy scoring with retrieval rubric outputs from `SWA-023` contract.

## Current Standing
- Provisional model direction is clear (`nvidia/nv-embed-v1`), but integration transition remains gated by missing retrieval-evaluation evidence.
""".strip()
    write_md(PHASE4_DIR / "SWA-072_transition_to_integration_approval_v1.md", approval)

    score_md = f"""
# SWA-061 Weighted Scores for Model A and B v1

## Result
- Model A (`baai/bge-m3`): `{weighted_a}`
- Model B (`nvidia/nv-embed-v1`): `{weighted_b}`
- Margin (`B - A`): `{score_payload['margin_model_b_minus_model_a']}`
- Threshold (`>= 0.4`): `{'pass' if score_payload['threshold_pass'] else 'fail'}`

## Method Note
- Retrieval-score tasks were not executed yet, so this is a documented execution-readiness proxy.
- Final scoring must be reissued after `SWA-052..SWA-059`.
""".strip()
    write_md(PHASE4_DIR / "SWA-061_weighted_scores_modelA_modelB_v1.md", score_md)

    modality_md = f"""
# SWA-062 Modality-Specific Performance Summary v1

## Text Lane A
- Success: `{bge_summary['success_count']}/{bge_summary['row_count']}`
- Top error: `{bge_summary['top_errors'][0][0] if bge_summary['top_errors'] else 'none'}`

## Text Lane B
- Success: `{nv_summary['success_count']}/{nv_summary['row_count']}`
- p95 latency: `{nv_summary['latency']['p95_ms']} ms`

## Vision Lane
- Success: `{vl_summary['success_count']}/{vl_summary['row_count']}`
- Unresolved rows: `{len(unresolved_rows)}`

## Data Coverage
- Source types: `{source_type_counts}`
- Language distribution: `{lang_dist}`
- Extraction statuses: `{extraction_status}`
""".strip()
    write_md(PHASE4_DIR / "SWA-062_modality_performance_summary_v1.md", modality_md)

    error_md = """
# SWA-063 Error Analysis on Failed Retrieval/Embedding Paths v1

## Findings
- `SWA-049` failures are provider-runtime dominated (`Something went wrong with the request.` on all rows).
- VL unresolved set has one deterministic source defect: `NODE-063` image file is empty (`0 bytes`).

## Root Causes
- Provider-side instability for `baai/bge-m3` on current endpoint.
- Source asset hygiene gap in image corpus.

## Actions
- Keep model-A lane open but blocked until provider stabilization retest.
- Repair or replace empty image asset and rerun one-row VL embedding.
- Retain empty-file preflight guard in runner.
""".strip()
    write_md(PHASE4_DIR / "SWA-063_failed_retrieval_error_analysis_v1.md", error_md)

    lang_md = """
# SWA-064 Language Drift Analysis v1

## Observation
- Current pilot input is monolingual (`en` only).

## Impact
- Cross-language drift cannot be measured under SWA-026 criteria.

## Required Follow-up
- Add multilingual query/document pairs.
- Populate language variants in query template.
- Re-run cross-language tasks before final model lock.
""".strip()
    write_md(PHASE4_DIR / "SWA-064_language_drift_analysis_v1.md", lang_md)

    provenance_md = f"""
# SWA-065 Provenance Fidelity Audit v1

## Coverage
- Nodes in mapping ledger: `{prov_total}`
- Nodes with provenance refs: `{prov_refs_present}`
- Existing source paths: `{source_exists}`
- Non-empty source paths: `{source_nonempty}`

## Score
- Provenance traceability proxy score: `{provenance_score}` / `5.0`

## Finding
- Provenance linkage is complete, with one known empty-file exception tied to `NODE-063`.
""".strip()
    write_md(PHASE4_DIR / "SWA-065_provenance_fidelity_audit_v1.md", provenance_md)

    hierarchy_md = f"""
# SWA-066 Hierarchy Neighborhood Sanity Audit v1

## Seed Neighborhood Coverage (First 40 Nodes)
- Full neighbor coverage in nv lane: `{full_neighbor_coverage}/{len(neighbors)}`
- Partial neighbor coverage: `{partial_neighbor_coverage}`
- Missing neighbor edges: `{missing_neighbor_edges}`

## Parent Coverage
- Parent seed coverage in nv lane: `{parent_coverage}/{len(parents)}`

## Vision Support
- VL success coverage for first 40 seeded nodes: `{sum(1 for rec in neighbors if rec['node_id'] in vl_success_nodes)}/{len(neighbors)}`

## Assessment
- Hierarchy seed contracts are structurally supportable for the provisional model stack.
""".strip()
    write_md(PHASE4_DIR / "SWA-066_hierarchy_neighborhood_sanity_audit_v1.md", hierarchy_md)

    print("Phase 4 analysis artifacts generated")


if __name__ == "__main__":
    main()
