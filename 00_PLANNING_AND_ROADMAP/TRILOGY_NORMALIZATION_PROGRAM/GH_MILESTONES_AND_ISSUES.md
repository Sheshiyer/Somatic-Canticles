# GitHub Milestones and Issues

**Repo:** `Sheshiyer/Somatic-Canticles`  
**Program:** Compiled Trilogy Normalization  
**Tracking model:** one issue, one owner, one branch/worktree, dependency-visible bodies

---

## Label Families

Recommended labels for this program:

- `phase:p1`
- `phase:p2`
- `phase:p3`
- `wave:w1`
- `wave:w2`
- `wave:w3`
- `wave:w4`
- `wave:w5`
- `wave:w6`
- `wave:w7`
- `wave:w8`
- `swarm:canon`
- `swarm:matter`
- `swarm:book1`
- `swarm:book2`
- `swarm:book3`
- `swarm:assembly`
- `swarm:qa`
- `area:editorial`
- `area:canon`
- `area:manuscript`
- `area:release`
- `agent:codex`
- `status:planned`
- `status:ready`
- `status:blocked`
- `status:in-progress`
- `status:in-review`
- `status:done`

If label creation is deferred, keep the same identifiers in issue bodies.

---

## Milestones

### Milestone M1

- **Title:** `SC M1 — Canon + Matter Freeze`
- **GitHub milestone number:** `1`
- **Purpose:** freeze doctrine and vocabulary, then normalize frontmatter/preface/backmatter/glossary before chapter work.

### Milestone M2

- **Title:** `SC M2 — Compiled Book Normalization`
- **GitHub milestone number:** `2`
- **Purpose:** calibrate from Book 3, then normalize Books 1–3 at the compiled-manuscript level.

### Milestone M3

- **Title:** `SC M3 — Omnibus + Release Readiness`
- **GitHub milestone number:** `3`
- **Purpose:** rebuild omnibus, run trilogy QA, and leave a durable handoff for downstream use.

---

## Tracker Issue

### SC-000

- **Title:** `[P1][W1][canon] SC-000 — Trilogy normalization program tracker`
- **GitHub issue:** `#1`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Owner role:** planner / orchestrator
- **Owner agent:** codex
- **Purpose:** top-level tracker for milestone status, wave summaries, linked issues, and restart notes.

Acceptance:
- references every issue in this program,
- carries wave-open and wave-close summary comments,
- records milestone progress and blocked edges.

Validation:
- tracker links to all milestones/issues,
- wave status remains current.

Branch:
- `plan/sc-000-program-tracker`

---

## Milestone 1 Issues

### SC-001

- **Title:** `[P1][W1][canon] SC-001 — Freeze trilogy editorial doctrine`
- **GitHub issue:** `#2`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `canon`
- **Area:** `editorial`
- **Owner role:** editorial doctrine owner
- **Dependencies:** `SC-000`
- **Branch:** `editorial/sc-001-doctrine-freeze`

Deliverable:
- doctrine document that defines allowed register, banned/demoted language, embedded-reference rules, and calibration sources.

Acceptance:
- explicitly names the preferred Noesis register,
- resolves authorship vs awakening language,
- documents how Easter eggs should function,
- identifies current canon sources and deprecated sources.

Validation:
- doctrine references the current brand docs and Content Engine pieces,
- doctrine is sufficient to guide matter rewrites without chat context.

### SC-002

- **Title:** `[P1][W1][canon] SC-002 — Build compiled-trilogy vocabulary replacement map`
- **GitHub issue:** `#3`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `canon`
- **Area:** `canon`
- **Owner role:** terminology owner
- **Dependencies:** `SC-001`
- **Branch:** `editorial/sc-002-vocabulary-map`

Deliverable:
- vocabulary map defining what survives, what is reframed, what is removed, and what becomes implicit.

Acceptance:
- covers old vs current Noesis vocabulary,
- includes examples from matter and books,
- distinguishes allowed technical language from over-explicit exposition.

Validation:
- map can be applied consistently across Books 1–3,
- map resolves known stale terms in `Backmatter.md`, `Glossary.md`, and chapter scaffolding.

### SC-003

- **Title:** `[P1][W1][canon] SC-003 — Audit compiled matter against the doctrine`
- **GitHub issue:** `#4`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `canon`
- **Area:** `manuscript`
- **Owner role:** editorial auditor
- **Dependencies:** `SC-001`, `SC-002`
- **Branch:** `editorial/sc-003-matter-audit`

Deliverable:
- file-by-file audit for `Frontmatter.md`, `Preface.md`, `Backmatter.md`, and `Glossary.md`.

Acceptance:
- identifies exact misalignments,
- calls out obsolete brand shells and meta-commentary,
- provides rewrite targets per file.

Validation:
- every matter file has a tracked delta between current state and doctrine target.

### SC-004

