# Active Task Tracker

This file is the active source of truth for repository execution status.

## Next Up

- [x] Establish a committed pre-expansion baseline for chapter growth:
  - [x] Generate a per-chapter baseline word-count report from the active `working/Chapter-*.md` lane
  - [x] Record a `3x` growth target for each chapter so later expansion passes have a measurable floor
  - [x] Commit the completed dossier wave, runner hardening, and baseline metrics on `codex/nvidia-expansion-lab`
- [ ] Reset the expansion architecture to the real trilogy target:
  - [x] Generate a trilogy-scale target profile that treats `300,000-400,000` words as the actual objective
  - [x] Reframe the old `3x` numbers as an intermediate safety floor only
  - [x] Mark the old v1 matrix length bands as interim so the next expansion wave aims at the macro target profile instead
- [ ] Launch the actual chapter expansion wave by book from the populated dossiers and macro target bands:
  - [ ] `Book 1` dossier-driven long-form expansion
  - [x] `Book 2` dossier-driven long-form expansion
  - [ ] `Book 3` dossier-driven long-form expansion
- [x] Complete the Book `2` expansion lane only after applying Book `1` runner lessons:
  - [x] Review Book `1` compression, duplicate-insert, style-gate, and named-operator lessons before selecting routes
  - [x] Probe current NVIDIA model availability instead of trusting the original Kimi/MiniMax plan
  - [x] Patch NVIDIA `202` polling so caller timeouts control hung model probes and monitored runs
  - [x] Reroute Book `2` dossiers and matrix rows to `qwen/qwen3.5-122b-a10b` for draft and `openai/gpt-oss-120b` for control
  - [x] Validate the resolved `Chapter 09` route with `--print-route`
  - [x] Start the monitored `Chapter 09` Book `2` smoke expansion only after route validation passes
- [x] Launch Wave `P2/W2` in parallel:
  - `NEP-003` / issue `#26`: repo-wide synthesis over canon and StoryOps surfaces
  - `NEP-004` / issue `#27`: source-root filters for blog, vault, and area corpora
  - `NEP-005` / issue `#28`: multimodal asset inventory and extraction registry
- [x] Execute the real NVIDIA-backed `P2/W2` model wave:
  - [x] Smoke-check NVIDIA settings load from the saved Codex config without exposing secrets
  - [x] Run `openai/gpt-oss-120b` over `generated/repo_synthesis_input_pack_v1.md`
  - [x] Run `minimaxai/minimax-m2.7` over the source-intake and filter-spec pair
  - [x] Run the curated visual seed set through a resilient multimodal lane with parser fallback
  - [x] Watch helper status and logs for graceful fallback if any model job fails
  - [x] Inspect the generated outputs before opening the next dossier/tooling wave
- [x] Close `P2/W2`, then execute `NEP-006` / `#29` and `NEP-007` / `#30` before dossier production starts
  - `NEP-006`: chapter-expansion matrix population from the synthesis report and source priority map
  - `NEP-007`: dossier builder/tooling scripts tied to the approved source tiers and visual registry
- [x] Launch `P3/W1` dossier generation in parallel:
  - [x] `NEP-008` / issue `#31`: generate Book `1` chapter dossiers from the scaffolds and approved source tiers
  - [x] `NEP-009` / issue `#32`: generate Book `2` chapter dossiers from the scaffolds and approved source tiers
  - [x] `NEP-010` / issue `#33`: generate Book `3` chapter dossiers from the scaffolds and approved source tiers
- [x] Stabilize the dossier population runner before full fan-out:
  - [x] Distinguish selected evidence from follow-up research needs in prompt instructions and validation
  - [x] Prevent unsupported placeholder sources or invented visual assets from landing in populated dossiers
  - [x] Re-run the monitored `NEP-008` smoke pass on `Chapter 01` until the output is source-bound and clean
  - [x] Launch `NEP-008`, `NEP-009`, and `NEP-010` in parallel only after the smoke dossier validates
  - [x] Verify all populated dossiers write to the expected book folders and preserve the `## 1` through `## 12` contract
- [ ] Optional release checkpoint: push the completed late-Book-3 and endmatter package after review

### NEP-008 / NEP-009 / NEP-010 Review

- [x] Verified `27` populated dossier files exist across Books `1-3`
- [x] Verified every dossier contains `# Chapter Source Dossier:`, `## 11. Model Routing`, and `## 12. Validation Checklist`
- [x] Verified no scaffold residue remains in populated dossiers
- [x] Verified no unsupported placeholder-source tokens remain in populated dossiers
- [x] Verified monitored helper statuses: `NEP-008=ok`, `NEP-009=ok`, `NEP-010=ok`

### NEP-011 Wordcount Baseline Review

- [x] Generated `generated/chapter_wordcount_baseline_v1.md`
- [x] Generated `generated/chapter_wordcount_baseline_v1.json`
- [x] Recorded trilogy pre-expansion baseline: `45,902` words
- [x] Recorded trilogy `3x` floor: `137,706` words
- [x] Recorded that only `4 / 27` current matrix target bands already cover the requested `3x` floor, so future chapter expansion must treat the baseline artifact as the growth floor

### NEP-012 Trilogy Length Target Reset

- [x] Generate `generated/trilogy_length_target_profile_v1.md`
- [x] Generate `generated/trilogy_length_target_profile_v1.json`
- [x] Record the macro trilogy objective: `300,000-400,000` words
- [x] Record the operational book bands that sum to the macro trilogy objective
- [x] Mark the v1 matrix target bands as interim dossier-era length bands rather than the final expansion target

### NEP-013 Book 1 Expansion Smoke

- [x] Build the first dossier-driven chapter expansion runner using the populated Chapter `01` dossier and the trilogy target profile
- [x] Repair the monitored helper so live wave status works cleanly under `zsh`
- [x] Add a prose-quality gate so Chapter `01` cannot pass on word count alone if wit, humor, and sentence-temperature variation are still under target
- [x] Harden the repair pass so failed stage drafts strip preamble residue and must add real material before validation
- [x] Add an insert-only fallback when full-chapter repairs keep compressing the accepted draft
- [x] Route initial partial-growth candidates, style-gate failures, non-additive repairs, and late-stage drafts over `5,000` words into additive insert fallback instead of repeated full rewrites
- [x] Add visible model-call logging and repair/insert call failure handling so the monitor shows where a smoke run is waiting
- [x] Run a monitored smoke expansion for `Book 1 / Chapter 01`
- [x] Record the first full monitored smoke failure: final Stage `4` reached `8,952` words but failed the control gate because late inserts repeated base material and collapsed voice/temperature
- [x] Harden insert normalization so generated inserts cannot repeat accepted-base paragraphs before merge
- [x] Record the second monitored smoke failure: Stage `3` correctly rejected duplicate-only inserts, but exhausted the fixed retry budget after a provider `504` and repeated sensory-architecture retries
- [x] Harden insert fallback again so it saves raw insert attempts, strips cross-paragraph repetition after merge, and changes retry lanes toward dialogue / protocol / consequence instead of replaying corridor or palace imagery
- [x] Record the third monitored smoke failure: Stage `3` recovered one additive insert to `5,385` words, then Kimi copied the accepted base on the remaining duplicate-recovery attempts instead of producing the final `636` new words
- [x] Add duplicate-recovery routing so late insert retries omit the full accepted draft from the prompt and switch to the control model after repeated duplicate-only Kimi outputs
- [x] Stop the next monitored run when Stage `3` again collapsed under full-chapter Kimi rewrite, before spending another long repair cycle
- [x] Switch Stage `3+` growth to insert-first mode so accepted prose is preserved and later stages no longer pay for known-compressive full-chapter rewrites
- [x] Detect and clean up orphaned Chapter `01` expansion processes after `nep_stop` killed the wrapper but not the child model call
- [x] Harden `nep_stop` to terminate the task process group, and switch Stage `2+` growth to insert-first mode because Stage `2` full rewrites also repeatedly compressed accepted prose
- [x] Record the fourth monitored smoke failure: Stage `4` reached `9,041` words, but the final inserts failed the control gate for weak wit lanes, weak double-meaning density, fragile braid balance, and a flattened lyrical/clinical register
- [x] Add a final-stage voice/style acceptance repair after the word floor is met so the runner fixes braid, wit, pressure-release, and pronoun consistency instead of only adding more prose
- [x] Re-run the monitored `Book 1 / Chapter 01` smoke after insert de-duplication
- [x] Verify the expanded Chapter `01` preserves canon while materially increasing length against the baseline
- [x] Verify the expanded Chapter `01` preserves the trilogy's biology / philosophy / technology braid and does not drift into over-clinical prose
- [x] Verify the expanded Chapter `01` carries layered meaning, character-true wit lanes, and sentence-temperature variation instead of one solemn register
- [x] Record the before/after word count for `Chapter 01` so later chapter waves use the same comparison contract

### NEP-013 Smoke Acceptance Review

- [x] Monitored helper status: `NEP-013-SMOKE=ok`
- [x] Final control gate passed after voice repair: `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`
- [x] Post-run canon cleanup removed unsupported `Rook` references from the accepted working chapter and raw artifact
- [x] Verified no production preamble residue, unsupported `Rook`, `PubMed`, or `doi` markers remain in the accepted working/raw outputs
- [x] Verified working and raw Chapter `01` outputs are byte-identical after cleanup
- [x] Recorded final Chapter `01` growth: `1,598` -> `8,846` words (`5.54x` baseline)

### NEP-014 Book 1 Style Alignment Gate

- [x] Generate a Book `1` cross-chapter style audit that compares Chapters `01-08` against the accepted StoryOps prose contract, not just per-chapter word growth
- [x] Identify any style/length outliers, especially chapters whose saved gates pass locally but still drift against the Book `1` lane
- [x] Record the two most likely repair candidates with evidence: word-count gap, gate depth, braid balance, wit/temperature, raw/working parity, and residue checks
- [x] Start the highest-priority repair pass only after the audit produces a durable ledger artifact
- [x] Verify the repaired chapter still matches its raw artifact and does not introduce production scaffolding or unsupported names

### NEP-014 Book 1 Style Alignment Review

- [x] Generated `generated/book_1_style_alignment_input_pack_v1.md`
- [x] Generated `generated/book_1_style_alignment_local_metrics_v1.json`
- [x] Generated `generated/book_1_style_alignment_audit_v1.md`
- [x] Initial audit flagged repair order `Chapter 04`, then `Chapter 07`
- [x] Repaired `Chapter 04` manually after Kimi timed out and the control-model tail candidate under-shot the word floor and invented unsupported material
- [x] Verified `Chapter 04` now reaches `7,829` words, working/raw parity is clean, and saved `gate-4` passes with `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=7`, `double_meaning_density=7`, `humor_pressure_release=8`
- [x] Re-ran the Book `1` style audit after `Chapter 04`; refreshed repair order is `Chapter 01`, then `Chapter 07`, with `Chapter 04` passing
- [x] Run a dedicated `Chapter 07` structural cleanup before treating it as a simple length pass; current late inserts include repeated extraction/debrief loops, explicit tarot/Crowley mentions, and apparent local-only names that need authority review
  - [x] Preserve the stable breathfield intervention spine through the unassisted-stability proof
  - [x] Consolidate the late extraction/debrief material into one chronological arc instead of repeated corridor/lift/triage loops
  - [x] Demote or remove local-only support names unless already backed by authority surfaces
  - [x] Remove explicit tarot/Crowley language and keep the scaffold subliminal
  - [x] Sync the repaired working chapter to raw, run saved style gate, and rerun the Book `1` audit
