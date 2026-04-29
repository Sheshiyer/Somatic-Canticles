# World-Bible Authority Registry

## Purpose

This file operationalizes `clarify_log.md` decision `CL-004` so `SC_STORYOPS` can use `01_WORLD_BIBLE/` without treating every surface as equally binding.

## Authority Legend

| Tier | Safe Use In `SC_STORYOPS` | Merge-Back Rule |
| --- | --- | --- |
| hard authority | safe to constrain concepts, packets, and later prose directly | may drive scene logic if it does not contradict editorial doctrine or chapter canon |
| review-required support | usable for intake, concept pressure, and soft packet support | must be triangulated with hard-authority world-bible or editorial sources before it becomes a hard scene promise |
| support-only / navigation | use for retrieval, compression, motif recall, or meta framing | do not cite as sole proof of lore claims |
| legacy / do not import blindly | keep for historical comparison only | requires explicit re-ratification before reuse |

## Surface Registry

| Surface | Tier | Safe Use In `SC_STORYOPS` | Representative Anchors | Notes |
| --- | --- | --- | --- | --- |
| `01_WORLD_BIBLE/00_CORE_FOUNDATION` | hard authority | ontology, definitions, lexicon, conlang, and base universe claims | `00_SERIES_BIBLE.md`, `01_KEY_CONCEPTS.md`, `02_DEFINITIONS.md`, `03_LEXICON_OF_NOESIS.md`, `SOMATIC_CANTICLES_CONLANG.md` | overrides downstream convenience docs when terminology conflicts |
| `01_WORLD_BIBLE/01_PROTOCOLS_AND_SYSTEMS` | hard authority | protocol logic, embodied-system rules, witness method, and symbolic-lens framing | `00_TRYAMBAKAM_PROTOCOL.md`, `01_BIOLOGICAL_STYLE_GUIDE.md`, `03_ALETHEOS_NARRATIVE_WEAVER_SYSTEM.md`, `The_13_Symbolic_Lenses.md` | governs method and scene mechanics more directly than later explanatory layers |
| `01_WORLD_BIBLE/02_CHARACTER_SYSTEM` | hard authority | cast, arcs, territories, and relationship pressure | `02-SOMANAUT-TEAM-ROSTER.md`, `TRILOGY-CHARACTER-ARCS.md`, `CONSCIOUSNESS_TERRITORIES.md`, `CHARACTER-SYSTEM-MAP.md` | `HOUSE_POLITICS.md`, `FAMILY_TREES_V2.md`, and `CULTURAL_MUSIC_DATABASE.md` are safe for pressure and asymmetry, but pair them with `04_WORLD_BUILDING` or editorial sources before turning them into macro-governance obligations |
| `01_WORLD_BIBLE/03_TECHNOLOGY` | review-required support | technical vocabulary, scene mechanics, diagnostic metaphors, and system texture | `Bio_Engineering/The_Stages_of_Ripening.md`, `Consciousness_Interfaces/The_Neural_Bridge_Protocols.md`, `Quantum_Systems/Quantum_Telemetry_Diagnostics.md`, `System_Operations/WitnessOS_Core_Architecture.md`, `System_Operations/The_Severance_Sequence.md` | useful and often strong, but do not let an isolated tech doc silently define canon stakes by itself |
| `01_WORLD_BIBLE/04_WORLD_BUILDING` | review-required support | governance, cultures, macro stakes, and symbolic-biological mapping | `00_GALACTIC_FEDERATION_CHARTER.md`, `01_GALACTIC_FEDERATION_TRANSFORMATION_PLAN.md`, `THREE_BODY_KINGDOM_INTEGRATION.md`, `04_TAROT_BIOLOGICAL_EVENT_MAP.md` | especially important for `Book 3`, but must be cross-checked before it hardens chapter obligations |
| `01_WORLD_BIBLE/05_VISUALIZATIONS` | support-only / navigation | motif recall, relationship mapping, and system compression | `01_KHALOREE_SYSTEMS.md`, `02_TECHNOLOGY_MAP.md`, `07_SYSTEM_DIAGRAMS.md`, `Somanaut_Extraction_Storyboard.md` | use to remember structure or recover handles, not to settle lore disputes alone |
| `01_WORLD_BIBLE/05_LEGACY_ARCHIVES` | legacy / do not import blindly | historical comparison only | `LEGACY-ARCHETYPES.md` | only reuse after explicit re-ratification into a hard-authority or review-required surface |
| `01_WORLD_BIBLE/06_PHILOSOPHICAL_ENGINE` | support-only / navigation | brand axioms, thematic guardrails, and reader-intent framing | `README.md` | useful for alignment, not for novel-specific factual claims until promoted into editorial or core/protocol surfaces |
| `01_WORLD_BIBLE/07_META_NARRATIVE_SYSTEM` | support-only / navigation | engagement model, witness-agent framing, and pacing posture | `README.md` | meta-delivery guidance, not automatic in-world canon |
| `01_WORLD_BIBLE/08_ARTIFACT_PROTOCOLS` | support-only / navigation | artifact ideas, transmedia bridges, and symbolic interfaces | `README.md` | may influence companion or artifact work, but should not silently create story obligations |

## File-Level Overrides

| File Or Surface | Use Posture | Why |
| --- | --- | --- |
| `01_WORLD_BIBLE/README.md` and `01_WORLD_BIBLE/README_NAVIGATOR.md` | support-only / navigation | master orientation docs; useful for route-finding, not sole lore proof |
| `01_WORLD_BIBLE/00_CORE_FOUNDATION/world_bible_registry.json` | support-only / navigation | machine index of domains and files; not a prose authority by itself |
| `01_WORLD_BIBLE/00_CORE_FOUNDATION/somatic_canticles_data_tapestry.json` | support-only / navigation | retrieval graph for pattern search, not a canon statement on its own |
| `01_WORLD_BIBLE/00_CORE_FOUNDATION/somatic_canticles_lore_data.json` and `somatic_canticles_trilogy_data.json` | support-only / navigation | structured data aids that still need human and textual corroboration |
| `01_WORLD_BIBLE/00_CORE_FOUNDATION/DATA_ARCHITECTURE_STRATEGY.md` | support-only / navigation | process doc for data handling, not a story-law file |
| any directory `README.md` under `01_WORLD_BIBLE/` | support-only / navigation unless already covered by a harder file | directory context does not outrank the specific source files it introduces |

## Intake Rules

- Start with hard authority before using lower tiers.
- When `03_TECHNOLOGY` or `04_WORLD_BUILDING` introduces something stronger or more interesting than the hard-authority layer, mark it `review-required` in intake notes instead of silently promoting it.
- Use `05_VISUALIZATIONS` and the meta directories to recover motifs, structure, or handles; then chase the supporting claim back into a harder text source.
- Do not let legacy or navigation surfaces create new chapter obligations by accident.
- For `Book 3` macro-governance work especially, require one hard-authority source family plus one corroborating support surface before anything moves from concept registry into packet-level scaffolding.
