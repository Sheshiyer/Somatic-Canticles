# Dependency Map - SWA Program

## Critical Path
`SWA-001 -> SWA-010 -> SWA-011..SWA-030 -> SWA-031..SWA-045 -> SWA-046..SWA-060 -> SWA-061..SWA-072 -> SWA-073..SWA-080`

## Parallelizable Clusters
- Data prep lanes can parallelize after schema contracts freeze:
  - SWA-035 and SWA-036
- Embedding lanes can parallelize after input prep:
  - SWA-049, SWA-050, SWA-051
- Retrieval eval lanes can parallelize after index build:
  - SWA-055, SWA-056, SWA-057

## Serialized Lock Zones
- Contract files in Phase 1
- Weighted decision memo in Phase 4
- Operational roadmap closeout in Phase 5

## Current Status
- Planning graph generated
- Phase 0 artifact execution in progress
