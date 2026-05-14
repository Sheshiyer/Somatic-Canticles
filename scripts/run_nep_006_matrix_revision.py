#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import REPO_ROOT, load_chapter_metadata

CURRENT_MATRIX = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "chapter_expansion_matrix.md"
SYNTHESIS_REPORT = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "repo_synthesis_report_v1.md"
SOURCE_PRIORITY = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "source_family_priority_map_v1.md"
VISUAL_REGISTRY = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "visual_motif_registry_seed_v1.md"
INPUT_PACK = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "repo_synthesis_input_pack_v1.md"
OUTPUT_MD = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.md"
OUTPUT_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.json"
OUTPUT_RAW = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.raw.txt"

ALLOWED_PRIORITY_CLUSTERS = {"high", "medium", "low"}
ALLOWED_DOSSIER_PRIORITIES = {"wave-1", "wave-2", "wave-3"}
ALLOWED_SOURCE_TIERS = {
    "published substrate",
    "concept support",
    "review-required support",
    "visual support",
}

# The frozen input pack only preserved the placeholder matrix through Chapter 17.
# These late-book target bands continue the same original sizing scheme so NEP-006
# can remain deterministic until the baseline matrix is committed.
FALLBACK_LATE_TARGET_BANDS = {
    18: "3200-4200",
    19: "3400-4400",
    20: "3400-4400",
    21: "3400-4400",
    22: "3200-4200",
    23: "3600-4600",
    24: "3600-4600",
    25: "3800-5000",
    26: "3600-4600",
    27: "3400-4400",
}


def compact_source_priority() -> str:
    text = SOURCE_PRIORITY.read_text(encoding="utf-8")
    lines: list[str] = []
    keep = False
    for line in text.splitlines():
        if line.startswith("## 1. Root-by-Root Execution Priority"):
            keep = True
        elif line.startswith("## 3. Highest-Risk Noise Families"):
            break
        if keep:
            lines.append(line)
    return "\n".join(lines).strip()


def compact_visual_registry() -> str:
    lines = VISUAL_REGISTRY.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[:36]).strip()


def compact_metadata() -> str:
    items = []
    for item in load_chapter_metadata():
        items.append(
            {
                "chapter_number": item.chapter_number,
                "chapter_title": item.chapter_title,
                "book_number": item.book_number,
                "book_label": item.book_label,
                "summary": item.summary,
                "working_file": item.working_file,
                "compiled_file": item.compiled_file,
                "current_words": item.current_words,
            }
        )
    return json.dumps(items, ensure_ascii=False, indent=2)


