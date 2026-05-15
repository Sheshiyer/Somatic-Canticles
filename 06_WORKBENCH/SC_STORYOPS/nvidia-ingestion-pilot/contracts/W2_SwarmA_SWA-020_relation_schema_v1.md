# SWA-020 Contract: Relation Schema v1

## Core Fields
- `relation_id`
- `source_node_id`
- `target_node_id`
- `relation_type`
- `evidence_ref`
- `confidence`

## Relation Types (v1)
- `supports`
- `contrasts`
- `extends`
- `historical_precedes`
- `maps_to`

## Validation
- All node references must resolve to existing `node_id` values.
- `confidence` must be numeric in `[0,1]`.
