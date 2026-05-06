# Repo Synthesis Manifest

## Purpose

This document is the control surface for the NVIDIA-assisted long-form expansion pass.

It should answer four questions before any chapter is rewritten:

1. What is canon right now?
2. Which repo surfaces control expansion behavior?
3. Which external/source families are allowed to deepen a given chapter?
4. Which model is responsible for which type of work?

## Canonical Export Surfaces

- `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md`
- `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md`
- `02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md`
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`

## StoryOps Control Surfaces

- `06_WORKBENCH/SC_STORYOPS/story/outline.md`
- `06_WORKBENCH/SC_STORYOPS/story/chapter_summaries.md`
- `06_WORKBENCH/SC_STORYOPS/story/book_rules.md`
- `06_WORKBENCH/SC_STORYOPS/story/dialogue_voice_matrix.md`
- `06_WORKBENCH/SC_STORYOPS/story/emotional_arcs.md`
- `06_WORKBENCH/SC_STORYOPS/story/character_matrix.md`
- `06_WORKBENCH/SC_STORYOPS/story/subplot_board.md`
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_projection_board.md`
- `06_WORKBENCH/SC_STORYOPS/story/intake/world_bible_authority_registry.md`

## Editorial Authority Surfaces

- `03_EDITORIAL/EDITORIAL_BRIEF.md`
- `03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md`
- `03_EDITORIAL/TERMINOLOGY_CLEANUP_PLAN.md`
- `03_EDITORIAL/Book_3_Editorial_Pass.md`
- `03_EDITORIAL/book1_anamnesis_engine_tasks.json`
- `03_EDITORIAL/book2_myocardial_chorus_tasks.json`
- `03_EDITORIAL/book3_the_ripening_tasks.json`

## External Deepening Surfaces

### Published text substrate

- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/content/posts`

This is the strongest external prose-adjacent substrate. Treat it as the public conceptual base layer for runtime, authorship, endocrine, compassion, pattern, and consciousness language.

### Vault research support

- `/Volumes/madara/2026/twc-vault/03-Resources`

Use this as a selective research corpus, not a wholesale import root.

Priority families:

- `Consciousness-Studies`
- `Consciousness`
- `Content`
- `General-Research`
- `Biological`
- `Esoteric/Intake-Integrated`

Visual support candidates:

- `Design`
- image-bearing files in `General-Research`
- diagram-bearing files in `Knowledge-Organization`

### Area notebooks and concept hubs

- `/Volumes/madara/2026/twc-vault/02-Areas`

Priority families:

- `Consciousness-Models`
- `Pattern-Studies`
- `Technical-Mystical-Integration`
- `Bioelectric-Body`
- `Logic-Gate-Linguistics`
- `Muse-Enneagram-Framework`

Excluded by default:

- `Daily-Logs`
- operational journaling
- personal notes that do not function as reusable concept surfaces

### Vision-first research root

- `/Users/sheshnarayaniyer/Documents/noesis/Research`

Primary uses:

- motif extraction
- cluster captioning
- worldbuilding support candidates
- symbolic recurrence tracing

### Internal world and visual support

- `01_WORLD_BIBLE/`
- `01_WORLD_BIBLE/04_WORLD_BUILDING/Visual_Archive/`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/assets/cards`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/cards`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/images`
- `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/maps`

## Admissibility Rules

### Hard canon

Only the repo's compiled surfaces, StoryOps control surfaces, and editorial/world-bible authority files may directly govern canon.

### Review-required text support

Blog posts, `03-Resources`, `02-Areas`, and supporting world-bible files may deepen:

- context
- atmosphere
- systems language
- chapter-local world pressure

They may not, by themselves, widen ontology, add new laws, or introduce decisive trilogy claims.

### Review-required visual support

Any claim extracted from images, cards, maps, diagrams, or screenshots stays non-canonical until it is corroborated by:

- an existing authority surface, or
- a text-support source that the chapter dossier already approves

Vision-derived material is allowed to deepen:

- motif recurrence
- sensory staging
- symbolic pressure
- governance or biology metaphors

It is not allowed to invent new plot-critical rules alone.

## Model Roles

### `openai/gpt-oss-120b`

- produce repo-wide synthesis
- map canon and authority relationships
- identify missing story layers by chapter
- classify where prose is rushed versus where doctrine is merely compressed

### `minimaxai/minimax-m2.7`

- design helper scripts and processing utilities
- build chapter dossier generators
- build source-to-chapter mapping helpers
- build repeatable processing for length audits and layer-gap reports
- build source-root filters so excluded material does not leak into dossiers

### `moonshotai/kimi-k2-thinking`

- diagnose scene failures before drafting
- propose chapter-level pacing correction
- identify where concept load outruns embodiment

### `moonshotai/kimi-k2-instruct`

- write the expanded chapter prose
- deepen atmosphere, scene dwell time, aftermath, and relational pressure
- integrate lore through scene behavior instead of explanation

### `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

- perform multimodal extraction over noesis images, blog cards, maps, diagrams, and selected vault visuals
- caption motif families in chapter-usable language
- emit lore/worldbuilding support candidates with provenance tags

### Optional multimodal synthesis

- `moonshotai/kimi-k2.6`

Use only after visual evidence exists and needs long-context narrative interpretation.

### Control models

- `nvidia/nemotron-3-super-120b-a12b`
- `openai/gpt-oss-120b`

Use for:

- canon drift review
- vocabulary drift review
- doctrine inflation review
- source-dossier compliance review

## Required Outputs Before Drafting

- repo-wide synthesis summary
- chapter expansion matrix
- chapter source dossier for the target chapter
- explicit target length band
- missing-layer diagnosis
- source-tier tags for every non-repo input
- visual extraction registry entries for any image-derived support
- validation checklist for canon and doctrine drift

## First Pass Deliverables

- a complete trilogy chapter expansion matrix
- dossier coverage for `Chapter 01-27`
- helper-script plan for dossier generation and word-count/layer-gap reporting
- a source-root filter plan that separates admissible support from excluded journaling/noise
- a multimodal extraction plan for noesis, blog cards/images, and approved vault visuals
