-- Canticles Lore Service: pgvector schema
-- Phase 5 approved stack: Postgres + pgvector + relation tables
-- Backend-neutral adapter contract preserved for future graph-native migration

CREATE EXTENSION IF NOT EXISTS vector;

-- Core lore node (extends SWA-019 contract)
CREATE TABLE IF NOT EXISTS lore_node (
    node_id         TEXT PRIMARY KEY,
    bucket_type     TEXT NOT NULL,
    source_path     TEXT,
    source_type     TEXT,
    language_hint   TEXT DEFAULT 'en',
    provenance_ref  TEXT NOT NULL,
    summary         TEXT,
    confidence_notes TEXT,
    quality_flags   JSONB DEFAULT '{}',
    text_preview    TEXT,
    embedding       vector(4096),
    vl_embedding    vector(2048),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Relation edges (extends SWA-020 contract)
-- Preserves the 5 v1 relation types and adds biorhythm_resonance
CREATE TABLE IF NOT EXISTS lore_edge (
    edge_id         SERIAL PRIMARY KEY,
    source_node_id  TEXT NOT NULL REFERENCES lore_node(node_id) ON DELETE CASCADE,
    target_node_id  TEXT NOT NULL REFERENCES lore_node(node_id) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL CHECK (relation_type IN (
        'supports', 'contrasts', 'extends',
        'historical_precedes', 'maps_to',
        'resonates_with', 'biorhythm_affinity'
    )),
    evidence_ref    TEXT,
    confidence      REAL NOT NULL DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_node_id, target_node_id, relation_type)
);

-- Biorhythm resonance profile (new: dyadic agent input)
-- Maps lore nodes to Enneagram/biorhythm affinities for personalized retrieval
CREATE TABLE IF NOT EXISTS biorhythm_affinity (
    affinity_id     SERIAL PRIMARY KEY,
    node_id          TEXT NOT NULL REFERENCES lore_node(node_id) ON DELETE CASCADE,
    enneagram_type   INTEGER CHECK (enneagram_type BETWEEN 1 AND 9),
    hormone_phase    TEXT,
    kosha_layer     TEXT CHECK (kosha_layer IN (
        'annamaya', 'pranamaya', 'manomaya', 'vijnanamaya', 'anandamaya'
    )),
    resonance_weight REAL NOT NULL DEFAULT 0.5 CHECK (resonance_weight >= 0 AND resonance_weight <= 1),
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(node_id, enneagram_type, kosha_layer)
);

-- Provenance chain (immutable audit trail)
CREATE TABLE IF NOT EXISTS provenance_chain (
    provenance_id    TEXT PRIMARY KEY,
    source_artifact  TEXT NOT NULL,
    extraction_method TEXT,
    extraction_date  TIMESTAMPTZ,
    checksum_sha256  TEXT,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- Vector search indexes
-- NOTE: pgvector indexes (both IVFFlat and HNSW) support max 2000 dimensions as of pgvector 0.3.x.
-- Our embedding vectors are 4096-dim and VL vectors are 2048-dim, both exceeding this limit.
-- Exact nearest-neighbor search (no index) is used for vector similarity queries.
-- At production scale, consider: (1) dimensionality reduction to ≤2000, or (2) upgrading to
-- pgvector 0.7+ which may relax this constraint, or (3) using a dedicated vector DB.

-- Standard indexes
CREATE INDEX IF NOT EXISTS idx_node_bucket ON lore_node(bucket_type);
CREATE INDEX IF NOT EXISTS idx_node_provenance ON lore_node(provenance_ref);
CREATE INDEX IF NOT EXISTS idx_edge_source ON lore_edge(source_node_id);
CREATE INDEX IF NOT EXISTS idx_edge_target ON lore_edge(target_node_id);
CREATE INDEX IF NOT EXISTS idx_edge_type ON lore_edge(relation_type);
CREATE INDEX IF NOT EXISTS idx_affinity_node ON biorhythm_affinity(node_id);
CREATE INDEX IF NOT EXISTS idx_affinity_enneagram ON biorhythm_affinity(enneagram_type);
CREATE INDEX IF NOT EXISTS idx_affinity_kosha ON biorhythm_affinity(kosha_layer);