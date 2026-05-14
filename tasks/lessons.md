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

### L-010: Long-form chapter expansion needs a smoke-floor target and transport retries

- Pattern:
  - the first dossier-driven chapter expansion smoke asked for a very large one-pass jump and failed on an upstream NVIDIA `504` before any draft was written
- Prevention:
  - first smoke passes should target the validated floor, not the full trilogy ceiling, so the transport can land a usable chapter before later enrichment passes
  - shared NVIDIA client calls must retry transient `408/429/5xx` failures with backoff
  - when prompt size is already dominated by dossier context, trim auxiliary excerpts before increasing timeout or token budgets again

### L-011: The symbolic scaffold is Toth/Crowley and stays implicit in prose

- Pattern:
  - expansion planning already used endocrine/muse/tarot logic, but the deck basis was not frozen tightly enough and could drift back into Rider–Waite language or become too explicit in the prose
- Prevention:
  - default all tarot-infused expansion work to the Toth/Crowley deck logic, not Rider–Waite
  - if legacy docs still use Rider–Waite names, translate them through Toth equivalents before using them for drafting
  - keep the tarot/enneagram/endocrine-muse scaffold subliminal: scene architecture, image pressure, pacing, and symbolic recurrence, not characters explaining the framework aloud

### L-012: Expansion prose must keep the biology / philosophy / technology braid intact

- Pattern:
  - the first successful expansion fragments gained length but over-indexed on anatomy and biomarker description, losing some of the trilogy's philosophical charge, technological atmosphere, and punchy delivery
- Prevention:
  - expansion prompts must explicitly preserve a three-lane braid: somatic biology, field/philosophical meaning, and technology/protocol pressure
  - each new biological intensification should be paired by either a technological consequence, a field-intelligence implication, or a sharp philosophical turn
  - later-stage growth should extend accepted prose additively instead of rewriting it wholesale, so the existing tonal spine does not get flattened into clinical description

### L-013: Symbolic scaffolding must modulate style, not just content

- Pattern:
  - a chapter can hit the factual scaffold while still feeling stylistically flat if the prose does not change temperature, wit, rhythm, and emotional color as the symbolic lane shifts
- Prevention:
  - treat the enneagram / muses / endocrine / tarot / zodiac / archetype chain as a style-and-emotion engine, not just a lore map
  - require layered meaning, pressure-release humor, and tonal modulation between fear, awe, wit, sorrow, and precision
  - avoid one-register expansion; each emotional turn should alter sentence texture, image density, and rhetorical pressure

### L-014: Character-specific wit must be assigned, not assumed

- Pattern:
  - asking generally for humor and wordplay improved the intent of the prompt, but still left the prose too solemn because no character had a defined lane for carrying wit or tonal release
- Prevention:
  - assign wit lanes by character and scene function
  - keep Jian's wit dry and precision-based, Gideon's wit blunt and defensive, Corv's wit oblique and double-edged, and Sona's wit gentle and relational
  - require later-stage passes to vary sentence temperature within a scene instead of sustaining one luminous or one clinical register for too long

### L-015: Expansion smoke passes need an explicit tone gate, not just better prose instructions

- Pattern:
  - the Chapter `01` smoke could hit the length floor and recover the biology / philosophy / technology braid while still remaining too solemn, wit-thin, and emotionally uniform
- Prevention:
  - validate live expansion smoke output against explicit prose criteria before accepting it: humor pressure-release, character-specific wit, sentence-temperature variation, and double-meaning density
  - if the control pass says the chapter is still flat, force a repair pass with those failures named directly rather than assuming another general rewrite will fix them
  - treat "good enough style" as a hard gate alongside canon and word-count growth during early expansion waves

### L-016: Shell helpers must be zsh-safe and avoid reserved parameter names

- Pattern:
  - the monitored wave helper reported false failures because it used `status` as a local variable under `zsh`, colliding with the shell's readonly `$status`, and its file reader depended on brittle external newline stripping
- Prevention:
  - do not use reserved shell parameter names like `status` in repo helper scripts
  - prefer built-in file reads and explicit newline trimming over tiny external subprocess assumptions in control scripts
  - smoke-test helper status commands in the same shell family the repo actually uses before trusting them during long-running model waves

### L-017: Expansion-stage prompts must enforce additive preservation explicitly, not just ask for it politely

