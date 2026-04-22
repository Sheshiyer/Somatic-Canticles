# Somatic Canticles Trilogy Normalization Release Handoff

Date: `2026-04-21`
Program scope: compiled manuscript normalization through omnibus rebuild, final QA, and downstream restart packaging.

## Status

The trilogy normalization program is complete through Milestone 3.

Completed end-state:
- compiled matter is normalized
- compiled books are normalized
- the omnibus has been regenerated from canonical sources
- final trilogy QA has been run
- restart-safe local artifacts and GitHub issue state are aligned

## Canonical Manuscript Files

The manuscript source of truth remains `01-Projects/Somatic-Canticles/02_MANUSCRIPTS/COMPILED/`.

Canonical compiled files:
- `02_MANUSCRIPTS/COMPILED/Frontmatter.md`
- `02_MANUSCRIPTS/COMPILED/Preface.md`
- `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md`
- `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md`
- `02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md`
- `02_MANUSCRIPTS/COMPILED/Glossary.md`
- `02_MANUSCRIPTS/COMPILED/Backmatter.md`
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`

Deprecated source:
- `02_MANUSCRIPTS/CLEAN/` is not an active manuscript source and should not be used for downstream ingestion.

## Omnibus Status

`02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` was regenerated on `2026-04-21` from the canonical compiled inputs only, in this order:

1. `Frontmatter.md`
2. `Preface.md`
3. `Book_1_Anamnesis_Engine.md`
4. `Book_2_The_Myocardial_Chorus.md`
5. `Book_3_The_Ripening.md`
6. `Glossary.md`
7. `Backmatter.md`

The rebuilt omnibus no longer carries the stale pre-normalization payload that had persisted in the older derivative file.

## Downstream Ingestion Guidance

If a downstream consumer needs the full trilogy as one file:
- ingest `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`

If a downstream consumer needs the trilogy as modular surfaces:
- ingest the compiled matter files plus the three compiled books from `02_MANUSCRIPTS/COMPILED/`

Rules:
- do not ingest from `02_MANUSCRIPTS/CLEAN/`
- do not reuse any earlier omnibus export cached outside `COMPILED/`
- if a web/mobile surface is intended to reflect the normalized manuscript canon, re-import from `COMPILED/`
- if another application is still wired to an older runtime feed, treat the sync as a separate downstream task; this normalization program did not perform app sync automatically

## Doctrine and Vocabulary Assets That Must Travel With The Manuscripts

If any future editor, exporter, or downstream integrator touches the normalized manuscript corpus, keep these editorial control files alongside the manuscript handoff:
- `03_EDITORIAL/TRILOGY_EDITORIAL_DOCTRINE.md`
- `03_EDITORIAL/TRILOGY_BOOK3_TONAL_CALIBRATION.md`
- `03_EDITORIAL/TRILOGY_VOCABULARY_REPLACEMENT_MAP.md`
- `03_EDITORIAL/TRILOGY_MATTER_AUDIT.md`

These are the control surfaces that explain:
- what language is banned, demoted, or still conditionally allowed
- why Book 3 remains the tonal calibration point
- how matter files were normalized
- how to avoid reintroducing stale Noesis / pre-Noesis framing in future revisions

## Residual Caveats

No blocker-level editorial defects remain from the normalization program.

Non-blocking caveats retained intentionally:
- `WitnessOS` appears once in `Glossary.md` and the omnibus as a historical precursor note under `NOESIS`; it is explanatory, not active doctrine
- some scene-level uses of `healing` and `transformation` remain where they describe concrete narrative conditions rather than the trilogy's governing metaphysics
- `Noetic Network` remains in Book 3 as a Book-3-specific end-state implication and should not be back-propagated into earlier books as a governing frame

## Validation References

Primary local evidence:
- `tasks/todo.md`
- `02_MANUSCRIPTS/README.md`
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`

GitHub execution trail:
- `#14` `SC-013` — trilogy consistency sweep
- `#15` `SC-014` — omnibus rebuild
- `#16` `SC-015` — final trilogy QA
- `#17` `SC-016` — release handoff and downstream source-of-truth note
- `#1` `SC-000` — top-level tracker

## Restart Instructions

If a new agent or human resumes work after chat loss, read in this order:

1. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/RELEASE_HANDOFF.md`
2. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/README.md`
3. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/GH_MILESTONES_AND_ISSUES.md`
4. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/PROCESS_RUNBOOK.md`
5. `tasks/todo.md`
6. the GitHub tracker issue `#1` and the latest comments in milestone `SC M3 — Omnibus + Release Readiness`

Then decide which of these you are actually doing:
- downstream content sync into web/mobile surfaces
- export / packaging work such as EPUB or PDF generation
- new editorial changes beyond the normalized canon

Do not reopen the normalization passes unless new evidence shows canon drift in `COMPILED/`.
