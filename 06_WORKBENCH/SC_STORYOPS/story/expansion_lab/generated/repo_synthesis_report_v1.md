# Repo Synthesis Report v1  

---

## 1. Canon Baseline  

| Source | Path | Role in Canon |
|--------|------|---------------|
| Compiled Book 1 | `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md` | Canonical text for Book 1 (diagnosis). |
| Compiled Book 2 | `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md` | Canonical text for Book 2 (integration). |
| Compiled Book 3 | `02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md` | Canonical text for Book 3 (liberation). |
| Omnibus Clean | `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` | Full‑trilogy reference, used for cross‑book consistency checks. |
| Editorial Brief | `03_EDITORIAL/EDITORIAL_BRIEF.md` | Governs tone, terminology, and high‑level narrative goals. |
| Master Style Sheet | `03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md` | Enforces spelling, capitalization, and stylistic conventions. |
| World‑Bible Authority Registry | `06_WORKBENCH/SC_STORYOPS/story/intake/world_bible_authority_registry.md` | Defines world‑building facts that must not be contradicted. |
| Chapter Summaries | `06_WORKBENCH/SC_STORYOPS/story/chapter_summaries.md` | Provides the canonical plot beats for each chapter. |
| Outline (macro thesis) | `06_WORKBENCH/SC_STORYOPS/story/outline.md` | Macro structure (27 chapters, 3 books) and thematic arcs. |
| Character Arcs | `01_WORLD_BIBLE/02_CHARACTER_SYSTEM/TRILOGY-CHARACTER-ARCS.md` | Canonical character trajectories and Khalorēē axioms. |
| Dialogue Voice Matrix | `06_WORKBENCH/SC_STORYOPS/story/dialogue_voice_matrix.md` | Canonical voice constraints for each Somanaut. |
| Book Rules (precedence) | `06_WORKBENCH/SC_STORYOPS/story/book_rules.md` | Hierarchy of source authority; must be obeyed for any conflict resolution. |

**Canonical baseline** = the compiled manuscripts plus the StoryOps control surfaces (outline, chapter summaries, character arcs, dialogue matrix) and the editorial authority (brief + style sheet). No edits may be made directly to the compiled files; all expansion work must be staged in `02_MANUSCRIPTS/CHAPTERS/` and validated against the above surfaces.

---

## 2. Control Surfaces That Must Govern Expansion  

1. **StoryOps Control Surfaces** (must be consulted for every chapter):  
   - `06_WORKBENCH/SC_STORYOPS/story/outline.md`  
   - `06_WORKBENCH/SC_STORYOPS/story/chapter_summaries.md`  
   - `06_WORKBENCH/SC_STORYOPS/story/book_rules.md` (precedence hierarchy)  
   - `06_WORKBENCH/SC_STORYOPS/story/dialogue_voice_matrix.md`  
   - `06_WORKBENCH/SC_STORYOPS/story/character_matrix.md` (if present)  

2. **Editorial Authority Surfaces** (override any StoryOps conflict):  
   - `03_EDITORIAL/EDITORIAL_BRIEF.md`  
   - `03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md`  

3. **World‑Bible Authority Registry** (non‑negotiable world facts):  
   - `06_WORKBENCH/SC_STORYOPS/story/intake/world_bible_authority_registry.md`  

4. **Chapter Expansion Matrix** (guides the quantitative and qualitative growth targets):  
   - `06_WORKBENCH/SC_STORYOPS/story/expansion_lab/chapter_expansion_matrix.md`  

These four families constitute the **Control Plane**. All downstream drafting, model selection, and validation must reference them explicitly.

---

## 3. Source Tier Understanding  

| Tier | Root Path | Primary Value | Filtering Guidance |
|------|-----------|---------------|--------------------|
| **Tier A – Primary External Substrate** | `/Volumes/madara/2026/tgw-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/content/posts` | 94 clean, thematically clustered blog posts (endocrine, consciousness, pattern). Highest‑value for “world‑pressure”, “lore embodiment”, and “somatic rhythm”. | Use whole posts; extract paragraphs that map to “Layer gaps” in the matrix. No additional filtering needed. |
| **Tier B – Vision‑First Multimodal** | `/Users/sheshnarayaniyer/Documents/noesis/Research` | 4 text files + 106 images (screenshots, pasted images). Provides visual metaphors, diagrammatic schematics, and research‑style footnotes. | Treat as **support only**; images may be described in prose but not inserted verbatim unless editorial brief permits. |
| **Tier C – Filtered Vault Support** | `/Volumes/madara/2026/tgw-vault/03-Resources` | 5 361 text‑like files, 2 113 images, 6 631 other assets. Very noisy; contains useful “protocol” excerpts, scientific references, and background lore. | Aggressive keyword filtering (e.g., “endocrine”, “bio‑acoustic”, “Khalorēē”). Only use files that are cross‑referenced in the world‑bible or appear in the blog clusters. |
| **Tier D – Area‑Notebook Concepts** | `/Volumes/madara/2026/tgw-vault/02-Areas` | 415 text files, many daily logs. Holds brainstorming concepts, early world‑building sketches. | Exclude daily‑log noise; admit only entries that have been **review‑required** flagged in `book_rules.md` or that appear in the blog after cross‑validation. |

