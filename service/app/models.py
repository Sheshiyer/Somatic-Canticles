from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LoreNode(BaseModel):
    node_id: str
    bucket_type: str
    source_path: str | None = None
    source_type: str | None = None
    language_hint: str = "en"
    provenance_ref: str
    summary: str | None = None
    confidence_notes: str | None = None
    quality_flags: dict[str, Any] = Field(default_factory=dict)
    text_preview: str | None = None
    vector_dim: int | None = None
    vl_vector_dim: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class LoreEdge(BaseModel):
    edge_id: int | None = None
    source_node_id: str
    target_node_id: str
    relation_type: str
    evidence_ref: str | None = None
    confidence: float = 1.0


class BiorhythmAffinity(BaseModel):
    affinity_id: int | None = None
    node_id: str
    enneagram_type: int | None = None
    hormone_phase: str | None = None
    kosha_layer: str | None = None
    resonance_weight: float = 0.5


class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 10
    bucket_filter: list[str] | None = None
    include_edges: bool = False


class QueryResult(BaseModel):
    node_id: str
    bucket_type: str
    provenance_ref: str
    text_preview: str | None = None
    summary: str | None = None
    similarity: float
    edges: list[LoreEdge] | None = None


class ResonanceRequest(BaseModel):
    enneagram_type: int = Field(ge=1, le=9)
    kosha_layer: str | None = None
    hormone_phase: str | None = None
    query_text: str | None = None
    top_k: int = 10
    min_resonance: float = 0.3


class ResonanceResult(BaseModel):
    node_id: str
    bucket_type: str
    provenance_ref: str
    text_preview: str | None = None
    summary: str | None = None
    enneagram_type: int | None = None
    kosha_layer: str | None = None
    resonance_weight: float
    semantic_similarity: float | None = None
    combined_score: float


class SeedStatus(BaseModel):
    loaded_nodes: int
    loaded_edges: int
    loaded_vectors: int
    loaded_vl_vectors: int
    loaded_provenance: int
    errors: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    db_connected: bool
    node_count: int
    edge_count: int