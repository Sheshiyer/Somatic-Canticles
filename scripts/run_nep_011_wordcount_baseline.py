#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT, load_chapter_metadata

MATRIX_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_expansion_matrix_v1.json"
)
OUT_MD = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_wordcount_baseline_v1.md"
)
OUT_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_wordcount_baseline_v1.json"
)


def parse_target_band(band: str) -> tuple[int, int]:
    low, high = band.split("-", 1)
    return int(low), int(high)


def main() -> None:
    matrix_rows = {row["chapter_number"]: row for row in json.loads(MATRIX_JSON.read_text(encoding="utf-8"))}
    metadata = load_chapter_metadata()

    rows: list[dict] = []
    totals = {
        "trilogy": {"current_words": 0, "triple_target_words": 0},
        1: {"current_words": 0, "triple_target_words": 0},
        2: {"current_words": 0, "triple_target_words": 0},
        3: {"current_words": 0, "triple_target_words": 0},
    }

    for item in metadata:
        matrix = matrix_rows[item.chapter_number]
        target_low, target_high = parse_target_band(matrix["target_band"])
        triple_target = item.current_words * 3
        delta_to_triple = triple_target - item.current_words
        rows.append(
            {
                "chapter_number": item.chapter_number,
                "chapter_title": item.chapter_title,
                "book_number": item.book_number,
                "book_label": item.book_label,
                "working_file": item.working_file,
                "current_words": item.current_words,
                "triple_target_words": triple_target,
                "delta_to_triple": delta_to_triple,
                "matrix_target_band": matrix["target_band"],
                "matrix_target_low": target_low,
                "matrix_target_high": target_high,
                "matrix_meets_triple_floor": target_high >= triple_target,
            }
        )
        totals[item.book_number]["current_words"] += item.current_words
        totals[item.book_number]["triple_target_words"] += triple_target
        totals["trilogy"]["current_words"] += item.current_words
        totals["trilogy"]["triple_target_words"] += triple_target

    payload = {
        "summary": {
            "books": {
                str(book_number): {
                    "current_words": totals[book_number]["current_words"],
                    "triple_target_words": totals[book_number]["triple_target_words"],
                    "delta_to_triple": totals[book_number]["triple_target_words"] - totals[book_number]["current_words"],
                }
                for book_number in (1, 2, 3)
            },
            "trilogy": {
                "current_words": totals["trilogy"]["current_words"],
                "triple_target_words": totals["trilogy"]["triple_target_words"],
                "delta_to_triple": totals["trilogy"]["triple_target_words"] - totals["trilogy"]["current_words"],
            },
        },
        "chapters": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Chapter Wordcount Baseline v1",
        "",
        "This is the committed pre-expansion baseline for the active `working/Chapter-*.md` lane in the isolated NVIDIA expansion worktree.",
        "",
        "## Summary",
        "",
        f"- Trilogy current words: `{payload['summary']['trilogy']['current_words']:,}`",
        f"- Trilogy `3x` target floor: `{payload['summary']['trilogy']['triple_target_words']:,}`",
        f"- Trilogy delta to `3x`: `{payload['summary']['trilogy']['delta_to_triple']:,}`",
        "",
        "| Book | Current Words | 3x Target Floor | Delta |",
        "|---|---:|---:|---:|",
    ]
    for book_number in (1, 2, 3):
        book = payload["summary"]["books"][str(book_number)]
        lines.append(
            f"| {book_number} | {book['current_words']:,} | {book['triple_target_words']:,} | {book['delta_to_triple']:,} |"
        )

    lines.extend(
        [
            "",
            "## Chapter Baseline",
            "",
            "| Ch | Book | Current | 3x Floor | Delta | Matrix Band | Matrix Covers 3x? |",
            "|---|---|---:|---:|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['chapter_number']:02d} | {row['book_number']} | {row['current_words']:,} | {row['triple_target_words']:,} | {row['delta_to_triple']:,} | {row['matrix_target_band']} | {'yes' if row['matrix_meets_triple_floor'] else 'no'} |"
        )

    lines.extend(["", "## Notes", ""])
    lines.append("- `Current` is measured from the active `working/Chapter-*.md` files, not the compiled books.")
    lines.append("- `3x Floor` is the minimum post-expansion target requested for later chapter passes.")
    lines.append("- `Matrix Covers 3x?` shows whether the existing v1 target band already reaches that `3x` floor.")
    lines.append("- Use this artifact as the before-state for all future chapter expansion verification.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
