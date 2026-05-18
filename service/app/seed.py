from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .db import get_db, load_json
from .models import SeedStatus


SEED_DIR = Path("/data/pilot/phase3")


def seed_from_pilot() -> SeedStatus:
    status = SeedStatus(loaded_nodes=0, loaded_edges=0, loaded_vectors=0, loaded_vl_vectors=0, loaded_provenance=0)

    model_b_index_path = SEED_DIR / "SWA-053_modelB_retrieval_index_v1.json"
    model_b_vectors_path = SEED_DIR / "SWA-053_modelB_vectors_v1.npy"
    multimodal_index_path = SEED_DIR / "SWA-054_multimodal_index_v1.json"
    multimodal_vectors_path = SEED_DIR / "SWA-054_multimodal_vectors_v1.npy"
    recall_path = SEED_DIR / "SWA-058_recall_match_metrics_v1.json"

    if not model_b_index_path.exists():
        status.errors.append(f"Missing Model B index: {model_b_index_path}")
        return status

    index_data = load_json(model_b_index_path)
    vectors = np.load(str(model_b_vectors_path)) if model_b_vectors_path.exists() else None

    rows = index_data.get("rows", [])
    provenance_set: set[str] = set()

    with get_db() as conn:
        for i, row in enumerate(rows):
            emb = vectors[i].tolist() if vectors is not None and i < len(vectors) else None
            prov_ref = row.get("provenance_ref", "")
            provenance_set.add(prov_ref)

            conn.execute(
                """
                INSERT INTO lore_node (node_id, bucket_type, source_path, provenance_ref,
                                       text_preview, quality_flags, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (node_id) DO UPDATE SET
                    bucket_type = EXCLUDED.bucket_type,
                    source_path = EXCLUDED.source_path,
                    provenance_ref = EXCLUDED.provenance_ref,
                    text_preview = EXCLUDED.text_preview,
                    quality_flags = EXCLUDED.quality_flags,
                    embedding = EXCLUDED.embedding,
                    updated_at = NOW()
                """,
                (
                    row["node_id"],
                    row.get("bucket_type", ""),
                    row.get("source_path", ""),
                    prov_ref,
                    row.get("text_preview", ""),
                    json.dumps(row.get("quality_flags", {})),
                    emb,
                ),
            )
            status.loaded_nodes += 1
            if emb is not None:
                status.loaded_vectors += 1

    if multimodal_index_path.exists():
        mm_data = load_json(multimodal_index_path)
        mm_vectors = np.load(str(multimodal_vectors_path)) if multimodal_vectors_path.exists() else None

        mm_rows = mm_data.get("rows", [])
        with get_db() as conn:
            for i, row in enumerate(mm_rows):
                vl_emb = mm_vectors[i].tolist() if mm_vectors is not None and i < len(mm_vectors) else None
                if vl_emb is not None:
                    conn.execute(
                        "UPDATE lore_node SET vl_embedding = %s WHERE node_id = %s",
                        (vl_emb, row["node_id"]),
                    )
                    status.loaded_vl_vectors += 1

    manifest_path = SEED_DIR.parent / "sample_manifest.csv"
    if manifest_path.exists():
        import csv

        with manifest_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nid = row.get("node_id", "")
                if nid:
                    provenance_set.add(f"manifest:{nid}")

    for prov_id in provenance_set:
        if not prov_id:
            continue
        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO provenance_chain (provenance_id, source_artifact, extraction_method)
                VALUES (%s, %s, %s)
                ON CONFLICT (provenance_id) DO NOTHING
                """,
                (prov_id, "pilot_seed", "automated"),
            )
            status.loaded_provenance += 1

    return status