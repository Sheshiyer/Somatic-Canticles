# Process Runbook

**Program:** Somatic Canticles compiled trilogy normalization  
**Repo:** `Sheshiyer/Somatic-Canticles`

---

## Operating Model

This work should be resumed and executed as a controlled editorial program, not as ad hoc manuscript editing.

Core rules:

1. `02_MANUSCRIPTS/COMPILED/` is canonical.
2. Matter gets normalized before books.
3. Doctrine and vocabulary are frozen before major chapter rewrites.
4. One issue owns one edit surface at a time.
5. Wave boundaries are the integration points.
6. Validation evidence is required before an issue is closed.

---

## Required Inputs Before Any Wave Starts

Read these first:

1. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/README.md`
2. `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/GH_MILESTONES_AND_ISSUES.md`
3. `tasks/todo.md`
4. current active issue(s) in GitHub
5. current milestone tracker issue comments

For editorial work, also read the current doctrine/vocabulary assets once they exist.

Current doctrine asset:

- `03_EDITORIAL/TRILOGY_EDITORIAL_DOCTRINE.md`
- `03_EDITORIAL/TRILOGY_VOCABULARY_REPLACEMENT_MAP.md`
- `03_EDITORIAL/TRILOGY_MATTER_AUDIT.md`
- `03_EDITORIAL/TRILOGY_BOOK3_TONAL_CALIBRATION.md`

---

## Standard Wave Lifecycle

### 1. Open the wave

- move included issues from `planned` to `ready`
- post a wave-start summary in the tracker
- identify lock-zone files
- confirm branch/worktree boundaries

### 2. Execute issue by issue

For each issue:

- create or switch to the issue branch
- reread issue acceptance and validation criteria
- edit only the declared surface
- update local planning docs if assumptions change
- record validation evidence in the issue before closing

### 3. Close the wave

- run the declared validation sweep
- post a wave-close summary in the tracker
- note any doctrine drift, unresolved risks, or blocked downstream work
- update the roadmap docs if the plan changed

---

## Validation Standard

Every issue must leave one or more of:

- grep-based stale-term evidence,
- before/after file diff summary,
- consistency notes,
- QA readthrough notes,
- explicit risk note if something intentionally remains.

Never close an editorial issue with “done” and no evidence.

---

## Lock Zones

Treat these as serialized lock zones:

- `02_MANUSCRIPTS/COMPILED/Frontmatter.md`
- `02_MANUSCRIPTS/COMPILED/Preface.md`
- `02_MANUSCRIPTS/COMPILED/Backmatter.md`
- `02_MANUSCRIPTS/COMPILED/Glossary.md`
- each compiled book file
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`
- roadmap docs under `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/`

If a task needs to modify a locked file already owned by another active issue, stop and re-plan at the tracker level.

---

## Resume After Chat Loss

If a new session picks this up:

1. inspect the active milestone in GitHub
2. open the tracker issue
3. read the latest wave-close comment
4. compare local repo state to the milestone’s expected issue state
5. resume from the first issue marked `ready` or `in-progress`

If GitHub and local docs disagree, the local docs define intended structure and the tracker issue should be updated to match reality before new edits begin.

---

## Doctrine Change Protocol

If new evidence forces a doctrine change:

1. stop the current issue if the change affects other open work
2. update the doctrine asset and vocabulary map first
3. post the doctrine change in the tracker issue
4. re-check downstream open issues for impact
5. only then resume editing

Do not silently mutate doctrine in the middle of book rewrites.

---

## GitHub Update Protocol

For each issue:

- keep dependencies visible in the body
- reference the owning branch
- add a completion comment with:
  1. what changed
  2. what was verified
  3. what remains risky
  4. what issue is now unblocked

For each milestone:

- keep a milestone summary in the tracker issue
- identify the current wave
- identify blockers and lock zones

---

## Downstream Handoff Protocol

At Milestone 3 completion, write a handoff note that explicitly states:

- which compiled files are canonical,
- whether the omnibus has been regenerated,
- whether downstream web/mobile surfaces should re-import content,
- and which vocabulary/doctrine assets must travel with the manuscripts.

---

## Minimum Restart-Safe Artifacts

The following files must remain current:

- `tasks/todo.md`
- `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/README.md`
- `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/GH_MILESTONES_AND_ISSUES.md`
- `00_PLANNING_AND_ROADMAP/TRILOGY_NORMALIZATION_PROGRAM/PROCESS_RUNBOOK.md`

If GitHub issues are created, the tracker issue must remain current as the external index of record.
