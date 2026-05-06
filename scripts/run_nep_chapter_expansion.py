#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import REPO_ROOT, load_chapter_metadata, word_count

DOSSIER_MANIFEST = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "dossier_manifest_v1.json"
)
MATRIX_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_expansion_matrix_v1.json"
)
TARGET_PROFILE_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "trilogy_length_target_profile_v1.json"
)
BOOK_RULES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "book_rules.md"
DIALOGUE_MATRIX = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "dialogue_voice_matrix.md"
EDITORIAL_BRIEF = REPO_ROOT / "03_EDITORIAL" / "EDITORIAL_BRIEF.md"
RAW_ROOT = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_expansion_raw"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Expand a working chapter from its dossier and macro target band.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def read_excerpt(path: Path, max_chars: int = 4000) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def load_manifest_row(chapter_number: int) -> dict:
    rows = json.loads(DOSSIER_MANIFEST.read_text(encoding="utf-8"))
    for row in rows:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing dossier manifest row for chapter {chapter_number:02d}")


def load_matrix_row(chapter_number: int) -> dict:
    rows = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    for row in rows:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing matrix row for chapter {chapter_number:02d}")


def load_target_row(chapter_number: int) -> dict:
    payload = json.loads(TARGET_PROFILE_JSON.read_text(encoding="utf-8"))
    for row in payload["chapters"]:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing target profile row for chapter {chapter_number:02d}")


def working_meta(chapter_number: int):
    for item in load_chapter_metadata():
        if item.chapter_number == chapter_number:
            return item
    raise RuntimeError(f"Missing chapter metadata for chapter {chapter_number:02d}")