- Pattern:
  - once the tone prompts improved, the first Kimi stage started producing better wit and emotional modulation but still compressed the chapter by rewriting it too freely
- Prevention:
  - tell the draft model that every existing paragraph and scene skeleton must survive in order unless a tiny line edit is unavoidable
  - say plainly that shorter-than-input output is invalid and that the correct action is insertion, not replacement
  - if a model keeps collapsing despite the instruction, treat that as a prompt-contract failure first, not as a stylistic failure

### L-018: External tone skills should be layered in as references, not allowed to replace the novel control plane

- Pattern:
  - the local `noesis-writer-skill` contains useful structure for tone, conviction, and humor, but it is built for brand/publishing workflows rather than trilogy chapter drafting
- Prevention:
  - use external writer skills like `noesis-writer-skill` only as supplemental tone references inside the expansion lab
  - borrow the useful parts: clinical precision at visionary scale, structural humor, directness, and conviction
  - explicitly ignore platform-format, image-generation, and content-marketing rules when applying that reference to novel chapters

### L-019: When a stage draft collapses, repair from the last accepted draft rather than the collapsed candidate

- Pattern:
  - the Chapter `01` smoke started producing better tonal fragments, but the stage draft could still shrink the chapter so hard that a repair pass working from the shrunken candidate inherited the collapse
- Prevention:
  - if a stage candidate fails growth validation, use the last accepted draft as the mandatory repair spine and treat the failed candidate only as a salvage source for phrasing, wit, or imagery
  - normalize headings before validation so near-miss repairs do not fail on formatting noise
  - keep early-stage floors relaxed enough that stylistically promising smoke output can advance to the tone gate instead of dying on a marginal word-count miss

### L-020: Repair passes must clean production residue and prove additive growth before validation

- Pattern:
  - a Chapter `01` repair pass returned the exact baseline length and reintroduced `**Somatic Event:**`, so the runner failed after spending a model call without gaining usable prose
- Prevention:
  - strip known preamble and production labels before validation instead of letting old scaffold residue poison an otherwise inspectable repair
  - pass explicit accepted-word and required-word floors into repair prompts
  - allow bounded repair retries from the last accepted draft, and fail only after each retry has demonstrated whether it truly grew the chapter

### L-021: If full-chapter repair keeps compressing, switch to insertion instead of asking for another full rewrite

- Pattern:
  - repeated full-chapter repair attempts for Chapter `01` preserved the improved tone but converged near the original length despite explicit word floors
- Prevention:
  - after bounded full-chapter repair failures, ask the prose model for insert-only material and merge it deterministically into the last accepted draft
  - validate the merged chapter rather than the standalone insert
  - use the insert fallback as a growth safety valve, not as the primary drafting path

### L-022: Style and near-miss growth failures need insertion, not another full rewrite

- Pattern:
  - Chapter `01` smoke runs showed three avoidable slow paths: partial-growth drafts that only needed a few hundred to a few thousand words, repair candidates that passed length but failed tone-temperature, and late-stage drafts over `5,000` words that stalled inside full-chapter repair calls
- Prevention:
  - treat initial partial growth as usable base material and add the missing word floor through insertion
  - route style-gate failures into targeted tonal inserts instead of full-chapter repair
  - skip full repair once the accepted draft is over the late-stage threshold, because insertion is safer for preserving canon and cheaper to monitor
  - catch repair and insert call failures so provider delays do not collapse the whole smoke run without a logged reason

### L-023: Insert fallback must be additive, not repetitive

- Pattern:
  - the monitored Chapter `01` smoke reached the final word floor, but Stage `4` failed because late insert attempts copied existing base paragraphs and overloaded the ending with repeated high-intensity sensory material
- Prevention:
  - de-duplicate generated insert paragraphs against the accepted draft before merging
  - reject inserts that return only duplicate material
  - make the insert prompt explicitly forbid restating accepted-base paragraphs, looping corridor descriptions, or recapping the current draft
  - for style-gate repairs, ask for calm counter-rhythm, distinct character voice, a clean technical consequence, and a character-true pressure-release exchange instead of more visionary escalation

### L-024: Duplicate rejection must change the retry lane, not just retry the same scene vector

