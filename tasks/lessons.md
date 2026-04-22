# Lessons

- When the user asks for wiki asset mapping, use the Brandmint handoff artifacts (`generation-manifest.json`, asset-map logic, synced media manifest) as the source of truth instead of deriving structure directly from `src/images` folder layout.
- When the user explicitly says to use the upstream Brandmint pipeline, run and verify the actual commands from `/Volumes/madara/2026/twc-vault/01-Projects/brandmint` instead of relying on repo-local assumptions or partial reproductions.
- Treat Brandmint `preview --json` and `visual generate` as separate code paths; verify exclusions on both before claiming provider-cost controls are working.
- For asset-parity questions, compare the committed archive inventory and category counts against the generated manifest IDs, not just against prompt names or aesthetic similarity.
- When the user says the upstream branch is fixed, verify the local checkout state again and do implementation work in a clean worktree if the parent repo is still dirty or stale.
- When the user narrows scope to one repo, stop cross-repo git work immediately and only stage, commit, and push files from the requested repo/surface.
- When the user frames `SC_STORYOPS` as a trilogy-wide `v0.2` intake and extraction pass, do not collapse execution to a single-book pilot. Keep vault/resource/image principle mapping upstream, and treat book assignment as a downstream projection unless the user explicitly asks for a per-book lane first.
- When the user explicitly names an adjacent project like `synchronocities-blog` as part of `SC_STORYOPS` intake, register it as a real source domain with article and image handles. Do not leave it implicit inside a generic "wider vault" label.
