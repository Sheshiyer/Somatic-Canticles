# Brandmint Wave 0-9 Audit

## Scope

This audit reconciles the requested "Wave 0 to Wave 9" walkthrough against the actual upstream Brandmint pipeline and the files currently present in this repo.

Source of truth used:

- `brandmint-input/product.md`
- `brandmint-input/brand-config.yaml`
- `brandmint-input/somatic-canticles-asset-registry.yaml`
- `brandmint-input/somatic-canticles/generation-manifest.json`
- `brandmint-input/somatic-canticles/prompt-cookbook.md`
- `brand-wiki-site/src/images/**/*`
- `brand-wiki-site/dist/`
- upstream Brandmint references in `/Volumes/madara/2026/twc-vault/01-Projects/brandmint`

## Discovery Summary

- Planning depth: standard
- Delivery mode: production packaging
- CI/CD expectation: basic GitHub publish flow
- Release model: phased rollout
- Quality bar: file-backed audit plus export verification
- Team topology: solo operator assumptions
- Safe default for publication: create a separate **private** GitHub repo for the Brandmint package, not a public manuscript repo

## Product Definition

The product is already clearly defined in [`brandmint-input/product.md`](/Volumes/madara/2026/twc-vault/01-Projects/Somatic-Canticles/brandmint-input/product.md):

- Name: `Somatic Canticles`
- Category: premium three-book hard science fiction trilogy
- Core proposition: "If Peter Watts wrote *The Body Keeps the Score* as visionary fiction."
- Audience: the "Philosopher-Healer"
- Launch goal: collector-grade literary SF property with crossover traction across hard SF, trauma-healing, embodiment, and consciousness communities

In practice, this repo is not just a manuscript repo. It already contains a Brandmint-ready brand system for the trilogy:

- product definition
- Brandmint config
- custom asset registry
- generated asset manifest
- generated prompt/scripts
- Astro wiki source
- Astro wiki build output

## Assets We Have Now

### Brand-definition assets

- `brandmint-input/product.md`
- `brandmint-input/brand-config.yaml`
- `brandmint-input/aesthetic-profile.json`
- `brandmint-input/somatic-canticles-asset-registry.yaml`
- `brandmint-input/somatic-canticles/prompt-cookbook.md`

### Generation-planning assets

- `brandmint-input/somatic-canticles/generation-manifest.json`
- `brandmint-input/somatic-canticles/scripts/generate-anchor.py`
- `brandmint-input/somatic-canticles/scripts/generate-identity.py`
- `brandmint-input/somatic-canticles/scripts/generate-illustrations.py`
- `brandmint-input/somatic-canticles/scripts/generate-narrative.py`
- `brandmint-input/somatic-canticles/scripts/generate-photography.py`
- `brandmint-input/somatic-canticles/scripts/generate-posters.py`
- `brandmint-input/somatic-canticles/scripts/generate-products.py`

### Generated visual assets already present locally

The committed Astro image library currently contains **42** web-ready visuals:

- `22` arcana cards
- `8` anatomy plates
- `3` book covers
- `8` logo variants
- `1` brand-kit board

These live under [`brand-wiki-site/src/images/`](/Volumes/madara/2026/twc-vault/01-Projects/Somatic-Canticles/brand-wiki-site/src/images).

### Publishing/doc assets already present locally

- full Astro source site in [`brand-wiki-site/`](/Volumes/madara/2026/twc-vault/01-Projects/Somatic-Canticles/brand-wiki-site)
- built static site in [`brand-wiki-site/dist/`](/Volumes/madara/2026/twc-vault/01-Projects/Somatic-Canticles/brand-wiki-site/dist)

## Assets Still Missing Or Not Yet Generated

These are the gaps if the goal is a full Brandmint-to-publication package rather than only the local visual/wiki handoff:

- Wave 6 distribution outputs:
  - finalized launch ads
  - social content engine outputs
  - influencer outreach outputs
  - press-release package
- Wave 7 publishing outputs:
  - NotebookLM notebook export
  - slide decks
  - audio artifacts
  - reports
  - quizzes / flashcards / data tables / mind maps
  - video deliverables
- A standalone GitHub package repo:
  - separate root `README`
  - package-level `.gitignore`
  - standalone repo structure assembled from this repo's source-of-truth files

Also note two drift issues remain from previous work:

- `brand-wiki-site/src/images/README.md` still references missing external source paths
- the current repo already has a GitHub remote (`Sheshiyer/Somatic-Canticles`), so a **new** publishable Brandmint package should be a separate repo, not a force-fit reuse of the current origin

## Wave-By-Wave Audit