- Pattern:
  - the next monitored Chapter `01` smoke correctly rejected duplicate-only Stage `3` inserts, but the remaining retries kept returning the same sensory-architecture family and exhausted the insert budget before reaching the stage floor
- Prevention:
  - save raw insert attempts before de-duplication so duplicate failures are inspectable
  - de-duplicate across paragraph boundaries and strip repeated paragraph clusters after deterministic merge, not only exact paragraph matches before merge
  - make later insert attempts change vectors explicitly toward dialogue, protocol consequence, consent pressure, and character-specific wit instead of asking for another corridor, palace, door, staircase, card, or CSF-floor set-piece
  - keep a bounded but wider insert retry budget so provider `504`s and duplicate-only generations do not prematurely kill an otherwise recoverable stage

### L-025: Late duplicate recovery should not keep the full accepted draft in prompt context

- Pattern:
  - after one valid Stage `3` additive insert, later Kimi retry attempts copied from the newly accepted base because the full accepted draft stayed in every insert prompt
- Prevention:
  - for late duplicate-recovery insert attempts, omit the full accepted draft and provide only a short forbidden-ending/context excerpt
  - omit the failed candidate in late duplicate-recovery prompts when it is more likely to reinforce compression or repetition than provide useful tone
  - after repeated duplicate-only Kimi inserts, route the next insert attempt to the control model instead of spending additional calls on the same prose-copying behavior

### L-026: Later expansion stages should be insert-first when full rewrites repeatedly compress

- Pattern:
  - repeated Stage `3` Kimi full-chapter rewrites collapsed accepted drafts by thousands of words and then forced slow repair cycles before the runner could return to the safer insert fallback
- Prevention:
  - once an accepted draft is established, use insert-first growth for later stages instead of asking the prose model to rewrite the whole chapter again
  - preserve the accepted draft as the spine, grow through bounded additive inserts, and validate the merged chapter with the same word-count and style gates
  - treat full-stage rewrites as an early-stage discovery tool only; later stages are expansion and calibration, not replacement

### L-027: Background stop helpers must kill task process groups, not only wrappers

- Pattern:
  - stopping `NEP-013-SMOKE` killed the detached wrapper but left a child Python expansion process alive, which later appended stale Stage `3` output into a new run's log
- Prevention:
  - when using detached task runners, stop the process group with `kill -TERM -<pid>` and escalate to `kill -KILL -<pid>` if the wrapper still lives
  - before trusting a fresh monitored run after a stop, check for orphaned command lines matching the task command
  - if a model runner is killed manually, treat the next log as untrusted until orphan cleanup and status reset are confirmed

### L-028: Final length is not final acceptance

- Pattern:
  - the Chapter `01` smoke reached `9,041` words, but the control gate still rejected it because the late inserts made the chapter longer without fixing the flattened lyrical / clinical register, weak wit lanes, weak pressure-release, and fragile braid balance
- Prevention:
  - after the final-stage word floor is met, route style-gate failures into a full-chapter acceptance repair instead of spending the remaining budget on more additive inserts
  - use the control model plus the dialogue matrix for this acceptance repair so it can rebalance voice, pronoun consistency, braid, double meanings, and pressure-release without inventing new plot
  - keep the word floor and canon validation active after acceptance repair so style fixes cannot pass by compressing the chapter

### L-029: Style gates can miss unsupported named operators

- Pattern:
  - the accepted Chapter `01` smoke passed the literary style gate but introduced `Rook`, an unsupported named teammate, into a scene that should only contain the established Chapter `01` Somanaut team
- Prevention:
  - explicitly forbid invented Somanaut teammates or named operators in stage, repair, insert, voice-repair, and control-gate prompts
  - after a model pass, run a concrete named-entity sanity scan against the chapter dossier and current working draft, not only a style score
  - patch both the working chapter and raw generated artifact when making post-run canon cleanup so the saved artifact matches the accepted prose lane

### L-030: Model lists are not route guarantees