**Rule:** Tier A is the *strongest* external source and must be the first point of reference for any expansion deficit. Tier B may be used for visual or research‑style enrichment. Tiers C/D are only admissible after they have been filtered and validated against the canonical authority registry.

---

## 4. Book‑by‑Book Deepening Opportunities  

| Book | Chapters (from outline) | Primary Deficits (matrix) | High‑Impact Source Families (from matrix) | Suggested Deepening Angle |
|------|------------------------|---------------------------|--------------------------------------------|--------------------------|
| **Book 1 – The Anamnesis Engine** | 01‑08 | Immersion, biological dread dwell, inherited‑pattern embodiment, endocrine doctrine elasticity, lineage legacy | *Book 1 editorial tasks*, *biological style guide*, *consciousness‑architecture blog cluster*, *lineage/captivity/legacy‑code surfaces* | Expand the **somatic rhythm** of the field collapse (Ch 1‑3) using blog posts on “biological dread”. Flesh out **lineage** in Ch 4‑5 with legacy‑code excerpts (filtered from Tier C). Add **post‑event aftermath** in Ch 6‑8 via endocrine‑blog paragraphs. |
| **Book 2 – The Myocardial Chorus** | 09‑15 | Sanctuary‑memory pacing, membrane conflict, pain‑signal dynamics, breath‑field inheritance, meaning‑relationship consequence, witness integration | *pain‑information*, *signal‑state‑story*, *barrier/protection world‑bible*, *breath and coherence surfaces*, *compass/calibration* | Deepen **pain‑signal** language in Ch 9‑11 using Tier A blog posts on “signal state”. Use **breath‑field** imagery (Tier A “breath” cluster) for Ch 7‑8. Integrate **compass calibration** concepts (Tier C filtered) into Ch 8. |
| **Book 3 – The Ripening** | 16‑25 | Regression pressure aftermath, Gardener encounter dwell, regression‑pressure, distributed witness consequence, governance pressure, final procedural authorship | *Gardener dossier*, *strategic deception images*, *legacy‑code*, *three‑body governance*, *wilt dossier*, *concealed‑truth cluster* | Leverage **Gardener dossier** (Tier C filtered) to flesh out Ch 17‑18. Use **three‑body governance** sources for Ch 14‑15. Expand **regression aftermath** in Ch 16‑17 with “wilt” and “concealed‑truth” assets. Emphasize **procedural authorship** in Ch 24‑25 via visual schematics from Tier B. |

**Overall:** Each book’s expansion should respect the *layer gaps* (world, relationships, meaning, etc.) identified in the matrix and draw primarily from the Tier A blog clusters that map to those gaps. Tier C/D material is only supplemental after cross‑validation.

---

## 5. Chapter Cluster Priorities  

| Chapter | Target Word Band | Primary Deficit | Layer Gaps | Top 2 Source Families (Tier A) | Draft Model | Control Pass |
|--------|------------------|----------------|-----------|-------------------------------|-------------|--------------|
| 01 | 3200‑4200 | Immersion & biological dread dwell | World, Mystery, Prose | **Consciousness‑architecture blog**, **Endocrine‑pressure cluster** | `moonshotai/kimi-k2-instruct` | `openai/gpt-oss-120b` |
| 04 | 3000‑3800 | Inherited‑pattern embodiment | Character, World, Prose | **Lineage / captivity / legacy‑code** (filtered) | `moonshotai/kimi-k2-instruct` | `nvidia/nemotron-3-super-120b-a12b` |
| 07 | 3600‑4600 | Breathfield world inheritance | World, Relationships | **Breath & coherence surfaces**, **Visual archive (Tier B)** | `moonshotai/kimi-k2-instruct` | `openai/gpt-oss-120b` |
|