## Wave 0: Config Triage

Upstream Brandmint defines Wave 0 as intake/extraction/wizard/export preparation.

Status: **Complete enough for packaging**

Evidence:

- `brandmint-input/product.md` exists
- `brandmint-input/brand-config.yaml` exists
- `brandmint-input/aesthetic-profile.json` exists

Interpretation:

- the intake and config artifacts are already saved in repo form
- the interactive Wave 0 quiz state is not preserved here, but the approved outputs of that stage are

## Wave 1: References + Prompting

Status: **Mostly complete**

Evidence:

- `brandmint-input/aesthetic-profile.json`
- `brandmint-input/somatic-canticles/prompt-cookbook.md`

Interpretation:

- prompt scaffolding and aesthetic direction exist
- the repo does not preserve a committed "top 30 reference library" bundle, so this wave is packaged as resolved prompt intent, not as a reference-corpus archive

## Wave 2: Generation Prep

Status: **Complete**

Evidence:

- generated pipeline scripts exist for anchor, identity, illustrations, narrative, photography, posters, and products

Interpretation:

- the brand is fully past prompt planning and into executable generation prep

## Wave 3: Run Orchestration

Status: **Complete for planning, partial for raw-run retention**

Evidence:

- `brandmint-input/somatic-canticles/generation-manifest.json` exists
- manifest reports:
  - `42` assets
  - `84` API calls
  - estimated cost `$6.72`

Interpretation:

- the orchestration layer clearly ran far enough to produce a finalized manifest
- raw generated intermediate folders are not the source of truth committed here; the repo keeps the curated outputs instead

## Wave 4: Delivery + Handoff

Status: **Complete**

Evidence:

- generated assets have been normalized into the Astro site image library
- counts line up with the curated brand family taxonomy:
  - `arcana: 22`
  - `anatomy: 8`
  - `covers: 3`
  - `logos: 8`
  - `brand-kit: 1`

Interpretation:

- this repo already contains the post-generation handoff layer for docs/site usage

## Wave 5: Visual Surfaces

Status: **Complete for current wiki surfaces**

Evidence:

- the visual families are wired into `brand-wiki-site`
- the built site exists in `brand-wiki-site/dist`

Interpretation:

- the repo already contains a working visual-surface consumer, namely the Astro brand/wiki site

## Wave 6: Distribution

Status: **Missing**

Evidence:

- no committed distribution deliverables were found for ads, social distribution, influencer outreach, or press release packaging

Interpretation:

- Brandmint's downstream launch/distribution outputs are not yet represented in this repo package

## Wave 7: Publishing Deliverables

Upstream Brandmint treats this as NotebookLM publishing and its artifact set.

Status: **Missing**

Evidence:

- no local `deliverables/notebooklm` tree was found
- no committed decks/reports/audio/video artifact bundle is present in this repo

Interpretation:

- the publishing wave has not been packaged locally for Somatic Canticles, even though upstream Brandmint supports it

## Wave 8: Docs + Astro Handoff

Status: **Complete**

Evidence:

- `brand-wiki-site/` source exists
- `brand-wiki-site/dist/` exists

Interpretation:

- this is the strongest completed downstream wave in the repo today

## Wave 9: GitHub Publication

This wave is **not** defined by upstream Brandmint. For this audit, Wave 9 is the final distribution wrapper:

- assemble a standalone repo from the current source-of-truth files
- initialize/push it as a separate GitHub repository

Status: **Pending**

Evidence:

- current origin already points to `Sheshiyer/Somatic-Canticles`
- no standalone Brandmint package repo has been created yet

## Recommended GitHub Package Contents

A clean publishable repo should contain:

- `README.md`
- `docs/BRANDMINT_WAVE_0_9_AUDIT.md`
- `brandmint-input/`
- `brand-wiki-site/`
- optional `brand-wiki-site/dist/` for immediate static review
- package-level `.gitignore`

It should intentionally exclude unrelated manuscript/editorial bulk that is not required for the Brandmint package.

## Default Publication Assumption

If no explicit preference is given, the safest default is:

- repo slug: `somatic-canticles-brandmint-kit`
- visibility: `private`

Reason:

- the source material includes unpublished manuscript/IP surfaces
- the user asked for publication help, but did not explicitly request public release

## Current Recommendation

The repo is already strong enough to publish a **private standalone Brandmint package** immediately, with these caveats:

- Wave 6 and Wave 7 marketing/publishing deliverables are still absent
- `brand-wiki-site/src/images/README.md` still references stale external origins
- the GitHub publication should be a new repo assembled from a curated export, not a reuse of the current manuscript repo root
