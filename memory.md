# PROJECT MEMORY

## Overview
Somatic Canticles is a sci-fi trilogy exploring consciousness, embodiment, and the transition from a synthetic "Vine" to a biological "Chorus." The project involves manuscript creation, editorial polish, world-building data management, and web app integration.

## Completed Tasks

### Interactive Experience Design (2026-02-07)
- [DONE] ~~Design 'Living Book' Interactive Experience~~
- [DONE] ~~Update JSON Schema for Interactive Mode~~
- **Concept**: "The Living Book" - A Bandersnatch-style experience driven by biorhythms (Circadian, Scroll Speed, Breath).
- **Triggers Added**: `circadian_rhythm`, `scroll_velocity`, `breath_detection` added to `somatic_canticles_trilogy_data.json`.

### World Bible Architecture (2026-02-07)
- [DONE] ~~Enhance World Bible Architecture~~
- **Outcome**: Created a multi-layered index system for the World Bible.
- **Artifacts**:
    - `01_WORLD_BIBLE/00_CORE_FOUNDATION/world_bible_registry.json` (Machine-readable index).
    - `01_WORLD_BIBLE/README_NAVIGATOR.md` (Human-readable hub with visual map).
    - Updated `somatic_canticles_data_tapestry.json` to link files to concepts.

### [2026-02-07] Book 3 Audit & Polish
- **Outcome**: Completed comprehensive audit of Book 3 for legacy terms and capitalization.
- **Breakthrough**: Standardized "Witness"-related terms; confirmed "The Gardener" consistency.
- **Code Changes**: 10+ edits to `Book_3_The_Ripening.md`; Rebuilt `Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`.
- **Errors Fixed**: Resolved file offset issues by switching to semantic phrase matching.

## Key Breakthroughs
- **The Tapestry Matrix**: A 4-dimensional mapping system (Chronological, Conceptual, Character, Geographic) allows for rich semantic querying of the narrative universe.
- **Somatic Directness**: The editorial shift from "felt/saw" to direct sensory experience (e.g., "The air tasted like ozone") has significantly deepened the reader's immersion.

## Error Patterns & Solutions
- **File Offsets**: Line numbers are unreliable in a rapidly changing manuscript. **Solution**: Use `grep` with context or unique semantic phrases to locate edit points.
