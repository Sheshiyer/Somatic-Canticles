#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib_dossier_sources import (
    SourceCandidate,
    render_candidates,
    select_area_candidates,
    select_blog_candidates,
    select_resource_candidates,
    select_visual_candidates,
)
from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import BOOK_LABELS, REPO_ROOT, load_chapter_metadata

MATRIX_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.json"
MANIFEST_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "dossier_manifest_v1.json"
CHAPTER_SUMMARIES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "chapter_summaries.md"
OUTLINE = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "outline.md"
BOOK_RULES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "book_rules.md"
DIALOGUE_MATRIX = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "dialogue_voice_matrix.md"
CHARACTER_ARCS = REPO_ROOT / "01_WORLD_BIBLE" / "02_CHARACTER_SYSTEM" / "TRILOGY-CHARACTER-ARCS.md"
EDITORIAL_BRIEF = REPO_ROOT / "03_EDITORIAL" / "EDITORIAL_BRIEF.md"
MASTER_STYLE = REPO_ROOT / "03_EDITORIAL" / "03_STYLE_GUIDE" / "MASTER_STYLE_SHEET.md"
TASK_JSON = {
    1: REPO_ROOT / "03_EDITORIAL" / "book1_anamnesis_engine_tasks.json",
    2: REPO_ROOT / "03_EDITORIAL" / "book2_myocardial_chorus_tasks.json",
    3: REPO_ROOT / "03_EDITORIAL" / "book3_the_ripening_tasks.json",
}
RAW_ROOT = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "dossier_raw"

PROMPT_SANITIZE = {
    "PubMed": "peer-reviewed biology",
    "NIH": "reviewed biology source",
    "Alex Grey": "visionary anatomical visual",
    "visual_archive": "selected visual support asset",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Populate chapter dossiers for a book wave.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3], help="Book number to populate.")
    parser.add_argument("--chapter", type=int, action="append", dest="chapters", help="Optional chapter restriction. May be repeated.")
    parser.add_argument("--force", action="store_true", help="Overwrite dossiers even if they already appear populated.")
    parser.add_argument("--max-chapters", type=int, help="Optional cap for smoke-testing.")
    return parser.parse_args()


def load_matrix_rows(book_number: int) -> list[dict]:
    rows = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    return [row for row in rows if row["book_number"] == book_number]


def load_manifest_rows() -> dict[int, dict]:
    return {row["chapter_number"]: row for row in json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))}


def load_task_map(book_number: int) -> dict[int, list[dict]]:
    payload = json.loads(TASK_JSON[book_number].read_text(encoding="utf-8"))
    result: dict[int, list[dict]] = {}
    for task in payload["tasks"]:
        chapter = task.get("chapter")
        if chapter is None:
            result.setdefault(0, []).append(task)
            continue
        result.setdefault(int(chapter), []).append(task)
    return result


def chapter_summary_map() -> dict[int, str]:
    result: dict[int, str] = {}
    pattern = re.compile(r"- `(?P<num>\d{2})\. (?P<title>[^`]+)` — (?P<summary>.+)")
    for line in CHAPTER_SUMMARIES.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            result[int(match.group("num"))] = match.group("summary").strip()
    return result


def read_excerpt(path: Path, max_chars: int = 5000) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def sanitize_prompt_text(text: str) -> str:
    for source, replacement in PROMPT_SANITIZE.items():
        text = text.replace(source, replacement)
    return text


def allowed_repo_paths(book_number: int, metadata_working_file: str, metadata_compiled_file: str) -> list[str]:
    return [
        "06_WORKBENCH/SC_STORYOPS/story/chapter_summaries.md",
        "06_WORKBENCH/SC_STORYOPS/story/outline.md",
        "06_WORKBENCH/SC_STORYOPS/story/book_rules.md",
        "06_WORKBENCH/SC_STORYOPS/story/dialogue_voice_matrix.md",
        "01_WORLD_BIBLE/02_CHARACTER_SYSTEM/TRILOGY-CHARACTER-ARCS.md",
        "03_EDITORIAL/EDITORIAL_BRIEF.md",
        "03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md",
        TASK_JSON[book_number].relative_to(REPO_ROOT).as_posix(),
        metadata_working_file,
        metadata_compiled_file,
    ]


