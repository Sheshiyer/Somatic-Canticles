# Task: Wiki Source Commit, QA, And UI Rehaul

## Plan
- [x] Inspect project instructions and current repo state
- [x] Verify current Astro build and deploy state
- [x] Inventory source docs and available visual assets
- [x] Rebuild IA and visual system around the actual Somatic Canticles brand assets
- [x] Fix functional UX gaps: mobile navigation and real search
- [x] Add asset-led homepage and a full visual atlas that maps the curated image library
- [x] Enhance doc pages with contextual visuals, stronger hierarchy, and related reading
- [x] Verify local build plus link and content integrity
- [x] Redeploy and validate the live wiki
- [ ] Stage and commit the wiki source changes

## Review
- Current state already has the source docs mapped from `wiki-output/` and the curated 42-image library mapped from `somatic-canticles/generated` into `brand-wiki-site/src/images`.
- Live QA found two concrete UX issues before redesign:
  - Mobile navigation collapses by hiding the sidebar without providing a replacement.
  - Search modal opens but does not search anything.
- Design direction selected from the requested skills:
  - Editorial archive rather than generic docs landing page.
  - Single premium warm-metal palette with gold accent, not purple/blue AI gradients.
  - Asset-led storytelling using covers, anatomy diagrams, logo system, and arcana gallery.
- Verification completed after redesign:
  - `npm run build` passes locally.
  - Static integrity pass over `dist/` reports `0` broken internal route or asset references and `0` leftover `.md` links.
  - Production alias `https://somatic-canticles-wiki.vercel.app` now serves the redesigned homepage, rewritten doc shell, and the visual atlas with all 42 mapped assets.
