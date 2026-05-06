# Lessons Log

Review this file at session start when the task touches planning, intake authority, chapter-state claims, or manuscript editing workflow.

## Active Rules

### L-001: Never cite missing upstream files as though they are canonical

- Pattern:
  - workbench docs referenced trilogy doctrine files and a Brandmint manifest that did not exist in this checkout
- Prevention:
  - if an upstream source is split across multiple live files, cite the live authority set directly
  - if a source family is external or unavailable, add an availability note and point to the local registry that preserves its extracted handles

### L-002: Keep one active task board

- Pattern:
  - root `todo.md`, `PLAN.md`, `memory.md`, and `SC_STORYOPS` docs drifted into overlapping status claims
- Prevention:
  - `tasks/todo.md` is the only active execution tracker
  - `tasks/lessons.md` is the only lessons log
  - historical plans must be marked as historical, superseded, or archival

### L-003: Separate canonical readiness from research completeness

- Pattern:
  - older docs called the trilogy fully release-ready while research/image mapping was still incomplete
- Prevention:
  - use `canon/export ready` for the manuscript/export surface
  - use `research/image mapping incomplete` when the intake or image layer is still open

### L-004: Canonical chapter count is 27

- Pattern:
  - older docs and motif systems drifted into `22` or `26` chapter language
- Prevention:
  - treat `27` chapters as canon unless a future explicit remap changes the structure
  - do not treat the `22`-card arcana system as chapter-count parity

### L-005: For live manuscript surfaces, prefer semantic anchors over line offsets

- Pattern:
  - line-number targeting becomes unreliable in fast-moving manuscript files
- Prevention:
  - use semantic phrase matching and local context when locating edit points in compiled or chapter text

### L-006: Start large expansion campaigns in an isolated git lane

- Pattern:
  - major post-canon expansion work can easily contaminate the validated compiled package if it starts in the primary worktree
- Prevention:
  - create a fresh branch or worktree before scaffolding any new long-form expansion pass
  - keep planning artifacts, draft automation, and prose-growth experiments in that isolated lane until they are verified and ready to merge back

### L-007: Long-running helper jobs must outlive the launching shell

- Pattern:
  - background launches that worked for short local preprocessing died immediately for slower remote model calls when they inherited a short-lived shell
- Prevention:
  - spawn long-running wave tasks through a detached subprocess, not a plain shell background job
  - prove the runner with a disposable sleep task before trusting it with external model calls
  - keep TLS/polling fixes in the shared client so transport issues do not masquerade as task-level failures

### L-008: Freeze baseline planning tables before model revision rewrites the live copy

- Pattern:
  - `NEP-006` initially overwrote the canonical chapter matrix before the parser had validated the model field order, and the frozen input pack preserved only Chapters `01-17` of the original placeholder table
- Prevention:
  - validate generated field shapes before promoting them into the canonical planning surface
  - keep a reusable raw-output recovery path so parser fixes do not force an unnecessary second model call
  - freeze critical baseline tables in a dedicated artifact or committed file before asking a model to revise them

### L-009: Source-bound dossier passes must separate selected evidence from follow-up audits

- Pattern:
  - early `NEP-008` smoke output pulled placeholder research and art references back into the dossier as if they were selected evidence, and it also risked truncating the final sections
- Prevention:
  - sanitize prompt-fed task language when it contains shorthand audit labels or aesthetic mnemonics
  - pass explicit external-source allowlists into validation and reject invented asset paths
  - if a source is still needed, force the model to write `needs follow-up biological source` or `needs follow-up visual candidate` instead of naming a guessed authority
  - keep a one-pass repair fallback so a malformed dossier can be corrected without silently promoting bad output