- [x] Decide whether `Chapter 01` needs another macro-length expansion or should remain accepted as the original smoke baseline despite the refreshed audit's macro-length watch
  - Decision: `Chapter 01` remains accepted only as the style/routing smoke baseline; it still needs a constrained macro-length expansion before the Book `1` lane can be called stable.
  - Evidence: refreshed audit repair order is `Chapter 07`, then `Chapter 01`; `Chapter 01` is `8,846 / 10,800` low macro target with local risk `3`, while `Chapter 07` is structurally clean but still `9,227 / 15,000` with local risk `4`.
  - `Chapter 07` cleanup result: working/raw parity restored, residue scan clean, saved `gate-5` passed with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
- [x] Run a constrained macro-length expansion on cleaned `Chapter 07` first, then a smaller `Chapter 01` macro-length expansion, preserving the current smoke baseline voice as the control sample.
  - [x] Run `Chapter 07` additive length expansion from the cleaned structural baseline, targeting the Book `1` macro low band without reintroducing corridor/debrief loops or explicit scaffold language
  - [x] Inspect expanded `Chapter 07` for additive growth, chronology, voice lanes, residue, and working/raw parity
  - [x] Save a fresh `Chapter 07` style gate and rerun the Book `1` audit
  - [x] Run `Chapter 01` additive macro-length expansion only after `Chapter 07` is accepted, using the current smoke chapter as the voice-control sample
  - [x] Save a fresh `Chapter 01` style gate, rerun the Book `1` audit, and record the final Book `1` readiness decision
  - `Chapter 07` result: `15,000` words, working/raw parity clean, residue scan clean, saved `gate-6` passed with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=9`, `double_meaning_density=8`, `humor_pressure_release=8`.
  - `Chapter 01` result: `10,801` words, working/raw parity clean, residue scan clean, saved `gate-7` passed with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - Book `1` readiness decision: not yet stable for commit-back as a full lane. The refreshed audit still returns `flag`, with repair order `Chapter 03`, then `Chapter 05`; `Chapter 02` and `Chapter 08` remain secondary watch items for macro-length shortfall.
- [ ] Next live step: expand and rebalance `Chapter 03` first, then `Chapter 05`, using the latest Book `1` audit as the control ledger.
  - [ ] Run `Chapter 03` additive expansion toward its `12,150` macro low target while deepening safety/freedom tension and adding pressure-release beats
  - [ ] Gate `Chapter 03`, verify raw parity/residue, and refresh the Book `1` audit
  - [ ] Run `Chapter 05` additive expansion toward its `9,700` macro low target while preserving endocrine doctrine stakes without flattening into biology-heavy exposition
  - [ ] Gate `Chapter 05`, verify raw parity/residue, and refresh the Book `1` audit

### NEP-015 Book 2 Routing Prep

- [x] Recorded model probe results in `generated/book_2_model_routing_probe_v1.md`
- [x] Classified current routes: `qwen/qwen3.5-122b-a10b` as guarded Book `2` draft, `openai/gpt-oss-120b` as control, Kimi/MiniMax as opt-in only, Mistral Large as opt-in slow lane only
- [x] Updated the runner to resolve both `control_pass` and legacy `control_model`
- [x] Added `--control-model` and `--print-route` so a chapter route can be validated without launching prose generation
- [x] Updated Book `2` matrix and all seven Book `2` dossiers to the fresh default route
- [x] Validate initial route for `Chapter 09` with `--print-route`: effective draft `mistralai/mistral-large-3-675b-instruct-2512`, effective control `openai/gpt-oss-120b`, default floor `9,520`
- [x] Stop the initial monitored `Chapter 09` smoke after Stage `1` produced no artifact for several minutes on Mistral Large
- [x] Re-probe fallback candidates and update the NVIDIA client to extract `reasoning_content` / `reasoning` response text
- [x] Validate rerouted `Chapter 09` path with Qwen: effective draft `qwen/qwen3.5-122b-a10b`, effective control `openai/gpt-oss-120b`
- [x] Stop the first Qwen smoke before the 900-second timeout because the large full-chapter Stage `1` rewrite still produced no artifact inside the smoke threshold
- [x] Switch the expansion runner to insert-first from Stage `1` so Book `2` begins with additive growth instead of another full rewrite path
- [x] Stop the first insert-first smoke after it proved the Chapter `09` working baseline still carried old preamble metadata into merged candidates
- [x] Normalize the accepted working baseline inside the expansion runner before merge/growth validation
- [x] Launch a fresh monitored insert-first smoke run from the normalized baseline
- [x] Promote the clean Stage `3` accepted candidate to the working lane after stopping the oversized final insert: `6,900` words, no residue, gate scores `8/7/8/6/7`
- [x] Cap per-insert requests at `1,100` words so final-stage growth uses smaller additive chunks instead of another oversized generation
- [x] Stop the first resume when even a small insert slowed down from resending the full `6,900`-word accepted base
- [x] Omit full accepted-base context for long insert prompts and use tail/context continuity instead
- [x] Resume `Chapter 09` again from the accepted `6,900`-word baseline to the `9,520` floor with `--minimum-words 9520`
- [x] Mark the completed numeric run as not accepted after post-run scan found unsupported `Kael` / `Jory` names and overt Toth/Crowley/Enneagram scaffold terms
- [x] Add validator hard bans for those unsupported names and explicit symbolic scaffold terms
- [x] Attempt a control-model canon cleanup on the `10,977`-word candidate; reject it because the model refused instead of repairing
- [x] Deterministically remove contaminated paragraphs and promote a clean `7,266`-word forge-native baseline with raw parity
- [x] Regrow attempt from the clean baseline failed safely because Stage `3` repeatedly produced explicit `Toth` and the new validator rejected every contaminated candidate
- [x] Patch hard-ban failures to switch the next insert attempt to the GPT-OSS control model instead of spending all retries on the same draft model
- [x] Regrow the clean `7,266`-word baseline to the `9,520` floor with hard bans and control-model fallback active
  - Result: `NEP-015-B2-C09-CANON3` completed successfully at `10,295` words, with working/raw parity restored and saved gate scores `8/7/8/6/7`.
  - Verification: post-run scan found no unsupported `Kael` / `Jory` / `Mara`, no overt Toth/Crowley/Enneagram scaffold terms, no ship-setting drift terms, and no preamble residue in the accepted working/raw surface.
  - Process note: rejected insert scratch artifacts from the run were not committed because they contained hard-ban terms; the durable artifacts are the accepted raw chapter, final voice repair, and gate reports.
- [x] Start `Chapter 10` Book `2` expansion with the same guarded insert-first route, hard-ban rollback, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C10-GPT5` completed successfully after the first Qwen insert was stopped for no artifact and Chapter `10` was rerouted through GPT-OSS draft override.
  - Runner hardening: removed explicit hidden-scaffold terms from generative prompts, sanitized hard-failure notes before prompt reuse, added smaller post-hard-failure insert chunks, and added `Lira` / `Juna` to local-only hard bans while preserving valid Chapter `10` authority for `Aurora Luminth`.
  - Verification: accepted Chapter `10` is `8,950` words, working/raw/accepted-voice parity is clean, saved `gate-4` passes with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`, and hard-ban scan is clean.
  - Process note: rejected insert scratch artifacts and the failed voice-repair artifact were not committed because they contained hard-ban terms or unsupported helper material.
- [x] Start `Chapter 11` Book `2` expansion with the cleaned submerged-scaffold prompts, guarded insert-first route, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C11-CASTLOCK` completed successfully at `10,653` words after the runner was hardened with Chapter `11` cast authority and chapter-scoped local-name bans.
  - Verification: working/raw parity is clean, saved `gate-4` passes with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`, and the hard-ban scan is clean.
  - Process note: rejected insert scratch artifacts from failed attempts were not committed because they contained local-only helper names or setting-drift terms.
- [x] Start `Chapter 12` Book `2` expansion with the same cast-aware runner, guarded insert-first route, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C12-FINAL` completed successfully at `8,332` words after promoting a clean `6,129`-word near-miss voice repair and adding only the final margin.
  - Runner hardening: added Book `2` cast hints for Chapters `12-15`, treated over-floor non-final style failures as eligible for final acceptance repair, and allowed an already-over-floor insert-first stage to gate instead of forcing unnecessary growth.
  - Verification: working/raw parity is clean, saved `gate-3` passes with `braid_balance=8`, `wit_lane_distinction=7`, `temperature_variation=8`, `double_meaning_density=6`, `humor_pressure_release=7`, and the hard-ban scan is clean.
  - Process note: rejected scratch artifacts from failed tone/setting/operator lanes were not committed.
- [x] Start `Chapter 13` Book `2` expansion with the same cast-aware runner, guarded insert-first route, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C13-GPT` completed successfully at `7,136` words after final-stage voice repair.
  - Verification: working/raw/accepted-voice parity is clean, saved `gate-3` passes with `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=7`, `double_meaning_density=6`, `humor_pressure_release=7`, and the hard-ban scan is clean.
  - Process note: rejected insert scratch artifacts were not committed.
- [x] Start `Chapter 14` Book `2` expansion with the same cast-aware runner, guarded insert-first route, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C14-GPT` completed successfully at `11,672` words.
  - Verification: working/raw parity is clean, saved `gate-4` passes with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=9`, `double_meaning_density=7`, `humor_pressure_release=8`, and the hard-ban scan is clean.
  - Lexical cleanup: normalized accepted Book `2` Chapters `09-14` working/raw surfaces to remove remaining `vibration` / `quantum` / related style-sheet carryovers while preserving working/raw parity.
  - Runner hardening: promoted those style-sheet carryovers into hard validation so Chapter `15` cannot reintroduce them.
  - Process note: rejected insert scratch artifacts were not committed.
- [x] Start `Chapter 15` Book `2` expansion with the same cast-aware and lexical-hard-ban runner, guarded insert-first route, and raw/parity acceptance scan.
  - Result: `NEP-015-B2-C15-NORM` completed successfully at `11,321` words.
  - Runner hardening: added deterministic lexical normalization before insert/chapter validation so legacy `quantum` / `vibration` / `manifestation` carryovers are removed before acceptance, not only after post-run cleanup.
  - Verification: working/raw/accepted-voice parity is clean, saved `gate-4` passes with `braid_balance=8`, `wit_lane_distinction=7`, `temperature_variation=7`, `double_meaning_density=6`, `humor_pressure_release=7`, and the hard-ban / lexical scan is clean.
  - Process note: rejected insert scratch artifacts were excluded from the durable acceptance set.

### NEP-015 Book 2 Acceptance Review

- [x] Accepted all Book `2` working chapters `09-15` through the guarded insert-first expansion lane.
- [x] Recorded final Book `2` expanded working word count: `68,359` words by the repo `word_count` function.
- [x] Verified each accepted Book `2` chapter has working/raw parity.
- [x] Verified each accepted Book `2` chapter has a saved passing style gate.
- [x] Verified the accepted Book `2` working/raw surfaces are clean of local-name bans, overt symbolic scaffold terms, production preamble residue, and lexical carryovers.
- [ ] Next live step: run the Book `2` compiled-surface coherence comparison before promoting this lane back into compiled manuscript surfaces.

### NEP-016 Book 3 Expansion Lane

- [x] Verify the Book `3` working lane starts from a clean git checkpoint after Book `2` acceptance.
- [x] Validate Chapter `16` route before generation: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`, control remains `openai/gpt-oss-120b`, and the pass floor is `12,000` words.
- [x] Harden the expansion runner for Book `3` before launch:
  - [x] Add deterministic cleanup for `frequency` / `shatter` style-sheet carryovers.
  - [x] Add Chapter `16` cast guidance: Corv, Sona, Jian, Gideon, and Mira Verath only; no on-page Gardener speaker yet.