def compact_control_surfaces(book_number: int) -> str:
    task_payload = json.loads(TASK_JSON[book_number].read_text(encoding="utf-8"))
    phase_summary = ", ".join(f"{key}={value}" for key, value in task_payload["phase_summary"].items())
    return "\n".join(
        [
            "## Control Surface Notes",
            "",
            "### Editorial brief",
            "- Clinical precision at visionary scale.",
            "- Do not dumb down technical language; opacity is part of the reader apprenticeship.",
            "- Corv must move from witness to authorship, and the Gardener remains conservational, not evil.",
            "",
            "### Style sheet",
            "- Preserve exact lexicon: `NOESIS`, `Khalorēē`, `Prana`, `Somanaut`, `The Vine`, `The Gardener`.",
            "- Prefer `self-consciousness` for witness capacity and avoid deprecated filler like `vibration`, `manifestation`, `Quantum Systems`.",
            "",
            "### Book rules",
            "- Show system behavior through scene pressure, sensation, and consequence before explanation.",
            "- Dialogue stays role-bound and subtext-heavy; no lore-dump monologues.",
            "- Every substantive addition must be traceable to project source plus conceptual/research source.",
            "",
            "### Dialogue matrix",
            "- Corv: pattern-legible, relational, restrained.",
            "- Sona: sensory, resonant, concrete in body shifts.",
            "- Jian: precise, structural, non-lecturing.",
            "- Gideon: boundary, load, protective clarity.",
            "- Gardener: sorrowful necessity, never sneering.",
            "",
            "### Book task pack",
            f"- Phase summary: {phase_summary}",
        ]
    )


def chapter_run_root(book_number: int) -> Path:
    return RAW_ROOT / f"book_{book_number}"


def output_already_populated(path: Path) -> bool:
    if not path.exists():
        return False
    first_line = path.read_text(encoding="utf-8").splitlines()[0:1]
    return bool(first_line and first_line[0].startswith("# Chapter Source Dossier:"))


def render_task_entries(entries: list[dict], shared_entries: list[dict] | None = None) -> str:
    combined = list(entries)
    if shared_entries:
        combined.extend(shared_entries[:6])
    if not combined:
        return "- none\n"
    lines: list[str] = []
    for task in combined[:12]:
        lines.extend(
            [
                f"- `{task['id']}` `{task['priority']}` `{task['phase_name']}` — {sanitize_prompt_text(task['title'])}",
                f"  - description: {sanitize_prompt_text(task['description'])}",
                f"  - gate: `{task['gate']}`",
            ]
        )
    return "\n".join(lines) + "\n"


def selected_candidates(row: dict) -> tuple[list[SourceCandidate], list[SourceCandidate], list[SourceCandidate], list[SourceCandidate]]:
    blog_candidates = select_blog_candidates(row)
    area_candidates = select_area_candidates(row)
    resource_candidates = select_resource_candidates(row)
    visual_candidates = select_visual_candidates(row)
    return blog_candidates, area_candidates, resource_candidates, visual_candidates


