# Vision Worldbuilding Ingestion Plan

## Purpose

This document defines how multimodal extraction may deepen lore and worldbuilding during the NVIDIA expansion pass without silently mutating canon.

The goal is not to let images dictate ontology. The goal is to extract usable motif, atmosphere, symbolic recurrence, and biological/governance pressure that can be bound to chapter dossiers and validated against the existing authority stack.

## Primary Visual Roots

### Noesis research root

- `/Users/sheshnarayaniyer/Documents/noesis/Research`

Primary use:

- dedicated vision-first extraction
- image-family clustering
- motif captioning
- symbolic and somatic pattern recovery

### Blog visual roots

- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/assets/cards`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/cards`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/images`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/maps`

Primary use:

- published symbolic cards
- public visual identity
- recurring runtime and authorship imagery

### Internal visual support

- `01_WORLD_BIBLE/04_WORLD_BUILDING/Visual_Archive/`
- selected image-bearing files under `/Volumes/madara/2026/twc-vault/03-Resources/Design`
- selected diagram/image files under `/Volumes/madara/2026/twc-vault/03-Resources/General-Research`
- selected diagram/image files under `/Volumes/madara/2026/twc-vault/03-Resources/Knowledge-Organization`

## Extraction Targets

The vision lane is allowed to extract:

- motif labels
- compositional recurrence
- symbolic tensions
- biological analogies
- governance analogies
- environmental tone and world-pressure cues
- chapter-relevant atmospheric detail

The vision lane is not allowed to create:

- new canonical laws
- new character facts
- new trilogy-endgame claims
- plot-critical rules without text corroboration

## Model Routing

### Primary extraction model

- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

Use for:

- image captioning
- motif extraction
- cluster comparison
- diagrams/maps/cards interpretation

### Optional synthesis model

- `moonshotai/kimi-k2.6`

Use only after image evidence exists and needs chapter-scale narrative interpretation or clustering across multiple visual families.

### Control review

- `openai/gpt-oss-120b`
- or `nvidia/nemotron-3-super-120b-a12b`

Use for:

- provenance enforcement
- authority-bound interpretation
- preventing symbolic overclaim

## Required Output Artifacts

Before image-derived material touches prose, produce:

1. A visual asset inventory
2. A motif extraction registry
3. A chapter-bound mapping from visual motif to dossier use
4. A provenance tag for every claim
5. A corroboration field showing which text or authority source supports the interpretation

## Dossier Integration Rules

Visual material may enter a chapter dossier only as one of:

- `atmospheric support`
- `symbolic support`
- `biological metaphor support`
- `governance metaphor support`

It may not enter as:

- `hard authority`
- `plot authority`
- `new law of the world`

## First-Pass Execution Order

1. Inventory the noesis visual root and blog visual roots.
2. Separate likely chapter-relevant assets from noise.
3. Run multimodal extraction by family, not one image at a time.
4. Write motif summaries in chapter-usable language.
5. Bind each extracted family to a dossier candidate section.
6. Validate every visual interpretation against text or authority surfaces.
7. Allow only validated extracts into lore/worldbuilding support.

## Initial Priority Families

- endocrine / bioelectric pattern families
- runtime / circuitry / architecture families
- tetramorphic and creature-assembly families
- authorship / cellular-polity / lawful-division families
- deception / concealment / exposure families
- pressure, wound, and substrate distortion families
