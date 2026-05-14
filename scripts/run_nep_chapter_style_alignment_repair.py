#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import REPO_ROOT, word_count
from run_nep_chapter_expansion import (
    DIALOGUE_MATRIX,
    RAW_ROOT,
    build_dossier_context,
    find_preamble_residue,
    load_manifest_row,
    load_matrix_row,
    load_target_row,
    normalize_chapter_text,
    run_style_gate,
    validate_chapter,
    validate_style_gate,
    working_meta,
)

GENERATED_DIR = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
)
AUDIT_JSON = GENERATED_DIR / "book_1_style_alignment_audit_v1.json"

FORBIDDEN_NAME_PATTERNS = [
    r"\bRook\b",
    r"\bPubMed\b",
    r"\bAlex Grey\b",
    r"\bCLIP-Vision\b",
    r"\bRider[- ]Waite\b",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a constrained additive style repair for one expanded chapter.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--mode", choices=["full", "tail"], default="tail")
    parser.add_argument("--min-new-words", type=int, default=1500)
    parser.add_argument("--max-new-words", type=int, default=2300)
    parser.add_argument("--model", default=None)
    parser.add_argument("--audit-json", default=str(AUDIT_JSON))
    parser.add_argument("--tail-anchor", default="Corv turned the prism over one more time")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--max-attempts", type=int, default=1)
    return parser.parse_args()


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def chapter_slug(chapter_number: int, chapter_title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", chapter_title.lower()).strip("-")
    return f"{chapter_number:02d}-{slug}"


def gate_sort_key(path: Path) -> int:
    match = re.search(r"\.gate-(\d+)\.md$", path.name)
    return int(match.group(1)) if match else -1


def next_gate_stage(raw_dir: Path, slug: str) -> int:
    gates = sorted(raw_dir.glob(f"{slug}.gate-*.md"), key=gate_sort_key)
    if not gates:
        return 1
    return max(gate_sort_key(path) for path in gates) + 1


def load_audit_item(path: Path, chapter_number: int) -> dict[str, Any]:
    audit = json.loads(path.read_text(encoding="utf-8"))
    for row in audit.get("chapters", []):
        if int(row.get("chapter_number", -1)) == chapter_number:
            return row
    raise RuntimeError(f"Audit item not found for Chapter {chapter_number:02d} in {path}")


def read_excerpt(path: Path, max_chars: int = 3000) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def contains_forbidden_names(text: str) -> list[str]:
    hits = []
    for pattern in FORBIDDEN_NAME_PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    return hits


def build_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    current_text: str,
    current_words: int,
    target_low: int,
    target_high: int,
    audit_item: dict[str, Any],
    matrix_row: dict[str, Any],
    target_row: dict[str, Any],
    dossier_context: str,
    dialogue_matrix: str,
) -> str:
    matrix_focus = {
        "primary_deficit": matrix_row.get("primary_deficit"),
        "layer_gaps": matrix_row.get("layer_gaps"),
        "best_source_families": matrix_row.get("best_source_families"),
        "notes": matrix_row.get("notes"),
    }
    return f"""
Repair this expanded novel chapter for Book 1 style alignment. This is a constrained additive repair, not a full re-expansion.

Hard output rules:
- Output the full chapter in markdown prose only.
- First line must be exactly: `# Chapter {chapter_number}: {chapter_title}`
- Do not include notes, analysis, bullets, section labels, or production metadata.
- Do not include preamble labels such as `Somatic Event`, `Character Focus`, `Political Context`, `RESONANCE PROFILE`, or `Chapter Status`.
- Do not mention PubMed, DOI, Alex Grey, CLIP-Vision, Rider-Waite, or the fact that a model/audit/runner exists.
- Do not invent additional Somanaut teammates, new operators, or new named systems.

Additive preservation rules:
- The current chapter is `{current_words:,}` words.
- Return a repaired chapter in the `{target_low:,}-{target_high:,}` word range.
- Preserve the current scene order, POV center, and chapter spine.
- Preserve most existing paragraphs and beats; add material before, between, and after them.
- Do not summarize, compress, or replace the chapter with a colder version.
- If a line is already strong, leave it alone and build around it.

Style repair targets:
- Break any one-register solemnity with sentence-temperature variation: clipped protocol, dread, irony, intimacy, field-philosophy, and short pressure-release beats.
- Strengthen character-specific wit without turning the prose into jokes:
  - Corv: oblique double-meaning, patient but not coy
  - Gideon: blunt protective edge, load-bearing language
  - Jian: dry technical understatement
  - Sona: gentle relational wit where relevant
- Keep the biology / philosophy / technology braid balanced. No long biological wash without a field implication or protocol consequence nearby.
- Add double-meaning phrases that can read technically and emotionally at once.
- Keep the endocrine / enneagram / Toth-Crowley tarot / zodiac / archetypal scaffold subliminal: pacing, pressure, image recurrence, and reversal only.
- Deepen worldbuilding through lived consequence, lineage pressure, architecture, protocol, and embodied reaction rather than exposition.

Audit item to repair:

```json
{json.dumps(audit_item, ensure_ascii=False, indent=2)}
```

Matrix focus:

```json
{json.dumps(matrix_focus, ensure_ascii=False, indent=2)}
```

Target profile row:

```json
{json.dumps(target_row, ensure_ascii=False, indent=2)}
```

Compact dossier context:

```md
{dossier_context}
```

Dialogue voice matrix excerpt:

```md
{dialogue_matrix}
```

Current chapter:

```md
{current_text}
```

    Return only the repaired full chapter.
"""


def build_tail_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    stable_prefix_context: str,
    current_tail: str,
    prefix_words: int,
    current_tail_words: int,
    target_tail_low: int,
    target_tail_high: int,
    target_full_low: int,
    target_full_high: int,
    audit_item: dict[str, Any],
    matrix_row: dict[str, Any],
    target_row: dict[str, Any],
    dossier_context: str,
    dialogue_matrix: str,
) -> str:
    matrix_focus = {
        "primary_deficit": matrix_row.get("primary_deficit"),
        "layer_gaps": matrix_row.get("layer_gaps"),
        "best_source_families": matrix_row.get("best_source_families"),
        "notes": matrix_row.get("notes"),
    }
    return f"""
Repair only the ending movement of Chapter {chapter_number}: {chapter_title}.

The first half of the chapter is stable and will remain unchanged. You are replacing the current tail because it contains stacked late-stage closure beats. Return only the revised tail, not the full chapter.

Hard output rules:
- Begin directly with prose that continues from the stable prefix context.
- Do not include the chapter title, notes, labels, bullets, analysis, or metadata.
- Do not include preamble labels such as `Somatic Event`, `Character Focus`, `Political Context`, `RESONANCE PROFILE`, or `Chapter Status`.
- Do not mention PubMed, DOI, Alex Grey, CLIP-Vision, Rider-Waite, or the fact that a model/audit/runner exists.
- Do not invent additional Somanaut teammates, new operators, or new named systems.

Length contract:
- Stable prefix words already kept: `{prefix_words:,}`.
- Current tail words being replaced: `{current_tail_words:,}`.
- Return a revised tail in the `{target_tail_low:,}-{target_tail_high:,}` word range so the full chapter lands around `{target_full_low:,}-{target_full_high:,}` words.
- Preserve the useful canon from the current tail: the fragment/pearl, subject consent, endocrine handoff toward Chapter 5, Gardener hesitation, capacitor/dampener decision, and clean exit.
- Consolidate repeated closure beats into one coherent sequence. Do not create multiple endings.

Style repair targets:
- Strengthen Corv/Gideon/Jian/Sona voice distinction through dialogue and decision pressure.
- Keep wit character-specific and load-bearing, not jokey filler.
- Balance biology, philosophy, and technology every few paragraphs.
- Add worldbuilding around the Emperor's lineage and governance through architecture, protocol, lineage pressure, and lived consequence.
- Use double meanings that are procedural and emotional at once: receipt, signature, inheritance, gate, pruning, consent, watermark.
- Keep endocrine / enneagram / Toth-Crowley tarot / zodiac / archetypal structure subliminal through reversal, pressure, image recurrence, and pacing.
- End with a clean handoff toward the endocrine layer without over-explaining Chapter 5.

Audit item to repair:

```json
{json.dumps(audit_item, ensure_ascii=False, indent=2)}
```

Matrix focus:

```json
{json.dumps(matrix_focus, ensure_ascii=False, indent=2)}
```

Target profile row:

```json
{json.dumps(target_row, ensure_ascii=False, indent=2)}
```

Compact dossier context:

```md
{dossier_context}
```

Dialogue voice matrix excerpt:

```md
{dialogue_matrix}
```

Stable prefix context immediately before the replacement:

```md
{stable_prefix_context}
```

Current tail to replace and consolidate:

```md
{current_tail}
```

Return only the revised tail prose.
"""


