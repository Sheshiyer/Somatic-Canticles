# SC_STORYOPS Input Availability

## Purpose

This file records which upstream inputs are repo-local, which are external but currently mounted, and which have to be treated as unavailable in this checkout.

Use it when a `story/` document needs to decide whether to cite:

- a canonical repo file,
- an external mounted research file,
- or a handle-level registry that stands in for an unavailable source corpus.

## Availability Matrix

| Source Family | Status | Current Authoritative Surface | Notes |
| --- | --- | --- | --- |
| Trilogy editorial doctrine and tone rules | repo-local replacement available | `03_EDITORIAL/EDITORIAL_BRIEF.md`, `03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md`, `03_EDITORIAL/TERMINOLOGY_CLEANUP_PLAN.md`, `03_EDITORIAL/Book_3_Editorial_Pass.md`, `01_WORLD_BIBLE/01_PROTOCOLS_AND_SYSTEMS/01_BIOLOGICAL_STYLE_GUIDE.md` | The older `TRILOGY_*` filenames cited in early `SC_STORYOPS` docs are not present in this repo. Their duties are split across these files. |
| Core world-bible canon | repo-local | `01_WORLD_BIBLE/00_CORE_FOUNDATION/`, `01_WORLD_BIBLE/01_PROTOCOLS_AND_SYSTEMS/`, `01_WORLD_BIBLE/02_CHARACTER_SYSTEM/` | Canonical trilogy inputs. |
| Mounted external Noesis research | external and currently mounted | `/Users/sheshnarayaniyer/Documents/noesis/Research/Excerpts.md`, `/Users/sheshnarayaniyer/Documents/noesis/Research/Images.md` | Valid outside-repo dependencies. |
| Mounted external `03-Resources` vault | external and currently mounted | `/Volumes/madara/2026/twc-vault/03-Resources/...` | `story/` docs may cite these paths directly when packet work requires them. |
| Synchronocities article and card corpus | external but currently unavailable in this checkout | `intake/blog_article_registry.md`, `image_index.md` | The earlier `/Volumes/madara/2026/twc-vault/01-Projects/synchronocities-blog/...` paths are not mounted here. Use local handle registries unless the source project is restored. |
| Brandmint machine-readable manifest | external and unavailable in this repo | `image_index.md`, `intake/image_principles.md` | No `brandmint-input/somatic-canticles/generation-manifest.json` tree exists in this checkout. Use the local Brandmint family registry and extracted image principles instead. |

## Use Rule

- Prefer repo-local canonical files when they exist.
- Keep mounted external dependencies explicit and absolute.
- If a previously cited source corpus is unavailable here, cite the local registry that preserves its extracted handles instead of repeating a dead path.