def build_prompt(
    *,
    row: dict,
    manifest: dict,
    chapter_text: str,
    summary_map: dict[int, str],
    task_map: dict[int, list[dict]],
    repo_control: str,
) -> str:
    chapter_number = row["chapter_number"]
    blog_candidates, area_candidates, resource_candidates, visual_candidates = selected_candidates(row)
    candidates: list[SourceCandidate] = []
    candidates.extend(blog_candidates)
    candidates.extend(area_candidates)
    candidates.extend(resource_candidates)
    candidates.extend(visual_candidates)
    source_block = render_candidates(candidates)
    selected_external_paths = [item.path for item in candidates]
    candidate_availability = "\n".join(
        [
            f"- text candidates selected: {'yes' if candidates and len(candidates) > len(visual_candidates) else 'no'}",
            f"- visual candidates selected: {'yes' if visual_candidates else 'no'}",
            f"- review-required support selected: {'yes' if resource_candidates else 'no'}",
            "- exact external paths allowed for sections 6-8 and 12:",
            *[f"  - `{path}`" for path in selected_external_paths],
        ]
    )

    prev_summary = summary_map.get(chapter_number - 1, "n/a")
    current_summary = summary_map[chapter_number]
    next_summary = summary_map.get(chapter_number + 1, "n/a")

    metadata = load_chapter_metadata()[chapter_number - 1]
    dossier_path = REPO_ROOT / manifest["dossier_file"]
    scaffold = dossier_path.read_text(encoding="utf-8")
    repo_paths = allowed_repo_paths(metadata.book_number, metadata.working_file, metadata.compiled_file)
    repo_paths_block = "\n".join(f"- `{path}`" for path in repo_paths)

    return f"""
Populate this chapter source dossier in markdown.

Rules:
- Output a complete dossier only, not prose for the novel itself.
- Replace scaffold placeholders with actual content.
- Use this exact title line: `# Chapter Source Dossier: {chapter_number:02d}. {row['chapter_title']}`
- Keep the numbered section structure `## 1.` through `## 12.`
- Do not use markdown tables. Use compact bullet lists only.
- Work only from the supplied evidence. Do not invent new source files.
- External sources may only come from the selected candidates below.
- Repo path citations may only use the allowlist below.
- If evidence is thin, say so plainly and mark follow-up needs instead of fabricating certainty.
- Treat visual evidence as support-only unless corroborated by text sources.
- Cite repo-relative paths for repo files and absolute paths for external sources.
- Prefer compact bullets over large tables.
- Keep the full dossier concise enough to fit all 12 sections; target roughly 900-1400 words.
- Keep sections short. Most sections should be 2-6 bullets.
- If a desired source is unavailable, write `needs follow-up` instead of inventing a path.
- Do not mention placeholder sources like `PubMed`, `NIH`, `Alex Grey`, `visual_archive`, `WORLD_BIBLE.md`, or `Preface.md`.
- Literal banned strings in the output: `PubMed`, `NIH`, `Alex Grey`, `visual archive`, `CLIP-Vision`.
- If an editorial task implies a future biological or visual audit but no selected external source is supplied, record it only as a follow-up need. Do not present it as a selected source.
- If a biological audit is still needed, write `needs follow-up biological source` instead of naming a journal, database, or institution.
- If a visual audit is still needed, write `needs follow-up visual candidate` instead of naming an artist, archive, or invented asset.
- In sections `6`, `7`, and `8`, list only the external sources whose exact paths appear in the selected candidate block.
- If no visual candidates are supplied, section `8. Multimodal Evidence` must say `needs follow-up visual candidate` and section `11. Model Routing` must set multimodal extraction model to `not selected yet`.
- If visual candidates are supplied, section `8. Multimodal Evidence` may mention only those exact asset paths and should not invent archive labels, alternate asset names, or alternate extraction models.
- In section `11. Model Routing`, use:
  - synthesis model: `openai/gpt-oss-120b`
  - reasoning model: `openai/gpt-oss-120b`
  - prose draft model: `{row['draft_model']}`
  - control model: `{row['control_pass']}`
  - multimodal extraction model: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` only if a visual candidate is supplied, otherwise `not selected yet`

Chapter matrix row:

```json
{json.dumps(row, ensure_ascii=False, indent=2)}
```

Manifest row:

```json
{json.dumps(manifest, ensure_ascii=False, indent=2)}
```

Chapter summaries:

- previous: {prev_summary}
- current: {current_summary}
- next: {next_summary}

Book outline excerpt:

{read_excerpt(OUTLINE, max_chars=3000)}

Control surfaces:

{repo_control}

Allowed repo citation paths:

{repo_paths_block}

Candidate availability:

{candidate_availability}

Character arcs:

{read_excerpt(CHARACTER_ARCS, max_chars=5000)}

Current working chapter text:

```md
{chapter_text}
```

Selected editorial task entries for this chapter:

{render_task_entries(task_map.get(chapter_number, []), task_map.get(0, []))}

Selected external source candidates:

{source_block}

Current scaffold:

```md
{scaffold}
```

Now write the populated dossier. It should be concrete, source-bound, and useful for later Kimi drafting.
"""


