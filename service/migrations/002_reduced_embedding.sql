-- Add reduced_embedding column for PCA-compressed vectors (1536 dims)
-- This enables HNSW indexing since pgvector's limit is 2000 dims
ALTER TABLE lore_node ADD COLUMN IF NOT EXISTS reduced_embedding vector(1536);

-- HNSW index on reduced column for fast approximate nearest-neighbor search
CREATE INDEX IF NOT EXISTS idx_node_reduced_embedding ON lore_node
    USING hnsw (reduced_embedding vector_cosine_ops);