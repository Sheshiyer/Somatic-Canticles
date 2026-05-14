# GitHub Issue Map: NVIDIA Expansion Program

This file turns the expansion architecture into GitHub-trackable work.

## Label Families

- `program:nvidia-expansion`
- `phase:p1`
- `phase:p2`
- `phase:p3`
- `phase:p4`
- `phase:p5`
- `wave:w1`
- `wave:w2`
- `wave:w3`
- `swarm:contracts`
- `swarm:github`
- `swarm:text-intel`
- `swarm:vision-intel`
- `swarm:tooling`
- `swarm:dossiers`
- `swarm:book1`
- `swarm:book2`
- `swarm:book3`
- `swarm:integration`
- `agent:codex`
- `agent:gpt-oss`
- `agent:minimax`
- `agent:kimi`
- `agent:omni`
- `agent:control`

## Milestone Map

| Milestone | Purpose |
|---|---|
| `P1 Contract and Memory Foundation` | persist spec, architecture, issue graph, and source contracts |
| `P2 Source Intelligence and Tooling` | repo synthesis, source filters, visual extraction registry, helper scripts |
| `P3 Chapter Dossier Production` | dossier coverage for `Chapter 01-27` |
| `P4 Parallel Book Expansion` | chapter reasoning, drafting, and validation by book |
| `P5 Compiled Rebuild and Release Prep` | merge-back, scans, omnibus rebuild, editorial release check |

## Issue Set

| Task ID | GitHub | Issue title | Phase | Wave | Swarm | Owner | Deliverable | Dependencies |
|---|---|---|---|---|---|---|---|---|
| `NEP-001` | `#24` | Persist NVIDIA expansion spec and architecture in repo | `p1` | `w1` | `contracts` | `codex` | repo-local init, spec, architecture docs | none |
| `NEP-002` | `#25` | Create GitHub execution graph for the expansion program | `p1` | `w1` | `github` | `codex` | labels, milestone plan, issue map, issue bodies | `NEP-001` |
| `NEP-003` | `#26` | Run repo-wide synthesis over canon and StoryOps surfaces | `p2` | `w2` | `text-intel` | `gpt-oss` | synthesis artifact and chapter-gap summary | `NEP-001` |
| `NEP-004` | `#27` | Build source-root filters for blog, vault, and area corpora | `p2` | `w2` | `tooling` | `minimax` | source admissibility filters and indexing plan | `NEP-001` |
| `NEP-005` | `#28` | Build multimodal asset inventory and extraction registry | `p2` | `w2` | `vision-intel` | `omni` | noesis/blog/vault visual inventory and registry | `NEP-001` |
| `NEP-006` | `#29` | Produce chapter expansion matrix v1 from synthesis outputs | `p2` | `w3` | `text-intel` | `gpt-oss` | matrix revision with priorities and target bands | `NEP-003`,`NEP-004` |
| `NEP-007` | `#30` | Implement helper scripts for dossier generation and layer-gap reporting | `p2` | `w3` | `tooling` | `minimax` | repeatable script plan or scripts | `NEP-004` |
| `NEP-008` | `#31` | Generate Book 1 chapter dossiers | `p3` | `w1` | `dossiers` | `gpt-oss` | dossier set for `Chapter 01-08` | `NEP-005`,`NEP-006`,`NEP-007` |
| `NEP-009` | `#32` | Generate Book 2 chapter dossiers | `p3` | `w1` | `dossiers` | `gpt-oss` | dossier set for `Chapter 09-15` | `NEP-005`,`NEP-006`,`NEP-007` |
| `NEP-010` | `#33` | Generate Book 3 chapter dossiers | `p3` | `w1` | `dossiers` | `gpt-oss` | dossier set for `Chapter 16-27` | `NEP-005`,`NEP-006`,`NEP-007` |
| `NEP-011` | `#34` | Expand and validate Book 1 chapters | `p4` | `w2` | `book1` | `kimi` | expanded and validated Book 1 working chapters | `NEP-008` |
| `NEP-012` | `#35` | Expand and validate Book 2 chapters | `p4` | `w2` | `book2` | `kimi` | expanded and validated Book 2 working chapters | `NEP-009` |
| `NEP-013` | `#36` | Expand and validate Book 3 chapters | `p4` | `w2` | `book3` | `kimi` | expanded and validated Book 3 working chapters | `NEP-010` |
| `NEP-014` | `#37` | Run control-model canon and doctrine audit across expanded books | `p4` | `w3` | `integration` | `control` | cross-book anti-drift validation set | `NEP-011`,`NEP-012`,`NEP-013` |
| `NEP-015` | `#38` | Rebuild compiled books, omnibus, and editorial package from validated expansion lane | `p5` | `w3` | `integration` | `codex` | rebuilt compiled package and scans | `NEP-014` |

## Created Milestones

- `NEP P1 — Contract and Memory Foundation`
- `NEP P2 — Source Intelligence and Tooling`
- `NEP P3 — Chapter Dossier Production`
- `NEP P4 — Parallel Book Expansion`
- `NEP P5 — Compiled Rebuild and Release Prep`

## Posting Strategy

- Post `NEP-001` and `NEP-002` first.
- Post `NEP-003` to `NEP-007` as the source-intelligence wave.
- Post dossier issues `NEP-008` to `NEP-010` only after source intelligence is stable.
- Post book-expansion issues `NEP-011` to `NEP-013` after dossiers exist.
- Keep `NEP-014` and `NEP-015` as downstream integration gates.

## Branch and Worktree Convention

- Branch pattern:
  `swarm/nvidia-expansion/<phase>-<wave>/<swarm>/<task-id>-<owner>`
- Worktree pattern:
  `.worktrees/<task-id>-<owner>`

Examples:

- `swarm/nvidia-expansion/p2-w2/text-intel/NEP-003-gpt-oss`
- `swarm/nvidia-expansion/p2-w2/vision-intel/NEP-005-omni`
- `swarm/nvidia-expansion/p4-w2/book3/NEP-013-kimi`

## Parallel Dispatch Rules

- `NEP-003`, `NEP-004`, and `NEP-005` may run in parallel after `NEP-001`.
- `NEP-008`, `NEP-009`, and `NEP-010` may run in parallel after the source-intelligence batch closes.
- `NEP-011`, `NEP-012`, and `NEP-013` may run in parallel only if each book keeps disjoint ownership and compiled surfaces stay untouched.
- `NEP-014` and `NEP-015` are serialized integration gates.
