#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT, load_chapter_metadata

OUT_MD = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "trilogy_length_target_profile_v1.md"
)
OUT_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "trilogy_length_target_profile_v1.json"
)

BOOK_TARGETS = {
    1: {"target_low": 90_000, "target_high": 120_000},
    2: {"target_low": 80_000, "target_high": 105_000},
    3: {"target_low": 130_000, "target_high": 175_000},
}


def round_to_50(value: float) -> int:
    return int(round(value / 50.0) * 50)


def main() -> None:
    chapters = load_chapter_metadata()
    book_current = {1: 0, 2: 0, 3: 0}
    for item in chapters:
        book_current[item.book_number] += item.current_words

    chapter_rows: list[dict] = []
    trilogy_current = sum(item.current_words for item in chapters)
    trilogy_3x = trilogy_current * 3
    trilogy_low = sum(targets["target_low"] for targets in BOOK_TARGETS.values())
    trilogy_high = sum(targets["target_high"] for targets in BOOK_TARGETS.values())

    for item in chapters:
        book_total = book_current[item.book_number]
        share = item.current_words / book_total if book_total else 0
        book_targets = BOOK_TARGETS[item.book_number]
        macro_low = round_to_50(book_targets["target_low"] * share)
        macro_high = round_to_50(book_targets["target_high"] * share)
        chapter_rows.append(
            {
                "chapter_number": item.chapter_number,
                "chapter_title": item.chapter_title,
                "book_number": item.book_number,
                "book_label": item.book_label,
                "working_file": item.working_file,
                "current_words": item.current_words,
                "intermediate_3x_floor": item.current_words * 3,
                "macro_target_low": macro_low,
                "macro_target_high": macro_high,
                "macro_delta_low": macro_low - item.current_words,
                "macro_delta_high": macro_high - item.current_words,
                "share_of_book_current_words": round(share, 4),
            }
        )

    payload = {
        "trilogy": {
            "current_words": trilogy_current,
            "intermediate_3x_floor": trilogy_3x,
            "macro_target_low": trilogy_low,
            "macro_target_high": trilogy_high,
            "delta_to_macro_low": trilogy_low - trilogy_current,
            "delta_to_macro_high": trilogy_high - trilogy_current,
        },
        "books": {
            str(book_number): {
                "current_words": book_current[book_number],
                "macro_target_low": BOOK_TARGETS[book_number]["target_low"],
                "macro_target_high": BOOK_TARGETS[book_number]["target_high"],
                "delta_to_macro_low": BOOK_TARGETS[book_number]["target_low"] - book_current[book_number],
                "delta_to_macro_high": BOOK_TARGETS[book_number]["target_high"] - book_current[book_number],
                "average_chapter_target_low": round(BOOK_TARGETS[book_number]["target_low"] / len([c for c in chapters if c.book_number == book_number]), 2),
                "average_chapter_target_high": round(BOOK_TARGETS[book_number]["target_high"] / len([c for c in chapters if c.book_number == book_number]), 2),
            }
            for book_number in (1, 2, 3)
        },
        "chapters": chapter_rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Trilogy Length Target Profile v1",
        "",
        "This artifact defines the actual macro-length objective for the NVIDIA expansion program.",
        "It supersedes the earlier assumption that a simple `3x` pass would be enough.",
        "",
        "## Trilogy Objective",
        "",
        f"- Current trilogy working-lane total: `{trilogy_current:,}`",
        f"- Intermediate `3x` floor: `{trilogy_3x:,}`",
        f"- Actual trilogy target band: `{trilogy_low:,}-{trilogy_high:,}`",
        f"- Additional words needed to reach macro floor: `{trilogy_low - trilogy_current:,}`",
        f"- Additional words needed to reach macro ceiling: `{trilogy_high - trilogy_current:,}`",
        "",
        "## Book Target Architecture",
        "",
        "| Book | Current | Macro Target Band | Delta to Floor | Delta to Ceiling | Avg Chapter Target |",
        "|---|---:|---|---:|---:|---|",
    ]
    for book_number in (1, 2, 3):
        book = payload["books"][str(book_number)]
        lines.append(
            f"| {book_number} | {book['current_words']:,} | {book['macro_target_low']:,}-{book['macro_target_high']:,} | {book['delta_to_macro_low']:,} | {book['delta_to_macro_high']:,} | {book['average_chapter_target_low']:,}-{book['average_chapter_target_high']:,} |"
        )

    lines.extend(
        [
            "",
            "## Chapter Planning Bands",
            "",
            "These chapter bands are proportional to each chapter's current share of its book's working-lane words.",
            "They are the planning bands the next expansion wave should use instead of the older short v1 matrix bands.",
            "",
            "| Ch | Book | Current | 3x Floor | Macro Band | Delta to Macro Floor |",
            "|---|---|---:|---:|---|---:|",
        ]
    )
    for row in chapter_rows:
        lines.append(
            f"| {row['chapter_number']:02d} | {row['book_number']} | {row['current_words']:,} | {row['intermediate_3x_floor']:,} | {row['macro_target_low']:,}-{row['macro_target_high']:,} | {row['macro_delta_low']:,} |"
        )

    lines.extend(
        [
            "",
            "## Planning Notes",
            "",
            "- `3x` remains useful as an anti-regression floor, but it is not the actual delivery target.",
            "- The macro target is intentionally weighted toward a longer Book `3`, while still keeping Books `1` and `2` in full-length novel range.",
            "- The next chapter-expansion wave should treat these bands as the real length objective and recalibrate the chapter matrix accordingly.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