def build_repair_prompt(
    *,
    chapter_title: str,
    failed_text: str,
    failure_reason: str,
    allowed_repo_paths: list[str],
    allowed_external_paths: list[str],
    has_visual_candidates: bool,
) -> str:
    repo_paths_block = "\n".join(f"- `{path}`" for path in allowed_repo_paths)
    external_paths_block = "\n".join(f"- `{path}`" for path in allowed_external_paths) or "- none selected"
    visual_line = (
        "- visual candidates are selected; only use the exact allowed external asset paths below"
        if has_visual_candidates
        else "- no visual candidates are selected; section 8 must say `needs follow-up visual candidate` and section 11 must say `not selected yet`"
    )
    return f"""
Repair this chapter source dossier so it satisfies the dossier contract exactly.

Chapter:
- `{chapter_title}`

Validation failure to fix:
- {failure_reason}

Hard rules:
- Preserve the exact title line and `## 1.` through `## 12.` section structure.
- Do not use markdown tables. Use compact bullet lists only.
- Remove unsupported placeholder tokens: `PubMed`, `NIH`, `Alex Grey`, `visual archive`, `CLIP-Vision`, `WORLD_BIBLE.md`, `Preface.md`.
- Do not cite any repo path outside the allowlist.
- Do not cite any external path outside the allowlist.
- If a research or visual source is missing, write `needs follow-up biological source` or `needs follow-up visual candidate`.
- Do not invent archive names, asset names, or extraction models.
- Keep the repaired dossier concise enough to finish all 12 sections.

Candidate state:
{visual_line}

Allowed repo paths:
{repo_paths_block}

Allowed external paths:
{external_paths_block}

Current dossier to repair:

```md
{failed_text}
```

Return the repaired dossier only.
"""

def validate_output(text: str, allowed_paths: list[str], allowed_external_paths: list[str]) -> None:
    required = [
        "# Chapter Source Dossier:",
        "## 1. Chapter Identity",
        "## 11. Model Routing",
        "## 12. Validation Checklist",
    ]
    for needle in required:
        if needle not in text:
            raise RuntimeError(f"Dossier output missing required marker: {needle}")
    forbidden = [
        "Use one copy of this template per chapter before expansion drafting begins.",
        "- `Chapter`",
        "- `Book`",
        "- `Current working file`",
    ]
    if any(token in text for token in forbidden):
        raise RuntimeError("Dossier output still contains unfilled template placeholders.")
    repo_paths = re.findall(r"`((?:01_WORLD_BIBLE|02_MANUSCRIPTS|03_EDITORIAL|06_WORKBENCH)/[^`]+)`", text)
    unknown = sorted({path for path in repo_paths if path not in allowed_paths})
    if unknown:
        raise RuntimeError(f"Dossier output cited unsupported repo paths: {unknown}")
    external_paths = re.findall(r"`(/[^`]+)`", text)
    unknown_external = sorted({path for path in external_paths if path not in allowed_external_paths})
    if unknown_external:
        raise RuntimeError(f"Dossier output cited unsupported external paths: {unknown_external}")
    forbidden_tokens = ["PubMed", "NIH", "Alex Grey", "visual_archive/", "WORLD_BIBLE.md", "Preface.md"]
    for token in forbidden_tokens:
        if token in text:
            raise RuntimeError(f"Dossier output cited unsupported placeholder source token: {token}")
    forbidden_phrases = ["CLIP-Vision", "visual archive", "generic)"]
    for phrase in forbidden_phrases:
        if phrase in text:
            raise RuntimeError(f"Dossier output cited unsupported placeholder phrase: {phrase}")