- [x] Start monitored Chapter `16` expansion from the populated dossier and accepted Book `2` carryover state.
  - Result: the default insert runner repeatedly drifted into hardware/action-repair imagery, on-page descent, or premature cure posture, so the accepted lane uses a constrained custom insert/merge with the same Chapter `16` validator.
  - Runner hardening: Chapter `16` now bans the observed bad outputs directly: invented House names, packet/relay/export mechanics, hardware-repair vocabulary, premature descent, and false-success language such as the field being willing to cooperate.
- [x] Verify Chapter `16` acceptance:
  - [x] Working/raw parity clean.
  - [x] Saved style gate passes braid, wit lanes, temperature variation, double meaning, and pressure-release thresholds.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
  - Result: `Chapter 16` accepted at `12,219` words with saved `gate-9` scores: `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
- [x] Commit and push Chapter `16` only after it passes acceptance.
- [ ] Continue Book `3` serially through Chapters `17-27`, widening only if a chapter route proves safe and has no dependency on unresolved prior-chapter prose.
  - Current live step: expand `Chapter 19` from its populated dossier and accepted `Chapter 18` handoff, preserving the Three-Point Problem as unresolved procedure rather than solved triangulation.

### NEP-017 Book 3 Chapter 17 Expansion

- [x] Review `Chapter 17` dossier, route, current working draft, and Gardener tone authority.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control is rerouted from `nvidia/nemotron-3-super-120b-a12b` to `openai/gpt-oss-120b`; pass floor is `11,280` words.
  - Current draft issues: preamble residue, under-length at roughly `2.3k` words, legacy lexical carryovers, rushed Gardener motive, and thin post-encounter relational aftermath.
- [x] Harden the runner for `Chapter 17` before launch:
  - [x] Add Chapter `17` cast guidance allowing only Corv, Sona, Jian, Gideon, Mira Verath as subject/terrain/case trace, and The Gardener as calm conservational intelligence.
  - [x] Ban observed/probable Gardener drift: villain coding, over-mechanized `law/universe/homeostasis` explanation, and Mira-as-helper dialogue.
- [x] Expand `Chapter 17` from the populated dossier and accepted `Chapter 16` handoff.
  - Result: accepted at `11,282` words using constrained encounter, refusal, aftermath, and protocol-handoff inserts.
  - Tone correction: The Gardener now speaks as calm conservational intelligence, not as a cartoon antagonist or abstract system monologue; the four refusal lanes remain distinct.
- [x] Verify `Chapter 17` acceptance:
  - [x] Working/raw parity clean.
  - [x] Saved style gate passes braid, wit lanes, temperature variation, double meaning, and pressure-release thresholds.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
  - Result: saved `gate-9` scores are `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=7`.
- [x] Commit and push `Chapter 17` only after it passes acceptance.
- [ ] Next live step: expand `Chapter 18` from its populated dossier and the accepted Gardener handoff, preserving the move from encounter aftermath into synthesis protocol rather than repeating the Gardener sermon.

### NEP-018 Book 3 Chapter 18 Expansion

- [x] Review `Chapter 18` dossier, route, current working draft, and compiled-hotspot ledger.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,040` words.
  - Current draft issues: old preamble metadata, under-length at `1,577` normalized words, vector-definition compression, and high risk of sermon voice / role flattening.
  - Governing constraint: convert the accepted Gardener handoff into enacted field surgery and threshold discipline, not another explanation of the Gardener.
- [x] Harden the runner for `Chapter 18` before launch:
  - [x] Add Chapter `18` cast guidance allowing only Corv, Sona, Jian, Gideon, and Mira Verath as case trace / recovery consequence.
  - [x] Ban observed/probable synthesis drift: new Gardener dialogue, law/homeostasis/system-sermon language, protocol-complete posture, and merger/fusion/unity phrasing.
  - [x] Add Chapter `18` insert guidance that keeps Pure Joy / Catalyst Clarity / Present Coherence exact and builds toward the Three-Point Problem without solving it.
- [x] Expand `Chapter 18` from the populated dossier and accepted `Chapter 17` handoff.
  - Result: accepted at `8,055` words after the default Qwen route stalled/false-failed on over-broad validation, the draft lane was rerouted through GPT-OSS, and the closing third was surgically rewritten to replace repeated calibration/spec loops with House-pressure, body consequence, distinct voice, and semantic-correction stakes.
- [x] Verify `Chapter 18` acceptance:
  - [x] Working/raw parity clean.
  - [x] Saved style gate passes braid, wit lanes, temperature variation, double meaning, and pressure-release thresholds.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
  - Result: saved `gate-9` scores are `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=7`, `double_meaning_density=8`, `humor_pressure_release=7`.
- [x] Commit and push `Chapter 18` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 19` from its populated dossier and the accepted `Chapter 18` handoff, preserving the Three-Point Problem as unresolved procedure rather than solved triangulation.

### NEP-019 Book 3 Chapter 19 Expansion

- [x] Review `Chapter 19` dossier, route, current working draft, and accepted `Chapter 18` handoff.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,200` words.
  - Macro target: low band is `10,250` words, but this pass uses the proven chapter-floor acceptance gate before later macro rebalancing.
  - Current draft issues: old preamble metadata, under-length at `1,598` normalized words, residual legacy cadence term, and high risk of solving triangulation too early.
  - Governing constraint: deepen the Three-Point Problem as live procedure under House-review pressure, not as completed alignment, merged witness, or Chapter `21` Test Fire.
- [x] Harden the runner for `Chapter 19` before launch:
  - [x] Add Chapter `19` cast guidance allowing only Corv, Sona, Jian, Gideon, and Mira Verath as proof case / trace / review consequence.
  - [x] Ban observed/probable triangulation drift: new Gardener dialogue, system-sermon language, solved-triangle posture, Test Fire bleed, new operators, and merger/unified-witness phrasing.
  - [x] Add Chapter `19` insert guidance that keeps Pure Joy / Catalyst Clarity / Present Coherence exact and unresolved while deepening geometry, House pressure, Jian's false-elegance temptation, and Corv/Gideon discipline tension.
- [x] Expand `Chapter 19` from the populated dossier and accepted `Chapter 18` handoff.
  - Result: accepted at `8,239` words after rejecting the first automated `8,262`-word output despite its passing gate because manual review found repeated calibration passages, unsupported prop logic, and false countdown pressure.
  - Repair: rebuilt the accepted surface from the clean chapter spine with controlled additions for higher-dimensional relation, House-review pressure, body cost, Mira-as-person-before-evidence, and a dry interval that defines convergence preparation without executing it.
  - Runner hardening: added Chapter `19` bans for unsupported prop/countdown drift and clarified that Mira Verath has no dialogue or wit lane in this chapter.
- [x] Verify `Chapter 19` acceptance:
  - [x] Working/raw parity clean.
  - [x] Saved style gate passes braid, wit lanes, temperature variation, double meaning, and pressure-release thresholds.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
  - Result: saved `gate-9` scores are `braid_balance=8`, `wit_lane_distinction=7`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
- [x] Commit and push `Chapter 19` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 20` from its populated dossier and accepted `Chapter 19` handoff, preserving convergence as threshold preparation rather than live-fire execution.

### NEP-020 Book 3 Chapter 20 Expansion

- [x] Review `Chapter 20` dossier, route, current working draft, and accepted `Chapter 19` handoff.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,840` words.
  - Macro target: low band is `11,050` words, but this pass uses the proven chapter-floor acceptance gate before later macro rebalancing.
  - Current draft issues: old preamble metadata, under-length at `1,728` normalized words, threshold timing compressed, and risk of treating convergence visibility as completed passage.
  - Governing constraint: convergence may reach the threshold and make the gap legible, but it must not begin Chapter `21` hostile-contact testing or claim mastery.
- [x] Harden the runner for `Chapter 20` before launch:
  - [x] Add Chapter `20` cast guidance allowing Corv, Sona, Jian, Gideon, Mira Verath as proof case / trace, and Anvel Verath only as historical wound coordinate.
  - [x] Ban observed/probable convergence drift: new Gardener dialogue, solved/mastered convergence posture, Test Fire bleed, unsupported props, new House speakers, and merger/unified-witness phrasing.
  - [x] Add Chapter `20` insert guidance that keeps Pure Joy / Catalyst Clarity / Present Coherence exact while deepening the negative-vertex, body cost, House-review pressure, and wound-without-doctrine logic.
- [x] Expand `Chapter 20` from the populated dossier and accepted `Chapter 19` handoff.
  - Result: accepted at `8,840` words after rejecting the first automated `9,857`-word output despite its passing gate because manual review found repeated late calibration beats, quasi-speaker Engine behavior, generic `universe` phrasing, and prop/interface clutter.
  - Repair: rebuilt the accepted surface from the clean convergence spine with controlled additions for failure rehearsal, body-cost accounting, House audit pressure, negative-vertex geometry, deliberate threshold visibility, and a non-contact boundary into Chapter `21`.
  - Runner hardening: added Chapter `20` bans for generic universe language, prop/interface drift, Engine-as-speaker language, stale Triangulation Engine naming, and House-speaker bleed.
- [x] Verify `Chapter 20` acceptance:
  - [x] Working/raw parity clean.
  - [x] Saved style gate passes braid, wit lanes, temperature variation, double meaning, and pressure-release thresholds.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
  - Result: saved `gate-9` scores are `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=7`, `double_meaning_density=7`, `humor_pressure_release=8`.
- [x] Commit and push `Chapter 20` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 21` from its populated dossier and accepted `Chapter 20` handoff, preserving hostile-contact Test Fire as local procedure without bleeding into Chapter `22` temptation logic.

### NEP-021 Book 3 Chapter 21 Expansion

- [x] Review `Chapter 21` dossier, route, current working draft, and accepted `Chapter 20` handoff.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,080` words.
  - Macro target: low band is `10,100` words, but this pass uses the proven chapter-floor acceptance gate before later macro rebalancing.
  - Current draft issues: old preamble metadata, under-length at `1,565` normalized words, stale `frequency` / `Triangulation Engine` drift, compressed hostile-contact pressure, and risk of bleeding into Chapter `22` temptation logic.
  - Governing constraint: the Test Fire is a bounded hostile-contact exposure only; it may discover counterfeit kindness / relief as the next danger, but it must not cross, sever, complete passage, or open personal temptation offers.
