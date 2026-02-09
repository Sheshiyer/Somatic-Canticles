# Implementation Plan: Somatic Canticles Finalization

**Goal:** Finalize the Somatic Canticles project infrastructure, documentation, and interactive elements for release readiness.

## Phase 1: Infrastructure & Cleanliness
- [ ] **Task 1: Repository Hygiene**
    - Audit root directory for loose files.
    - Ensure `.gitignore` is comprehensive (Node, System, Skills).
    - Archive deprecated files to `_ARCHIVE`.
- [ ] **Task 2: Documentation Standardization**
    - Verify all top-level directories have a `README.md` (MOC).
    - Ensure all links in `README_NAVIGATOR.md` are valid.
- [ ] **Task 3: Version Control Baseline**
    - Stage all clean files.
    - Create initial commit: "feat: baseline project structure".
    - Push to GitHub remote.

## Phase 2: Interactive Implementation (The Living Book)
- [ ] **Task 4: Web App Scaffolding**
    - Initialize a lightweight Next.js app in `05_DIGITAL_ASSETS/WEB_APP`.
    - Configure routing to consume `somatic_canticles_trilogy_data.json`.
- [ ] **Task 5: Biorhythm Engine Core**
    - Implement `useBiorhythm` hook (Time of Day, Scroll Speed).
    - Create the "Pulse Proxy" component.
- [ ] **Task 6: Text Variation System**
    - Update `Chapter 13` JSON with conditional text blocks.
    - Render variable text based on Biorhythm state.

## Phase 3: Easter Egg Injection
- [ ] **Task 7: The Binary Heartbeat**
    - Implement the binary stream decoder in the Web App.
    - Add the static binary content to the Manuscript (Chapter 13).
- [ ] **Task 8: The Thermochromic Link**
    - Create the hidden landing page for the physical book link.
    - Generate the QR code asset.
- [ ] **Task 9: The Breathfield**
    - Implement microphone/gyroscope listener in Web App.
    - Create the "Witness" overlay visual effect.

## Phase 4: Production Polish
- [ ] **Task 10: Manuscript Final Compilation**
    - Re-run the Omnibus builder with all latest text tweaks.
    - Verify frontmatter/backmatter placement.
- [ ] **Task 11: EPUB/PDF Generation**
    - Generate release-ready EPUB files from the Markdown source.
    - Validate formatting on standard readers.
- [ ] **Task 12: Final Audit**
    - Run `scan_consistency.py` one last time.
    - Manual spot-check of key scenes.

## Phase 5: Release
- [ ] **Task 13: Release Tagging**
    - Tag the git commit as `v1.0.0-gold`.
    - Create GitHub Release with changelog.
- [ ] **Task 14: Deployment**
    - Deploy Web App to Vercel/Netlify.
    - Upload Artifacts to release page.