- **Title:** `[P1][W2][matter] SC-004 — Rewrite Frontmatter.md in the current Noesis register`
- **GitHub issue:** `#5`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `matter`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-003`
- **Branch:** `editorial/sc-004-frontmatter`

Deliverable:
- normalized `02_MANUSCRIPTS/COMPILED/Frontmatter.md`

Acceptance:
- aligns with the doctrine,
- avoids soft spiritual framing,
- introduces the trilogy without obsolete shells or diluted language.

Validation:
- doctrine and vocabulary map checks pass,
- file reads cleanly as the trilogy’s entry surface.

### SC-005

- **Title:** `[P1][W2][matter] SC-005 — Rewrite Preface.md without legacy meta-commentary drift`
- **GitHub issue:** `#6`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `matter`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-003`
- **Branch:** `editorial/sc-005-preface`

Deliverable:
- normalized `02_MANUSCRIPTS/COMPILED/Preface.md`

Acceptance:
- removes recovered-artifact drift where it weakens authorship,
- removes “process is the author” framing,
- preserves seriousness and invitation without coddling.

Validation:
- preface matches the current Noesis message architecture,
- no obsolete or demoted terms remain without intent.

### SC-006

- **Title:** `[P1][W2][matter] SC-006 — Rewrite Backmatter.md around current brand and canon`
- **GitHub issue:** `#7`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `matter`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-003`
- **Branch:** `editorial/sc-006-backmatter`

Deliverable:
- normalized `02_MANUSCRIPTS/COMPILED/Backmatter.md`

Acceptance:
- removes `The Why Chromosome`, old domain references, stale counts, and legacy explanatory frame,
- reframes the trilogy’s relationship to Noesis and related work without overt product copy,
- leaves subtle ecosystem recognitions only where earned.

Validation:
- no obsolete links or legacy brand references remain,
- backmatter is compatible with web/mobile source-of-truth use.

### SC-007

- **Title:** `[P1][W2][matter] SC-007 — Rewrite Glossary.md to match the new doctrine`
- **GitHub issue:** `#8`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `matter`
- **Area:** `canon`
- **Owner role:** glossary editor
- **Dependencies:** `SC-002`, `SC-003`
- **Branch:** `editorial/sc-007-glossary`

Deliverable:
- normalized `02_MANUSCRIPTS/COMPILED/Glossary.md`

Acceptance:
- glossary entries match the doctrine and current Noesis distinctions,
- transitional or obsolete entries are removed or reframed,
- explanatory language is precise and non-promotional.

Validation:
- glossary terms align with compiled-book usage targets,
- no old-system explanation survives by accident.

### SC-008

- **Title:** `[P1][W3][qa] SC-008 — Perform matter consistency QA and freeze Milestone 1 outputs`
- **GitHub issue:** `#9`
- **Milestone:** `SC M1 — Canon + Matter Freeze`
- **Swarm:** `qa`
- **Area:** `editorial`
- **Owner role:** validation reviewer
- **Dependencies:** `SC-004`, `SC-005`, `SC-006`, `SC-007`
- **Branch:** `editorial/sc-008-matter-qa`

Deliverable:
- QA report for all matter files and a freeze note for chapter work.

Acceptance:
- matter files are mutually consistent,
- doctrine/vocabulary assumptions are recorded,
- open risks for book-level normalization are named.

Validation:
- grep-based stale-term checks pass,
- restart package updated with M1 state.

---

## Milestone 2 Issues

### SC-009

- **Title:** `[P2][W4][canon] SC-009 — Extract Book 3 tonal calibration for trilogy normalization`
- **GitHub issue:** `#10`
- **Milestone:** `SC M2 — Compiled Book Normalization`
- **Swarm:** `book3`
- **Area:** `editorial`
- **Owner role:** calibration analyst
- **Dependencies:** `SC-008`
- **Branch:** `editorial/sc-009-book3-calibration`

Deliverable:
- calibration note defining what Book 3 already gets right and what to propagate backward.

Acceptance:
- identifies prose, exposition, and system-behavior patterns to preserve,
- distinguishes reusable tone from Book 3-specific plot behavior.

Validation:
- calibration note is explicit enough to drive Book 1 and Book 2 rewrites.

### SC-010