- [x] Harden the runner for `Chapter 21` before launch:
  - [x] Add Chapter `21` cast guidance allowing Corv, Sona, Jian, Gideon, Mira Verath as proof case / trace, Anvel Verath only as historical wound coordinate, and the Gardener only as hostile load / correction attention.
  - [x] Ban observed/probable Test Fire drift: new Gardener dialogue, solved/mastered passage posture, Test Fire bleed into Chapter `22`, unsupported props, new House speakers, stale Triangulation Engine naming, and merger/unified-witness phrasing.
  - [x] Add Chapter `21` insert guidance that keeps the one controlled hostile-contact window exact while deepening vessel hum, metallic taste, edge discipline, review pressure, and counterfeit-kindness discovery.
- [x] Expand `Chapter 21` from the populated dossier and accepted `Chapter 20` handoff.
  - Result: the monitored GPT-OSS insert-first run failed safely after repeated hard-ban contamination and style-gate flattening, so the accepted lane uses a controlled dossier/source-bound rebuild from the clean Test Fire spine.
  - Repair: expanded the one-second hostile-contact exposure with vessel hum, metallic taste, body-signal timing, House-review simulation pressure, counterfeit-kindness detection, and differentiated witness humor while preserving the boundary against Chapter `22` personal temptation.
- [x] Verify `Chapter 21` acceptance:
  - [x] Working/raw parity clean at `8,265` words.
  - [x] Saved `gate-9` passes with `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=7`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [x] Commit `Chapter 21` only after it passes acceptance.
- [x] Push the accepted `Chapter 21` checkpoint.
- [x] Next live step after push: expand `Chapter 22` from its populated dossier and accepted `Chapter 21` handoff, preserving individualized temptation logic without bleeding into Chapter `23` safety/control temptation.

### NEP-022 Book 3 Chapter 22 Expansion

- [x] Review `Chapter 22` dossier, route, current working draft, and accepted `Chapter 21` handoff.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `6,520` words.
  - Current draft issues: under-length at `1,364` words, stale `frequency` / `corridor` language, over-smooth harmony, and a packet-era contradiction where Gideon's Chapter `23` safety/control lane must stay boundary-only in Chapter `22`.
  - Governing constraint: Chapter `22` may enact Jian's certainty offer, Sona's painless-peace offer, and Corv's perfect-meaning offer, but it must not reveal the Chapter `23` structural lie or move Gideon into his safety/control temptation.
- [x] Harden the runner for `Chapter 22` before launch:
  - [x] Add Chapter `22` cast guidance limiting live voice lanes to Corv, Sona, Jian, and Gideon, with Mira / Anvel only as proof-case or historical wound coordinates.
  - [x] Ban observed/probable Perfect World drift: explicit tarot scaffold terms, stale `frequency` / `corridor` language, Gardener dialogue/body, solved passage posture, unsupported props, new House speakers, and Gideon safety/control bleed.
  - [x] Add Chapter `22` insert guidance that keeps the false-offer phase individualized, subliminally source-bound, and closed before Chapter `23` structural-lie pressure.
- [x] Expand `Chapter 22` from the populated dossier and accepted `Chapter 21` handoff.
  - Result: rebuilt the chapter from the active temptation spine rather than accepting the short baseline, preserving Jian's solved-map refusal, Sona's false-rest refusal, Corv's beautiful-closure refusal, and Gideon's unopened Chapter `23` lane.
  - Repair: removed stale `frequency` / `corridor` language, kept the tarot/world-completion source motifs submerged, and ended on satisfaction-as-pressure rather than a structural-lie reveal.
- [x] Verify `Chapter 22` acceptance:
  - [x] Working/raw parity clean at `6,520` words.
  - [x] Saved `gate-9` passes with `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [x] Commit and push `Chapter 22` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 23` from its populated dossier and accepted `Chapter 22` handoff, preserving structural-lie discovery without bleeding into Chapter `24` severance pressure.

### NEP-023 Book 3 Chapter 23 Expansion

- [x] Review `Chapter 23` dossier, route, current working draft, and accepted `Chapter 22` handoff.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,000` words.
  - Current draft issues: under-length at `1,677` words, stale `harmonized` / `shattered`-family risk, thin relational aftermath, and a rushed move from structural-lie recognition toward Chapter `24` severance.
  - Governing constraint: Chapter `23` may reveal hidden authorship and Gideon's manageability/protection temptation, but it must end at the cut-line for Chapter `24`, not enact severance.
- [x] Harden the runner for `Chapter 23` before launch:
  - [x] Add Chapter `23` cast guidance limiting live voice lanes to Corv, Sona, Jian, and Gideon, with Mira / Anvel only as proof-case or historical wound coordinates.
  - [x] Ban observed/probable Flaw-in-the-Code drift: explicit source scaffold terms, stale `frequency` / `resonant` / `harmonized` language, Gardener dialogue/body, severance enactment, unsupported props, and new House speakers.
  - [x] Add Chapter `23` insert guidance that opens hidden authorship and Gideon's manageability refusal while keeping Chapter `24` severance closed.
- [x] Expand `Chapter 23` from the populated dossier and accepted `Chapter 22` handoff.
  - Result: rebuilt the chapter around clean-state deception, Gideon's manageability refusal, hidden-authorship testing, review-language propagation, and a Chapter `24` entry-conditions cut-line.
  - Repair: the first accepted-length surface failed style gate for technical flattening and quasi-personified Gardener/hidden-author language; the final pass removes unsupported review-role/simulator language, replaces Gardener personhood with pruning-layer logic, and adds a display-off relational beat to restore warmth, panic, and pressure release.
- [x] Verify `Chapter 23` acceptance:
  - [x] Working/raw parity clean at `8,495` words.
  - [x] Saved `gate-9` passes with `braid_balance=8`, `wit_lane_distinction=7`, `temperature_variation=8`, `double_meaning_density=6`, `humor_pressure_release=7`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [x] Commit and push `Chapter 23` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 24` from its populated dossier and accepted `Chapter 23` cut-line, preserving severance as a live act without bleeding into Chapter `25` void aftermath.

### NEP-024 Book 3 Chapter 24 Expansion

- [x] Review `Chapter 24` dossier, route, current working draft, and accepted `Chapter 23` cut-line.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,200` words.
  - Current draft issues: under-length at `1,718` words, stale `universe` / `Triangulation Engine` / `Gardener did not scream` drift, compressed `13.7` sequence, and risk of bleeding into Chapter `25` void aftermath.
  - Governing constraint: Chapter `24` may enact the final procedure / severance against hidden authorship's exclusive claim, but it must end at release with relation intact before Chapter `25` adaptation begins.
- [x] Harden the runner for `Chapter 24` before launch:
  - [x] Add Chapter `24` cast guidance limiting live voice lanes to Corv, Sona, Jian, and Gideon, with Mira / Anvel only as proof-case or historical wound coordinates.
  - [x] Ban observed/probable Final Procedure drift: stale field terms, explicit scaffold terms, Gardener dialogue/body/scream, new House speakers, triumph/coronation posture, and Chapter `25` void aftermath.
  - [x] Add Chapter `24` insert guidance that permits the severance act while preserving distinct witnesses, embodied procedure, and a clean stop before aftermath.
- [x] Expand `Chapter 24` from the populated dossier and accepted `Chapter 23` cut-line.
  - Result: rebuilt the live severance lane around the Chapter `23` cut-line, the moving refusal seam, a `13.7`-second anti-spectacular procedure, and a release boundary that stops before Chapter `25` void aftermath.
  - Repair: the first style-gated surface was rejected for procedural flattening and `Corvan` drift; the accepted pass normalizes `Corv`, removes the duplicate activation replay, and turns the replay pressure into a record-custody temptation that strengthens body/philosophy/technology braid.
- [x] Verify `Chapter 24` acceptance:
  - [x] Working/raw parity clean at `8,287` words.
  - [x] Saved `gate-9` passes with `braid_balance=8`, `wit_lane_distinction=7`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [x] Commit and push `Chapter 24` only after it passes acceptance.
- [x] Next live step after commit: expand `Chapter 25` from its populated dossier and accepted `Chapter 24` release, preserving void aftermath without premature authored-reality stabilization.

### NEP-025 Book 3 Chapter 25 Expansion

- [x] Review `Chapter 25` dossier, route, current working draft, and accepted `Chapter 24` release.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,720` words.
  - Current draft issues: under-length at `1,826` words, legacy `Corvan` naming, rushed void-aftershock, thin source-substrate embodiment, and risk of jumping too early into Chapter `26` authored-world construction.
  - Governing constraint: Chapter `25` may deepen void aftermath, invalidity, keptness, and potential-before-allocation, but it must not stabilize a new reality or begin the architecture-building phase.
- [x] Harden the runner for `Chapter 25` before launch:
  - [x] Normalize `Corvan` to `Corv` in runner lexical cleanup.
  - [x] Add Chapter `25` cast guidance limiting live voice lanes to Corv, Sona, Jian, and Gideon.
  - [x] Ban observed/probable Void drift: explicit scaffold terms, stale field terms, Gardener dialogue/body, new-role contamination, triumph posture, and Chapter `26` new-reality/architecture bleed.
  - [x] Add Chapter `25` insert guidance that privileges silence, failed measurement, body inventory, relation without coordinates, and source-substrate pattern logic without exposition.
- [x] Expand `Chapter 25` from the populated dossier and accepted `Chapter 24` release.
  - Result: stabilized the void aftermath lane around invalidity, no inherited coordinates, Sona's Note without sweetness, Jian's no-score status check, Corv's refusal of premature story, and Gideon's keptness without walls.
  - Repair: the first monitored pass reached word floor but was rejected editorially for repeated `lattice/thrum/raw` drift and sci-fi props; the accepted surface uses a controlled reconstruction plus final voice repair with Chapter `25` anti-drift guidance included in the voice-repair prompt.
- [x] Verify `Chapter 25` acceptance:
  - [x] Working/raw parity clean at `9,962` words.
  - [x] Saved `gate-9` passes with `braid_balance=9`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [x] Commit and push `Chapter 25` only after it passes acceptance.
- [x] Next live step after commit: open `Chapter 26` from its populated dossier and accepted `Chapter 25` threshold, opening authored architecture only after the void lane is stable.

### NEP-026 Book 3 Chapter 26 Expansion

- [x] Review `Chapter 26` dossier, route, current working draft, and accepted `Chapter 25` threshold.
  - Route: default Kimi route is rerouted to `qwen/qwen3.5-122b-a10b`; control remains `openai/gpt-oss-120b`; pass floor is `8,080` words.
  - Current draft issues: under-length at `1,696` words, legacy `Corvan` naming, stale `ground frequency` / `manifestation` carryovers, compressed condition-building, and risk of overclaiming a finished world.
  - Governing constraint: Chapter `26` may establish provisional ground, joy-as-permission, living boundary, direction, and responsibility, but it must not stabilize Chapter `27` habitation or open contact with others.