def main() -> None:
    args = parse_args()
    repo_control = compact_control_surfaces(args.book)
    summary_map = chapter_summary_map()
    manifest_rows = load_manifest_rows()
    task_map = load_task_map(args.book)

    rows = load_matrix_rows(args.book)
    if args.chapters:
        wanted = set(args.chapters)
        rows = [row for row in rows if row["chapter_number"] in wanted]
    rows.sort(key=lambda row: row["chapter_number"])
    if args.max_chapters:
        rows = rows[: args.max_chapters]

    run_root = chapter_run_root(args.book)
    run_root.mkdir(parents=True, exist_ok=True)

    metadata_map = {item.chapter_number: item for item in load_chapter_metadata()}

    for row in rows:
        manifest = manifest_rows[row["chapter_number"]]
        dossier_path = REPO_ROOT / manifest["dossier_file"]
        raw_path = run_root / f"{row['chapter_number']:02d}-{re.sub(r'[^a-z0-9]+', '-', row['chapter_title'].lower()).strip('-')}.raw.md"
        repair_path = run_root / f"{row['chapter_number']:02d}-{re.sub(r'[^a-z0-9]+', '-', row['chapter_title'].lower()).strip('-')}.repair.md"
        if output_already_populated(dossier_path) and not args.force:
            print(f"Skipping populated dossier {dossier_path}")
            continue

        metadata = metadata_map[row["chapter_number"]]
        chapter_text = read_excerpt(REPO_ROOT / metadata.working_file, max_chars=9000)
        blog_candidates, area_candidates, resource_candidates, visual_candidates = selected_candidates(row)
        allowed_external_paths = [item.path for item in [*blog_candidates, *area_candidates, *resource_candidates, *visual_candidates]]
        repo_allowlist = allowed_repo_paths(args.book, metadata.working_file, metadata.compiled_file)
        prompt = build_prompt(
            row=row,
            manifest=manifest,
            chapter_text=chapter_text,
            summary_map=summary_map,
            task_map=task_map,
            repo_control=repo_control,
        )

        response = chat_completion(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You populate source-bound chapter dossiers for a fiction expansion lab. "
                        "Do not write chapter prose. Do not invent canon. Output markdown only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4200,
            extra_body={"reasoning_effort": "low"},
        )
        text = extract_text(response).strip() + "\n"
        raw_path.write_text(text, encoding="utf-8")
        try:
            validate_output(text, repo_allowlist, allowed_external_paths)
        except RuntimeError as err:
            repair_prompt = build_repair_prompt(
                chapter_title=row["chapter_title"],
                failed_text=text,
                failure_reason=str(err),
                allowed_repo_paths=repo_allowlist,
                allowed_external_paths=allowed_external_paths,
                has_visual_candidates=bool(visual_candidates),
            )
            repair_response = chat_completion(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You repair chapter source dossiers to satisfy strict source-binding and formatting rules. "
                            "Output markdown only."
                        ),
                    },
                    {"role": "user", "content": repair_prompt},
                ],
                temperature=0.1,
                max_tokens=4200,
                extra_body={"reasoning_effort": "low"},
            )
            text = extract_text(repair_response).strip() + "\n"
            repair_path.write_text(text, encoding="utf-8")
            validate_output(text, repo_allowlist, allowed_external_paths)
        dossier_path.write_text(text, encoding="utf-8")
        print(f"Wrote {dossier_path}")
        print(f"Wrote {raw_path}")
        if repair_path.exists():
            print(f"Wrote {repair_path}")


if __name__ == "__main__":
    main()
