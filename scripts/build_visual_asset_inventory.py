#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated"
MD_PATH = OUTPUT_DIR / "visual_asset_inventory_v1.md"
JSON_PATH = OUTPUT_DIR / "visual_asset_inventory_v1.json"

ROOTS = {
    "noesis_research": Path("/Users/sheshnarayaniyer/Documents/noesis/Research"),
    "blog_src_cards": Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/assets/cards"),
    "blog_dist_cards": Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/cards"),
    "blog_dist_images": Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/images"),
    "blog_dist_maps": Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/dist/maps"),
    "vault_design": Path("/Volumes/madara/2026/twc-vault/03-Resources/Design"),
    "vault_general_research": Path("/Volumes/madara/2026/twc-vault/03-Resources/General-Research"),
    "vault_knowledge_org": Path("/Volumes/madara/2026/twc-vault/03-Resources/Knowledge-Organization"),
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def summarize(root: Path) -> dict:
    ext_counter: Counter[str] = Counter()
    samples: list[str] = []
    total = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        total += 1
        ext_counter[path.suffix.lower()] += 1
        if len(samples) < 12:
            samples.append(str(path))
    return {
        "path": str(root),
        "exists": root.exists(),
        "image_count": total,
        "extensions": dict(ext_counter),
        "samples": samples,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = {name: summarize(path) for name, path in ROOTS.items()}
    JSON_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    lines = [
        "# Visual Asset Inventory v1",
        "",
        "This inventory is the first multimodal handoff for `NEP-005`.",
        "",
    ]
    for name, info in data.items():
        lines.append(f"## {name}")
        lines.append("")
        lines.append(f"- `path`: `{info['path']}`")
        lines.append(f"- `exists`: `{info['exists']}`")
        lines.append(f"- `image_count`: `{info['image_count']}`")
        lines.append("- `extensions`:")
        for ext, count in sorted(info["extensions"].items()):
            lines.append(f"  - `{ext}`: `{count}`")
        lines.append("- `sample assets`:")
        for sample in info["samples"]:
            lines.append(f"  - `{sample}`")
        lines.append("")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {MD_PATH}")
    print(f"Wrote {JSON_PATH}")


if __name__ == "__main__":
    main()
