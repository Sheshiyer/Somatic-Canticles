#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT, slugify_chapter_title

MATRIX_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.json"
DOSSIER_ROOT = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "dossiers"
OUT_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "dossier_manifest_v1.json"
OUT_MD = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "dossier_manifest_v1.md"


def dossier_relpath(book_number: int, chapter_number: int, chapter_title: str) -> str:
    book_dir = {
        1: "book_1_anamnesis_engine",
        2: "book_2_myocardial_chorus",
        3: "book_3_the_ripening",
    }[book_number]
    filename = f"{chapter_number:02d}-{slugify_chapter_title(chapter_title)}.md"
    return f"06_WORKBENCH/SC_STORYOPS/story/expansion_lab/dossiers/{book_dir}/{filename}"


def main() -> None:
    rows = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    manifest = []
    for row in rows:
        manifest.append(
            {
                "chapter_number": row["chapter_number"],
                "chapter_title": row["chapter_title"],
                "book_number": row["book_number"],
                "book_label": row["book_label"],
                "dossier_priority": row["dossier_priority"],
                "priority_cluster": row["priority_cluster"],
                "working_file": row["working_file"],
                "compiled_file": row["compiled_file"],
                "dossier_file": dossier_relpath(row["book_number"], row["chapter_number"], row["chapter_title"]),
                "best_source_families": row["best_source_families"],
                "visual_support": row["visual_support"],
                "source_tier_focus": row["source_tier_focus"],
            }
        )

    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Dossier Manifest v1",
        "",
        "This manifest freezes chapter-to-dossier file layout before `NEP-008` to `NEP-010` generate populated dossiers.",
        "",
        "| Chapter | Book | Dossier priority | Priority | Dossier file | Working file | Source focus |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in manifest:
        lines.append(
            "| "
            f"`{item['chapter_number']:02d}. {item['chapter_title']}` | "
            f"`{item['book_label']}` | "
            f"`{item['dossier_priority']}` | "
            f"`{item['priority_cluster']}` | "
            f"`{item['dossier_file']}` | "
            f"`{item['working_file']}` | "
            f"{', '.join(item['source_tier_focus'])} |"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
