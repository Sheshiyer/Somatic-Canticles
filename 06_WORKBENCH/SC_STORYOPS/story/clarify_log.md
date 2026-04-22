# Clarify Log

## Locked Decisions

### CL-001: Canonical chapter count

- Decision: the active canonical manuscript count is `27` chapters.
- Evidence:
  - `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`
  - `02_MANUSCRIPTS/CHAPTERS/BOOK_3_THE_RIPENING/Chapter-27-The-New-Beginning.md`
- Impact:
  - any doc still claiming `26` or `22` chapters is non-authoritative until corrected.

### CL-002: Arcana vs chapter policy

- Decision: the `22`-card arcana system is a supporting visual and conceptual taxonomy, not a current one-to-one chapter-count contract.
- Temporary policy:
  - chapter canon remains `27`,
  - arcana assets remain `22`,
  - downstream copy must stop saying `22 chapters mapped to Major Arcana` unless a future remap explicitly restores that contract.
- Impact:
  - visual families can still guide motif work,
  - but they cannot currently be treated as exact chapter parity.

### CL-003: Readiness language

- Decision: use dual readiness labels until the source/image mapping loop is complete.
- Approved labels:
  - `canon/export ready`
  - `research/image mapping incomplete`
- Avoid calling the trilogy fully release-ready while the mapping layer remains partial.

### CL-004: Canon vs legacy world-bible policy

- Core canon by default:
  - `03_EDITORIAL` doctrine and calibration files
  - `01_WORLD_BIBLE/00_CORE_FOUNDATION`
  - `01_WORLD_BIBLE/01_PROTOCOLS_AND_SYSTEMS`
  - `01_WORLD_BIBLE/02_CHARACTER_SYSTEM`
- Working canon with review:
  - `01_WORLD_BIBLE/03_TECHNOLOGY`
  - `01_WORLD_BIBLE/04_WORLD_BUILDING`
  - `01_WORLD_BIBLE/05_VISUALIZATIONS`
- Legacy / non-authoritative unless specifically re-ratified:
  - `01_WORLD_BIBLE/05_LEGACY_ARCHIVES`
  - older production plans
  - older overview docs that still claim `26 chapters`, `13 engines`, or pre-doctrine framing

### CL-005: Workbench copy policy

- Decision: all working derivatives inside this folder are sourced from `02_MANUSCRIPTS/CHAPTERS/`.
- Merge-back gate:
  - any future return to canon must compare staged chapter work against current `COMPILED/` text before editing release surfaces.

### CL-006: Sequencing policy for `v0.2`

- Decision: the current cycle is trilogy-wide intake first, book assignment second.
- Operating rule:
  - extract principles from editorial doctrine, world bible, `03-Resources`, Brandmint, and external Noesis research,
  - register them in the intake layer,
  - then project them into book lanes once the fit is defensible.
- Impact:
  - existing Book 2 packets are provisional support material, not the governing scope of the workbench.

## Open Blockers

### BL-001: Downstream copy drift

- Problem: repo-adjacent marketing and wiki docs still claim `22 chapters` and older production states.
- Needed next action: one targeted downstream copy audit after this workbench setup is stable.

### BL-002: World-bible ratification pass

- Problem: the world bible still contains useful but mixed-status material.
- Needed next action: create a canon registry or status legend before using lower-tier docs as hard inputs for prose rewrites.

### BL-003: External image semantics

- Problem: the external Noesis image folder is still mostly uncaptioned.
- Needed next action: continue sampling and tag enough images to support chapter-packet work without false certainty.

### BL-004: Projection freeze

- Problem: concept-to-book fit is still intuitive in many places rather than explicitly justified.
- Needed next action: use `intake/book_projection_board.md` to keep projections soft until source, image, and lore support converge.
