from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .config import settings
from .db import get_db, get_db_readonly
from .models import (
    HealthResponse,
    LoreNode,
    LoreEdge,
    BiorhythmAffinity,
    QueryRequest,
    QueryResult,
    ResonanceRequest,
    ResonanceResult,
    SeedStatus,
)
from .seed import seed_from_pilot
from .affinity_mappings import BUCKET_AFFINITIES, ENNEAGRAM_HORMONE_MAP, KOSHA_DESCRIPTION
from .lore_entries import INITIAL_LORE_ENTRIES
from .embeddings import embed_text

app = FastAPI(
    title="Somatic Canticles Lore Service",
    version="0.1.0",
    description="Embedding + provenance-bound relation graph retrieval for non-editorial world-building knowledge. Backend-neutral adapter with Postgres+pgvector default.",
)


@app.get("/health", response_model=HealthResponse)
async def health():
    try:
        conn = get_db_readonly()
        node_count = conn.execute("SELECT COUNT(*) FROM lore_node").fetchone()[0]
        edge_count = conn.execute("SELECT COUNT(*) FROM lore_edge").fetchone()[0]
        conn.close()
        return HealthResponse(status="ok", db_connected=True, node_count=node_count, edge_count=edge_count)
    except Exception:
        return HealthResponse(status="degraded", db_connected=False, node_count=0, edge_count=0)


@app.post("/seed", response_model=SeedStatus)
async def seed_database():
    result = seed_from_pilot()
    return result


