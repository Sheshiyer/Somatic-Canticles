# SWA-029 Contract: Artifact Versioning Policy

## Versioning
- Stable files: canonical names without suffix
- Regenerated reports: append date stamp
- Experimental outputs: append run id

## Required Metadata
- `generated_at`
- `source_inputs`
- `model_lane`
- `checksum` when applicable

## Policy
- Never overwrite acceptance evidence without preserving prior version.
