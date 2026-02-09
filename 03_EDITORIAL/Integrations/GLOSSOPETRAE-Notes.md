# GLOSSOPETRAE → Somatic Canticles (Integration Notes)

**Source repo (local):** `04_SOURCES/External-Research/GLOSSOPETRAE/`

## 1) What it is (editorial summary)

GLOSSOPETRAE is a **seeded conlang generator** (JS, zero dependencies) that outputs a full language plus a **Skillstone**—a compact, agent-teachable language spec.

For SC, treat it as:

- a *procedural language forge* to generate faction tongues, ritual registers, and inscriptional scripts;
- a *diegetic artifact generator*: Skillstones can become “tongue-stones”/tablets/manuals that transmit a canticle tradition.

It generates:
- phonology + phonotactics
- prosody (tone/stress/intonation)
- morphology (case/verbs/agreements)
- lexicon (semantic fields)
- writing system (script)
- translation examples + interlinear gloss

## 2) Key hooks for Somatic Canticles worldbuilding

### A. Somatics → phonology/phonotactics
Use mouth/breath constraints as story logic:
- a sect trained in nasal breathwork → nasal-heavy inventories
- augmented jaw/teeth culture → click/affricate-heavy inventories
- vow-of-silence order → vowel-only humming register (restrict onset consonants)

### B. Canticles → prosody
Prosody is the bridge to SC:
- tone languages → “pitch-locked” ritual melodies
- stress systems → breath/beat choreography
- rhythmic constraints → chant meters; can be mirrored in action pacing

### C. Scripts → props & archaeology
Script generation supports:
- marginalia, tattoos, hospital forms, monastery ledgers
- carved “skillstones” (stone/teeth/amulets) with glyphs

### D. Dead language revival → lineage + authority
Revival modes let you create “authority languages”:
- Neo-Latin mutated for medical guilds
- Ancient Greek authentic for scholastic/temple archives
- Proto-IE speculative for deep-time myth layers

### E. Ephemeral languages → liturgical cycles
Time-rotating languages model:
- daily changing prayer keys
- weekly vow-renewals
- seasonal metamorphosis rites

> Editorial caution: the repo includes overt “covert/stego/adversarial” framing for AI security research. In SC, use this as **fictional semiotic power** (secrecy, initiation, taboo) rather than an instruction set.

## 3) Quick start (for writers / designers)

### Web UI
```bash
open "01-Projects/Somatic-Canticles/04_SOURCES/External-Research/GLOSSOPETRAE/index.html"
```

### Node demo
```bash
cd "01-Projects/Somatic-Canticles/04_SOURCES/External-Research/GLOSSOPETRAE"
node test.mjs
```

### Minimal JS snippet
```js
import { Glossopetrae } from './src/Glossopetrae.js';

const lang = Glossopetrae.musical(20260204);
const ex = lang.translationEngine.translateToConlang('The body remembers the vow.');
console.log(lang.name, ex.target);
```

## 4) Dependency / license notes

- Node >= 18 or any modern browser
- zero external dependencies; works offline
- **AGPL-3.0**: OK for internal worldbuilding; be cautious if publishing modified engine code as part of a distributed project.

## 5) What to extract into the SC vault (recommended)

### A. Create “Language Packets” (canonical artifacts)
For each SC faction/arc, store a language packet (outside the repo):
- Seed + method (preset/factory) used
- Skillstone text (or excerpted sections)
- 10–30 core phrases (greetings, oaths, commands, taboos)
- Pronunciation & performance notes (somatic notes)
- Script samples (glyph sheet / screenshots)

Suggested template:
- `# <Language Name> (Seed <n>)`
- `## Speakers / Institution`
- `## Phonology (sound palette for scenes)`
- `## Prosody (how it’s chanted)`
- `## Morphology tells you what the culture notices`
- `## Lexicon: sacred words`
- `## Scene-ready phrases`

### B. Seed registry (continuity)
Create a single page tracking canonical seeds:
- language name, seed, method, faction, first appearance, status

### C. Visual prop pipeline
When a script is generated:
- screenshot the glyph inventory
- trace/standardize into an SC “font sheet”
- keep 3–5 recurring logograms for motifs (vow/body/breath/stone)

## 6) PARA mapping (editorial operations)

- **Projects:** each story arc that needs a tongue gets a packet + seed locked.
- **Areas:** “Linguistics & Semiotics” continuity; seed registry; naming conventions.
- **Resources:** this repo + selected Skillstones; phoneme palettes; script references.
- **Archive:** retired seeds/packets.

## 7) Most important docs / entry points (index)

- `README.md` — feature overview + factory methods
- `AGENT_QUICKSTART.md` — fast API examples
- `src/Glossopetrae.js` — authoritative list of generators (musical/archaic/tonal/abugida/etc.)
- `src/modules/ProsodyEngine.js` — prosody model (key for canticles)
- `src/modules/ScriptGenerator.js` — writing system options (key for props)
- `src/modules/StoneGenerator.js` — Skillstone structure (diegetic artifact)
- `skills/glossopetrae/SKILL.md` — skill interface and commands

## 8) SC-specific “promptable” use cases (ready to deploy)

1) **Ritual chant tongue** (for scenes): `Glossopetrae.musical(seed)`
2) **Archive/temple language**: `Glossopetrae.archaic(seed)` or `Glossopetrae.reviveGreek('authentic', seed)`
3) **Medical guild argot**: `Glossopetrae.reviveLatin('mutated', seed)`
4) **Initiation language that changes daily**: `Glossopetrae.ephemeral(seed, 'daily')`
5) **Island/communal folk tongue**: `Glossopetrae.quick(seed)` or `PRESETS.oceanic`

## 9) Open questions (for main SC decisions)

- How many canonical tongues will SC support without overwhelming readers?
- Will the story show scripts directly (props), or mostly phonetic romanization?
- Are “tongue-stones” literal artifacts in-world (teeth/stone tablets) or metaphorical manuals?
- What is the aesthetic constraint set (preferred phoneme palette, preferred script shapes)?
