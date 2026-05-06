#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated"
MD_PATH = OUTPUT_DIR / "source_root_filter_spec_v1.md"
JSON_PATH = OUTPUT_DIR / "source_root_filter_spec_v1.json"

SPEC = {
    "version": "v1",
    "generated_from": [
        "source_root_intake_v1.md",
        "repo_synthesis_manifest.md",
        "vision_worldbuilding_ingestion_plan.md",
    ],
    "roots": [
        {
            "name": "blog_posts",
            "path": "/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/content/posts",
            "admissibility": "published substrate",
            "default_action": "include",
            "include_keywords": [
                "pattern",
                "consciousness",
                "runtime",
                "endocrine",
                "muse",
                "compassion",
                "code",
                "debug",
                "pain",
                "tryambakam",
            ],
            "review_required": [],
            "excluded": [],
        },
        {
            "name": "vault_resources",
            "path": "/Volumes/madara/2026/twc-vault/03-Resources",
            "admissibility": "review-required support",
            "default_action": "filter",
            "default_include_dirs": [
                "Consciousness-Studies",
                "Research",
                "General-Research",
                "Health",
                "Design",
            ],
            "review_required_dirs": [
                "Consciousness",
                "Alternative-Science",
                "Occult",
                "Critical-Thinking",
                "Knowledge",
                "Tetryonics-Integration",
            ],
            "excluded_dirs": [
                "Social-Inbox",
                "website-downloader-tool",
                "Websites",
            ],
        },
        {
            "name": "area_notebooks",
            "path": "/Volumes/madara/2026/twc-vault/02-Areas",
            "admissibility": "concept support",
            "default_action": "filter",
            "default_include_dirs": [
                "Consciousness-Models",
                "Pattern-Studies",
                "Technical-Mystical-Integration",
                "Muse-Enneagram-Framework",
            ],
            "review_required_dirs": [
                "Bioelectric-Body",
                "Logic-Gate-Linguistics",
                "Creative-Ideas",
            ],
            "excluded_dirs": [
                "Daily-Logs",
                "TheWhyChromosome-Brand",
                "ThoughtSeed-Operations",
            ],
        },
        {
            "name": "noesis_research",
            "path": "/Users/sheshnarayaniyer/Documents/noesis/Research",
            "admissibility": "visual support only",
            "default_action": "vision-only",
            "text_anchor_files": [
                "Images.md",
                "Excerpts.md",
                "Scientific Papers.md",
                "Pasted image 20240714224530.png.md",
            ],
        },
    ],
}


def write_markdown() -> None:
    lines = [
        "# Source Root Filter Spec v1",
        "",
        "This file converts `source_root_intake_v1.md` into an executable filtering contract for the first wave.",
        "",
    ]
    for root in SPEC["roots"]:
        lines.append(f"## {root['name']}")
        lines.append("")
        lines.append(f"- `path`: `{root['path']}`")
        lines.append(f"- `admissibility`: `{root['admissibility']}`")
        lines.append(f"- `default action`: `{root['default_action']}`")
        if "include_keywords" in root:
            lines.append("- `include keywords`:")
            lines.extend([f"  - `{item}`" for item in root["include_keywords"]])
        if "default_include_dirs" in root:
            lines.append("- `default include dirs`:")
            lines.extend([f"  - `{item}`" for item in root["default_include_dirs"]])
        if root.get("review_required_dirs"):
            lines.append("- `review-required dirs`:")
            lines.extend([f"  - `{item}`" for item in root["review_required_dirs"]])
        if root.get("excluded_dirs"):
            lines.append("- `excluded dirs`:")
            lines.extend([f"  - `{item}`" for item in root["excluded_dirs"]])
        if root.get("text_anchor_files"):
            lines.append("- `text anchor files`:")
            lines.extend([f"  - `{item}`" for item in root["text_anchor_files"]])
        lines.append("")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")
    write_markdown()
    print(f"Wrote {MD_PATH}")
    print(f"Wrote {JSON_PATH}")


if __name__ == "__main__":
    main()