@app.post("/query", response_model=list[QueryResult])
async def query_lore(req: QueryRequest):
    if not req.query_text.strip():
        raise HTTPException(status_code=400, detail="query_text must not be empty")

    try:
        query_vectors = await embed_text([req.query_text])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Embedding failed: {exc}")

    query_vec = query_vectors[0]
    bucket_filter_clause = ""
    params: list = [query_vec, req.top_k]

    if req.bucket_filter:
        placeholders = ",".join(["%s"] * len(req.bucket_filter))
        bucket_filter_clause = f"AND bucket_type IN ({placeholders})"
        params = [query_vec] + req.bucket_filter + [req.top_k]

    conn = get_db_readonly()
    try:
        rows = conn.execute(
            f"""
            SELECT node_id, bucket_type, provenance_ref, text_preview, summary,
                   1 - (embedding <=> %s) AS similarity
            FROM lore_node
            WHERE embedding IS NOT NULL {bucket_filter_clause}
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            params,
        ).fetchall()
    finally:
        conn.close()

    results: list[QueryResult] = []
    for row in rows:
        edges = None
        if req.include_edges:
            edge_conn = get_db_readonly()
            try:
                edge_rows = edge_conn.execute(
                    "SELECT source_node_id, target_node_id, relation_type, confidence FROM lore_edge WHERE source_node_id = %s OR target_node_id = %s",
                    (row[0], row[0]),
                ).fetchall()
                edges = [
                    LoreEdge(
                        source_node_id=er[0],
                        target_node_id=er[1],
                        relation_type=er[2],
                        confidence=er[3],
                    )
                    for er in edge_rows
                ]
            finally:
                edge_conn.close()

        results.append(
            QueryResult(
                node_id=row[0],
                bucket_type=row[1],
                provenance_ref=row[2],
                text_preview=row[3],
                summary=row[4],
                similarity=float(row[5]),
                edges=edges,
            )
        )

    return results


@app.post("/resonance", response_model=list[ResonanceResult])
async def resonance_query(req: ResonanceRequest):
    semantic_vector = None
    if req.query_text:
        try:
            vectors = await embed_text([req.query_text])
            semantic_vector = vectors[0]
        except Exception:
            pass

    conn = get_db_readonly()
    try:
        params: list = [req.enneagram_type, req.min_resonance, req.top_k]
        kosha_clause = ""
        if req.kosha_layer:
            kosha_clause = "AND ba.kosha_layer = %s"
            params.insert(2, req.kosha_layer)
            params = [req.enneagram_type, req.min_resonance, req.kosha_layer, req.top_k] if not req.query_text else params

        semantic_join = ""
        semantic_select = ""
        semantic_order = ""
        if semantic_vector is not None:
            semantic_join = "JOIN lore_node ln ON ba.node_id = ln.node_id"
            semantic_select = ", 1 - (ln.embedding <=> %s) AS semantic_similarity"
            semantic_order = "ORDER BY (ba.resonance_weight + COALESCE(1 - (ln.embedding <=> %s), 0)) / 2 DESC"
            params_with_vec = [semantic_vector] + params
        else:
            params_with_vec = params
            semantic_order = "ORDER BY ba.resonance_weight DESC"

        rows = conn.execute(
            f"""
            SELECT ba.node_id, ln.bucket_type, ln.provenance_ref, ln.text_preview, ln.summary,
                   ba.enneagram_type, ba.kosha_layer, ba.resonance_weight
                   {semantic_select}
            FROM biorhythm_affinity ba
            JOIN lore_node ln ON ba.node_id = ln.node_id
            {semantic_join}
            WHERE ba.enneagram_type = %s
              AND ba.resonance_weight >= %s
              {kosha_clause}
            {semantic_order}
            LIMIT %s
            """,
            params_with_vec,
        ).fetchall()
    finally:
        conn.close()

    results: list[ResonanceResult] = []
    for row in rows:
        semantic_sim = float(row[8]) if semantic_vector is not None and len(row) > 8 else None
        resonance = float(row[7])
        combined = (resonance + (semantic_sim or 0)) / 2 if semantic_sim is not None else resonance

        results.append(
            ResonanceResult(
                node_id=row[0],
                bucket_type=row[1],
                provenance_ref=row[2],
                text_preview=row[3],
                summary=row[4],
                enneagram_type=row[5],
                kosha_layer=row[6],
                resonance_weight=resonance,
                semantic_similarity=semantic_sim,
                combined_score=combined,
            )
        )

    return results


@app.post("/nodes", response_model=LoreNode)
async def create_node(node: LoreNode):
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO lore_node (node_id, bucket_type, source_path, provenance_ref,
                                   text_preview, quality_flags)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (node_id) DO UPDATE SET
                bucket_type = EXCLUDED.bucket_type,
                source_path = EXCLUDED.source_path,
                provenance_ref = EXCLUDED.provenance_ref,
                text_preview = EXCLUDED.text_preview,
                quality_flags = EXCLUDED.quality_flags,
                updated_at = NOW()
            """,
            (
                node.node_id,
                node.bucket_type,
                node.source_path,
                node.provenance_ref,
                node.text_preview,
                node.quality_flags,
            ),
        )
    return node


@app.post("/edges", response_model=LoreEdge)
async def create_edge(edge: LoreEdge):
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO lore_edge (source_node_id, target_node_id, relation_type, evidence_ref, confidence)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source_node_id, target_node_id, relation_type) DO UPDATE SET
                evidence_ref = EXCLUDED.evidence_ref,
                confidence = EXCLUDED.confidence
            """,
            (edge.source_node_id, edge.target_node_id, edge.relation_type, edge.evidence_ref, edge.confidence),
        )
    return edge


@app.post("/affinities", response_model=BiorhythmAffinity)
async def create_affinity(affinity: BiorhythmAffinity):
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO biorhythm_affinity (node_id, enneagram_type, hormone_phase, kosha_layer, resonance_weight)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (node_id, enneagram_type, kosha_layer) DO UPDATE SET
                hormone_phase = EXCLUDED.hormone_phase,
                resonance_weight = EXCLUDED.resonance_weight
            """,
            (affinity.node_id, affinity.enneagram_type, affinity.hormone_phase, affinity.kosha_layer, affinity.resonance_weight),
        )
    return affinity


