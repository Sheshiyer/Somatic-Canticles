# Somatic Canticles Image Library (Curated)

This folder contains the **brand-relevant curated media** copied from:
- `/Volumes/madara/2026/Somatic-Canticles/somatic-canticles/generated`

## Brand Context Applied

From `wiki-output` docs, the visual brand is **Clinical Mysticism — Rigorous Sacred**:
- neuroscience precision + visionary mysticism
- tarot biological mapping (0–21 major arcana)
- trilogy identity (3 books / 3 phases)
- symbolic logo systems (glass + wax seal variants)

## Curated Sets

- `arcana/` → 22 tarot-biological chapter assets
- `anatomy/` → 8 biological systems visuals (heart-brain, vagal, triangulation, etc.)
- `covers/` → 3 trilogy book covers
- `logos/` → 8 logo variants
- `brand-kit/` → brand bento grid (overview board)

## Why WebP

WebP variants were selected for source usage to keep docs/pages lightweight and fast.

## Astro Usage Example

```mdx
import cover1 from '@/images/covers/book-cover-1-anamnesis-engine.webp';

<img src={cover1.src} alt="Book 1 cover" />
```

Or from markdown with static path patterns, depending on your page/layout pipeline.
