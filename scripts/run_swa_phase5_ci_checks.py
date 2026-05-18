#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "nvidia-ingestion-pilot"
PHASE3_DIR = PILOT_DIR / "phase3"
PHASE5_DIR = PILOT_DIR / "phase5"

THRESHOLD_MATRIX = PHASE5_DIR / "SWA-075_ci_threshold_matrix_v1.json"
CHECKSUM_FILE = PHASE3_DIR / "SWA-052_059_artifact_checksums_v1.json"

MODEL_B_INDEX = PHASE3_DIR / "SWA-053_modelB_retrieval_index_v1.json"
MULTIMODAL_INDEX = PHASE3_DIR / "SWA-054_multimodal_index_v1.json"
RECALL_METRICS = PHASE3_DIR / "SWA-058_recall_match_metrics_v1.json"
HIERARCHY_METRICS = PHASE3_DIR / "SWA-059_hierarchy_coherence_metrics_v1.json"
QUERY_SET = PHASE3_DIR / "SWA-055_057_query_set_v1.json"

REPORT_JSON = PHASE5_DIR / "SWA-075_ci_check_report_latest.json"
REPORT_MD = PHASE5_DIR / "SWA-075_ci_check_report_latest.md"


@dataclass
class CheckResult:
    check_id: str
    severity: str
    status: str
    details: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def find_lane(lanes: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for lane in lanes:
        if lane.get("lane") == name:
            return lane
    raise RuntimeError(f"Lane not found: {name}")


def status_for_failures(failures: list[str]) -> str:
    return "fail" if failures else "pass"


def run_checks() -> dict[str, Any]:
    threshold = read_json(THRESHOLD_MATRIX)
    checksum_rows = read_json(CHECKSUM_FILE)
    checksum_map = {row["artifact"]: row["sha256"] for row in checksum_rows}

    model_b = read_json(MODEL_B_INDEX)
    multimodal = read_json(MULTIMODAL_INDEX)
    recall = read_json(RECALL_METRICS)
    hierarchy = read_json(HIERARCHY_METRICS)
    query_set = read_json(QUERY_SET)

    checks: list[CheckResult] = []

    # C1 fixture integrity
    missing: list[str] = []
    mismatched: list[dict[str, str]] = []
    for rel in threshold["fixtures"]:
        abs_path = PILOT_DIR / rel
        if not abs_path.exists():
            missing.append(rel)
            continue
        expected = checksum_map.get(rel)
        if expected:
            actual = sha256_file(abs_path)
            if actual != expected:
                mismatched.append({"artifact": rel, "expected": expected, "actual": actual})

    checks.append(
        CheckResult(
            check_id="C1_fixture_integrity",
            severity="hard_fail",
            status="fail" if missing or mismatched else "pass",
            details={
                "fixture_count": len(threshold["fixtures"]),
                "missing": missing,
                "checksum_mismatches": mismatched,
            },
        )
    )

    # C2 embedding lane health
    c2_threshold = next(c for c in threshold["checks"] if c["check_id"] == "C2_embedding_lane_health")
    c2_failures: list[str] = []

    model_b_expected = c2_threshold["thresholds"]["model_b"]
    if model_b.get("row_count") != model_b_expected["row_count_eq"]:
        c2_failures.append("model_b.row_count")
    if model_b.get("success_count") != model_b_expected["success_count_eq"]:
        c2_failures.append("model_b.success_count")
    if model_b.get("fail_count") != model_b_expected["fail_count_eq"]:
        c2_failures.append("model_b.fail_count")
    if model_b.get("vector_dim") != model_b_expected["vector_dim_eq"]:
        c2_failures.append("model_b.vector_dim")

    multimodal_expected = c2_threshold["thresholds"]["multimodal"]
    if multimodal.get("row_count") != multimodal_expected["row_count_eq"]:
        c2_failures.append("multimodal.row_count")
    if multimodal.get("success_count", 0) < multimodal_expected["success_count_gte"]:
        c2_failures.append("multimodal.success_count")
    if multimodal.get("fail_count", 0) > multimodal_expected["fail_count_lte"]:
        c2_failures.append("multimodal.fail_count")
    if multimodal.get("vector_dim") != multimodal_expected["vector_dim_eq"]:
        c2_failures.append("multimodal.vector_dim")

    checks.append(
        CheckResult(
            check_id="C2_embedding_lane_health",
            severity="hard_fail",
            status=status_for_failures(c2_failures),
            details={
                "failures": c2_failures,
                "observed": {
                    "model_b": {
                        "row_count": model_b.get("row_count"),
                        "success_count": model_b.get("success_count"),
                        "fail_count": model_b.get("fail_count"),
                        "vector_dim": model_b.get("vector_dim"),
                    },
                    "multimodal": {
                        "row_count": multimodal.get("row_count"),
                        "success_count": multimodal.get("success_count"),
                        "fail_count": multimodal.get("fail_count"),
                        "vector_dim": multimodal.get("vector_dim"),
                    },
                },
            },
        )
    )

    # C3 retrieval quality regression
    c3_threshold = next(c for c in threshold["checks"] if c["check_id"] == "C3_retrieval_quality_regression")
    c3_values = c3_threshold["thresholds"]
    c3_failures: list[str] = []

    recall_lane = find_lane(recall["lanes"], "model_b")
    hierarchy_lane = find_lane(hierarchy["lanes"], "model_b")
    bucket_scores = hierarchy_lane.get("bucket_mean_scores", {})

    if recall_lane.get("recall_at_10", 0.0) < c3_values["model_b_recall_at_10_gte"]:
        c3_failures.append("model_b.recall_at_10")
    if recall_lane.get("mean_match_count", 0.0) < c3_values["model_b_mean_match_count_gte"]:
        c3_failures.append("model_b.mean_match_count")
    if hierarchy_lane.get("mean_hierarchy_score_0_5", 0.0) < c3_values["model_b_mean_hierarchy_score_0_5_gte"]:
        c3_failures.append("model_b.mean_hierarchy_score_0_5")

    bucket_thresholds = c3_values["model_b_bucket_mean_scores"]
    if bucket_scores.get("bio_field_charts", 0.0) < bucket_thresholds["bio_field_charts_gte"]:
        c3_failures.append("model_b.bucket.bio_field_charts")
    if bucket_scores.get("interpretation_maps", 0.0) < bucket_thresholds["interpretation_maps_gte"]:
        c3_failures.append("model_b.bucket.interpretation_maps")
    if bucket_scores.get("cross_integration_histories", 0.0) < bucket_thresholds["cross_integration_histories_gte"]:
        c3_failures.append("model_b.bucket.cross_integration_histories")

    checks.append(
        CheckResult(
            check_id="C3_retrieval_quality_regression",
            severity="hard_fail",
            status=status_for_failures(c3_failures),
            details={
                "failures": c3_failures,
                "observed": {
                    "recall_at_10": recall_lane.get("recall_at_10"),
                    "mean_match_count": recall_lane.get("mean_match_count"),
                    "mean_hierarchy_score_0_5": hierarchy_lane.get("mean_hierarchy_score_0_5"),
                    "bucket_mean_scores": bucket_scores,
                },
            },
        )
    )

    # C4 provenance completeness
    c4_threshold = next(c for c in threshold["checks"] if c["check_id"] == "C4_provenance_completeness")
    provenance_rows = model_b.get("rows", []) + multimodal.get("rows", [])
    provenance_non_empty = sum(1 for row in provenance_rows if str(row.get("provenance_ref", "")).strip())
    provenance_ratio = provenance_non_empty / len(provenance_rows) if provenance_rows else 0.0
    null_anchor_count = sum(1 for row in query_set if not str(row.get("anchor_node_id", "")).strip())

    c4_failures: list[str] = []
    if provenance_ratio < c4_threshold["thresholds"]["non_empty_provenance_ref_ratio_eq"]:
        c4_failures.append("provenance_ref_ratio")
    if null_anchor_count != c4_threshold["thresholds"]["null_anchor_query_count_eq"]:
        c4_failures.append("null_anchor_query_count")

    checks.append(
        CheckResult(
            check_id="C4_provenance_completeness",
            severity="hard_fail",
            status=status_for_failures(c4_failures),
            details={
                "failures": c4_failures,
                "observed": {
                    "provenance_rows": len(provenance_rows),
                    "provenance_non_empty": provenance_non_empty,
                    "provenance_ratio": round(provenance_ratio, 6),
                    "null_anchor_query_count": null_anchor_count,
                },
            },
        )
    )

    # C5 rollback trigger probe (warning)
    c5_threshold = next(c for c in threshold["checks"] if c["check_id"] == "C5_rollback_trigger_probe")
    unresolved_rate = (
        multimodal.get("fail_count", 0) / multimodal.get("row_count", 1)
        if multimodal.get("row_count", 0)
        else 0.0
    )
    unresolved_limit = c5_threshold["thresholds"]["unresolved_vl_rate_lte"]
    c5_status = "warn" if unresolved_rate > unresolved_limit else "pass"
    checks.append(
        CheckResult(
            check_id="C5_rollback_trigger_probe",
            severity="warn",
            status=c5_status,
            details={
                "observed": {
                    "unresolved_vl_rate": round(unresolved_rate, 6),
                    "fail_count": multimodal.get("fail_count", 0),
                    "row_count": multimodal.get("row_count", 0),
                },
                "threshold": unresolved_limit,
                "source_contract": c5_threshold.get("source_contract"),
            },
        )
    )

    hard_fail_any = any(c.severity == "hard_fail" and c.status == "fail" for c in checks)
    warn_any = any(c.status == "warn" for c in checks)
    if hard_fail_any:
        overall = "fail"
    elif warn_any:
        overall = "warn"
    else:
        overall = "pass"

    payload = {
        "generated_at": utc_now(),
        "task_id": "SWA-075",
        "overall_status": overall,
        "checks": [
            {
                "check_id": c.check_id,
                "severity": c.severity,
                "status": c.status,
                "details": c.details,
            }
            for c in checks
        ],
    }
    return payload


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# SWA-075 CI Check Report (latest)",
        "",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "| Check | Severity | Status |",
        "|---|---|---|",
    ]
    for check in report["checks"]:
        lines.append(f"| {check['check_id']} | {check['severity']} | {check['status']} |")

    lines.extend(["", "## Check Details"])
    for check in report["checks"]:
        lines.extend(
            [
                "",
                f"### {check['check_id']}",
                f"- Severity: `{check['severity']}`",
                f"- Status: `{check['status']}`",
                "- Details:",
                "",
                "```json",
                json.dumps(check["details"], indent=2),
                "```",
            ]
        )

    return "\n".join(lines)


def main() -> None:
    report = run_checks()
    write_json(REPORT_JSON, report)
    write_md(REPORT_MD, render_markdown(report))
    print(f"Wrote {REPORT_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_MD.relative_to(REPO_ROOT)}")
    print(f"overall_status={report['overall_status']}")


if __name__ == "__main__":
    main()
