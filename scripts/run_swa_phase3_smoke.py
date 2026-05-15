#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path
from typing import Any

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE3_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "nvidia-ingestion-pilot" / "phase3"
LIB_PATH = REPO_ROOT / "scripts" / "lib_nvidia_nim.py"


def load_lib() -> Any:
    spec = importlib.util.spec_from_file_location("lib_nvidia_nim", LIB_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load NVIDIA helper library from {LIB_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            rows.append(json.loads(raw))
    return rows


def embed_once(
    *,
    base_url: str,
    api_key: str,
    model: str,
    input_value: str,
    input_type: str | None = None,
    timeout_seconds: int = 120,
) -> tuple[bool, dict[str, Any], float]:
    payload: dict[str, Any] = {"model": model, "input": input_value}
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

    data: dict[str, Any]
    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text[:800]}

    success = response.status_code == 200 and isinstance(data.get("data"), list) and len(data["data"]) > 0
    if success:
        vec = data["data"][0].get("embedding", [])
        return True, {"status_code": response.status_code, "vector_dim": len(vec)}, elapsed_ms

    return (
        False,
        {
            "status_code": response.status_code,
            "error": data.get("error") or data.get("detail") or str(data)[:800],
        },
        elapsed_ms,
    )


def run_text_smoke(
    *,
    base_url: str,
    api_key: str,
    model: str,
    rows: list[dict[str, Any]],
    batch_size: int,
    offset: int,
    input_type: str | None,
) -> dict[str, Any]:
    picked = rows[offset : offset + batch_size]
    results: list[dict[str, Any]] = []

    for row in picked:
        ok, detail, elapsed_ms = embed_once(
            base_url=base_url,
            api_key=api_key,
            model=model,
            input_value=row.get("text", ""),
            input_type=input_type,
        )
        results.append(
            {
                "node_id": row.get("node_id"),
                "bucket_type": row.get("bucket_type"),
                "success": ok,
                "latency_ms": round(elapsed_ms, 2),
                **detail,
            }
        )

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    dims = [r.get("vector_dim", 0) for r in results if r["success"]]

    return {
        "model": model,
        "offset": offset,
        "batch_size": len(results),
        "success_count": success_count,
        "fail_count": fail_count,
        "vector_dim_set": sorted(set(dims)),
        "results": results,
    }


def run_vl_smoke(
    *,
    lib: Any,
    base_url: str,
    api_key: str,
    rows: list[dict[str, Any]],
    batch_size: int,
    offset: int,
    vision_model: str,
    embed_model: str,
    input_type: str,
) -> dict[str, Any]:
    picked = rows[offset : offset + batch_size]
    results: list[dict[str, Any]] = []

    for row in picked:
        image_path = Path(row["image_path"])
        rec: dict[str, Any] = {
            "node_id": row.get("node_id"),
            "bucket_type": row.get("bucket_type"),
            "image_path": str(image_path),
            "success": False,
        }

        if not image_path.exists():
            rec["error"] = "image_not_found"
            results.append(rec)
            continue

        if image_path.stat().st_size == 0:
            rec["error"] = "image_empty_0_bytes"
            results.append(rec)
            continue

        try:
            data_url = lib.image_to_data_url(image_path)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Describe this image for graph indexing in under 120 words. "
                                "Include key entities, relationships, and measurement cues."
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ]
            vision_response = lib.chat_completion(
                model=vision_model,
                messages=messages,
                temperature=0.1,
                max_tokens=220,
                timeout_seconds=120,
                max_attempts=1,
            )
            caption = lib.extract_text(vision_response).strip()
            caption = " ".join(caption.split())
            if not caption:
                rec["error"] = "empty_caption"
                results.append(rec)
                continue

            ok, detail, elapsed_ms = embed_once(
                base_url=base_url,
                api_key=api_key,
                model=embed_model,
                input_value=caption,
                input_type=input_type,
            )
            rec.update(
                {
                    "success": ok,
                    "caption_preview": caption[:200],
                    "caption_chars": len(caption),
                    "latency_ms": round(elapsed_ms, 2),
                    **detail,
                }
            )
        except Exception as exc:
            rec["error"] = f"{type(exc).__name__}: {exc}"

        results.append(rec)

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    dims = [r.get("vector_dim", 0) for r in results if r["success"]]

    return {
        "vision_model": vision_model,
        "embed_model": embed_model,
        "offset": offset,
        "batch_size": len(results),
        "success_count": success_count,
        "fail_count": fail_count,
        "vector_dim_set": sorted(set(dims)),
        "results": results,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_summary(path: Path, blocks: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# SWA Phase 3 Smoke Summary v1",
        "",
        "## Outcomes",
    ]
    for key, data in blocks.items():
        lines.extend(
            [
                f"- **{key}**",
                f"  - batch_size: `{data.get('batch_size', 0)}`",
                f"  - success_count: `{data.get('success_count', 0)}`",
                f"  - fail_count: `{data.get('fail_count', 0)}`",
                f"  - vector_dim_set: `{data.get('vector_dim_set', [])}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Notes",
            "- bge-m3 was attempted as requested and may fail depending on current NVIDIA runtime health.",
            "- VL lane uses vision captioning (`meta/llama-3.2-11b-vision-instruct`) then embeds caption text with `nvidia/llama-nemotron-embed-vl-1b-v2`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SWA Phase 3 smoke embedding batch")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--input-type", default="passage")
    parser.add_argument("--output-suffix", default="v1")
    parser.add_argument("--skip-bge", action="store_true")
    parser.add_argument("--skip-nv", action="store_true")
    parser.add_argument("--skip-vl", action="store_true")
    args = parser.parse_args()

    lib = load_lib()
    settings = lib.load_nvidia_settings()
    base_url = settings["base_url"]
    api_key = settings["api_key"]

    text_a = read_jsonl(PHASE3_DIR / "SWA-046_bge_m3_input_set_v1.jsonl")
    text_b = read_jsonl(PHASE3_DIR / "SWA-047_nv_embed_v1_input_set_v1.jsonl")
    vl_rows = read_jsonl(PHASE3_DIR / "SWA-048_vl_input_set_v1.jsonl")

    blocks: dict[str, dict[str, Any]] = {}

    if not args.skip_bge:
        bge_result = run_text_smoke(
            base_url=base_url,
            api_key=api_key,
            model="baai/bge-m3",
            rows=text_a,
            batch_size=args.batch_size,
            offset=args.offset,
            input_type=None,
        )
        blocks["SWA-049 bge-m3"] = bge_result
    if not args.skip_nv:
        nv_result = run_text_smoke(
            base_url=base_url,
            api_key=api_key,
            model="nvidia/nv-embed-v1",
            rows=text_b,
            batch_size=args.batch_size,
            offset=args.offset,
            input_type=None,
        )
        blocks["SWA-050 nv-embed-v1"] = nv_result
    if not args.skip_vl:
        vl_result = run_vl_smoke(
            lib=lib,
            base_url=base_url,
            api_key=api_key,
            rows=vl_rows,
            batch_size=args.batch_size,
            offset=args.offset,
            vision_model="meta/llama-3.2-11b-vision-instruct",
            embed_model="nvidia/llama-nemotron-embed-vl-1b-v2",
            input_type=args.input_type,
        )
        blocks["SWA-051 vl-caption-embed"] = vl_result

    suffix = args.output_suffix
    if "SWA-049 bge-m3" in blocks:
        write_json(PHASE3_DIR / f"SWA-049_bge_m3_smoke_results_{suffix}.json", blocks["SWA-049 bge-m3"])
    if "SWA-050 nv-embed-v1" in blocks:
        write_json(PHASE3_DIR / f"SWA-050_nv_embed_v1_smoke_results_{suffix}.json", blocks["SWA-050 nv-embed-v1"])
    if "SWA-051 vl-caption-embed" in blocks:
        write_json(PHASE3_DIR / f"SWA-051_vl_smoke_results_{suffix}.json", blocks["SWA-051 vl-caption-embed"])
    write_summary(
        PHASE3_DIR / f"SWA-049_051_smoke_summary_{suffix}.md",
        blocks,
    )

    print("Smoke run complete")
    compact: dict[str, dict[str, int]] = {}
    if "SWA-049 bge-m3" in blocks:
        compact["SWA-049"] = {
            "success": blocks["SWA-049 bge-m3"]["success_count"],
            "fail": blocks["SWA-049 bge-m3"]["fail_count"],
        }
    if "SWA-050 nv-embed-v1" in blocks:
        compact["SWA-050"] = {
            "success": blocks["SWA-050 nv-embed-v1"]["success_count"],
            "fail": blocks["SWA-050 nv-embed-v1"]["fail_count"],
        }
    if "SWA-051 vl-caption-embed" in blocks:
        compact["SWA-051"] = {
            "success": blocks["SWA-051 vl-caption-embed"]["success_count"],
            "fail": blocks["SWA-051 vl-caption-embed"]["fail_count"],
        }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
