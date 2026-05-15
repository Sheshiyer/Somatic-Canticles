# SWA-021 Contract: Language and Locale Metadata

## Metadata Fields
- `language_hint` (ISO code when known)
- `script_hint` (latin/devanagari/etc)
- `locale_hint` (optional region)
- `translation_needed` (boolean)

## Rules
1. Unknown language must be `unknown` not blank.
2. Mixed-language nodes should include dominant language plus notes.
3. Query evaluation must include cross-language match checks.