@app.post("/seed-affinities")
async def seed_affinities():
    rows_inserted = 0
    with get_db() as conn:
        node_rows = conn.execute("SELECT node_id, bucket_type FROM lore_node").fetchall()
        for node_id, bucket_type in node_rows:
            affinities = BUCKET_AFFINITIES.get(bucket_type, [])
            for aff in affinities:
                hormone = ENNEAGRAM_HORMONE_MAP.get(aff["enneagram_type"])
                conn.execute(
                    """
                    INSERT INTO biorhythm_affinity (node_id, enneagram_type, hormone_phase, kosha_layer, resonance_weight)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (node_id, enneagram_type, kosha_layer) DO UPDATE SET
                        hormone_phase = EXCLUDED.hormone_phase,
                        resonance_weight = EXCLUDED.resonance_weight
                    """,
                    (node_id, aff["enneagram_type"], hormone, aff["kosha_layer"], aff["resonance_weight"]),
                )
                rows_inserted += 1
    return {"rows_inserted": rows_inserted, "nodes_processed": len(node_rows)}


class ReadingRequest(BaseModel):
    enneagram_type: int = Field(ge=1, le=9)
    kosha_layer: str | None = None
    hormone_phase: str | None = None
    query_text: str | None = None
    top_k: int = 5
    min_resonance: float = 0.3


class ReadingResponse(BaseModel):
    reading_context: str
    concept_cluster: list[dict]
    enneagram_type: int
    kosha_layer: str | None
    hormone_phase: str | None
    resonance_mode: str


READING_SYSTEM_PROMPT = """You are the Somatic Canticles reading agent. You do not recite chapter text. You deliver personalized resolution through discourse.

Your role:
- Receive a concept cluster of lore nodes scored by biorhythm resonance
- The user's Enneagram type and Kosha layer define their current resonance profile
- Speak TO the user about WHY these concepts matter for THEM right now
- Use biorhythmic language: breath, field, witness, resolution, coherence
- Never summarize chapters. Deliver insight that resolves, not information that describes
- Honor the Pancha Kosha arc: each concept connects through a specific sheath
- The user's current phase determines which resolution door is open"""

READING_TEMPLATE = """Enneagram Type {enneagram}: {hormone_name}
Kosha Layer: {kosha}
Current resonance mode: {mode}

Retrieved concepts (ranked by combined resonance + semantic score):
{concept_list}

Deliver a personalized reading that:
1. Names the specific tension the user carries in this Enneagram/Kosha configuration
2. Maps how the retrieved concepts illuminate that tension
3. Offers the resolution door that is open RIGHT NOW (not later, not in theory)
4. Ends with a practice or recognition that anchors the resolution in the body"""