def run_tail_repair(
    *,
    args: argparse.Namespace,
    model: str,
    meta: Any,
    current_text: str,
    current_words: int,
    target_low: int,
    target_high: int,
    audit_item: dict[str, Any],
    matrix_row: dict[str, Any],
    target_row: dict[str, Any],
    dossier_context: str,
    dialogue_matrix: str,
    raw_dir: Path,
    slug: str,
) -> str:
    anchor_index = current_text.find(args.tail_anchor)
    if anchor_index == -1:
        raise RuntimeError(f"Tail anchor not found: {args.tail_anchor}")
    prefix = current_text[:anchor_index].rstrip()
    current_tail = current_text[anchor_index:].strip()
    prefix_words = word_count(prefix)
    current_tail_words = word_count(current_tail)
    target_tail_low = max(current_tail_words + args.min_new_words, target_low - prefix_words)
    target_tail_high = max(target_tail_low + 400, current_tail_words + args.max_new_words, target_high - prefix_words)
    stable_prefix_context = prefix[-3500:]
    prompt = build_tail_repair_prompt(
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        stable_prefix_context=stable_prefix_context,
        current_tail=current_tail,
        prefix_words=prefix_words,
        current_tail_words=current_tail_words,
        target_tail_low=target_tail_low,
        target_tail_high=target_tail_high,
        target_full_low=target_low,
        target_full_high=target_high,
        audit_item=audit_item,
        matrix_row=matrix_row,
        target_row=target_row,
        dossier_context=dossier_context,
        dialogue_matrix=dialogue_matrix,
    )
    print(
        f"[chapter {args.chapter:02d}] nvidia_call=tail_style_repair model={model} tail_target={target_tail_low}-{target_tail_high}",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a literary revision engine. Return only the replacement prose tail requested.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.58,
        max_tokens=8000,
        timeout_seconds=args.timeout_seconds,
        max_attempts=args.max_attempts,
        retry_backoff_seconds=12,
    )
    tail_candidate = extract_text(response).strip()
    tail_candidate = re.sub(r"^\s*#+\s*Chapter\s+\d+.*\n+", "", tail_candidate).strip()
    tail_candidate = re.sub(r"```(?:md)?", "", tail_candidate).strip()
    tail_path = raw_dir / f"{slug}.style-tail-repair-1.md"
    tail_path.write_text(tail_candidate.strip() + "\n", encoding="utf-8")
    merged = f"{prefix}\n\n{tail_candidate.strip()}\n"
    return normalize_chapter_text(
        merged,
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
    )


