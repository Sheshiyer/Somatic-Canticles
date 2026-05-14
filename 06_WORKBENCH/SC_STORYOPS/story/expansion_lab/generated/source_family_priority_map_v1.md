# Source Family Priority Map v1

## Overview

This artifact maps the four source roots into an operational priority framework for the first expansion wave. It translates the intake rulings and filter spec into execution-order decisions, fast-win identification, noise exclusion targets, and book-specific first-pass families.

---

## 1. Root-by-Root Execution Priority

| Priority | Root | Admissibility | Rationale |
|----------|------|---------------|-----------|
| **1** | `synchronocities-blog/src/content/posts` | `published substrate` | Cleanest, most focused corpus. 94 posts with pre-identified high-signal families. No filtering overhead. Direct chapter-binding capability. |
| **2** | `02-Areas` | `concept support` | Smaller surface (415 files), strong overlap with blog families. Functions as translation layer from blog concepts into tighter internal system language. Low noise floor when Daily-Logs and brand material excluded. |
| **3** | `03-Resources` | `review-required support` | Large corpus (5361 text files) requiring aggressive pre-filtering. High-value slices exist but must be extracted before use. Provides biology, system pressure, and symbolic support that blog and Areas cannot. |
| **4** | `noesis/Research` | `visual support only` | Image-first. Text anchors are minimal context docs. Must not feed text-synthesis lane. Serves multimodal lane only. Lowest priority for first-pass dossier production. |

**Execution constraint**: Roots 1–3 run in parallel on text lanes. Root 4 runs on visual lane independently. Do not gate text-lane progress on visual-lane completion.

---

## 2. Fastest Wins for Dossier Production

These families can be ingested, filtered, and bound to chapter dossiers with minimal friction.

### Fast Win Set A — Blog Substrate (No Filtering Required)

| Family | Post Count | Dossier Value |
|--------|------------|---------------|
| `pattern` | 11 | Pattern-recognition framework, cross-reference system, bioelectric mapping |
| `consciousness` | 9 | Consciousness architecture hub, legacy code, runtime diagrams, three-layer stack |
| `runtime` | 6 | Compassion-runtime, runtime-of-god, sacred-runtime ancient debugging |
| `endocrine` | 6 | Endocrine constellation patterns, nine-muses endocrine system, muse integration |
| `muse` | 5 | Muse-enneagram matrix, endocrine-muse integration |
| `debug` | 3 | Ancient debugging protocols, signal-state story debug edition |

**Why fast**: These families are already identified, post-counted, and slug-mapped. No directory traversal, no exclusion logic, no review-required gating. Bind directly to chapter groups.

### Fast Win Set B — 02-Areas Default Include (Low Noise, Pre-Filtered)

| Directory | File Count | Dossier Value |
|-----------|------------|---------------|
| `Consciousness-Models` | 17 | Pain-Information-Architecture, Bioelectric-Pattern-Framework, mitochondrial-subconsciousness |
| `Pattern-Studies` | 21 | Pattern-recognition hub, Lorenz-Kundli mapping |
| `Technical-Mystical-Integration` | 45 | HTTP-Status-Codes Mental States, Reptilian-BIOS Architecture, Unix-Guide-to-Consciousness, Word-as-Code |
| `Muse-Enneagram-Framework` | 8 | Endocrine-constellation pattern, muse-enneagram matrix, spolski-endocrine correspondence |

**Why fast**: Explicitly listed as default-include in filter spec. No review-required gating. Strong conceptual overlap with blog families enables direct cross-referencing.

### Fast Win Set C — 03-Resources Default Include (Biology/System Pressure)

| Directory | File Count | Dossier Value |
|-----------|------------|---------------|
| `Consciousness-Studies` | ~161 | TWC-style prose-adjacent material, consciousness framing, metaphysical register |
| `General-Research` | 202 | Neuromodulation, wireless-body-area-network material |
| `Health/Hormonal-Health` | subset of 774 | Endocrine and stress-axis embodiment |
| `Design` | subset | Vision lane only; image captions for bioelectric/circuitry motifs |

**Why fast (conditional)**: These directories are default-include but still require directory-level filtering before ingestion. Once `Social-Inbox` and `website-downloader-tool` are excluded, the remaining slices are clean enough for first-pass binding.

---

## 3. Highest-Risk Noise Families to Exclude Aggressively

These families must be blocked at the filter level before any parallel wave begins. Ingesting them wastes processing cycles and introduces contamination that corrupts prose tone.

### Tier 1 — Hard Excludes (Block at Root Level)

| Family | File Count | Risk Type |
|--------|------------|-----------|
| `Social-Inbox` | 4148 | Social noise, operational detritus, zero narrative value |
| `website-downloader-tool` | 2131 | Scraped operational HTML, no prose quality, machine-generated noise |
| `Websites` | unspecified | Scraped operational HTML, continuation of downloader-tool contamination |
| `Daily-Logs` | 210 | Journal drift, personal narrative, first-person operational notes |
| `TheWhyChromosome-Brand` | 58 | Brand/marketing material, non-story surface |

**Filter action**: Add all Tier 1 families to `excluded_dirs` in filter spec. Block at directory traversal, not at file level.

### Tier 2 — Conditional Excludes (Block Unless Explicit Chapter Justification)

| Family | File Count | Risk Type |
|--------|------------|-----------|
| `Tetryonics-Integration` | 1444 | High-volume proprietary system; may introduce unsupported physics ontology |
| `Alternative-Science` | 327 | Risk of lore-dump inflation; requires chapter-local justification before use |
| `Occult` | 661 | Symbolic pressure exists but may overwhelm narrative voice if over-ingested |
| `Critical-Thinking` | unspecified | Meta-commentary surface, not story substrate |
| `Knowledge/Research` | unspecified | Overlapping with General-Research but noisier; gate behind review-required |
| `Bioelectric-Body` | 40 (sparse) | Useful concept but shallow at first scan; defer until deeper Areas
