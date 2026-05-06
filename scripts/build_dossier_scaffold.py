#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT

MATRIX_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "chapter_expansion_matrix_v1.json"
MANIFEST_JSON = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "dossier_manifest_v1.json"
TEMPLATE = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "chapter_source_dossier_template.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build chapter dossier scaffolds from the v1 matrix and dossier manifest.")
    parser.add_argument("--chapter", type=int, action="append", dest="chapters", help="Chapter number to emit. May be repeated.")
    parser.add_argument("--all", action="store_true", help="Emit all dossier scaffold files.")
    parser.add_argument("--dry-run", action="store_true", help="Print the target dossier paths without writing files.")
    return parser.parse_args()


def render_scaffold(row: dict, manifest: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    preface = [
        f"# Dossier Scaffold: {row['chapter_number']:02d}. {row['chapter_title']}",
        "",
        "This scaffold was generated from `chapter_expansion_matrix_v1.json` and `dossier_manifest_v1.json`.",
        "",
        "## Preloaded Metadata",
        "",
        f"- `Chapter`: `{row['chapter_number']:02d}. {row['chapter_title']}`",
        f"- `Book`: `{row['book_label']}`",
        f"- `Current working file`: `{row['working_file']}`",
        f"- `Current compiled file`: `{row['compiled_file']}`",
        f"- `Current word count`: `{row['current_words']}`",
        f"- `Target word band`: `{row['target_band']}`",
        f"- `Priority cluster`: `{row['priority_cluster']}`",
        f"- `Dossier priority`: `{row['dossier_priority']}`",
        f"- `Primary deficit`: {row['primary_deficit']}",
        f"- `Layer gaps`: {', '.join(row['layer_gaps'])}",
        f"- `Best source families`: {'; '.join(row['best_source_families'])}",
        f"- `Visual support`: {'; '.join(row['visual_support']) or 'none'}",
        f"- `Source tier focus`: {', '.join(row['source_tier_focus'])}",
        f"- `Dossier file`: `{manifest['dossier_file']}`",
        "",
        "---",
        "",
    ]
    return "\n".join(preface) + template


def main() -> None:
    args = parse_args()
    rows = {row["chapter_number"]: row for row in json.loads(MATRIX_JSON.read_text(encoding="utf-8"))}
    manifest = {row["chapter_number"]: row for row in json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))}
    wanted = sorted(rows.keys()) if args.all else sorted(set(args.chapters or []))
    if not wanted:
        raise SystemExit("Specify --chapter <n> or --all")

    for chapter in wanted:
        row = rows[chapter]
        meta = manifest[chapter]
        output_path = REPO_ROOT / meta["dossier_file"]
        if args.dry_run:
            print(output_path)
            continue
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_scaffold(row, meta), encoding="utf-8")
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