- [x] Harden the runner for `Chapter 26` before launch:
  - [x] Remove runner encouragement toward repeated `lattice/thrum/resonance` shorthand.
  - [x] Normalize `Corvan`, `ground frequency`, `manifestation`, and `resonance` carryovers before validation.
  - [x] Add Chapter `26` cast guidance limiting live voice lanes to Corv, Sona, Jian, and Gideon.
  - [x] Ban observed/probable architecture drift: explicit source/blog scaffold terms, stale field terms, Gardener presence, sci-fi equipment, new roles, paradise/omnipotence posture, and Chapter `27` bridge/contact bleed.
- [x] Expand `Chapter 26` from the populated dossier and accepted `Chapter 25` threshold.
  - Result: the monitored GPT-OSS insert-first run reached the word floor but stalled in voice repair after repeated `boot` prop drift and an over-solemn final candidate, so the accepted lane promotes the clean near-floor spine and applies a controlled final architecture/practice repair.
  - Repair: kept ground, joy, boundary, direction, and responsibility provisional; added character-specific wit, agreement-vs-rule logic, Manas Interface restraint, and support-without-ownership pressure while avoiding Chapter `27` habitation/contact bleed.
- [x] Verify `Chapter 26` acceptance:
  - [x] Working/raw parity clean at `8,147` words.
  - [x] Saved `gate-9` passes with `braid_balance=8`, `wit_lane_distinction=8`, `temperature_variation=8`, `double_meaning_density=7`, `humor_pressure_release=8`.
  - [x] Hard-ban and lexical scan clean.
  - [x] Rejected scratch inserts excluded from commit.
- [ ] Commit and push `Chapter 26` only after it passes acceptance.
- [ ] Next live step after commit: expand `Chapter 27` from accepted `Chapter 26`, preserving first habitation and bridge-to-others as bounded beginning rather than utopian closure.

### NEP-006 Matrix Revision

- [x] Generate `generated/chapter_expansion_matrix_v1.md` from the current matrix plus `repo_synthesis_report_v1.md` and `source_family_priority_map_v1.md`
- [x] Generate a machine-readable `generated/chapter_expansion_matrix_v1.json`
- [x] Update the canonical lab matrix at `story/expansion_lab/chapter_expansion_matrix.md` so it reflects the v1 revision instead of the pre-synthesis placeholder
- [x] Verify the revised matrix still respects chapter summaries, book boundaries, and source-tier admissibility rules

### NEP-007 Dossier Tooling

- [x] Implement a repeatable script to scaffold chapter dossiers from the template and matrix metadata
- [x] Implement a repeatable script to generate a layer-gap report by book, layer, and priority cluster
- [x] Generate an initial dossier manifest/index so `NEP-008` to `NEP-010` can batch-create dossiers without re-deciding file layout
- [x] Verify the tooling only emits source-bound scaffolds and does not invent canon or prose

### NEP-006 / NEP-007 Review

- [x] Recover baseline target bands from the frozen input pack and explicit late-book fallback map instead of trusting the already-mutated live matrix
- [x] Add a `--reuse-raw` recovery path to `run_nep_006_matrix_revision.py` so parser fixes do not require a fresh model call
- [x] Regenerate `chapter_expansion_matrix_v1.{md,json}` from validated raw output and verify field admissibility
- [x] Regenerate `dossier_manifest_v1.{md,json}` and `layer_gap_report_v1.{md,json}` from the corrected matrix
- [x] Emit all `27` dossier scaffold files under `story/expansion_lab/dossiers/`

### Monitored Wave Runner

- [x] Create a sourceable shell helper for background task launch, status checks, log tailing, and failure summaries
- [x] Standardize runtime state under a repo-local `.wave_runtime/` directory so runs are inspectable and restartable
- [x] Smoke-test the helper with a safe command and verify `running`, `ok`, and `failed` states
- [x] Keep a dedicated monitoring terminal session available before launching the real P2/W2 jobs

### P2/W2 Source Understanding Launch

- [x] `P2/W2-A` Profile the four named source roots into concrete text, concept, and vision families with exclusions and priority slices
- [x] `P2/W2-B` Create the first operational intake artifact that synthesis, tooling, and vision lanes can all consume without re-reading chat
- [x] `P2/W2-C` Record which parts of `03-Resources` and `02-Areas` are admissible by default versus review-required versus excluded
- [x] `P2/W2-D` Record the first-pass blog post families most likely to deepen Book `1`, Book `2`, and Book `3`
- [x] `P2/W2-E` Record the first-pass noesis/blog visual families that should enter the multimodal extraction registry before chapter work begins

### P2/W2 Review

- [x] Generate `generated/repo_synthesis_report_v1.md` from the repo synthesis input pack with `openai/gpt-oss-120b`
- [x] Generate `generated/source_family_priority_map_v1.md` from the intake + filter spec with `minimaxai/minimax-m2.7`
- [x] Generate `generated/visual_motif_registry_seed_v1.json` and `generated/visual_motif_registry_seed_v1.md` from the curated multimodal seed set
- [x] Harden the monitored wave runner so long-running jobs survive shell exit via detached subprocess launch
- [x] Harden the NVIDIA client for explicit CA-bundle loading and 202/status polling
- [x] Record the multimodal fallback path: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` primary, `meta/llama-3.2-11b-vision-instruct` fallback

### Swarm Architecture and GitHub Sync

- [x] Create a durable project spec for the NVIDIA expansion program that captures goal, source material roots, authority boundaries, and target outputs
- [x] Create a project architecture document that captures model routing, parallel execution boundaries, validation gates, and merge-back flow
- [x] Create a milestone and phase-wave execution map so the repo has a durable rollout plan independent of chat history
- [x] Create a GitHub issue map and issue-ready bodies for the expansion program
- [x] If GitHub auth is available, open the issue set and record the issue IDs back into the repo docs
- [x] Verify the persistent docs point back to the existing `expansion_lab` control surfaces instead of duplicating conflicting truth

### NVIDIA Expansion Lab

- [x] Create an isolated git lane for long-form expansion work at worktree `../Somatic-Canticles-nvidia-expansion` on branch `codex/nvidia-expansion-lab`
- [x] Define the multi-model routing architecture so `gpt-oss-120b`, `MiniMax M2.7`, `Kimi`, and control models have non-overlapping jobs
- [x] Create `story/expansion_lab/repo_synthesis_manifest.md` as the control document for canon understanding, source families, chapter targets, and model roles
- [x] Create `story/expansion_lab/chapter_expansion_matrix.md` with chapter-by-chapter current length, target length band, missing layers, and source dossier pointers
- [x] Create `story/expansion_lab/chapter_source_dossier_template.md` so each chapter expansion pass is source-bound to StoryOps, editorial, world-bible, and synchronocities-blog surfaces
- [x] Verify the expansion lab is isolated from `main`, documented clearly, and ready for the first repo-synthesis pass
- [x] Classify the four external source roots into published substrate, vault support, area-notebook support, and vision-first support tiers
- [x] Add a dedicated multimodal ingestion plan so `Documents/noesis/Research`, blog cards/images, and approved vault visuals can deepen lore and worldbuilding without becoming silent canon
- [x] Extend the chapter dossier template so every non-repo source carries admissibility tags, provenance, and visual-evidence tracking

### Completed Optional Cleanup

- [x] Normalize the remaining compiled `**Somatic Event:**` preamble markers out of Book `1`, Book `2`, and the omnibus for a stricter prose-only export surface

### Active Serial Wave: Finish Book 3 and Endmatter

- [x] `23` Open the structural-lie lane from `Chapter 22` without importing `Chapter 24` severance pressure too early
- [x] `23a` Keep Gideon's safety/control temptation exact, local, and anti-heroic; keep Corv's false-mercy refusal exact and anti-sermonic
- [x] `23b` Compare active `Chapter 23` against the compiled Book `3` surface and record the meaningful divergences
- [x] `24` Open the final-procedure lane as live enacted authorship, not battle spectacle or deterministic countdown myth
- [x] `24a` Hold the Tryambakam / triangulation vocabulary exact while keeping the scene embodied and role-bound
- [x] `24b` Compare active `Chapter 24` against the compiled Book `3` surface and record the meaningful divergences
- [x] `25` Open the void lane only after severance is clean, removing `RESONANCE PROFILE`, `Chapter Status`, and all other embedded production residue
- [x] `25a` Use the topological-pocket and timelessness substrate only to sharpen orientation loss, not to replace scene logic with essay logic
- [x] `25b` Compare active `Chapter 25` against the compiled Book `3` surface and record the meaningful divergences
- [x] `26` Open the architecture lane as chosen constraint, shared authorship, and first-principles creation rather than omnipotent metaphysical declaration
- [x] `26a` Use source-code / compiler language only where it stays embodied and narratively earned
- [x] `26b` Compare active `Chapter 26` against the compiled Book `3` surface and record the meaningful divergences
- [x] `27` Open the new-beginning lane as habitable field formation, relational future, and first bridge to others without utopian flattening
- [x] `27a` Strip all remaining end-of-draft scaffolding and keep `Noetic Network` emergence as later-horizon promise rather than sequel bait
- [x] `27b` Compare active `Chapter 27` against the compiled Book `3` surface and record the meaningful divergences
- [x] `B1` Create `02_MANUSCRIPTS/COMPILED/Bibliography.md`
- [x] `B2` Create `02_MANUSCRIPTS/COMPILED/Closing_Note.md`
- [x] `B3` Update `Preface.md`, `Backmatter.md`, and `Glossary.md` to match the final trilogy vocabulary and conceptual posture
- [x] `B4` Merge the refreshed Book `3` and endmatter into the compiled canonical surfaces

### Complete the Late Book 3 and Endmatter Package

- [x] Open, stabilize, and compare `Chapter 23` as the structural-lie lane, making hidden authorship explicit without bleeding into `Chapter 24` procedure
- [x] Open, stabilize, and compare `Chapter 24` as the live severance lane, keeping the 13.7-second cut exact and anti-spectacular
- [x] Open, stabilize, and compare `Chapter 25` as the first post-Severance lane, stripping all embedded production residue and grounding the void in lived disorientation
- [x] Open, stabilize, and compare `Chapter 26` as authored reality in practice, building the new field through chosen conditions rather than manifesto abstraction
- [x] Open, stabilize, and compare `Chapter 27` as first habitation, relational future, and bounded horizon without sugary transcendence
- [x] Update the Book `3` packet board, workbench README, source packet map, projection board, concept-authority matrix, and chapter-lane surfaces so `Chapter 16-27` now read as a full constrained prose lane
- [x] Create `02_MANUSCRIPTS/COMPILED/Bibliography.md` from the research references and synchronocities-blog substrate
- [x] Create `02_MANUSCRIPTS/COMPILED/Closing_Note.md`
- [x] Refine `Frontmatter.md`, `Preface.md`, `Backmatter.md`, and `Glossary.md` to match the final late-book authorship frame
- [x] Rebuild `02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md` from the active `working/Chapter-16-27` lane with lane-only metadata stripped from the compiled surface
- [x] Rebuild `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` so the refreshed Book `3`, glossary, bibliography, closing note, and backmatter are all present in one canonical export surface
- [x] Verify the rebuilt package with `git diff --check`, `scan_consistency.py`, and direct residual-term searches against the compiled Book `3` surface

### Planned Next Wave: Book 3 Unfreeze Prep

- [x] `01` Build a Book 3 authority pack from `hard authority` first: `00_TRYAMBAKAM_PROTOCOL.md`, core foundation lexicon/definitions, character arcs, roster, and the active editorial/style surfaces
- [x] `02` Build a separate `review-required` macro-governance pack from `04_WORLD_BUILDING` and Meru-linked `03-Resources` surfaces without promoting any of it to canon yet
- [x] `03` Produce a single Book 3 concept-to-authority matrix for `Wilt`, `Gardener`, `Three-Point Problem`, `Perfect World`, `Flaw in the Code`, `Void of Pure Potential`, and `Authored reality`
- [x] `04` Close the image gap for `Strategic deception layers` by adding sister-image coverage beyond `20240921170304.png`
- [x] `05` Close the image gap for `Cellular polity / authored reality` by adding sister-image coverage beyond `20240921165748.png`
- [x] `06` Re-check the tetramorphic / authored-reality family so macro-governance imagery is supported by more than one symbolic lane
- [x] `07` Update `intake/noesis_image_cluster_registry.md` and `image_index.md` so the Book 3 image families carry explicit narrative utility, biological hook, and governance hook
- [x] `08` Re-run `intake/book_projection_board.md` for Book 3 using the strengthened authority plus image bundles and restate what is still `soft` versus packet-ready
- [x] `09` Build a Book 3 source packet map at chapter-cluster level: `16-18`, `19-21`, `22-24`, `25-27`
- [x] `10` Audit the current Book 3 compiled surface against the trilogy rules: vocabulary, role-bound dialogue, anti-sermon posture, and Gardener conservational voice
- [x] `11` Extract the highest-risk compiled Book 3 drift into a delta ledger: premature mastery, flattened revelation voice, loose macro-lore, or overclaimed governance logic
- [x] `12` Validate cross-book carryover from merged Book 1 / Book 2 into Book 3 entry conditions: Verath wound, team integration threshold, three-vector foreshadowing, and house-politics pressure
- [x] `13` Decide whether Book 3 may open packet scaffolding at all; if yes, open only `Chapter 16-18` starter packets first and keep `working/` closed
- [x] `14` Only after packet validation, promote `Chapter 16` into the first active prose lane and keep `Chapter 17-27` packet-only
- [x] `15` After `Chapter 16-18` stabilize, decide whether the rest of Book 3 opens serially or remains partially frozen based on authority, image, and continuity verification

## Completed This Session

### Repair the compiled-surface audit helper

- [x] Patch `03_EDITORIAL/scan_consistency.py` so it resolves the current repo root instead of a stale absolute workspace path
- [x] Regenerate `03_EDITORIAL/consistency_report.md` inside this checkout
- [x] Verify the first successful run against the current compiled books

### Merge Book 2 back into canonical surfaces

- [x] Replace `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md` with the active `Chapter 09-15` working lane
- [x] Resync the omnibus `Chapter 09-15` block so the old hybrid `Chapter 08 -> Chapter 09` boundary disappears
- [x] Restore a proper `# Chapter 16: The Wilt` break in the omnibus while leaving the Book 3 text itself untouched
- [x] Confirm the separate Book 2 compiled file matches the working lane exactly
- [x] Confirm the omnibus now carries a clean canonical handoff from `Chapter 08` through `Chapter 16`