def load_baseline_matrix_text() -> str:
    text = INPUT_PACK.read_text(encoding="utf-8")
    pattern = re.compile(
        r"## 06_WORKBENCH/SC_STORYOPS/story/expansion_lab/chapter_expansion_matrix\.md\s+```md\n(?P<body>.*?)\n```",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Could not extract baseline matrix from {INPUT_PACK}")
    return match.group("body").strip()


def baseline_target_band_appendix() -> str:
    bands = load_baseline_target_bands()
    lines = ["Recovered target-band appendix:", ""]
    for chapter_number in range(1, 28):
        lines.append(f"- `{chapter_number:02d}` -> `{bands[chapter_number]}`")
    return "\n".join(lines)


def make_prompt() -> str:
    return f"""
Revise the chapter expansion matrix into `v1`.

You are not generating canon prose. You are only revising planning fields.

Use the local metadata as fixed truth for:
- chapter number
- chapter title
- book number
- book label
- working file
- compiled file
- current words

For each chapter `01` through `27`, output exactly one line with these pipe-delimited fields and no header:

chapter_number|target_band|priority_cluster|dossier_priority|primary_deficit|layer_gaps_semicolon|best_source_families_semicolon|visual_support_semicolon|draft_model|control_pass|source_tier_focus_semicolon|notes

Rules:
- copy `target_band` verbatim from the baseline matrix below
- `priority_cluster` must be one of `high`, `medium`, `low`
- `dossier_priority` must be one of `wave-1`, `wave-2`, `wave-3`
- `layer_gaps_semicolon`, `best_source_families_semicolon`, `visual_support_semicolon`, `source_tier_focus_semicolon` must use `;` as the separator with no bullet markers
- `source_tier_focus_semicolon` may only contain: `published substrate`; `concept support`; `review-required support`; `visual support`
- keep `notes` brief and chapter-local
- prefer blog substrate first, then concept support, then filtered review-required support
- use `visual support` only where it is clearly relevant
- output 27 lines only, nothing before or after

Fixed metadata:

{compact_metadata()}

Baseline matrix:

{load_baseline_matrix_text()}

Repo synthesis report:

{SYNTHESIS_REPORT.read_text(encoding="utf-8")}

Source priority excerpt:

{compact_source_priority()}

Visual motif seed excerpt:

{compact_visual_registry()}

{baseline_target_band_appendix()}
"""


def parse_rows(raw: str) -> list[dict]:
    metadata = {item.chapter_number: item for item in load_chapter_metadata()}
    target_bands = load_baseline_target_bands()
    fallback_visual_support = load_fallback_visual_support()
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    rows: list[dict] = []
    for line in lines:
        if "|" not in line:
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) not in {12, 13}:
            continue
        chapter_number = int(parts[0])
        meta = metadata[chapter_number]
        if len(parts) == 13:
            target_band = parts[1]
            priority_cluster = parts[2]
            dossier_priority = parts[3]
            primary_deficit = parts[4]
            layer_gaps = split_field(parts[5])
            best_source_families = split_field(parts[6])
            visual_support = split_field(parts[7])
            draft_model = parts[8]
            control_pass = parts[9]
            source_tier_focus = split_field(parts[10])
            notes = parts[11]
        else:
            if re.fullmatch(r"\d{4}-\d{4}", parts[1]):
                target_band = parts[1]
                priority_cluster = parts[2]
                dossier_priority = parts[3]
                primary_deficit = parts[4]
                layer_gaps = split_field(parts[5])
                best_source_families = split_field(parts[6])
                maybe_field = split_field(parts[7])
                draft_model = parts[8]
                control_pass = parts[9]
                tier_tail = split_field(parts[10])
                notes = parts[11]
                if maybe_field and all(item in ALLOWED_SOURCE_TIERS for item in maybe_field):
                    visual_support = fallback_visual_support.get(chapter_number, [])
                    source_tier_focus = normalize_source_tiers(maybe_field + tier_tail)
                else:
                    visual_support = maybe_field
                    source_tier_focus = tier_tail
            else:
                target_band = target_bands[chapter_number]
                priority_cluster = parts[1]
                dossier_priority = parts[2]
                primary_deficit = f"{parts[3]} / {parts[4]}"
                layer_gaps = split_field(parts[5])
                best_source_families = split_field(parts[6])
                visual_support = split_field(parts[7])
                draft_model = parts[8]
                control_pass = parts[9]
                source_tier_focus = split_field(parts[10])
                notes = parts[11]
        if visual_support and "visual support" not in source_tier_focus:
            source_tier_focus = normalize_source_tiers(source_tier_focus + ["visual support"])
        validate_row(
            chapter_number=chapter_number,
            target_band=target_band,
            priority_cluster=priority_cluster,
            dossier_priority=dossier_priority,
            source_tier_focus=source_tier_focus,
        )
        rows.append(
            {
                "chapter_number": chapter_number,
                "chapter_title": meta.chapter_title,
                "book_number": meta.book_number,
                "book_label": meta.book_label,
                "working_file": meta.working_file,
                "compiled_file": meta.compiled_file,
                "current_words": meta.current_words,
                "target_band": target_band,
                "priority_cluster": priority_cluster,
                "dossier_priority": dossier_priority,
                "primary_deficit": primary_deficit,
                "layer_gaps": layer_gaps,
                "best_source_families": best_source_families,
                "visual_support": visual_support,
                "draft_model": draft_model,
                "control_pass": control_pass,
                "source_tier_focus": source_tier_focus,
                "notes": notes,
            }
        )
    if len(rows) != 27:
        raise RuntimeError(f"Expected 27 parsed rows, got {len(rows)}. Raw output saved to {OUTPUT_RAW}")
    rows.sort(key=lambda row: row["chapter_number"])
    return rows


