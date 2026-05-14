#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated"
MD_PATH = OUTPUT_DIR / "repo_synthesis_input_pack_v1.md"

CONTROL_DOCS = [
    "NVIDIA_EXPANSION_INIT.md",
    "DesignSpec.md",
    "ProjectArchitecture.md",
    "06_WORKBENCH/SC_STORYOPS/story/expansion_lab/repo_synthesis_manifest.md",
    "06_WORKBENCH/SC_STORYOPS/story/expansion_lab/source_root_intake_v1.md",
    "06_WORKBENCH/SC_STORYOPS/story/expansion_lab/chapter_expansion_matrix.md",
    "06_WORKBENCH/SC_STORYOPS/story/outline.md",
    "06_WORKBENCH/SC_STORYOPS/story/chapter_summaries.md",
    "06_WORKBENCH/SC_STORYOPS/story/book_rules.md",
    "06_WORKBENCH/SC_STORYOPS/story/dialogue_voice_matrix.md",
    "01_WORLD_BIBLE/02_CHARACTER_SYSTEM/TRILOGY-CHARACTER-ARCS.md",
    "03_EDITORIAL/EDITORIAL_BRIEF.md",
    "03_EDITORIAL/03_STYLE_GUIDE/MASTER_STYLE_SHEET.md",
]


def excerpt(path: Path, max_lines: int = 35) -> str:
    if not path.exists():
        return f"[missing] {path}"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[:max_lines])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    parts = [
        "# Repo Synthesis Input Pack v1",
        "",
        "This pack is the first structured input artifact for `NEP-003`.",
        "",
        "It does not replace model prompting, but it collects the highest-priority control docs in one place so synthesis starts from the same baseline every time.",
        "",
    ]
    for rel in CONTROL_DOCS:
        path = REPO_ROOT / rel
        parts.append(f"## {rel}")
        parts.append("")
        parts.append("```md")
        parts.append(excerpt(path))
        parts.append("```")
        parts.append("")

    MD_PATH.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {MD_PATH}")


if __name__ == "__main__":
    main()