### Run the full Book 1 coherence pass and merge it back to canon

- [x] Audit `Chapter 01-08` for residual metadata, terminology, and register drift before merge-back
- [x] Normalize the remaining chapter-surface drift in `Chapter 02`, `Chapter 05`, and `Chapter 06`
- [x] Replace `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md` with the active `Chapter 01-08` working lane
- [x] Sync the omnibus `Chapter 01-08` block to the new Book 1 compiled surface while intentionally leaving the old Book 2 text in place
- [x] Confirm the recalibrated `Chapter 08` ending is now the canonical Book 1 exit state that will govern the later Book 2 merge

### Run the full Book 2 coherence pass and decide merge-back order

- [x] Audit `Chapter 09-15` for lane-level terminology, voice, metadata, and continuity drift
- [x] Normalize the residual chapter-surface drift in `Chapter 12-15` so the Book 2 lane presents one active prose surface
- [x] Compare the staged `Chapter 09-15` lane against the compiled Book 2 surface and confirm the highest-value merge-back deltas
- [x] Decide merge-back order: Book 1 first, Book 2 second

### Batch-execute Book 2 Packet 09-15 and serialize the lane

- [x] Promote Packet `09` into an active prose lane and rewrite `Chapter 09` around Gideon's structural-care logic
- [x] Batch-execute Packets `10-15` in disjoint parallel chapter groups without crossing file ownership
- [x] Mark Packet `09-15` active and baseline-ready for compiled comparison
- [x] Reconcile the Book 2 lane so `Chapter 09-15` now operate as one active working surface

### Batch-execute Packet 06-08 in parallel

- [x] Promote Packet `06` into an active prose lane and open `Chapter 06` under `working/`
- [x] Preserve the logic-versus-feeling conflict in `Chapter 06` as method tension that resolves through signal recognition rather than soft compromise
- [x] Promote Packet `07` into an active prose lane and create the Sona-centered `Chapter 07` working copy
- [x] Promote Packet `08` into an active prose lane and create the Jian-centered `Chapter 08` working copy
- [x] Stabilize `Chapter 06-08` enough to be ready for compiled comparison

### Open Packet 05 and continue the chapter-by-chapter flow

- [x] Promote Packet `05` into an active prose lane and open `Chapter 05` under `working/`
- [x] Carry forward the `Chapter 04` exit state so the pituitary descent inherits the authored-rot thread rather than resetting scene logic
- [x] Rebuild `Chapter 05` around endocrine receiver-loop doctrine with clinically exact HPA-axis language
- [x] Preserve the missed anomaly as a meaningful interpretive error and stabilize the `Chapter 05` working copy for compiled comparison

### Open the first patterned-captivity lane with Packet 04

- [x] Promote Packet `04` into an active prose lane and open `Chapter 04` under `working/`
- [x] Re-center `Chapter 04` on Corv's witness logic instead of house-schism exposition
- [x] Introduce The Gardener as conservational maintenance pressure rather than a full Book 3 reveal
- [x] Stabilize the `Chapter 04` working copy enough to be ready for compiled comparison

### Run a diagnostic-lane coherence pass before Packet 04

- [x] Audit `Chapter 01-03` for voice and terminology drift before opening the first patterned-captivity lane
- [x] Canonicalize Jian's witness-vessel naming inside the active `Chapter 02` working copy
- [x] Remove the residual `Quantum` shorthand from the active `Chapter 02` working copy where the style surfaces already forbid it

### Close Packet 02 and finish the diagnostic architecture lane activation

- [x] Mark Packet `02` baseline-ready for compiled comparison and record its compiled-surface drift
- [x] Promote Packet `03` into an active prose lane and open `Chapter 03` under `working/`
- [x] Apply the first surgical pass to `Chapter 03` against the packet constraints
- [x] Stabilize the `Chapter 03` working copy enough to be ready for compiled comparison

### Promote Packet 01 into an active prose lane

- [x] Open `Chapter 01` as the first `working/` copy under the Book 1 lane
- [x] Mark Packet `01` and the Book 1 packet board as active rather than scaffold-only
- [x] Apply the first surgical prose pass to `Chapter 01` against the packet checklist and dialogue matrix
- [x] Stabilize the `Chapter 01` working copy enough to be ready for compiled comparison

### Issue #23: Scaffold the Book 1 packet lane and preserve the Book 3 freeze

- [x] Upgrade the `Book 1` lane docs from reservation stubs to an active scaffolding contract
- [x] Map Chapters `01-08` into a packet board tied to the intake-backed Book 1 spine
- [x] Create starter packet files grounded in current chapter, source, and image evidence without opening prose rewrites yet
- [x] Re-state the `Book 3` freeze as an explicit downstream rule with remaining gates

### Issue #22: Continue second-pass Noesis image captioning and image-principle coverage

- [x] Expand the active Noesis cluster registry beyond representative singletons
- [x] Register sister images with observed motif, extracted principle, biological hook, and governance/lore hook
- [x] Update the image index so the image layer is usable for concept support without chapter-level overreach

### Issue #21: Create the world-bible authority registry

- [x] Define a reusable authority table that separates `hard authority`, `review-required support`, and `legacy / do not import blindly`
- [x] Map the major `01_WORLD_BIBLE` surfaces and key files to those tiers
- [x] Update intake docs so `SC_STORYOPS` cites the new registry instead of relying on shorthand lore labels

### Issue #19: Normalize task tracking and add a lessons log

- [x] Define `tasks/` as the active operations surface
- [x] Create `tasks/lessons.md`
- [x] Record baseline prevention rules for tracker drift, missing authority inputs, readiness language, and chapter-count drift
- [x] Update high-visibility docs to point at the new tracking system or mark older trackers as historical
- [x] Verify there is no competing active task board left in repo-facing surfaces

### Issue #20: Audit chapter-count and readiness drift

- [x] Confirm the canonical state from `SC_STORYOPS`:
  - `27` canonical chapters
  - arcana is not chapter-count parity
  - current phase is trilogy-wide `v0.2` intake / mapping
  - readiness language should distinguish export readiness from mapping completeness
- [x] Update high-visibility docs that still claim final production / release-ready / interactive implementation as the active phase
- [x] Verify high-visibility docs no longer contradict current phase or chapter-count policy

### Issue #18: Restore SC_STORYOPS authority spine and path integrity

- [x] Inventory repo-local and external references under `06_WORKBENCH/SC_STORYOPS/story`
- [x] Classify broken references into `replace`, `mark external`, or `remove`
- [x] Patch canonical workbench docs to point at live sources
- [x] Patch downstream packet references that still cite phantom trilogy doctrine files
- [x] Verify the active intake workflow no longer cites missing local files without an availability note

## Review