def split_field(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def load_baseline_target_bands() -> dict[int, str]:
    text = load_baseline_matrix_text()
    pattern = re.compile(r"\| `(?P<num>\d{2})` \| `\d+` \| `(?P<band>[^`]+)` \|")
    bands: dict[int, str] = {}
    for line in text.splitlines():
        match = pattern.search(line)
        if match:
            bands[int(match.group("num"))] = match.group("band").strip()
    bands.update(FALLBACK_LATE_TARGET_BANDS)
    if len(bands) != 27:
        raise RuntimeError(f"Expected 27 baseline target bands from input pack, got {len(bands)}")
    return bands


def load_fallback_visual_support() -> dict[int, list[str]]:
    support: dict[int, list[str]] = {}
    if not CURRENT_MATRIX.exists():
        return support
    for line in CURRENT_MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `") or ". " not in line:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 9:
            continue
        chapter_label = parts[0].strip("`")
        chapter_number = int(chapter_label.split(".", 1)[0])
        visual_cell = parts[8]
        if visual_cell.lower() == "none":
            support[chapter_number] = []
        else:
            support[chapter_number] = [item.strip() for item in visual_cell.split(";") if item.strip()]
    return support


def normalize_source_tiers(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def validate_row(
    *,
    chapter_number: int,
    target_band: str,
    priority_cluster: str,
    dossier_priority: str,
    source_tier_focus: list[str],
) -> None:
    if not re.fullmatch(r"\d{4}-\d{4}", target_band):
        raise RuntimeError(f"Chapter {chapter_number:02d} has invalid target band: {target_band!r}")
    if priority_cluster not in ALLOWED_PRIORITY_CLUSTERS:
        raise RuntimeError(f"Chapter {chapter_number:02d} has invalid priority cluster: {priority_cluster!r}")
    if dossier_priority not in ALLOWED_DOSSIER_PRIORITIES:
        raise RuntimeError(f"Chapter {chapter_number:02d} has invalid dossier priority: {dossier_priority!r}")
    invalid_tiers = [tier for tier in source_tier_focus if tier not in ALLOWED_SOURCE_TIERS]
    if invalid_tiers:
        raise RuntimeError(f"Chapter {chapter_number:02d} has invalid source tiers: {invalid_tiers!r}")


def render_markdown(rows: list[dict]) -> str:
    lines = [
        "# Chapter Expansion Matrix v1",
        "",
        "This revision is derived from `repo_synthesis_report_v1.md`, `source_family_priority_map_v1.md`, and the curated visual motif seed.",
        "",
        "## Column Definitions",
        "",
        "- `Current words`: current `working/` surface length",
        "- `Target band`: desired expanded length range",
        "- `Priority`: dossier/build order urgency",
        "- `Dossier priority`: batching wave for dossier creation",
        "- `Primary deficit`: what is most missing now",
        "- `Layer gaps`: which story layers are under-served",
        "- `Best source families`: highest-value deepening surfaces",
        "- `Visual support`: approved motif families that may deepen atmosphere or structure",
        "- `Source tier focus`: admissible external source tiers for this chapter",
        "",
        "## Matrix",
        "",
        "| Chapter | Current words | Target band | Priority | Dossier priority | Primary deficit | Layer gaps | Best source families | Visual support | Source tier focus | Draft model | Control pass | Notes |",
        "| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['chapter_number']:02d}. {row['chapter_title']}` | "
            f"`{row['current_words']}` | "
            f"`{row['target_band']}` | "
            f"`{row['priority_cluster']}` | "
            f"`{row['dossier_priority']}` | "
            f"{row['primary_deficit']} | "
            f"{', '.join(row['layer_gaps'])} | "
            f"{'; '.join(row['best_source_families'])} | "
            f"{'; '.join(row['visual_support']) or 'none'} | "
            f"{', '.join(row['source_tier_focus'])} | "
            f"`{row['draft_model']}` | "
            f"`{row['control_pass']}` | "
            f"{row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `wave-1` dossier chapters should be generated first in `NEP-008` to `NEP-010`.",
            "- Visual motifs remain support-only and require chapter-local provenance in the eventual dossier.",
            "- This matrix supersedes the pre-synthesis placeholder matrix in the expansion lab.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse-raw", action="store_true", help="Reuse the existing raw model output instead of calling the model again.")
    args = parser.parse_args()

    if args.reuse_raw:
        raw = OUTPUT_RAW.read_text(encoding="utf-8").strip()
    else:
        response = chat_completion(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You revise a chapter expansion matrix for a fiction expansion program. "
                        "Do not invent canon or new files. Output only the requested pipe-delimited lines."
                    ),
                },
                {"role": "user", "content": make_prompt()},
            ],
            temperature=0.2,
            max_tokens=3600,
            extra_body={"reasoning_effort": "low"},
        )
        raw = extract_text(response).strip()
        OUTPUT_RAW.write_text(raw + "\n", encoding="utf-8")
    rows = parse_rows(raw)
    OUTPUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = render_markdown(rows)
    OUTPUT_MD.write_text(markdown, encoding="utf-8")
    CURRENT_MATRIX.write_text(markdown, encoding="utf-8")
    print(f"Wrote {OUTPUT_RAW}")
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"Updated {CURRENT_MATRIX}")


if __name__ == "__main__":
    main()
