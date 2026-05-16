#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np
import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "nvidia-ingestion-pilot"
PHASE2_DIR = PILOT_DIR / "phase2"
PHASE3_DIR = PILOT_DIR / "phase3"
LIB_PATH = REPO_ROOT / "scripts" / "lib_nvidia_nim.py"

MODEL_A = "baai/bge-m3"
MODEL_B = "nvidia/nv-embed-v1"
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"
VL_EMBED_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2"


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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            rows.append(json.loads(raw))
    return rows


def load_lib() -> Any:
    spec = importlib.util.spec_from_file_location("lib_nvidia_nim", LIB_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load NVIDIA helper from {LIB_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def node_sort_key(node_id: str) -> int:
    try:
        return int(node_id.split("-")[-1])
    except Exception:
        return 0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with (PILOT_DIR / "sample_manifest.csv").open("r", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            out[row["node_id"]] = row
    return out


def load_neighbors() -> dict[str, list[str]]:
    neighbors = {}
    rows = read_json(PHASE2_DIR / "SWA-039_expected_neighbors_seed_v1.json")
    for row in rows:
        neighbors[row["node_id"]] = row.get("expected_neighbors", [])
    return neighbors


def load_parents() -> dict[str, str]:
    parents = {}
    rows = read_json(PHASE2_DIR / "SWA-040_expected_parent_seed_v1.json")
    for row in rows:
        parents[row["node_id"]] = row.get("expected_parent", "")
    return parents


def clean_stem(path_text: str) -> str:
    stem = Path(path_text).stem
    stem = stem.replace("_", " ").replace("-", " ")
    return " ".join(stem.split())


def derive_query_text(manifest_row: dict[str, str], text_payload: str, bucket: str) -> str:
    source_type = manifest_row.get("source_type", "")
    if source_type == "image":
        stem = clean_stem(manifest_row.get("source_path", ""))
        return f"{bucket} reference for {stem}"
    words = text_payload.split()
    snippet = " ".join(words[:22])
    if snippet:
        return snippet
    stem = clean_stem(manifest_row.get("source_path", ""))
    return f"{bucket} document about {stem}"


def build_query_set(
    *,
    manifest_by_node: dict[str, dict[str, str]],
    text_rows_by_node: dict[str, dict[str, Any]],
    neighbors: dict[str, list[str]],
    parents: dict[str, str],
) -> list[dict[str, Any]]:
    template_rows: list[dict[str, str]] = []
    with (PILOT_DIR / "pilot_query_eval_template.csv").open("r", encoding="utf-8") as handle:
        template_rows = list(csv.DictReader(handle))

    bucket_nodes: dict[str, list[str]] = {
        "bio_field_charts": [],
        "interpretation_maps": [],
        "cross_integration_histories": [],
    }
    for node_id, row in manifest_by_node.items():
        bucket = row.get("bucket_type", "")
        if bucket in bucket_nodes:
            bucket_nodes[bucket].append(node_id)
    for bucket in bucket_nodes:
        bucket_nodes[bucket] = sorted(bucket_nodes[bucket], key=node_sort_key)

    cursor = {k: 0 for k in bucket_nodes}
    queries: list[dict[str, Any]] = []
    for row in template_rows:
        bucket = row["bucket_focus"]
        nodes = bucket_nodes[bucket]
        idx = cursor[bucket]
        anchor = nodes[idx % len(nodes)]
        cursor[bucket] += 1

        manifest = manifest_by_node[anchor]
        text_payload = text_rows_by_node.get(anchor, {}).get("text", "")
        query_text = derive_query_text(manifest, text_payload, bucket)

        expected = [anchor]
        expected.extend(neighbors.get(anchor, [])[:2])
        dedup_expected: list[str] = []
        for item in expected:
            if item not in dedup_expected:
                dedup_expected.append(item)

        queries.append(
            {
                "query_id": row["query_id"],
                "bucket_focus": bucket,
                "language": manifest.get("language_hint", "en"),
                "query_text": query_text,
                "anchor_node_id": anchor,
                "expected_node_ids": dedup_expected,
                "expected_parent": parents.get(anchor, ""),
            }
        )

    out_json = PHASE3_DIR / "SWA-055_057_query_set_v1.json"
    write_json(out_json, queries)

    out_csv = PHASE3_DIR / "SWA-055_057_query_set_v1.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "query_id",
                "bucket_focus",
                "language",
                "query_text",
                "anchor_node_id",
                "expected_node_ids",
                "expected_parent",
            ]
        )
        for q in queries:
            writer.writerow(
                [
                    q["query_id"],
                    q["bucket_focus"],
                    q["language"],
                    q["query_text"],
                    q["anchor_node_id"],
                    "|".join(q["expected_node_ids"]),
                    q["expected_parent"],
                ]
            )

    return queries


def embed_once(
    *,
    base_url: str,
    api_key: str,
    model: str,
    input_text: str,
    input_type: str | None = None,
    timeout_seconds: int = 120,
) -> tuple[bool, dict[str, Any], float]:
    payload: dict[str, Any] = {"model": model, "input": input_text}
    if input_type:
        payload["input_type"] = input_type

    started = time.perf_counter()
    response = requests.post(
        f"{base_url}/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout_seconds,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000.0

    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text[:800]}

    if response.status_code == 200 and isinstance(data.get("data"), list) and data["data"]:
        vec = data["data"][0].get("embedding", [])
        return True, {"status_code": response.status_code, "vector": vec}, elapsed_ms

    err = data.get("error")
    if isinstance(err, dict):
        err_msg = err.get("message") or str(err)
    else:
        err_msg = err or data.get("detail") or str(data)[:800]
    return False, {"status_code": response.status_code, "error": str(err_msg)}, elapsed_ms


def embed_with_retry(
    *,
    base_url: str,
    api_key: str,
    model: str,
    input_text: str,
    input_type: str | None = None,
    max_attempts: int = 3,
    retry_backoff_seconds: int = 4,
) -> tuple[bool, dict[str, Any]]:
    retryable_status = {408, 429, 500, 502, 503, 504}
    last: dict[str, Any] = {"status_code": None, "error": "unknown"}
    last_elapsed = 0.0

    for attempt in range(1, max_attempts + 1):
        try:
            ok, detail, elapsed_ms = embed_once(
                base_url=base_url,
                api_key=api_key,
                model=model,
                input_text=input_text,
                input_type=input_type,
            )
            last_elapsed = elapsed_ms
            if ok:
                return True, {
                    "status_code": detail["status_code"],
                    "vector": detail["vector"],
                    "latency_ms": round(elapsed_ms, 2),
                    "attempt": attempt,
                }

            status_code = detail.get("status_code")
            last = {**detail, "attempt": attempt, "latency_ms": round(elapsed_ms, 2)}
            if status_code in retryable_status and attempt < max_attempts:
                time.sleep(retry_backoff_seconds * attempt)
                continue
            return False, last
        except requests.RequestException as exc:
            last = {
                "status_code": None,
                "error": f"RequestException: {exc}",
                "attempt": attempt,
                "latency_ms": round(last_elapsed, 2),
            }
            if attempt < max_attempts:
                time.sleep(retry_backoff_seconds * attempt)
                continue
            return False, last

    return False, last


def build_model_a_index() -> dict[str, Any]:
    source = read_json(PHASE3_DIR / "SWA-049_bge_m3_smoke_results_full_text_v1.json")
    payload = {
        "generated_at": utc_now(),
        "task_id": "SWA-052",
        "model_lane": MODEL_A,
        "status": "blocked",
        "row_count": source.get("batch_size", 0),
        "success_count": source.get("success_count", 0),
        "fail_count": source.get("fail_count", 0),
        "vector_dim": None,
        "vector_file": None,
        "top_error": (
            source.get("results", [{}])[0].get("error")
            if source.get("results")
            else "No results available"
        ),
        "reason": "No successful model A vectors available for index build.",
        "source_inputs": [
            "phase3/SWA-046_bge_m3_input_set_v1.jsonl",
            "phase3/SWA-049_bge_m3_smoke_results_full_text_v1.json",
        ],
    }
    out = PHASE3_DIR / "SWA-052_modelA_retrieval_index_v1.json"
    write_json(out, payload)
    return payload


def build_dense_index(
    *,
    task_id: str,
    model_name: str,
    input_rows: list[dict[str, Any]],
    base_url: str,
    api_key: str,
    input_type: str | None,
    vector_file_name: str,
    meta_file_name: str,
) -> dict[str, Any]:
    vectors: list[list[float]] = []
    rows_out: list[dict[str, Any]] = []

    for row in input_rows:
        ok, detail = embed_with_retry(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            input_text=row.get("text", ""),
            input_type=input_type,
        )

        rec = {
            "node_id": row.get("node_id"),
            "bucket_type": row.get("bucket_type"),
            "provenance_ref": row.get("provenance_ref"),
            "success": ok,
            "status_code": detail.get("status_code"),
            "latency_ms": detail.get("latency_ms"),
            "attempt": detail.get("attempt"),
        }

        if ok:
            rec["vector_index"] = len(vectors)
            rec["vector_dim"] = len(detail["vector"])
            rec["text_preview"] = row.get("text", "")[:220]
            vectors.append(detail["vector"])
        else:
            rec["error"] = detail.get("error")

        rows_out.append(rec)

    if vectors:
        mat = np.array(vectors, dtype=np.float32)
        vector_dim = int(mat.shape[1])
    else:
        mat = np.zeros((0, 0), dtype=np.float32)
        vector_dim = 0

    vector_path = PHASE3_DIR / vector_file_name
    np.save(vector_path, mat)

    meta = {
        "generated_at": utc_now(),
        "task_id": task_id,
        "model_lane": model_name,
        "row_count": len(input_rows),
        "success_count": int(sum(1 for r in rows_out if r["success"])),
        "fail_count": int(sum(1 for r in rows_out if not r["success"])),
        "vector_dim": vector_dim,
        "vector_file": f"phase3/{vector_file_name}",
        "source_inputs": [
            "phase3/SWA-047_nv_embed_v1_input_set_v1.jsonl",
        ],
        "rows": rows_out,
    }
    write_json(PHASE3_DIR / meta_file_name, meta)
    return meta


def build_multimodal_index(
    *,
    lib: Any,
    input_rows: list[dict[str, Any]],
    base_url: str,
    api_key: str,
) -> dict[str, Any]:
    vectors: list[list[float]] = []
    rows_out: list[dict[str, Any]] = []

    prompt = (
        "Describe this image for retrieval indexing in under 120 words. "
        "Include key entities, relationships, and domain cues."
    )

    for row in input_rows:
        image_path = Path(row.get("image_path", ""))
        rec = {
            "node_id": row.get("node_id"),
            "bucket_type": row.get("bucket_type"),
            "provenance_ref": row.get("provenance_ref"),
            "image_path": str(image_path),
            "success": False,
        }

        if not image_path.exists():
            rec["error"] = "image_not_found"
            rows_out.append(rec)
            continue
        if image_path.stat().st_size == 0:
            rec["error"] = "image_empty_0_bytes"
            rows_out.append(rec)
            continue

        try:
            data_url = lib.image_to_data_url(image_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ]
            vision_raw = lib.chat_completion(
                model=VISION_MODEL,
                messages=messages,
                temperature=0.1,
                max_tokens=240,
                timeout_seconds=120,
                max_attempts=2,
            )
            caption = " ".join(lib.extract_text(vision_raw).split())
            if not caption:
                rec["error"] = "empty_caption"
                rows_out.append(rec)
                continue

            ok, detail = embed_with_retry(
                base_url=base_url,
                api_key=api_key,
                model=VL_EMBED_MODEL,
                input_text=caption,
                input_type="passage",
            )
            rec["status_code"] = detail.get("status_code")
            rec["latency_ms"] = detail.get("latency_ms")
            rec["attempt"] = detail.get("attempt")
            rec["caption_preview"] = caption[:220]
            rec["caption_chars"] = len(caption)

            if ok:
                rec["success"] = True
                rec["vector_index"] = len(vectors)
                rec["vector_dim"] = len(detail["vector"])
                vectors.append(detail["vector"])
            else:
                rec["error"] = detail.get("error")
        except Exception as exc:
            rec["error"] = f"{type(exc).__name__}: {exc}"

        rows_out.append(rec)

    if vectors:
        mat = np.array(vectors, dtype=np.float32)
        vector_dim = int(mat.shape[1])
    else:
        mat = np.zeros((0, 0), dtype=np.float32)
        vector_dim = 0

    vector_path = PHASE3_DIR / "SWA-054_multimodal_vectors_v1.npy"
    np.save(vector_path, mat)

    meta = {
        "generated_at": utc_now(),
        "task_id": "SWA-054",
        "vision_model": VISION_MODEL,
        "embedding_model": VL_EMBED_MODEL,
        "row_count": len(input_rows),
        "success_count": int(sum(1 for r in rows_out if r["success"])),
        "fail_count": int(sum(1 for r in rows_out if not r["success"])),
        "vector_dim": vector_dim,
        "vector_file": "phase3/SWA-054_multimodal_vectors_v1.npy",
        "source_inputs": [
            "phase3/SWA-048_vl_input_set_v1.jsonl",
        ],
        "rows": rows_out,
    }
    write_json(PHASE3_DIR / "SWA-054_multimodal_index_v1.json", meta)
    return meta


def cosine_topk(
    matrix: np.ndarray,
    query_vec: np.ndarray,
    k: int,
) -> tuple[np.ndarray, np.ndarray]:
    if matrix.size == 0:
        return np.array([], dtype=np.int64), np.array([], dtype=np.float32)

    row_norms = np.linalg.norm(matrix, axis=1)
    row_norms[row_norms == 0.0] = 1.0
    q_norm = float(np.linalg.norm(query_vec))
    if q_norm == 0.0:
        q_norm = 1.0

    sims = (matrix @ query_vec) / (row_norms * q_norm)
    k = min(k, sims.shape[0])
    idx = np.argpartition(-sims, kth=k - 1)[:k]
    idx_sorted = idx[np.argsort(-sims[idx])]
    return idx_sorted, sims[idx_sorted]


def execute_query_set(
    *,
    task_id: str,
    query_set: list[dict[str, Any]],
    index_meta: dict[str, Any],
    vector_file_path: Path | None,
    query_model: str,
    query_input_type: str | None,
    base_url: str,
    api_key: str,
    result_file_name: str,
) -> dict[str, Any]:
    if index_meta.get("status") == "blocked":
        rows = []
        for q in query_set:
            rows.append(
                {
                    "query_id": q["query_id"],
                    "bucket_focus": q["bucket_focus"],
                    "anchor_node_id": q["anchor_node_id"],
                    "expected_node_ids": q["expected_node_ids"],
                    "top10": [],
                    "hit_at_10": 0,
                    "match_count": 0,
                    "status": "index_blocked",
                }
            )
        out = {
            "generated_at": utc_now(),
            "task_id": task_id,
            "query_model": query_model,
            "index_model": index_meta.get("model_lane"),
            "row_count": len(query_set),
            "results": rows,
        }
        write_json(PHASE3_DIR / result_file_name, out)
        return out

    if vector_file_path is None or not vector_file_path.exists():
        raise RuntimeError(f"Missing vector file for {task_id}: {vector_file_path}")

    matrix = np.load(vector_file_path)

    row_by_index: dict[int, dict[str, Any]] = {}
    for row in index_meta.get("rows", []):
        if row.get("success"):
            row_by_index[int(row["vector_index"])] = row

    results: list[dict[str, Any]] = []
    for q in query_set:
        ok, detail = embed_with_retry(
            base_url=base_url,
            api_key=api_key,
            model=query_model,
            input_text=q["query_text"],
            input_type=query_input_type,
            max_attempts=3,
        )

        record = {
            "query_id": q["query_id"],
            "bucket_focus": q["bucket_focus"],
            "anchor_node_id": q["anchor_node_id"],
            "expected_node_ids": q["expected_node_ids"],
            "query_latency_ms": detail.get("latency_ms"),
            "top10": [],
            "hit_at_10": 0,
            "match_count": 0,
            "status": "ok" if ok else "query_embed_failed",
        }

        if ok:
            qvec = np.array(detail["vector"], dtype=np.float32)
            idx, sims = cosine_topk(matrix, qvec, 10)
            top_rows = []
            top_ids: list[str] = []
            for i, s in zip(idx.tolist(), sims.tolist()):
                meta = row_by_index.get(i)
                if not meta:
                    continue
                node_id = meta["node_id"]
                top_ids.append(node_id)
                top_rows.append(
                    {
                        "node_id": node_id,
                        "bucket_type": meta.get("bucket_type"),
                        "score": round(float(s), 6),
                        "provenance_ref": meta.get("provenance_ref"),
                    }
                )

            expected = set(q["expected_node_ids"])
            matched = [node for node in top_ids if node in expected]
            record["top10"] = top_rows
            record["hit_at_10"] = 1 if matched else 0
            record["match_count"] = len(matched)
        else:
            record["error"] = detail.get("error")

        results.append(record)

    out = {
        "generated_at": utc_now(),
        "task_id": task_id,
        "query_model": query_model,
        "index_model": index_meta.get("model_lane") or index_meta.get("embedding_model"),
        "row_count": len(query_set),
        "results": results,
    }
    write_json(PHASE3_DIR / result_file_name, out)
    return out


def summarize_recall_metrics(*, lane_name: str, query_results: dict[str, Any]) -> dict[str, Any]:
    rows = query_results["results"]
    total = len(rows)
    hits = sum(int(r.get("hit_at_10", 0)) for r in rows)
    mean_match = mean([float(r.get("match_count", 0)) for r in rows]) if rows else 0.0

    by_bucket: dict[str, dict[str, Any]] = {}
    for r in rows:
        b = r["bucket_focus"]
        if b not in by_bucket:
            by_bucket[b] = {"query_count": 0, "hit_count": 0, "match_total": 0.0}
        by_bucket[b]["query_count"] += 1
        by_bucket[b]["hit_count"] += int(r.get("hit_at_10", 0))
        by_bucket[b]["match_total"] += float(r.get("match_count", 0))

    for bucket, item in by_bucket.items():
        qcount = item["query_count"]
        item["recall_at_10"] = round((item["hit_count"] / qcount) if qcount else 0.0, 4)
        item["mean_match_count"] = round((item["match_total"] / qcount) if qcount else 0.0, 4)
        del item["match_total"]

    return {
        "lane": lane_name,
        "query_count": total,
        "hit_count": hits,
        "recall_at_10": round((hits / total) if total else 0.0, 4),
        "mean_match_count": round(mean_match, 4),
        "by_bucket": by_bucket,
    }


def summarize_hierarchy_metrics(
    *,
    lane_name: str,
    query_results: dict[str, Any],
    manifest_by_node: dict[str, dict[str, str]],
    neighbors: dict[str, list[str]],
    parents: dict[str, str],
) -> dict[str, Any]:
    rows = query_results["results"]
    per_query: list[dict[str, Any]] = []

    for row in rows:
        top_nodes = [item["node_id"] for item in row.get("top10", [])]
        if not top_nodes:
            per_query.append(
                {
                    "query_id": row["query_id"],
                    "bucket_focus": row["bucket_focus"],
                    "hierarchy_score_0_5": 0.0,
                    "bucket_alignment": 0.0,
                    "neighbor_hit_ratio": 0.0,
                    "parent_hit_ratio": 0.0,
                }
            )
            continue

        anchor = row["anchor_node_id"]
        expected_neighbors = neighbors.get(anchor, [])
        expected_parent = parents.get(anchor, "")
        bucket = row["bucket_focus"]

        same_bucket = 0
        for node_id in top_nodes:
            if manifest_by_node.get(node_id, {}).get("bucket_type") == bucket:
                same_bucket += 1
        bucket_alignment = same_bucket / len(top_nodes)

        neighbor_hits = sum(1 for node_id in top_nodes if node_id in expected_neighbors)
        neighbor_hit_ratio = neighbor_hits / (len(expected_neighbors) if expected_neighbors else 1)

        parent_hits = 0
        for node_id in top_nodes:
            if parents.get(node_id, "") == expected_parent and expected_parent:
                parent_hits += 1
        parent_hit_ratio = parent_hits / len(top_nodes)

        score = 5.0 * (
            (0.5 * bucket_alignment)
            + (0.3 * min(neighbor_hit_ratio, 1.0))
            + (0.2 * min(parent_hit_ratio, 1.0))
        )

        per_query.append(
            {
                "query_id": row["query_id"],
                "bucket_focus": bucket,
                "hierarchy_score_0_5": round(score, 4),
                "bucket_alignment": round(bucket_alignment, 4),
                "neighbor_hit_ratio": round(min(neighbor_hit_ratio, 1.0), 4),
                "parent_hit_ratio": round(min(parent_hit_ratio, 1.0), 4),
            }
        )

    mean_score = mean([x["hierarchy_score_0_5"] for x in per_query]) if per_query else 0.0

    by_bucket: dict[str, list[float]] = {}
    for row in per_query:
        by_bucket.setdefault(row["bucket_focus"], []).append(row["hierarchy_score_0_5"])
    bucket_scores = {k: round(mean(v), 4) for k, v in by_bucket.items()}

    return {
        "lane": lane_name,
        "query_count": len(per_query),
        "mean_hierarchy_score_0_5": round(mean_score, 4),
        "bucket_mean_scores": bucket_scores,
        "per_query": per_query,
    }


def main() -> None:
    started_at = utc_now()
    PHASE3_DIR.mkdir(parents=True, exist_ok=True)

    lib = load_lib()
    settings = lib.load_nvidia_settings()
    base_url = settings["base_url"]
    api_key = settings["api_key"]

    manifest_by_node = load_manifest()
    neighbors = load_neighbors()
    parents = load_parents()

    text_rows = read_jsonl(PHASE3_DIR / "SWA-047_nv_embed_v1_input_set_v1.jsonl")
    text_rows_by_node = {row["node_id"]: row for row in text_rows}
    vl_rows = read_jsonl(PHASE3_DIR / "SWA-048_vl_input_set_v1.jsonl")

    queries = build_query_set(
        manifest_by_node=manifest_by_node,
        text_rows_by_node=text_rows_by_node,
        neighbors=neighbors,
        parents=parents,
    )

    model_a_index = build_model_a_index()

    model_b_index = build_dense_index(
        task_id="SWA-053",
        model_name=MODEL_B,
        input_rows=text_rows,
        base_url=base_url,
        api_key=api_key,
        input_type=None,
        vector_file_name="SWA-053_modelB_vectors_v1.npy",
        meta_file_name="SWA-053_modelB_retrieval_index_v1.json",
    )

    multimodal_index = build_multimodal_index(
        lib=lib,
        input_rows=vl_rows,
        base_url=base_url,
        api_key=api_key,
    )

    query_a = execute_query_set(
        task_id="SWA-055",
        query_set=queries,
        index_meta=model_a_index,
        vector_file_path=None,
        query_model=MODEL_A,
        query_input_type=None,
        base_url=base_url,
        api_key=api_key,
        result_file_name="SWA-055_modelA_query_results_v1.json",
    )

    query_b = execute_query_set(
        task_id="SWA-056",
        query_set=queries,
        index_meta=model_b_index,
        vector_file_path=PHASE3_DIR / "SWA-053_modelB_vectors_v1.npy",
        query_model=MODEL_B,
        query_input_type=None,
        base_url=base_url,
        api_key=api_key,
        result_file_name="SWA-056_modelB_query_results_v1.json",
    )

    query_vl = execute_query_set(
        task_id="SWA-057",
        query_set=queries,
        index_meta=multimodal_index,
        vector_file_path=PHASE3_DIR / "SWA-054_multimodal_vectors_v1.npy",
        query_model=VL_EMBED_MODEL,
        query_input_type="passage",
        base_url=base_url,
        api_key=api_key,
        result_file_name="SWA-057_multimodal_query_results_v1.json",
    )

    recall_metrics = {
        "generated_at": utc_now(),
        "task_id": "SWA-058",
        "lanes": [
            summarize_recall_metrics(lane_name="model_a", query_results=query_a),
            summarize_recall_metrics(lane_name="model_b", query_results=query_b),
            summarize_recall_metrics(lane_name="multimodal", query_results=query_vl),
        ],
    }
    write_json(PHASE3_DIR / "SWA-058_recall_match_metrics_v1.json", recall_metrics)

    recall_md_lines = [
        "# SWA-058 Recall and Match Metrics v1",
        "",
    ]
    for lane in recall_metrics["lanes"]:
        recall_md_lines.extend(
            [
                f"## {lane['lane']}",
                f"- query_count: `{lane['query_count']}`",
                f"- recall_at_10: `{lane['recall_at_10']}`",
                f"- mean_match_count: `{lane['mean_match_count']}`",
                "",
            ]
        )
    write_md(PHASE3_DIR / "SWA-058_recall_match_metrics_v1.md", "\n".join(recall_md_lines))

    hierarchy_metrics = {
        "generated_at": utc_now(),
        "task_id": "SWA-059",
        "lanes": [
            summarize_hierarchy_metrics(
                lane_name="model_a",
                query_results=query_a,
                manifest_by_node=manifest_by_node,
                neighbors=neighbors,
                parents=parents,
            ),
            summarize_hierarchy_metrics(
                lane_name="model_b",
                query_results=query_b,
                manifest_by_node=manifest_by_node,
                neighbors=neighbors,
                parents=parents,
            ),
            summarize_hierarchy_metrics(
                lane_name="multimodal",
                query_results=query_vl,
                manifest_by_node=manifest_by_node,
                neighbors=neighbors,
                parents=parents,
            ),
        ],
    }
    write_json(PHASE3_DIR / "SWA-059_hierarchy_coherence_metrics_v1.json", hierarchy_metrics)

    hierarchy_md_lines = [
        "# SWA-059 Hierarchy Coherence Metrics v1",
        "",
    ]
    for lane in hierarchy_metrics["lanes"]:
        hierarchy_md_lines.extend(
            [
                f"## {lane['lane']}",
                f"- query_count: `{lane['query_count']}`",
                f"- mean_hierarchy_score_0_5: `{lane['mean_hierarchy_score_0_5']}`",
                f"- bucket_mean_scores: `{lane['bucket_mean_scores']}`",
                "",
            ]
        )
    write_md(PHASE3_DIR / "SWA-059_hierarchy_coherence_metrics_v1.md", "\n".join(hierarchy_md_lines))

    artifacts = [
        "phase3/SWA-052_modelA_retrieval_index_v1.json",
        "phase3/SWA-053_modelB_retrieval_index_v1.json",
        "phase3/SWA-053_modelB_vectors_v1.npy",
        "phase3/SWA-054_multimodal_index_v1.json",
        "phase3/SWA-054_multimodal_vectors_v1.npy",
        "phase3/SWA-055_057_query_set_v1.json",
        "phase3/SWA-055_057_query_set_v1.csv",
        "phase3/SWA-055_modelA_query_results_v1.json",
        "phase3/SWA-056_modelB_query_results_v1.json",
        "phase3/SWA-057_multimodal_query_results_v1.json",
        "phase3/SWA-058_recall_match_metrics_v1.json",
        "phase3/SWA-058_recall_match_metrics_v1.md",
        "phase3/SWA-059_hierarchy_coherence_metrics_v1.json",
        "phase3/SWA-059_hierarchy_coherence_metrics_v1.md",
    ]

    checksums = []
    for rel in artifacts:
        abs_path = PILOT_DIR / rel.replace("phase3/", "phase3/")
        if not abs_path.exists():
            raise RuntimeError(f"Expected artifact missing for checksum: {rel}")
        checksums.append({"artifact": rel, "sha256": sha256_file(abs_path), "bytes": abs_path.stat().st_size})
    write_json(PHASE3_DIR / "SWA-052_059_artifact_checksums_v1.json", checksums)

    run_log = {
        "task_group": "SWA-052..SWA-059",
        "started_at": started_at,
        "finished_at": utc_now(),
        "artifacts": artifacts + ["phase3/SWA-052_059_artifact_checksums_v1.json"],
        "model_a_index_status": model_a_index.get("status"),
        "model_b_index_success": model_b_index.get("success_count"),
        "multimodal_index_success": multimodal_index.get("success_count"),
    }
    write_json(PHASE3_DIR / "SWA-052_059_run_log_v1.json", run_log)

    print("SWA-052..SWA-059 execution complete")
    print(
        json.dumps(
            {
                "SWA-053_success": model_b_index.get("success_count"),
                "SWA-054_success": multimodal_index.get("success_count"),
                "SWA-058_lanes": [lane["lane"] for lane in recall_metrics["lanes"]],
                "SWA-059_lanes": [lane["lane"] for lane in hierarchy_metrics["lanes"]],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