- `03_EDITORIAL/scan_consistency.py` now resolves paths relative to the current checkout and writes its report back into `03_EDITORIAL/consistency_report.md` instead of a stale absolute path outside the repo.
- The repaired audit helper now runs successfully against the current compiled trilogy surfaces, and the regenerated consistency report currently finds no terminology issues in Book 1, Book 2, or Book 3.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_hard_authority_pack.md` now consolidates the late-trilogy rules that are already safe from `hard authority`, including Gardener posture, vector logic, refusal logic, and the trilogy end-goal continuity inherited from Books `1-2`.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_macro_governance_pack.md` now separates usable governance pressure from stale worldbuilding bulk and adjacent Meru / vault synthesis without promoting any of it directly to canon.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_concept_authority_matrix.md` now makes the freeze operational by showing which Book `3` concepts are ready for `16-18` source mapping, which remain `soft-high`, and which stay projection-heavy.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/README.md` now points directly at the required intake artifacts before any unfreeze decision is made.
- `06_WORKBENCH/SC_STORYOPS/story/intake/noesis_image_cluster_registry.md` now expands `Strategic deception layers` with witness/exposure/memory and admissibility-control sisters, expands `Cellular polity / authored reality` with border-intelligence and lawful-division sisters, and strengthens the tetramorphic family with a radiant-authority lane.
- `06_WORKBENCH/SC_STORYOPS/story/image_index.md` and `intake/image_principles.md` now make the Book `3` image families explicit as narrative arguments rather than thin mood-board handles.
- The Book `3` freeze no longer depends on raw singleton scarcity in those two image families; the projection rerun now narrows the next blocker to compiled-surface audit, cross-book carryover validation, and macro-governance corroboration.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_projection_board.md` now restates Book `3` by chapter cluster: `16-18` are source-packet-map ready, `19-24` remain soft for different reasons, and `25-27` stay projection-heavy.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_source_packet_map.md` now turns the Book `3` cluster ruling into an executable inheritance map, separating mandatory authority packets, review-required support packets, image packets, carryover constraints, and not-yet-safe imports for `16-18`, `19-21`, `22-24`, and `25-27`.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/README.md` now treats the new source packet map as a required intake artifact before any unfreeze decision.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_compiled_surface_audit.md` now records the actual compiled `Book 3` drift surface: embedded scaffolding still in-body, Chapter `18` as the densest exposition/voice-flattening hotspot, unstable witness/vector lexicon, and an over-mechanized Gardener register.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_entry_carryover_validation.md` now records the `Chapter 15 -> 16` hinge state: thematic carryover is strong, but the Verath case bridge is recap-heavy, threshold retention is underdramatized, and house-politics pressure thins too sharply at Book `3` entry.
- `06_WORKBENCH/SC_STORYOPS/story/intake/book_3_delta_ledger.md` now orders the actual packet-opening risks: compiled scaffolding contamination, Chapter `18` exposition collapse, `15 -> 16` threshold softness, Gardener over-mechanization, lexicon instability, `22-24` governance/sermon risk, and `25-27` premature-mastery drift.
- The delta ledger now sharpens `Issue 13`: either keep the freeze fully intact, or open only `16-18` starter packets under explicit ledger constraints. Nothing later is cleared.
- `Issue 13` is now decided in favor of a narrow opening: `06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/packet_board.md` plus starter packets `16-18` opened first while `working/` still remained closed and `19-27` stayed freeze-controlled.
- `Chapter 16`, `17`, and `18` starter packets were first opened as delta-constrained scaffolds; only the later `Issue 14` decision promotes `Chapter 16` beyond packet-only status.
- `Issue 14` is now decided in favor of the narrowest possible Book `3` prose opening: `Chapter 16` is active under `working/`, `Chapter 17-18` remain packet-only, and `Chapter 19-27` remain freeze-controlled.
- The first `Chapter 16` pass strips embedded scaffolding, restores the `Chapter 15 -> 16` hinge discipline, normalizes witness-vessel and self-consciousness language, and keeps the descent field explicitly non-fusional.
- `Chapter 16` is now stabilized to a compiled-comparison baseline: the working copy carries explicit review-House consequence, tighter Verath-case continuity, stronger no-fusion threshold language, and no residual scaffolding or stale witness-vessel phrasing.
- `Packet 16` now marks the lane `ready for compiled comparison`, while `Chapter 17-18` remain packet-only and outside prose.
- The concrete `Chapter 16` versus compiled-Book-3 deltas are now recorded in `Packet 16`: stronger `15 -> 16` hinge carryover, tighter House-stakes framing, normalized self-consciousness / witness-vessel lexicon, removal of embedded production scaffolding, and a more role-bound procedural reveal.
- `Issue 15` is now decided in favor of a serial opening with a hard stop: `Chapter 17` is promoted into the second active Book `3` prose lane, `Chapter 18` remains packet-only, and `Chapter 19-27` remain freeze-controlled.
- The `Chapter 17` first pass is allowed because `Chapter 16` proved the lane can hold threshold discipline, while the Gardener reveal still has a local enough risk profile to edit without opening the `Chapter 18` hotspot.
- `Chapter 17` is now stabilized to a compiled-comparison baseline: the working copy keeps the Gardener local, restores a concrete House-level consequence on return, preserves shared-field / no-fusion discipline, and avoids manifesto closure.
- The concrete `Chapter 17` versus compiled-Book-3 deltas are now recorded in `Packet 17`: stronger `Chapter 16 -> 17` threshold carryover, normalized witness-vessel and self-consciousness lexicon, tighter Gardener locality, restored House-level consequence on return, and removal of embedded production scaffolding plus manifesto closure.
- `Packet 17` now marks the lane `compiled comparison recorded`, while `Chapter 18` remains packet-only and `Chapter 19-27` remain freeze-controlled.
- The recorded `Chapter 17` deltas are now judged sufficient to open `Chapter 18` in the narrowest valid way: as an active hotspot-constrained prose lane rather than as a blanket Book `3` unfreeze.
- `Packet 18` is now promoted into an active prose lane with a `working/Chapter-18-The-Synthesis-Protocol.md` copy, but the lane remains explicitly fenced against vector drift, ontology overclaiming, role flattening, merger logic, and doctrine monologue.
- `Chapter 18` is now stabilized to a compiled-comparison baseline: the working copy keeps the Triangulation Engine procedural rather than alive, preserves exact `Pure Joy` / `Catalyst Clarity` / `Present Coherence` language, rejects merger logic, and restores House-level consequence to the synthesis frame.
- The concrete `Chapter 18` versus compiled-Book-3 deltas are now recorded in `Packet 18`: stronger immediate post-Gardener chamber stakes, normalized lexicon and shorter naming, exact three-vector operational language, preserved non-fusional shared-field discipline, rejection of Engine-as-new-life rhetoric, and removal of embedded production scaffolding plus manifesto closure.
- `Packet 18` now marks the lane `compiled comparison recorded`, while `Chapter 19-27` remain freeze-controlled pending the next gate decision.
- The recorded `Chapter 18` deltas are now judged sufficient to open `Chapter 19`, but only as a constrained starter packet rather than a prose lane.
- `Packet 19` now exists as the first `19-21` packet surface: it captures the compiled branch's hinge reset, stale lexicon, merger drift, scaffolding contamination, and protocol-overexplanation risks without authorizing a `working/` copy yet.
- `Chapter 19` prose remains closed for now; `Chapter 20-27` remain freeze-controlled until the new packet contract proves the triangulation lane can stay procedural, embodied, and non-sermonic.
- `Packet 19` is now judged strong enough to promote `Chapter 19` into an active prose lane without widening the cluster beyond it.
- [Chapter-19-The-Three-Point-Problem.md](/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Somatic-Canticles-book/Somatic-Canticles/06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/working/Chapter-19-The-Three-Point-Problem.md) now inherits the live `Chapter 18` handoff directly, removes the stale three-day reset and old lexicon, keeps `Pure Joy` / `Catalyst Clarity` / `Present Coherence` exact, and preserves non-fusional shared-field discipline while turning triangulation back into live procedure.
- `Chapter 19` is now the fourth active Book `3` prose lane; `Chapter 20-27` remain freeze-controlled pending a later gate decision.
- `Chapter 19` is now stabilized to a compiled-comparison baseline: the working copy keeps triangulation procedural, removes the last filter-word residue from the active lane, and holds the old protocol labels beneath rather than above the earned `Pure Joy` / `Catalyst Clarity` / `Present Coherence` frame.
- The concrete `Chapter 19` versus compiled-Book-3 deltas are now recorded in `Packet 19`: direct `Chapter 18 -> 19` handoff instead of a three-day reset, normalized lexicon and naming, exact vector language over older protocol-label drift, rejection of merger rhetoric, procedural rather than montage/manifesto triangulation, and removal of embedded compiled scaffolding.
- `Packet 19` now marks the lane `compiled comparison recorded`, which is strong enough to open `Packet 20` but not yet strong enough to authorize a `working/Chapter 20` copy.
- `Packet 20` now exists as a starter packet only: it captures the compiled/source branch's merger rhetoric, explanatory inflation, stale field branding, and premature `Test Fire` escalation without opening prose.
- `Packet 20` is now judged strong enough to promote `Chapter 20` into an active prose lane without widening the cluster beyond it.
- [Chapter-20-The-Convergence-Point.md](/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Somatic-Canticles-book/Somatic-Canticles/06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/working/Chapter-20-The-Convergence-Point.md) now inherits the live `Chapter 19` exit directly, rejects merger rhetoric and stale field-brand language, keeps convergence procedural, and holds the `Chapter 20 -> 21` boundary by stopping at threshold rather than live fire.
- `Chapter 20` is now the fifth active Book `3` prose lane; `Chapter 21-27` remain freeze-controlled pending a later gate decision.
- `Chapter 20` is now stabilized to a compiled-comparison baseline: the working copy keeps convergence embodied and role-bound, removes packet corruption from the review surface, and preserves threshold-without-Test-Fire discipline.
- The concrete `Chapter 20` versus compiled-Book-3 deltas are now recorded in `Packet 20`: direct `Chapter 19 -> 20` handoff instead of a fresh chamber reset, normalized lexicon over old field branding, rejection of merger rhetoric, embodied convergence over substrate sermon, exact wound-handling instead of uplifted explanation, and a clean stop before `Chapter 21` live-fire pressure.
- `Packet 20` now marks the lane `compiled comparison recorded`, while `Chapter 21-27` remain freeze-controlled pending the next gate decision.
- The recorded `Chapter 20` deltas are now judged sufficient to open `Packet 21`, but not yet a `working/Chapter 21` prose lane.
- `Packet 21` now exists as a starter packet only: it captures the compiled/source branch's reset framing, merged-field rhetoric, stale field branding, live-fire inflation, and scaffolding residue without authorizing prose.
- `Packet 21` is now judged strong enough to promote `Chapter 21` into an active prose lane without widening the cluster beyond it.
- [Chapter-21-The-Test-Fire.md](/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Somatic-Canticles-book/Somatic-Canticles/06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/working/Chapter-21-The-Test-Fire.md) now inherits the live `Chapter 20` exit directly, rejects reset framing and merger rhetoric, keeps the Test Fire local and procedural, and preserves the boundary to `Chapter 22` by ending at first hostile-contact consequence rather than temptation logic.
- `Chapter 21` is now the sixth active Book `3` prose lane; `Chapter 22-27` remain freeze-controlled pending a later gate decision.
- `Chapter 21` is now stabilized to a compiled-comparison baseline: the working copy keeps the Test Fire local, procedural, and role-bound, preserves differentiated shared-field discipline under notice pressure, and makes the House / station review consequence explicit without bleeding into `Chapter 22`.
- The concrete `Chapter 21` versus compiled-Book-3 deltas are now recorded in `Packet 21`: direct `Chapter 20 -> 21` threshold carryover instead of a three-day reset, normalized vector and witness lexicon over stale field-brand language, rejection of merged-observation rhetoric, local first-contact pressure over proto-liberation theater, explicit House / station review consequence, and removal of embedded compiled scaffolding plus countdown urgency.
- `Packet 21` now marks the lane `compiled comparison recorded`, while `Chapter 22-27` remain freeze-controlled pending the next gate decision.
- The recorded `Chapter 21` deltas are now judged sufficient to open `Packet 22`, but not yet a `working/Chapter 22` prose lane.
- `Packet 22` now exists as a starter packet only: it captures the compiled/source branch's false-peace and false-certainty temptations, reset softness, over-smooth harmony, and scaffolding residue without authorizing prose.
- `Packet 22` review is now complete: the chapter stays prose-closed because the current branch still lacks the full `Chapter 22` custom-temptation contract, especially Corv's false-mercy / perfect-ending lane.
- `Packet 22` is now refined against the full `Chapter 22` custom-temptation contract: Jian, Sona, and Corv each have an explicit required offer/refusal lane on the packet surface, and Gideon's `Chapter 23` safety lane is now enforced as a boundary rather than backfilled early.
- `Packet 22` is now judged strong enough to promote `Chapter 22` into an active prose lane without widening the cluster beyond it.
- [Chapter-22-The-Perfect-World.md](/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/Somatic-Canticles-book/Somatic-Canticles/06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/working/Chapter-22-The-Perfect-World.md) now inherits the live `Chapter 21` exit directly, adds Corv's `Perfect Ending / False Mercy of Meaning` refusal lane, and keeps Gideon's `Chapter 23` safety temptation out of the chapter.
- `Chapter 22` is now the seventh active Book `3` prose lane; `Chapter 23-27` remain freeze-controlled pending the next gate decision.
- `Chapter 22` is now stabilized to a compiled-comparison baseline: the working copy keeps counterfeit-kindness pressure live from `Chapter 21`, makes Corv's refusal lane local rather than sermonic, and preserves the boundary so Gideon's safety temptation does not bleed forward from `Chapter 23`.
- The concrete `Chapter 22` versus compiled-Book-3 deltas are now recorded in `Packet 22`: direct `Chapter 21 -> 22` counterfeit-kindness carryover instead of softened aftermath glow, cleaner and less cosmetically elevated refusal language, a fully restored Corv false-mercy lane that the compiled branch lacks entirely, a harder boundary against `Chapter 23` safety pressure, and removal of all embedded compiled scaffolding.
- `Packet 22` now marks the lane `compiled comparison recorded`, while `Chapter 23-27` remain freeze-controlled pending the next gate decision.
- GitHub umbrella issues `#18-23` are now closed with completion notes, so the remote backlog once again matches the local StoryOps tracker state.
- `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md` now matches the active Book 2 working lane rather than the older compiled prose branch.
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` is no longer hybrid at the Book 1 / Book 2 boundary; it now carries the merged Book 1 `Chapter 08` exit directly into the merged Book 2 `Chapter 09` opening.
- The omnibus also now restores a proper `# Chapter 16: The Wilt` heading break instead of leaving that transition glued to the end of old Book 2 prose.
- The Book 1 coherence pass found smaller but real residual drift in the active lane: `Chapter 02` still carried an older Quoril doctrine label, and `Chapter 05-06` were missing the fuller chapter metadata frame already present elsewhere in the lane. That drift is now normalized before merge-back.
- `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md` now matches the active Book 1 working lane rather than the older, more expository compiled surface.
- The highest-value compiled Book 1 deltas are now resolved in canon:
  - continuity: the compiled Book 1 surface now carries the active lane's chapter-to-chapter pressure instead of resetting at key turns
  - register: the compiled surface now uses the tighter working-lane prose instead of older consciousness-theory exposition and inflated metaphysical framing
  - role specificity: Jian, Sona, Gideon, and Corv now keep their sharper operational voices instead of flattening into shared revelation language
  - boundary logic: the `Chapter 08` ending now preserves the faint forward-bearing and withheld anomaly notice that Book 2 `Chapter 09` is built to inherit