def main() -> None:
    args = parse_args()
    meta = working_meta(args.chapter)
    if meta.book_number != args.book:
        raise RuntimeError(f"Chapter {args.chapter:02d} does not belong to Book {args.book}")

    working_path = REPO_ROOT / meta.working_file
    raw_dir = RAW_ROOT / f"book_{args.book}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    slug = chapter_slug(args.chapter, meta.chapter_title)
    raw_path = raw_dir / f"{slug}.raw.md"
    repair_path = raw_dir / f"{slug}.style-repair-1.md"

    manifest_row = load_manifest_row(args.chapter)
    matrix_row = load_matrix_row(args.chapter)
    target_row = load_target_row(args.chapter)
    audit_item = load_audit_item(Path(args.audit_json), args.chapter)
    model = args.model or matrix_row["draft_model"]

    current_text = working_path.read_text(encoding="utf-8")
    current_words = word_count(current_text)
    target_low = max(int(target_row["macro_target_low"]), current_words + args.min_new_words)
    target_high = max(target_low + 400, current_words + args.max_new_words)

    dossier_path = REPO_ROOT / manifest_row["dossier_file"]
    dossier_context = build_dossier_context(dossier_path.read_text(encoding="utf-8"))
    dialogue_matrix = read_excerpt(DIALOGUE_MATRIX, 3200)

    if args.mode == "tail":
        candidate = run_tail_repair(
            args=args,
            model=model,
            meta=meta,
            current_text=current_text,
            current_words=current_words,
            target_low=target_low,
            target_high=target_high,
            audit_item=audit_item,
            matrix_row=matrix_row,
            target_row=target_row,
            dossier_context=dossier_context,
            dialogue_matrix=dialogue_matrix,
            raw_dir=raw_dir,
            slug=slug,
        )
    else:
        prompt = build_repair_prompt(
            chapter_number=args.chapter,
            chapter_title=meta.chapter_title,
            current_text=current_text,
            current_words=current_words,
            target_low=target_low,
            target_high=target_high,
            audit_item=audit_item,
            matrix_row=matrix_row,
            target_row=target_row,
            dossier_context=dossier_context,
            dialogue_matrix=dialogue_matrix,
        )
        print(
            f"[chapter {args.chapter:02d}] nvidia_call=style_alignment_repair model={model} target={target_low}-{target_high}",
            flush=True,
        )
        response = chat_completion(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a literary revision engine. Preserve canon and return only the repaired full chapter.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.55,
            max_tokens=12000,
            timeout_seconds=args.timeout_seconds,
            max_attempts=args.max_attempts,
            retry_backoff_seconds=12,
        )
        candidate = normalize_chapter_text(
            extract_text(response),
            chapter_number=args.chapter,
            chapter_title=meta.chapter_title,
        )
    repair_path.write_text(candidate, encoding="utf-8")
    candidate_words = word_count(candidate)
    print(f"[chapter {args.chapter:02d}] repair_candidate_words={candidate_words}", flush=True)

    validate_chapter(
        candidate,
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        current_words=current_words,
        minimum_words=target_low,
    )
    if candidate_words > target_high + 800:
        raise RuntimeError(f"Repair overshot constrained target: {candidate_words} > {target_high + 800}")
    residue = find_preamble_residue(candidate)
    if residue:
        raise RuntimeError(f"Repair contains preamble residue: {residue}")
    forbidden_hits = contains_forbidden_names(candidate)
    if forbidden_hits:
        raise RuntimeError(f"Repair contains forbidden name/source patterns: {forbidden_hits}")

    gate_stage = next_gate_stage(raw_dir, slug)
    style_gate = run_style_gate(
        model=matrix_row.get("control_model", "openai/gpt-oss-120b"),
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        candidate_text=candidate,
        raw_dir=raw_dir,
        slug=slug,
        stage_index=gate_stage,
    )
    print(
        f"[chapter {args.chapter:02d}] gate_stage={gate_stage} gate_scores={style_gate.get('scores', {})}",
        flush=True,
    )
    validate_style_gate(style_gate)

    raw_path.write_text(candidate, encoding="utf-8")
    working_path.write_text(candidate, encoding="utf-8")
    if raw_path.read_text(encoding="utf-8") != working_path.read_text(encoding="utf-8"):
        raise RuntimeError("Raw and working outputs differ after repair write")

    print(f"Wrote {repo_rel(working_path)}", flush=True)
    print(f"Wrote {repo_rel(raw_path)}", flush=True)
    print(f"Wrote {repo_rel(repair_path)}", flush=True)
    print(f"before_words={current_words}", flush=True)
    print(f"after_words={candidate_words}", flush=True)
    print(f"target_low={target_low}", flush=True)
    print(f"target_high={target_high}", flush=True)


if __name__ == "__main__":
    main()
