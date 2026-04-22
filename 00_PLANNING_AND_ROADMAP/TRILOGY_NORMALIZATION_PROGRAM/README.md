# Somatic Canticles Trilogy Normalization Program

**Created:** 2026-04-21  
**Repo:** `Sheshiyer/Somatic-Canticles`  
**Program status:** Milestone 1 complete; Milestone 2 underway  
**Canonical manuscript surface:** `02_MANUSCRIPTS/COMPILED/`

## Live GitHub State

- Tracker issue: `#1` — `SC-000`
- Milestone `#1`: `SC M1 — Canon + Matter Freeze`
- Milestone `#2`: `SC M2 — Compiled Book Normalization`
- Milestone `#3`: `SC M3 — Omnibus + Release Readiness`

---

## Purpose

This program turns the approved normalization strategy for the compiled Somatic Canticles books into a restart-safe execution package that survives chat loss, agent turnover, and branch changes.

The core objective is to normalize the trilogy so the compiled books:

- speak in the current Noesis register,
- stop carrying obsolete brand shells and legacy explanatory language,
- preserve complexity without collapsing into glossary-on-page exposition,
- and become the stable manuscript source of truth for downstream web and mobile surfaces.

---

## Source of Truth

### Editorial source of truth

- `02_MANUSCRIPTS/COMPILED/`
- `03_EDITORIAL/TRILOGY_EDITORIAL_DOCTRINE.md`
- `03_EDITORIAL/TRILOGY_VOCABULARY_REPLACEMENT_MAP.md`
- `03_EDITORIAL/TRILOGY_MATTER_AUDIT.md`
- `03_EDITORIAL/TRILOGY_BOOK3_TONAL_CALIBRATION.md`
- current Noesis voice/messaging docs in `01-Projects/tryambakam-noesis/brand-docs-final/tryambakam-noesis-aleph/`
- current Content Engine reference pieces under `01-Projects/Content-Engine/_processing/`

### Deprecated or secondary inputs

- `02_MANUSCRIPTS/CLEAN/` is deprecated and should not be used as a live manuscript source.
- chapter working files under `02_MANUSCRIPTS/CHAPTERS/` can inform rewrites, but compiled outputs remain canonical.
- legacy skill references that still assume `13 Symbolic Lenses` or old `CLEAN/` routing must not override the current editorial doctrine.

---

## Program Outcomes

By the end of this program:

1. `TRILOGY_EDITORIAL_DOCTRINE.md` will define the active normalization authority.
2. A trilogy-wide vocabulary replacement map will exist and govern chapter rewrites.
3. A durable compiled-matter audit will define exact rewrite targets for `Frontmatter.md`, `Preface.md`, `Backmatter.md`, and `Glossary.md`.
4. `Frontmatter.md`, `Preface.md`, `Backmatter.md`, and `Glossary.md` will reflect current Noesis doctrine.
5. A durable Book 3 tonal calibration note will define what propagates backward into Books 1 and 2.
6. Book 1 and Book 2 will be normalized out of legacy dossier/explainer mode.
7. Book 3 will be lightly normalized against the same doctrine.
8. The omnibus will be regenerated from normalized compiled sources.
9. GitHub milestones/issues will provide resumable execution state outside the chat.

---

## Editorial Doctrine Summary

The normalization pass should favor:

- authorship over awakening language,
- Kha-Ba-La as governing architecture rather than decorative jargon,
- `16 engines` over older counting systems,
- upstream/downstream and source-writing over generic self-help phrasing,
- sovereignty, rigor, and non-coddling precision,
- subtle embedded recognitions over overt productized meta-commentary.

The pass should demote or remove:

- `journey`, `healing`, `authentic self`, `higher self`,
- `the process is the author`,
- recovered-artifact framing that weakens authorship,
- obsolete shells such as `The Why Chromosome`,
- and system-dump scaffolding that belongs in notes rather than the novel surface.

---

## Milestones

### Milestone 1 — Canon + Matter Freeze

Goal:
- lock the editorial doctrine,
- freeze the vocabulary map,
- and rewrite the trilogy matter so the books have the correct interpretive frame before chapter work begins.

Exit criteria:
- doctrine doc approved,
- vocabulary map approved,
- frontmatter/preface/backmatter/glossary rewritten and internally consistent.

### Milestone 2 — Compiled Book Normalization

Goal:
- use Book 3 as tonal calibration,
- heavily normalize Book 1 and Book 2,
- lightly normalize Book 3,
- and perform a cross-book consistency sweep.

Exit criteria:
- each compiled book conforms to the doctrine,
- stale vocabulary has been reduced or removed,
- overt metadata scaffolding has been eliminated or intentionally retained with rationale.

### Milestone 3 — Omnibus + Release Readiness

Goal:
- regenerate the omnibus,
- run trilogy-wide continuity and language QA,
- and leave a final handoff package for downstream consumers.

Exit criteria:
- omnibus rebuilt from normalized sources,
- trilogy QA completed,
- release/handoff note written with canon assumptions and remaining risks.

---

## Wave Structure

### Phase 1 — Canon + Matter Freeze

#### Wave 1 — Doctrine and contract freeze
- define the editorial doctrine
- define the vocabulary replacement map
- audit compiled matter against the doctrine

#### Wave 2 — Matter rewrite
- rewrite frontmatter
- rewrite preface
- rewrite backmatter
- rewrite glossary

#### Wave 3 — Matter closeout
- perform consistency QA across all matter files
- freeze doctrine inputs for chapter work

### Phase 2 — Book-level normalization

#### Wave 4 — Calibration + Book 1
- extract Book 3 tonal calibration
- normalize Book 1 against the doctrine

#### Wave 5 — Book 2
- normalize Book 2

#### Wave 6 — Book 3 + trilogy sweep
- lightly normalize Book 3
- run a cross-book term and doctrine consistency sweep

### Phase 3 — Assembly + release readiness

#### Wave 7 — Omnibus rebuild
- regenerate the omnibus from normalized compiled sources

#### Wave 8 — QA + handoff
- run trilogy-wide QA
- write release/handoff notes

---

## Restart Protocol

If this chat ends, restart from these artifacts in order:

1. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/RELEASE_HANDOFF.md`
2. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/README.md`
3. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/GH_MILESTONES_AND_ISSUES.md`
4. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/PROCESS_RUNBOOK.md`
5. `tasks/todo.md`
6. the GitHub tracker issue `#1` and the latest milestone comments in `Sheshiyer/Somatic-Canticles`

Then resume from the first issue still marked planned or in-progress.

---

## Current Next Step

Normalization is complete through Milestone 3.

Next downstream action depends on the consumer:
- re-import manuscript content from `02_MANUSCRIPTS/COMPILED/` if a web/mobile or export surface needs the normalized text
- otherwise treat the trilogy corpus as stabilized canon and start from `RELEASE_HANDOFF.md` for any future extension work

- doctrine is established in `03_EDITORIAL/TRILOGY_EDITORIAL_DOCTRINE.md`,
- vocabulary map is established in `03_EDITORIAL/TRILOGY_VOCABULARY_REPLACEMENT_MAP.md`,
- matter audit is established in `03_EDITORIAL/TRILOGY_MATTER_AUDIT.md`,
- Book 3 calibration is established in `03_EDITORIAL/TRILOGY_BOOK3_TONAL_CALIBRATION.md`,
- compiled matter under `02_MANUSCRIPTS/COMPILED/` is frozen as the Milestone 1 interpretive frame,
- next execute `#11` `SC-010` to normalize Book 1 using the doctrine, vocabulary map, and Book 3 calibration.