- `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` now carries the merged Book 1 `Chapter 01-08` surface, but it intentionally remains hybrid at the `Chapter 08 -> Chapter 09` boundary until Book 2 is merged back.
- The Book 2 coherence pass found one real residual inconsistency: `Chapter 12-15` still carried older metadata framing (`mastery`, `harmonization`, `cathedral`, `purification`) even though the active body prose had already been tightened. That top-matter drift is now normalized.
- The highest-value compiled Book 2 deltas are now clear across the whole lane:
  - continuity: the active lane carries exact chamber-to-chamber handoffs, while the compiled surface still resets too often at chapter openings
  - terminology: the active lane removes stale doctrinal/procedural labels and uses the current `SC_STORYOPS` register
  - voice: the active lane gives each lead a harder, role-specific function instead of letting revelation language flatten everyone into one chorus
  - posture: the active lane consistently rejects premature mastery, merger, coronation, and sermonizing in favor of threshold, procedure, and earned coordination
- Merge-back order is now decided: Book 1 should merge first, then Book 2.
- The reason is structural rather than sentimental: the active Book 2 opening in `Chapter 09` depends on the recalibrated `Chapter 08` exit state from Book 1, so merging Book 2 first would preserve internal Book 2 coherence while still leaving the compiled cross-book handoff stale.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_2_myocardial_chorus/README.md` and `06_WORKBENCH/SC_STORYOPS/story/chapters/README.md` now agree that Book 2 is an active packet lane rather than a provisional stub.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_2_myocardial_chorus/packets/09-15` now all carry active-prose metadata, canonical source references, compiled-surface comparison notes, and `ready for compiled comparison` baseline status.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_2_myocardial_chorus/working/Chapter-09-The-Sigil-Smith.md` through `Chapter-15-The-Witness-Integration.md` now form a complete first-pass Book 2 working lane with differentiated chapter logic instead of carried-over compiled exposition.
- `tasks/README.md` now defines the planning contract:
  - `tasks/todo.md` = active task tracker
  - `tasks/lessons.md` = recurring lessons log
  - `memory.md` = historical context, not the active board
- `tasks/lessons.md` now captures the baseline rules that would have prevented the source-graph and tracker drift discovered in issues `#18` through `#20`.
- `06_WORKBENCH/SC_STORYOPS/story/intake/world_bible_authority_registry.md` now makes the world-bible authority tiers explicit, including file-level overrides for readmes and machine indexes.
- `06_WORKBENCH/SC_STORYOPS/story/intake/noesis_image_cluster_registry.md` and `06_WORKBENCH/SC_STORYOPS/story/image_index.md` now carry second-pass coverage across the priority clusters instead of leaving them as single-image placeholders.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_1_anamnesis_engine/packet_board.md` now turns Chapters `01-08` into an evidence-backed packet board instead of a placeholder lane.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_1_anamnesis_engine/packets/` now contains starter packets for all eight Book 1 chapters, and `Chapter 01-08` are now promoted into `working/`.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_1_anamnesis_engine/working/Chapter-01-The-Choroid-Plexus.md` is now the first active Book 1 working copy.
- Packet `01` now carries active-prose metadata, and the first pass tightened wider-regression foreshadowing plus Jian/Gideon command-language precision without opening a full rewrite.
- Packet `01` is now marked baseline-ready for compiled comparison rather than open-ended drafting.
- Packet `02` is now marked baseline-ready for compiled comparison and records where the compiled Book 1 surface still overexplains doctrine, softens Jian, and turns the redaction into an earlier tunnel reveal.
- The active diagnostic lane now uses the canonical `Manas Interface` naming for Jian across `Chapter 01-02`, and the residual `Daoist Quantum Mechanics` phrasing has been normalized to field-language in `Chapter 02`.
- Packet `03` is now promoted into an active prose lane with a `working/Chapter-03-The-Blood-Brain-Barrier.md` copy.
- Packet `04` is now promoted into an active prose lane with a `working/Chapter-04-The-Emperors-Genome.md` copy, and its first pass keeps The Gardener local, conservational, and morally unsettling rather than fully exposed.
- Packet `05` is now promoted into an active prose lane with a `working/Chapter-05-The-Endocrine-Dogma.md` copy, and its first pass keeps the HPA-axis loop embodied, doctrinal, and tethered to the authored-rot trail from `Chapter 04`.
- Packet `06` is now promoted into an active prose lane with a `working/Chapter-06-The-Synaptic-Crossroads.md` copy, keeping Jian/Sona method conflict sharp until the measurable pulse forces alignment.
- Packet `07` is now promoted into an active prose lane with a `working/Chapter-07-The-Breathfield-Weaver.md` copy, keeping regulation physiological and exposing the healer-shadow beat where imposed calm becomes suppression.
- Packet `08` is now promoted into an active prose lane with a `working/Chapter-08-The-Compass-Calibration.md` copy, keeping compass/compassion as an operational discovery rather than a slogan.
- The Book 1 lane now consistently reports `Chapter 01-08` as active working copies, with the full book converted into the first-pass working lane.
- The Book 2 lane now consistently reports `Chapter 09-15` as active working copies, with the full book converted into the first-pass working lane.
- Packet `03` now treats Gideon's threshold ethics, the Pattern Weavers, and the repair-versus-replacement distinction as the controlling local posture for any later merge-back.
- `06_WORKBENCH/SC_STORYOPS/story/chapters/book_3_the_ripening/README.md` now makes the late-trilogy freeze explicit instead of implying it.
- Root `README.md` now points to `tasks/todo.md` and `tasks/lessons.md`.
- Root `todo.md` is now an explicit status snapshot rather than a competing live task board.
- Root `PLAN.md` is now a strategic sequencing snapshot rather than a live checklist.
- Verification:
  - the Book 1 lane, packet board, and packet metadata now consistently report `Chapter 01-08` as active working copies
  - the Book 2 lane, packet metadata, and chapter-lane README now consistently report `Chapter 09-15` as active working copies
  - Packet `01-03` mark the diagnostic architecture lane as active prose work, `04-06` mark patterned captivity as active prose work, and `07-08` mark calibration/reorientation as active prose work
  - the current `Chapter 01-08` working copies resolve on disk and differ from their source chapters only in the intended first-pass edits
  - `02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md` now resolves to the active `Chapter 01-08` working lane rather than the older compiled prose branch
  - Packet `01-08` are now baseline-ready for compiled comparison rather than open-ended drafting
  - Packet `09-15` are now baseline-ready for compiled comparison rather than provisional stubs
  - the Book 2 coherence pass now confirms `Chapter 09-15` share one working register at both metadata and body-prose level
  - the current `Chapter 09-15` working copies resolve on disk and differ from their source chapters only in the intended first-pass edits
  - `02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md` now resolves exactly to the active `Chapter 09-15` working lane
  - `02_MANUSCRIPTS/COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md` now matches the merged Book 1 and Book 2 surfaces through `Chapter 15`, with a proper `Chapter 16` break restored
  - no active Book 2 packet or working chapter now uses the stale `Manas Yantra` or `Khalorēē Field Architecture programming` terminology as live prose
  - all eight Book 1 starter packet files now exist under `story/chapters/book_1_anamnesis_engine/packets/`
  - all seven Book 2 packet files now exist under `story/chapters/book_2_myocardial_chorus/packets/`
  - every packet's canonical chapter source and compiled reference path resolves on disk
  - the story-level README, chapter-lane README, projection board, Book 1 lane, and Book 3 lane now agree on `Book 1` scaffolding and `Book 3` freeze state
  - every world-bible file cited in the new authority registry exists
  - every Noesis image file named in the upgraded second-pass registry exists in the mounted research corpus
  - `SC_STORYOPS` now cites `world_bible_authority_registry.md` from the story README, source lattice, lore map, and clarify log
  - no active/high-visibility doc matches the old `22 chapters`, `26 chapters`, `Production / Final Polish`, `Interactive Experience Design & Easter Egg Implementation`, or `Moving to Final Production` claims
  - the only remaining `release-ready` hits in active docs are prevention rules, not status claims
  - `git diff --check` is clean