def chapter_slug(chapter_number: int, chapter_title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", chapter_title.lower()).strip("-")
    return f"{chapter_number:02d}-{slug}"


def cleaned_heading(chapter_number: int, chapter_title: str) -> str:
    return f"# Chapter {chapter_number}: {chapter_title}\n"


def extract_dossier_section(dossier_text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## \d+\. |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(dossier_text)
    if not match:
        return ""
    return match.group("body").strip()


def build_dossier_context(dossier_text: str) -> str:
    sections = [
        ("2. Canon Function", extract_dossier_section(dossier_text, "2. Canon Function")),
        ("3. Character-Arc Obligations", extract_dossier_section(dossier_text, "3. Character-Arc Obligations")),
        ("8a. Implicit Symbolic Scaffold", extract_dossier_section(dossier_text, "8a. Implicit Symbolic Scaffold")),
        ("9. Scene Growth Opportunities", extract_dossier_section(dossier_text, "9. Scene Growth Opportunities")),
        ("10. Vocabulary and Voice Constraints", extract_dossier_section(dossier_text, "10. Vocabulary and Voice Constraints")),
    ]
    rendered: list[str] = []
    for heading, body in sections:
        if body:
            rendered.append(f"## {heading}\n{body}")
    return "\n\n".join(rendered)


def build_stage_targets(*, current_words: int, minimum_words: int) -> list[int]:
    targets = [
        max(current_words + 1200, min(minimum_words, max(3200, int(minimum_words * 0.35)))),
        max(current_words + 2400, min(minimum_words, max(5000, int(minimum_words * 0.60)))),
        max(current_words + 4200, min(minimum_words, max(7000, int(minimum_words * 0.82)))),
        minimum_words,
    ]
    result: list[int] = []
    previous = current_words
    for target in targets:
        if target <= previous:
            continue
        if result and target <= result[-1]:
            continue
        result.append(target)
        previous = target
    return result


def build_stage_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    current_draft: str,
    dossier_context: str,
    matrix_row: dict,
    target_row: dict,
    stage_index: int,
    stage_count: int,
    stage_low: int,
    stage_high: int,
) -> str:
    matrix_focus = {
        "primary_deficit": matrix_row["primary_deficit"],
        "layer_gaps": matrix_row["layer_gaps"],
        "best_source_families": matrix_row["best_source_families"],
        "notes": matrix_row["notes"],
    }
    preserve_existing = (
        "Preserve at least 85% of the existing sentences verbatim and grow by insertion around them."
        if stage_index > 1
        else "Preserve the existing beats and tonal spine while enlarging the chapter additively."
    )
    return f"""
Expand this novel chapter additively. This is stage {stage_index} of {stage_count}.

Rules:
- Output markdown only.
- First line must be exactly: `# Chapter {chapter_number}: {chapter_title}`
- Do not include section labels like `Somatic Event`, `Character Focus`, `Political Context`, or any dossier metadata.
- Do not include notes, explanations, or bullet lists.
- Preserve canon, scene order, and the outbound obligation from the dossier.
- Treat the current draft as a base text that must survive. Do not compress, omit, summarize, or skip existing beats.
- {preserve_existing}
- Keep the same POV center and chapter identity, but deepen atmosphere, somatic rhythm, relational consequence, and world pressure.
- Add new material before, between, and after existing beats so the chapter breathes.
- Use dossier deepening sources only through scene, image, sensation, dialogue, behavior, and consequence. Do not lecture.
- Keep dialogue role-bound per the voice matrix.
- Preserve and correctly use project lexicon such as `Khalorēē field`, `Manas Interface`, `Adawat al-Wa'i`, `Klei Toda'ah`, and `The Vine` when relevant.
- If the chapter draws on tarot / enneagram / endocrine-muse logic, default that symbolic lattice to **Toth/Crowley** semantics, not Rider–Waite.
- The full submerged scaffold may also include zodiac recurrence and archetypal patterning. Use the whole chain as an emotional and stylistic regulator, not as overt exposition.
- Keep that symbolic lattice subliminal: scene architecture, image pressure, pacing, tonal reversal, and biological emphasis. Do not have characters explain it aloud.
- Maintain a three-lane braid at all times:
  - somatic / biological precision
  - philosophical or field-intelligence pressure
  - technological / protocol atmosphere
- Do not let biology dominate the chapter. Each strong biological image or diagnostic beat should be counterweighted by either a technological consequence, a field/philosophical implication, or a sharp relational turn within the next few sentences.
- Keep the delivery punchy. Use short declarative lines at pressure points so the prose does not become a continuous clinical wash.
- Bring layered meanings and verbal play where natural. Let phrases do double duty without turning ornamental.
- Allow intelligent pressure-release humor or dry wit when character-true. Do not make everyone speak in the same solemn register.
- Modulate the emotional temperature. Let fear, wonder, irony, intimacy, technical focus, and grief alter the sentence texture rather than flattening into one style.
- Banned carryover terms or patterns: `Quantum Systems`, `vibration`, `manifestation`, lore-dump monologues, pseudo-spiritual filler, production scaffolding.
- Remove the old preamble metadata entirely and integrate its information into the prose itself.
- This is a smoke pass for the first live expansion wave, so the draft should materially deepen the chapter, not just line-edit it.
- The goal of this stage is to land the chapter in the `{stage_low:,}-{stage_high:,}` word range while keeping every existing scene beat intact.

Matrix focus:

```json
{json.dumps(matrix_focus, ensure_ascii=False, indent=2)}
```

Macro target profile row:

```json
{json.dumps(target_row, ensure_ascii=False, indent=2)}
```

Compact dossier context:

```md
{dossier_context}
```

Current chapter draft to expand without compression:

```md
{current_draft}
```

Now write the full revised chapter at this stage length.
"""


def build_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    current_draft: str,
    stage_low: int,
    stage_high: int,
) -> str:
    return f"""
Repair this expanded chapter so it grows materially without losing any existing beats.

Requirements:
- Keep the same title line: `# Chapter {chapter_number}: {chapter_title}`
- Preserve all existing canon beats and invented prose that is already working.
- Do not compress or summarize the draft you are given.
- Preserve the draft's tonal spine. Extend it by insertion and local deepening, not by revoicing the chapter into a colder or more clinical register.
- Do not add metadata, notes, or bullet lists.
- Increase scene dwell time, sensory embodiment, relational consequence, and aftermath.
- Add only scene-native material; do not add essays or lore-dump paragraphs.
- Keep any tarot / enneagram / endocrine-muse scaffolding implicit and Toth/Crowley-based rather than Rider–Waite-coded or overtly explained.
- Preserve the chapter's layered meaning, wit, and emotional temperature shifts. If humor or irony is already present or naturally available, sharpen it rather than sanding it away.
- Keep the biology / philosophy / technology braid intact. Do not over-index on raw anatomy or biomarker description.
- Add punch: short decisive lines, cleaner turns, and stronger protocol aura where the prose gets soggy.
- Bring the chapter into the `{stage_low:,}-{stage_high:,}` word range if possible.

Current draft:

```md
{current_draft}
```

Return the full revised chapter only.
"""


def validate_chapter(text: str, *, chapter_number: int, chapter_title: str, current_words: int, minimum_words: int) -> None:
    first_line = text.splitlines()[0].strip() if text.splitlines() else ""
    expected = f"# Chapter {chapter_number}: {chapter_title}"
    if first_line != expected:
        raise RuntimeError(f"Expanded chapter missing exact heading: {expected}")
    forbidden = [
        "**Somatic Event:**",
        "**Character Focus:**",
        "**Family Context:**",
        "**Political Context:**",
        "**Territory Context:**",
        "**Cultural Context:**",
        "PubMed",
        "NIH",
        "Alex Grey",
        "visual archive",
        "CLIP-Vision",
        "WORLD_BIBLE.md",
        "Preface.md",
    ]
    for token in forbidden:
        if token in text:
            raise RuntimeError(f"Expanded chapter contains forbidden token: {token}")
    expanded_words = word_count(text)
    if expanded_words <= current_words:
        raise RuntimeError(f"Expanded chapter did not grow: current={current_words}, expanded={expanded_words}")
    if expanded_words < minimum_words:
        raise RuntimeError(f"Expanded chapter below minimum pass floor: {expanded_words} < {minimum_words}")