- **Title:** `[P2][W4][book1] SC-010 — Normalize Book 1 compiled manuscript`
- **GitHub issue:** `#11`
- **Milestone:** `SC M2 — Compiled Book Normalization`
- **Swarm:** `book1`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-008`, `SC-009`
- **Branch:** `editorial/sc-010-book1-normalization`

Deliverable:
- normalized `Book_1_Anamnesis_Engine.md`

Acceptance:
- removes or integrates overt metadata scaffolding,
- reduces legacy system-dossier behavior,
- preserves system richness while restoring dramatic reality.

Validation:
- stale vocabulary sweep passes,
- doctrine alignment pass completed with noted exceptions.

### SC-011

- **Title:** `[P2][W5][book2] SC-011 — Normalize Book 2 compiled manuscript`
- **GitHub issue:** `#12`
- **Milestone:** `SC M2 — Compiled Book Normalization`
- **Swarm:** `book2`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-008`, `SC-009`
- **Branch:** `editorial/sc-011-book2-normalization`

Deliverable:
- normalized `Book_2_The_Myocardial_Chorus.md`

Acceptance:
- removes heavy dossier/explainer scaffolding,
- sharpens the Noesis register,
- keeps the emotional and symbolic structure intact.

Validation:
- stale vocabulary sweep passes,
- cross-check against Book 1 and Book 3 calibration completed.

### SC-012

- **Title:** `[P2][W6][book3] SC-012 — Perform light normalization pass on Book 3`
- **GitHub issue:** `#13`
- **Milestone:** `SC M2 — Compiled Book Normalization`
- **Swarm:** `book3`
- **Area:** `manuscript`
- **Owner role:** manuscript editor
- **Dependencies:** `SC-010`, `SC-011`
- **Branch:** `editorial/sc-012-book3-light-pass`

Deliverable:
- lightly normalized `Book_3_The_Ripening.md`

Acceptance:
- removes residual diagnostic/instructional artifacts,
- trims stale wording without destabilizing the strongest current tone.

Validation:
- calibration remains intact,
- residual artifact sweep passes.

### SC-013

- **Title:** `[P2][W6][qa] SC-013 — Run cross-book doctrine and terminology consistency sweep`
- **GitHub issue:** `#14`
- **Milestone:** `SC M2 — Compiled Book Normalization`
- **Swarm:** `qa`
- **Area:** `canon`
- **Owner role:** validation reviewer
- **Dependencies:** `SC-010`, `SC-011`, `SC-012`
- **Branch:** `editorial/sc-013-trilogy-consistency`

Deliverable:
- trilogy-wide consistency report across compiled books.

Acceptance:
- term drift and doctrine drift are identified and resolved,
- remaining intentional deviations are documented.

Validation:
- grep-based term checks and targeted readthrough checks pass.

---

## Milestone 3 Issues

### SC-014

- **Title:** `[P3][W7][assembly] SC-014 — Rebuild omnibus from normalized compiled sources`
- **GitHub issue:** `#15`
- **Milestone:** `SC M3 — Omnibus + Release Readiness`
- **Swarm:** `assembly`
- **Area:** `release`
- **Owner role:** build editor
- **Dependencies:** `SC-013`
- **Branch:** `editorial/sc-014-omnibus-rebuild`

Deliverable:
- regenerated `Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`

Acceptance:
- omnibus reflects normalized books and matter,
- no stale backmatter/glossary payload is carried forward.

Validation:
- omnibus spot checks pass against source files,
- stale-term sweep passes on omnibus output.

### SC-015

- **Title:** `[P3][W8][qa] SC-015 — Run trilogy-wide final continuity and language QA`
- **GitHub issue:** `#16`
- **Milestone:** `SC M3 — Omnibus + Release Readiness`
- **Swarm:** `qa`
- **Area:** `editorial`
- **Owner role:** final reviewer
- **Dependencies:** `SC-014`
- **Branch:** `editorial/sc-015-final-qa`

Deliverable:
- final QA report covering matter, books, and omnibus.

Acceptance:
- continuity risks documented,
- doctrine adherence documented,
- downstream source-of-truth suitability confirmed.

Validation:
- targeted readthrough and grep-based checks pass,
- all milestone outputs referenced in the report.

### SC-016

- **Title:** `[P3][W8][assembly] SC-016 — Write release handoff and downstream source-of-truth note`
- **GitHub issue:** `#17`
- **Milestone:** `SC M3 — Omnibus + Release Readiness`
- **Swarm:** `assembly`
- **Area:** `release`
- **Owner role:** handoff owner
- **Dependencies:** `SC-015`
- **Branch:** `editorial/sc-016-release-handoff`

Deliverable:
- release/handoff note documenting what changed, what is canonical, and how downstream consumers should ingest it.

Acceptance:
- identifies source-of-truth files,
- identifies residual caveats,
- explains how a new agent or human should resume or extend the work.

Validation:
- references the final files and QA report,
- restart instructions are complete.

---

## Wave Comment Protocol

At wave start, add a tracker comment with:

- wave goal,
- included issue IDs,
- dependencies,
- lock zones,
- expected evidence for completion.

At wave close, add a tracker comment with:

- completed issues,
- deferred issues,
- validation evidence,
- doctrine changes,
- blockers for the next wave.

---

## Branch and Worktree Rule

One issue should map to one branch/worktree.

Recommended branch pattern:

- `editorial/sc-001-doctrine-freeze`
- `editorial/sc-004-frontmatter`
- `editorial/sc-010-book1-normalization`

Do not overlap multiple active issue branches on the same compiled manuscript file unless a wave boundary explicitly re-plans the lock zone.
