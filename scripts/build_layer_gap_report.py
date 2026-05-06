#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT

MATRIX_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.json"
OUT_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "layer_gap_report_v1.json"
OUT_MD = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "layer_gap_report_v1.md"


def main() -> None:
    rows = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))

    by_book: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    global_layers: dict[str, list[str]] = defaultdict(list)
    high_priority: list[dict] = []

    for row in rows:
        chapter_label = f"{row['chapter_number']:02d}. {row['chapter_title']}"
        for layer in row["layer_gaps"]:
            by_book[row["book_label"]][layer].append(chapter_label)
            global_layers[layer].append(chapter_label)
        if row["priority_cluster"] == "high":
            high_priority.append(
                {
                    "chapter": chapter_label,
                    "book": row["book_label"],
                    "primary_deficit": row["primary_deficit"],
                    "dossier_priority": row["dossier_priority"],
                }
            )

    payload = {
        "by_book": by_book,
        "global_layers": global_layers,
        "high_priority_chapters": high_priority,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Layer Gap Report v1",
        "",
        "This report groups the revised chapter matrix by under-served layers and high-priority dossier targets.",
        "",
        "## High-Priority Chapters",
        "",
        "| Chapter | Book | Dossier priority | Primary deficit |",
        "| --- | --- | --- | --- |",
    ]
    for item in high_priority:
        lines.append(
            f"| `{item['chapter']}` | `{item['book']}` | `{item['dossier_priority']}` | {item['primary_deficit']} |"
        )

    for book, layers in by_book.items():
        lines.extend(["", f"## {book}", ""])
        for layer, chapters in sorted(layers.items()):
            lines.append(f"- `{layer}`: {', '.join(f'`{chapter}`' for chapter in chapters)}")

    lines.extend(["", "## Global Layer Pressure", ""])
    for layer, chapters in sorted(global_layers.items()):
        lines.append(f"- `{layer}` ({len(chapters)}): {', '.join(f'`{chapter}`' for chapter in chapters)}")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