def validate_stage(
    text: str,
    *,
    chapter_number: int,
    chapter_title: str,
    previous_words: int,
    stage_floor: int,
) -> None:
    relaxed_floor = max(previous_words + 400, int(stage_floor * 0.85))
    validate_chapter(
        text,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        current_words=previous_words,
        minimum_words=relaxed_floor,
    )


def stage_output_path(raw_dir: Path, slug: str, stage_index: int, kind: str = "stage") -> Path:
    return raw_dir / f"{slug}.{kind}-{stage_index}.md"


def run_stage(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    dossier_context: str,
    matrix_row: dict,
    target_row: dict,
    current_draft: str,
    stage_index: int,
    stage_count: int,
    stage_low: int,
    stage_high: int,
    raw_dir: Path,
    slug: str,
) -> str:
    prompt = build_stage_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        current_draft=current_draft,
        dossier_context=dossier_context,
        matrix_row=matrix_row,
        target_row=target_row,
        stage_index=stage_index,
        stage_count=stage_count,
        stage_low=stage_low,
        stage_high=stage_high,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are expanding an existing literary science-fantasy chapter into a longer, more embodied novel chapter. "
                    "Preserve canon, grow additively, and output markdown only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=min(10000, 4000 + stage_index * 1500),
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=900,
        max_attempts=4,
        retry_backoff_seconds=12,
    )
    text = extract_text(response).strip() + "\n"
    stage_output_path(raw_dir, slug, stage_index).write_text(text, encoding="utf-8")
    return text


def run_stage_repair(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    current_draft: str,
    stage_index: int,
    stage_low: int,
    stage_high: int,
    raw_dir: Path,
    slug: str,
) -> str:
    prompt = build_repair_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        current_draft=current_draft,
        stage_low=stage_low,
        stage_high=stage_high,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You repair an expanded chapter by preserving all existing beats and deepening it additively. "
                    "Output markdown only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=min(10000, 4500 + stage_index * 1500),
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=900,
        max_attempts=4,
        retry_backoff_seconds=12,
    )
    text = extract_text(response).strip() + "\n"
    stage_output_path(raw_dir, slug, stage_index, kind="repair").write_text(text, encoding="utf-8")
    return text


def main() -> None:
    args = parse_args()
    meta = working_meta(args.chapter)
    if meta.book_number != args.book:
        raise RuntimeError(f"Chapter {args.chapter:02d} does not belong to book {args.book}")

    manifest_row = load_manifest_row(args.chapter)
    matrix_row = load_matrix_row(args.chapter)
    target_row = load_target_row(args.chapter)

    working_path = REPO_ROOT / meta.working_file
    dossier_path = REPO_ROOT / manifest_row["dossier_file"]
    raw_dir = RAW_ROOT / f"book_{args.book}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    slug = chapter_slug(args.chapter, meta.chapter_title)
    raw_path = raw_dir / f"{slug}.raw.md"
    if args.force:
        for stale_path in raw_dir.glob(f"{slug}*.md"):
            stale_path.unlink()

    current_text = working_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    dossier_context = build_dossier_context(dossier_text)
    current_words = word_count(current_text)
    minimum_words = max(int(target_row["macro_target_low"] * 0.8), current_words * 2)

    stage_targets = build_stage_targets(current_words=current_words, minimum_words=minimum_words)
    draft = current_text
    previous_words = current_words
    for stage_index, stage_low in enumerate(stage_targets, start=1):
        stage_high = min(target_row["macro_target_low"], stage_low + 1200)
        candidate = run_stage(
            model=matrix_row["draft_model"],
            chapter_number=args.chapter,
            chapter_title=meta.chapter_title,
            dossier_context=dossier_context,
            matrix_row=matrix_row,
            target_row=target_row,
            current_draft=draft,
            stage_index=stage_index,
            stage_count=len(stage_targets),
            stage_low=stage_low,
            stage_high=stage_high,
            raw_dir=raw_dir,
            slug=slug,
        )
        try:
            validate_stage(
                candidate,
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                previous_words=previous_words,
                stage_floor=stage_low,
            )
        except RuntimeError:
            candidate = run_stage_repair(
                model=matrix_row["draft_model"],
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                current_draft=candidate,
                stage_index=stage_index,
                stage_low=stage_low,
                stage_high=stage_high,
                raw_dir=raw_dir,
                slug=slug,
            )
            validate_stage(
                candidate,
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                previous_words=previous_words,
                stage_floor=stage_low,
            )
        draft = candidate
        previous_words = word_count(draft)

    text = draft
    raw_path.write_text(text, encoding="utf-8")
    validate_chapter(
        text,
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        current_words=current_words,
        minimum_words=minimum_words,
    )

    working_path.write_text(text, encoding="utf-8")
    print(f"Wrote {working_path}")
    print(f"Wrote {raw_path}")
    print(f"before_words={current_words}")
    print(f"after_words={word_count(text)}")
    print(f"minimum_words={minimum_words}")


if __name__ == "__main__":
    main()