@app.post("/reading", response_model=ReadingResponse)
async def reading(req: ReadingRequest):
    resonance_req = ResonanceRequest(
        enneagram_type=req.enneagram_type,
        kosha_layer=req.kosha_layer,
        hormone_phase=req.hormone_phase,
        query_text=req.query_text,
        top_k=req.top_k,
        min_resonance=req.min_resonance,
    )

    resonance_results = await resonance_query(resonance_req)

    if not resonance_results:
        raise HTTPException(status_code=404, detail="No resonance results found for this profile")

    enneagram_names = {
        1: "Perfectionist", 2: "Giver", 3: "Achiever", 4: "Individualist",
        5: "Investigator", 6: "Loyalist", 7: "Enthusiast", 8: "Challenger", 9: "Peacemaker",
    }
    kosha_names = {
        "annamaya": "Physical Nourishment", "pranamaya": "Vital Breath",
        "manomaya": "Emotional Mind", "vijnanamaya": "Discerning Wisdom",
        "anandamaya": "Bliss Integration",
    }
    mode_names = {
        "annamaya": "grounding", "pranamaya": "breath-bearing",
        "manomaya": "meaning-seeking", "vijnanamaya": "truth-discerning",
        "anandamaya": "release-receiving",
    }

    hormone_name = ENNEAGRAM_HORMONE_MAP.get(req.enneagram_type, "unknown")
    kosha_desc = KOSHA_DESCRIPTION.get(req.kosha_layer, "") if req.kosha_layer else ""
    primary_kosha = req.kosha_layer or resonance_results[0].kosha_layer or "manomaya"
    mode = mode_names.get(primary_kosha, "seeking")

    concept_list = ""
    for i, r in enumerate(resonance_results, 1):
        kosha_name = kosha_names.get(r.kosha_layer, r.kosha_layer or "unknown")
        concept_list += f"\n{i}. [{r.bucket_type}] {r.text_preview[:120]}... (resonance={r.resonance_weight:.2f}, semantic={r.semantic_similarity:.3f if r.semantic_similarity else 'N/A'}, combined={r.combined_score:.3f}, kosha={kosha_name})"

    reading_context = READING_TEMPLATE.format(
        enneagram=req.enneagram_type,
        hormone_name=hormone_name.replace("_", " "),
        kosha=kosha_names.get(primary_kosha, primary_kosha),
        mode=mode,
        concept_list=concept_list,
    )

    concept_cluster = [
        {
            "node_id": r.node_id,
            "bucket_type": r.bucket_type,
            "provenance_ref": r.provenance_ref,
            "enneagram_type": r.enneagram_type,
            "kosha_layer": r.kosha_layer,
            "resonance_weight": r.resonance_weight,
            "semantic_similarity": r.semantic_similarity,
            "combined_score": r.combined_score,
        }
        for r in resonance_results
    ]

    return ReadingResponse(
        reading_context=reading_context,
        concept_cluster=concept_cluster,
        enneagram_type=req.enneagram_type,
        kosha_layer=primary_kosha,
        hormone_phase=hormone_name,
        resonance_mode=mode,
    )


@app.post("/seed-lore")
async def seed_lore_entries():
    nodes_created = 0
    edges_created = 0
    affinities_created = 0
    errors: list[str] = []

    for entry in INITIAL_LORE_ENTRIES:
        try:
            with get_db() as conn:
                conn.execute(
                    """
                    INSERT INTO lore_node (node_id, bucket_type, source_path, source_type, provenance_ref, text_preview, summary, quality_flags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (node_id) DO UPDATE SET
                        bucket_type = EXCLUDED.bucket_type,
                        source_path = EXCLUDED.source_path,
                        provenance_ref = EXCLUDED.provenance_ref,
                        text_preview = EXCLUDED.text_preview,
                        summary = EXCLUDED.summary,
                        quality_flags = EXCLUDED.quality_flags,
                        updated_at = NOW()
                    """,
                    (
                        entry["node_id"],
                        entry["bucket_type"],
                        entry["source_path"],
                        entry["source_type"],
                        entry["provenance_ref"],
                        entry["text_preview"],
                        entry["summary"],
                        json.dumps(entry["quality_flags"]),
                    ),
                )
                nodes_created += 1

                for aff in entry.get("affinities", []):
                    hormone = ENNEAGRAM_HORMONE_MAP.get(aff["enneagram_type"])
                    conn.execute(
                        """
                        INSERT INTO biorhythm_affinity (node_id, enneagram_type, hormone_phase, kosha_layer, resonance_weight)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (node_id, enneagram_type, kosha_layer) DO UPDATE SET
                            hormone_phase = EXCLUDED.hormone_phase,
                            resonance_weight = EXCLUDED.resonance_weight
                        """,
                        (entry["node_id"], aff["enneagram_type"], hormone, aff["kosha_layer"], aff["resonance_weight"]),
                    )
                    affinities_created += 1
        except Exception as exc:
            errors.append(f"{entry['node_id']}: {exc}")

    return {
        "nodes_created": nodes_created,
        "affinities_created": affinities_created,
        "total_lore_entries": len(INITIAL_LORE_ENTRIES),
        "errors": errors,
    }