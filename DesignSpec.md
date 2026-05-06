# Design Spec: NVIDIA-Assisted Trilogy Expansion

## 1. Summary

This project expands the current *Somatic Canticles* trilogy from a structurally coherent but compressed canonical surface into a longer, more breathable narrative system without losing the canon, authority boundaries, or StoryOps logic already established in the repo.

The main need is not new concepts. The need is more room for:

- somatic rhythm
- scene dwell time
- aftermath
- relational consequence
- world pressure
- lore embodiment through behavior
- slower revelation pacing

## 2. Current State

- Books `1-3` are canonically stabilized and compiled.
- Book `3` has already been operationally unblocked and merged into the compiled package.
- StoryOps control surfaces, world-bible authority surfaces, and editorial doctrine are already present.
- The late-book image and lore authority work has already been done enough to support a controlled expansion lane.
- The current prose surface still feels short relative to the amount of available substrate.

## 3. Problem Statement

The current trilogy inherits too much same-model compression:

- chapters are too short for the conceptual load they carry
- worldbuilding often arrives as compressed implication instead of lived context
- somatic pacing is present but under-extended
- revelation logic is correct but sometimes lands too quickly
- lore exists in source material but is not fully metabolized into the chapter surfaces

## 4. Objective

Build a durable expansion pipeline that can:

1. synthesize the entire repo and source material
2. generate chapter-bound source dossiers
3. use multiple specialized models in parallel
4. expand chapters book by book without canon drift
5. rebuild compiled surfaces only after validation

## 5. Delivery Profile

- Planning depth: `deeply detailed`
- Delivery mode: `production`
- Release model: `phased rollout`
- CI/CD expectation: `basic` repo validation plus manual editorial verification
- Human team shape: `solo human lead with model swarm`

## 6. Quality Bar

- no canon contradiction
- no doctrine inflation beyond the authority stack
- no image-derived ontology without corroboration
- no same-model dryness left untreated
- every expanded chapter must feel more embodied, relational, and breathable than the current compiled version

## 7. Source Material Scope

### Internal authority and control

- StoryOps surfaces under `06_WORKBENCH/SC_STORYOPS/story`
- editorial surfaces under `03_EDITORIAL`
- world-bible authority surfaces under `01_WORLD_BIBLE`
- compiled canon under `02_MANUSCRIPTS/COMPILED`

### External source roots

- published substrate:
  `/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/content/posts`
- vault support:
  `/Volumes/madara/2026/twc-vault/03-Resources`
- area support:
  `/Volumes/madara/2026/twc-vault/02-Areas`
- vision-first support:
  `/Users/sheshnarayaniyer/Documents/noesis/Research`

## 8. Non-Negotiable Constraints

- Canon is still governed by repo-local authority surfaces.
- External sources deepen chapters; they do not silently rewrite doctrine.
- Visual extraction is review-required support only.
- Parallel execution must be contract-first.
- Shared lock zones are serialized.
- Expansion happens in the isolated worktree before any merge-back.

## 9. Required Deliverables

- repo-wide synthesis artifact
- source-tiered chapter expansion matrix
- dossier coverage for `Chapter 01-27`
- multimodal extraction registry
- helper scripts for source filtering and dossier generation
- expanded working chapters
- validated rebuilt compiled books and omnibus
- updated glossary / bibliography / endmatter only if expansion requires it

## 10. Success Criteria

The program is successful when:

- every chapter has a source-bound dossier
- each book can be expanded without re-deriving scope from chat
- model roles are explicit and non-overlapping
- the trilogy grows in length and depth without flattening voice or widening unsupported lore
- the compiled surfaces can be rebuilt from validated working chapters
