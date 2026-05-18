# Somatic Canticles Lore Service

Local service stack for embedding + provenance-bound relation graph retrieval.

## Quick Start

```bash
# From the service/ directory
docker compose up -d

# Seed the pilot data (100 nodes, vectors, provenance)
curl -X POST http://localhost:8000/seed

# Check health
curl http://localhost:8000/health

# Query lore by semantic similarity
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query_text": "biofield measurement techniques", "top_k": 5}'

# Query lore by biorhythm resonance (dyadic agent input)
curl -X POST http://localhost:8000/resonance \
  -H "Content-Type: application/json" \
  -d '{"enneagram_type": 5, "kosha_layer": "vijnanamaya", "query_text": "witness consciousness", "top_k": 5}'

# Add a new lore node (ongoing ingestion)
curl -X POST http://localhost:8000/nodes \
  -H "Content-Type: application/json" \
  -d '{"node_id": "LORE-001", "bucket_type": "bio_field_charts", "provenance_ref": "manual:001", "text_preview": "new lore entry"}'

# Teardown
docker compose down
```

## Architecture

```
service/
  docker-compose.yml    # pgvector + API
  Dockerfile            # Python 3.12 + FastAPI
  requirements.txt      # Dependencies
  migrations/
    001_init_schema.sql  # DDL: nodes, edges, affinities, provenance, indexes
  app/
    main.py             # FastAPI endpoints
    config.py           # Settings from env
    models.py           # Pydantic request/response schemas
    db.py               # psycopg + pgvector connection
    embeddings.py       # NVIDIA NIM embedding client
    seed.py             # Pilot data loader from phase3 artifacts
```

## Schema (extends SWA-019 and SWA-020 contracts)

- `lore_node` — Core node with 4096-dim text embedding + 2048-dim VL embedding + provenance
- `lore_edge` — Directed edges with 7 relation types (5 original + `resonates_with` + `biorhythm_affinity`)
- `biorhythm_affinity` — Enneagram type + Pancha Kosha layer + resonance weight per node
- `provenance_chain` — Immutable audit trail

## Dyadic Agent Path

The `/resonance` endpoint is the foundation for the dyadic agent:
1. User biorhythm state → Enneagram type + Kosha layer
2. Resonance query retrieves lore nodes that match the user's profile
3. Combined score = (resonance_weight + semantic_similarity) / 2
4. Agent uses the scored concept cluster to deliver personalized readings, not chapter text

## Railway Deployment (future)

Change `DATABASE_URL` to a Railway Postgres+pgvector instance and set `NVIDIA_API_KEY` in Railway env vars. No code changes needed.