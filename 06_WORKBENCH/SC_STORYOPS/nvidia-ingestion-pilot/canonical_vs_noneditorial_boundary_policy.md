# Canonical vs Non-Editorial Boundary Policy

## Canonical Zone (Do Not Mutate in Pilot)
- `02_MANUSCRIPTS/COMPILED`
- Canon-defining doctrine in `01_WORLD_BIBLE` and `03_EDITORIAL`

## Non-Editorial Pilot Zone (Mutable)
- `06_WORKBENCH/SC_STORYOPS/nvidia-ingestion-pilot`
- Derived manifests, extraction outputs, retrieval evaluations, and model decision logs

## Allowed Data Classes
- Biofield charts
- Interpretation maps
- Cross-integration histories

## Disallowed Pilot Behaviors
- Direct manuscript rewrites
- Unproven doctrinal additions
- Ontology creation without provenance

## Enforcement Rules
1. Every node requires `source_path` and provenance reference fields
2. Every relation requires evidence pointer and confidence
3. Editorial/canon references may be read for constraints, never overwritten by pilot artifacts
4. Any future integration into canon requires a separate editorial approval cycle