- Pattern:
  - Book `2` prep found several listed NVIDIA models that were not safe defaults: Kimi, MiniMax, GLM, and DeepSeek timed out on small probes, and Palmyra Creative was listed but unavailable to the account
  - Mistral Large was callable on a small probe but too slow at Chapter `09` Stage `1` scale, producing no artifact before the smoke threshold
  - Qwen was fast on a small probe, but the same runner path still stalled when asked for a large full-chapter Stage `1` rewrite
  - Chapter `09` still had old preamble metadata in the working baseline, so valid inserts failed after merge because the accepted base itself was contaminated
  - final-stage requests for thousands of new words in one insert repeated the same slow-call behavior as full rewrites
  - after promoting a `6,900`-word accepted base, even a small insert call slowed down because the prompt resent the entire long chapter
  - style gates missed unsupported named helpers (`Kael`, `Jory`) and explicit symbolic scaffold language after a numerically successful Chapter `09` run
  - after hard bans were added, Qwen still repeated explicit `Toth` across every final-stage retry instead of adapting to the forbidden-token failure
  - failed hard-ban insert candidates can poison the next prompt if the runner keeps the contaminated merge as the active accepted draft
  - the control model can still introduce a plausible but unsupported helper name (`Mara`) during high-pressure final inserts, so newly caught local-only names must graduate into validator bans
  - Chapter `10` proved that a route can be safe for one chapter and still too slow for the next; Qwen stalled on the first guarded insert while GPT-OSS completed the chapter after prompt cleanup
  - generative prompts that explicitly name the hidden symbolic scaffold can cause the model to copy those words into prose, making the validator fight the prompt
  - a passing style gate can still miss a late invented helper name (`Juna`), so post-run hard scans must remain independent from model gate verdicts
  - some NVIDIA chat-compatible routes returned useful text under `reasoning_content` or `reasoning` instead of `message.content`, which made the old extractor reject otherwise callable responses
  - the NVIDIA client also allowed pending `202` polling to exceed the caller timeout, leaving monitor output stale during a hung probe
  - the expansion matrix used `control_pass`, but runners only checked legacy `control_model`, so route intent could be silently ignored
- Prevention:
  - probe a model with a small live request before making it a default prose or control route
  - run a monitored chapter-scale smoke before trusting a model that only passed a tiny prompt
  - for expansion waves, start with additive inserts rather than full-chapter rewrites when the goal is length growth from an accepted baseline
  - normalize the accepted working baseline before any merge so legacy packet metadata cannot poison otherwise clean generated inserts
  - cap individual insert requests and let the runner accumulate several smaller additions when the remaining word gap is large
  - omit the full accepted base from insert prompts once the chapter is long; use tail/context excerpts to preserve continuity without context bloat
  - hard-ban unsupported names and overt tarot/enneagram/Crowley/Toth markers in validation instead of relying on the literary style gate to notice them
  - route the next insert attempt to the control model after a forbidden-token failure, because retrying the same draft model can exhaust the budget on the same violation
  - after any preamble or forbidden-token failure, roll the active candidate back to the last clean draft and omit the failed candidate from the next prompt
  - do not include hard-banned scaffold terms in generative instructions; describe the hidden system generically as submerged symbolic-muse pressure
  - after repeated hard failures, shrink insert requests into smaller additive chunks before spending another large scene-level generation
  - verify named-person authority before hard-banning: `Aurora Luminth` is valid for Chapter `10`, while `Lira`, `Mara`, and `Juna` are not locally authorized
  - do not commit rejected scratch insert artifacts that contain hard-ban terms; keep the accepted raw chapter and gate reports as the durable baseline
  - keep Kimi/MiniMax opt-in unless a fresh probe passes and a chapter-specific quality review justifies the risk
  - pass caller timeouts through all pending/polling branches in the NVIDIA client
  - support provider-specific text fields before classifying a model as unusable
  - resolve both `control_pass` and `control_model` in every runner that performs validation or repair

### L-031: Below-floor candidates still need canon/name validation before becoming retry bases

- Pattern:
  - Chapter `11` produced a below-floor partial-growth candidate that carried unsupported helper names; because the candidate failed on word count before the style gate, it became the next insert base and contaminated later retries.
- Prevention:
  - treat unsupported-character style-gate findings as hard canon failures, not ordinary prose-style failures
  - keep chapter-scoped forbidden-name lists when a name is invalid for one chapter but valid elsewhere in the trilogy
  - add chapter cast hints to generation and gate prompts so the model does not solve pressure-release beats by inventing operators or assistants
  - if a hard-failed candidate is long enough, salvage only by deterministic paragraph stripping and revalidation; never preserve contaminated material as the accepted base
